#!/usr/bin/env python3
"""Comfy Studio: a Higgsfield-style front end for ComfyUI API workflows.
Run with ComfyUI's own Python (only needs aiohttp):  python studio.py
Env: COMFY_URL (default http://127.0.0.1:8188), COMFY_DIR, COMFY_ARGS, PORT (default 7860)."""
import asyncio, copy, json, math, mimetypes, os, random, re, shlex, subprocess, sys, time, uuid, webbrowser
from pathlib import Path
from urllib.parse import urlencode, urlparse

import aiohttp
from aiohttp import web

ROOT = Path(__file__).parent
WF = ROOT / "workflows"
WF.mkdir(exist_ok=True)
SETUP = ROOT / "setup"  # per-workflow Setup choices, kept apart so replacing a workflow keeps them
SETUP.mkdir(exist_ok=True)
COMFY = os.environ.get("COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
PORT = int(os.environ.get("PORT", 7860))
COMFY_DIR = Path(os.environ.get("COMFY_DIR", ROOT.parent))  # the folder that contains ComfyUI's main.py
MARK = re.compile(r"\s*\(\s*(?:(\d+)\s*\.\s*)?(input|output|setup|switch|slider|credits)\b([^()]*)\)\s*", re.I)
RULE = re.compile(r"\{([^}]*)\}\s*(on|off)\b\s*(?:\[([\d,\s]*)\])?", re.I)
# Marks:  (Input Slider [1] {Height} min=256/max=2048/stp=32/dec=0)  (Input Switch)  (Credits 351.6)  (Input)  - after the keyword, the order is free (2.Input [1,3]) (Input optional {Reference photos} [image 2/10]) (Switch {Custom ratio} [1]) (Setup {Main model} [1]) (Output)
# Rule outside the marks:  {custom ratio} on [1]  = show field 1 only while the switch named "custom ratio" is on (or "off")
# class_type -> (media kind, input field that holds the filename)
MEDIA = {"LoadImage": ("image", "image"), "LoadImageMask": ("image", "image"),
         "LoadAudio": ("audio", "audio"), "VHS_LoadAudio": ("audio", "audio"),
         "LoadVideo": ("video", "file"), "VHS_LoadVideo": ("video", "video")}
OUT = {"SaveImage": "image", "PreviewImage": "image", "SaveAnimatedWEBP": "image", "SaveAnimatedPNG": "image",
       "SaveVideo": "video", "VHS_VideoCombine": "video",
       "SaveAudio": "audio", "SaveAudioMP3": "audio", "SaveAudioOpus": "audio", "PreviewAudio": "audio"}
TEXT_FIELDS = ("text", "prompt", "value", "string")
SEEDS = ("seed", "noise_seed")
CAST = {"int": lambda x: int(float(x)), "float": float, "bool": lambda x: str(x).lower() in ("true", "1", "on")}
OI, JOBS, S, PROC, PB, API = {}, {}, None, None, {}, {}


def link(v): return isinstance(v, list) and len(v) == 2 and isinstance(v[0], str)
def tags(n):
    """-> (plain title, [marks], [show-rules]). A title can hold several marks, e.g. 'Switch (Input) (Switch {Custom ratio} [1])'."""
    t = n.get("_meta", {}).get("title", ""); marks = []
    for m in MARK.finditer(t):
        rest = m.group(3); nm = re.search(r"\{([^}]*)\}", rest); rest = re.sub(r"\{[^}]*\}", "", rest)
        br = re.search(r"\[([^\]]*)\]", rest); br = br.group(1) if br else ""
        kind = m.group(2).lower()
        o = {"kind": "input" if kind in ("switch", "slider") else kind, "slider": kind == "slider" or bool(re.search(r"\bslider\b", re.sub(r"\{[^}]*\}", "", m.group(3)), re.I)), "order": int(m.group(1)) if m.group(1) else None,
             "optional": bool(re.search(r"\boptional\b", rest, re.I)),
             "name": (nm.group(1).strip() or None) if nm else None, "idx": [], "group": None}
        for kk, names in (("min", ("min",)), ("max", ("max",)), ("stp", ("stp", "step")), ("dec", ("dec",))):  # min=0/max=10/stp=2/dec=1  (":" works too)
            o[kk] = next((float(mm.group(1)) for nm_ in names for mm in [re.search(rf"\b{nm_}\s*[:=]\s*(-?\d+(?:\.\d+)?)", rest, re.I)] if mm), None)
        if kind == "credits":
            mm = re.search(r"-?\d+(?:\.\d+)?", rest); o["credits"] = float(mm.group(0)) if mm else None
        g = re.fullmatch(r"\s*([A-Za-z_][\w ]*?)\s*(\d+)\s*/\s*(\d+)\s*", br)
        if g: o["group"] = (g.group(1).strip().lower(), int(g.group(2)), int(g.group(3)))
        else: o["idx"] = [int(x) for x in re.findall(r"\d+", br)]
        marks.append(o)
    outside = MARK.sub(" ", t)
    rules = [{"name": r.group(1).strip().lower(), "on": r.group(2).lower() == "on", "idx": [int(x) for x in re.findall(r"\d+", r.group(3) or "")]}
             for r in RULE.finditer(outside)]
    return re.sub(r"\s+", " ", RULE.sub(" ", outside)).strip(), marks, rules
def slug(s): return re.sub(r"[^\w\-.]+", "_", s).strip("_.")  # dots are kept: "Qwen 2.1" stays "Qwen 2.1"
def add(lst, e):
    """Add an entry; when one node field is exposed twice, the named one wins over the plain one."""
    for k, x in enumerate(lst):
        if (x["node"], x["field"]) == (e["node"], e["field"]):
            order = e["order"] if e.get("order") is not None else x.get("order")
            lst[k] = e if e.get("named") and not x.get("named") else x
            lst[k]["order"] = order
            return lst[k]
    lst.append(e); return e
def chk(v, opts):
    if v is None or (isinstance(v, str) and not v.strip()): return "empty"
    if opts and v not in opts: return "missing"
def read_wf(wid):
    """The stored workflow with the user's Setup choices applied on top."""
    g = json.loads((WF / f"{wid}.json").read_text("utf-8")); sf = SETUP / f"{wid}.json"
    for k, v in (json.loads(sf.read_text("utf-8")) if sf.exists() else {}).items():
        nid, _, f = k.partition(".")
        if nid in g and f in g[nid]["inputs"] and not link(g[nid]["inputs"][f]): g[nid]["inputs"][f] = v
    return g
def is_out(n): return n["class_type"] in OUT or any(m["kind"] == "output" for m in tags(n)[1])
def has_out(g): return any(is_out(n) for n in g.values())
def file_kind(name):
    return (mimetypes.guess_type(name)[0] or "image/").split("/")[0] if not name.endswith(".opus") else "audio"


async def info(cls):
    """Input spec of a node class from ComfyUI (cached)."""
    if cls not in OI:
        try:
            async with S.get(f"{COMFY}/object_info/{cls}") as r:
                e = (await r.json()).get(cls, {}); OI[cls] = e.get("input", {}); PB[cls] = e.get("price_badge"); API[cls] = bool(e.get("api_node"))
        except (aiohttp.ClientError, ValueError):
            return {}
    return OI[cls]


async def prune(g, drop):
    """Disable nodes in `drop`. Downstream links to them are cut if the input is optional,
    otherwise the downstream node is disabled too (cascade)."""
    g, dead, changed = copy.deepcopy(g), set(drop), True
    while changed:
        changed = False
        for nid, n in g.items():
            if nid in dead:
                continue
            for k, v in list(n["inputs"].items()):
                if link(v) and v[0] in dead:
                    oi = await info(n["class_type"]); opt = oi.get("optional") or {}
                    # optional inputs, and entries of dynamic lists such as "images.image3", can simply be dropped
                    if k in opt or ("." in k and k.split(".")[0] in {**(oi.get("required") or {}), **opt}):
                        del n["inputs"][k]
                    else:
                        dead.add(nid); changed = True; break
    return {i: n for i, n in g.items() if i not in dead}


# ---------- credits: ComfyUI's API (partner) nodes carry a price formula; this evaluates a small JSONata subset ----------
CPU = float(os.environ.get("COMFY_CREDITS_PER_USD", 211))  # ComfyUI shows credits = dollars x 211
WARNED = set()
JTOK = re.compile(r"""\s*(?:(?P<num>\d+\.?\d*(?:[eE][+-]?\d+)?)|(?P<str>"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(?P<var>\$\$|\$[A-Za-z_]\w*|\$)|(?P<name>[A-Za-z_]\w*|`[^`]*`)|(?P<op>:=|!=|<=|>=|[-+*/%&=<>?:;,.(){}\[\]]))""")


def jlex(src):
    src, out, i = re.sub(r"/\*.*?\*/", " ", src, flags=re.S), [], 0
    while src[i:].strip():
        m = JTOK.match(src, i)
        if not m: raise ValueError(f"unexpected text near {src[i:i + 14]!r}")
        out.append((m.lastgroup, m.group(m.lastgroup))); i = m.end()
    return out


def _unq(v): return json.loads(v) if v[0] == '"' else v[1:-1].replace("\\'", "'")


class JP:
    def __init__(s, toks): s.t, s.p = toks, 0
    def peek(s, k=0): return s.t[s.p + k] if s.p + k < len(s.t) else (None, None)
    def eat(s, v=None):
        if v is not None and s.peek()[1] != v: raise ValueError(f"expected {v!r} but found {s.peek()[1]!r}")
        s.p += 1; return s.t[s.p - 1]
    def accept(s, v):
        if s.peek()[1] == v and s.peek()[0] in ("op", "name"): s.p += 1; return True
        return False
    def parse(s):
        b = s.block(None)
        if s.p != len(s.t): raise ValueError(f"unexpected {s.peek()[1]!r}")
        return b
    def block(s, end):
        out = []
        while s.peek()[1] != end:
            out.append(s.stmt())
            if not s.accept(";"): break
        return ("block", out)
    def stmt(s):
        if s.peek()[0] == "var" and s.peek(1)[1] == ":=":
            name = s.eat()[1]; s.eat(":="); return ("bind", name, s.expr())
        return s.expr()
    def expr(s):
        c = s.bin(0)
        if s.accept("?"):
            a = s.expr(); return ("if", c, a, s.expr() if s.accept(":") else ("lit", None))
        return c
    LV = [{"or"}, {"and"}, {"=", "!=", "<", "<=", ">", ">=", "in"}, {"&"}, {"+", "-"}, {"*", "/", "%"}]
    def bin(s, lv):
        if lv == len(s.LV):
            if s.accept("-"): return ("neg", s.bin(lv))
            return s.postfix()
        l = s.bin(lv + 1)
        while s.peek()[1] in s.LV[lv] and s.peek()[0] in ("op", "name"):
            op = s.eat()[1]; l = ("bin", op, l, s.bin(lv + 1))
        return l
    def postfix(s):
        e = s.primary()
        while True:
            if s.peek() == ("op", "."):
                s.eat(); k, v = s.eat(); e = ("step", e, _unq(v) if k == "str" else v.strip("`"))
            elif s.peek() == ("op", "["): s.eat(); i = s.expr(); s.eat("]"); e = ("index", e, i)
            elif s.peek() == ("op", "(") and e[0] == "var":
                s.eat(); args = []
                while s.peek()[1] != ")":
                    args.append(s.expr())
                    if not s.accept(","): break
                s.eat(")"); e = ("call", e[1], args)
            else: return e
    def primary(s):
        k, v = s.eat()
        if k == "num": return ("lit", float(v))
        if k == "str": return ("lit", _unq(v))
        if k == "var": return ("var", v)
        if k == "name":
            return ("lit", v == "true") if v in ("true", "false") else ("lit", None) if v == "null" else ("name", v.strip("`"))
        if v == "(": b = s.block(")"); s.eat(")"); return b
        if v == "{":
            items = []
            while s.peek()[1] != "}":
                key = s.expr(); s.eat(":"); items.append((key, s.expr()))
                if not s.accept(","): break
            s.eat("}"); return ("obj", items)
        if v == "[":
            items = []
            while s.peek()[1] != "]":
                items.append(s.expr())
                if not s.accept(","): break
            s.eat("]"); return ("arr", items)
        raise ValueError(f"unexpected {v!r}")


def jstr(v):
    if v is None: return ""
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, float) and v == int(v): return str(int(v))
    if isinstance(v, (int, float)): return format(v, ".15g")
    return v if isinstance(v, str) else json.dumps(v)
def truthy(v):
    if v is None: return False
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)): return v != 0
    if isinstance(v, str): return v != ""
    return any(truthy(x) for x in v) if isinstance(v, list) else bool(v)
def jnum(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)): raise ValueError(f"{x!r} is not a number")
    return x
def _flat(a):
    out = []
    for x in a: out += _flat(x) if isinstance(x, list) else [] if x is None else [jnum(x)]
    return out
def _n(f): return lambda x, *r: None if x is None else f(jnum(x), *r)
JF = {"$lookup": lambda o, k=None: o.get(k) if isinstance(o, dict) else None, "$round": lambda x, p=0: None if x is None else round(jnum(x), int(p)),
      "$number": lambda x: None if x is None else float(x), "$string": jstr, "$boolean": truthy, "$not": lambda x: not truthy(x),
      "$exists": lambda x: x is not None, "$contains": lambda s, sub: None if s is None else str(sub) in str(s),
      "$lowercase": lambda s: None if s is None else str(s).lower(), "$uppercase": lambda s: None if s is None else str(s).upper(),
      "$length": lambda s: None if s is None else len(str(s)), "$min": lambda *a: min(_flat(a)), "$max": lambda *a: max(_flat(a)),
      "$sum": lambda *a: sum(_flat(a)), "$count": lambda *a: len(_flat(a)), "$floor": _n(math.floor), "$ceil": _n(math.ceil),
      "$abs": _n(abs), "$sqrt": _n(math.sqrt), "$power": lambda a, b: None if a is None or b is None else jnum(a) ** jnum(b)}


def jeval(n, env, ctx):
    t = n[0]
    if t == "lit": return n[1]
    if t == "name": return ctx.get(n[1])
    if t == "var": return ctx if n[1] in ("$", "$$") else env.get(n[1])
    if t == "step":
        l = jeval(n[1], env, ctx); return l.get(n[2]) if isinstance(l, dict) else None
    if t == "index":
        l, i = jeval(n[1], env, ctx), jeval(n[2], env, ctx)
        return l[int(i)] if isinstance(l, list) and isinstance(i, (int, float)) and -len(l) <= int(i) < len(l) else None
    if t == "block":
        e2, r = dict(env), None
        for st in n[1]: r = jeval(st, e2, ctx)
        return r
    if t == "bind": env[n[1]] = jeval(n[2], env, ctx); return env[n[1]]
    if t == "obj":
        out = {}
        for k, v in n[1]:
            val = jeval(v, env, ctx)
            if val is not None: out[jstr(jeval(k, env, ctx))] = val
        return out
    if t == "arr": return [x for x in (jeval(i, env, ctx) for i in n[1]) if x is not None]
    if t == "if": return jeval(n[2] if truthy(jeval(n[1], env, ctx)) else n[3], env, ctx)
    if t == "neg":
        x = jeval(n[1], env, ctx); return None if x is None else -jnum(x)
    if t == "call":
        if n[1] not in JF: raise ValueError(f"unsupported function {n[1]}")
        return JF[n[1]](*[jeval(a, env, ctx) for a in n[2]])
    op = n[1]
    if op == "and": return truthy(jeval(n[2], env, ctx)) and truthy(jeval(n[3], env, ctx))
    if op == "or": return truthy(jeval(n[2], env, ctx)) or truthy(jeval(n[3], env, ctx))
    a, b = jeval(n[2], env, ctx), jeval(n[3], env, ctx)
    if op == "&": return jstr(a) + jstr(b)
    if op == "in": return a in b if isinstance(b, list) else a == b
    if op in ("=", "!="): return ((a == b) == (op == "=")) if a is not None and b is not None else False
    if a is None or b is None: return None if op in ("+", "-", "*", "/", "%") else False
    if op in ("<", "<=", ">", ">="): return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]
    a, b = jnum(a), jnum(b)
    return {"+": lambda: a + b, "-": lambda: a - b, "*": lambda: a * b, "/": lambda: a / b, "%": lambda: a % b}[op]()


def usd_range(r):
    num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)
    if num(r): return (r, r)
    if isinstance(r, dict):
        if "min_usd" in r or "max_usd" in r:
            lo = r.get("min_usd", r.get("max_usd")); return (lo, r.get("max_usd", lo))
        u = r.get("usd")
        if isinstance(u, list) and u and all(num(x) for x in u): return (min(u), max(u))
        if num(u): return (u, u)


async def node_price(nid, n, fixed, marked=()):
    """(low, high) credits for one API node, or None when it has no price / it can't be worked out."""
    if nid in fixed: return (fixed[nid], fixed[nid])
    await info(n["class_type"]); pb = PB.get(n["class_type"])
    if not pb:
        if (nid in marked or API.get(n["class_type"])) and n["class_type"] not in WARNED:
            WARNED.add(n["class_type"]); print(f"[credits] ComfyUI gave no price formula for {n['class_type']}. Update ComfyUI, or write the price by hand: (Credits 351.6)")
        return None
    try:
        dep = pb.get("depends_on") or {}
        inputs = {k: {"connected": link(v)} for k, v in n["inputs"].items()}
        for nm in dep.get("inputs", []): inputs.setdefault(nm, {"connected": False})
        groups = {nm: {"connected": sum(1 for k, v in n["inputs"].items() if k.startswith(nm + ".") and link(v))} for nm in dep.get("input_groups", [])}
        ctx = {"widgets": {f: v for f, v in n["inputs"].items() if not link(v)}, "inputs": inputs, "input_groups": groups}
        r = jeval(JP(jlex(pb["expr"])).parse(), {}, ctx); rg = usd_range(r)
        if rg is None: raise ValueError(f"the formula gave {r!r}, which has no price in it")
        return (rg[0] * CPU, rg[1] * CPU)
    except Exception as e:
        if n["class_type"] not in WARNED:
            WARNED.add(n["class_type"]); print(f"[credits] could not work out the price of {n['class_type']}: {e}\n          formula: {str(pb.get('expr'))[:400]}")
        return None


def fix_num(e, n):
    """Keep a number inside min/max, snap it to the closest stp (counted from min) and round it to dec decimals."""
    lo, hi = e.get("min"), e.get("max")
    if lo is not None: n = max(lo, n)
    if hi is not None: n = min(hi, n)
    if e.get("stp"):
        base = lo if lo is not None else 0
        n = base + math.floor((n - base) / e["stp"] + 0.5) * e["stp"]
        if hi is not None and n > hi: n -= e["stp"]
        if lo is not None and n < lo: n += e["stp"]
    if e["type"] == "int": return int(round(n))
    return round(n, e["dec"] if e.get("dec") is not None else 6)


def live(g):
    seen, stack = set(), [i for i, n in g.items() if is_out(n)]
    while stack:
        i = stack.pop()
        if i in seen or i not in g: continue
        seen.add(i); stack += [v[0] for v in g[i]["inputs"].values() if link(v)]
    return seen


async def price_of(wid, vals, present):
    """Credits for this workflow with these settings and these inputs present -> [low, high] or None."""
    g = read_wf(wid); m = await parse(wid, g); drop = []
    for i in m["inputs"]:
        k, ni = f'{i["node"]}.{i["field"]}', g[i["node"]]["inputs"]
        if i["kind"] == "param" and vals.get(k) not in (None, ""):
            try:
                val = CAST.get(i["type"], str)(vals[k]); ni[i["field"]] = fix_num(i, val) if i["type"] in ("int", "float") else val
            except (ValueError, TypeError): pass
        elif i["kind"] in ("image", "audio", "video") and k not in present: drop.append(i["node"])
    g = await prune(g, drop); lo = hi = 0.0; found = False
    for nid in live(g):
        r = await node_price(nid, g[nid], m["credits"], m["priced"])
        if r: lo += r[0]; hi += r[1]; found = True
    return [round(lo, 1), round(hi, 1)] if found else None


def spec_of(oi, inputs, f):
    """ComfyUI's definition of one field, also for sub-fields of dynamic combos such as 'format.bit_depth'."""
    d = (oi.get("required") or {}).get(f) or (oi.get("optional") or {}).get(f)
    if d: return d
    if "." in f:
        parent, _, child = f.partition(".")
        ps = (oi.get("required") or {}).get(parent) or (oi.get("optional") or {}).get(parent) or []
        opts = ps[1].get("options") if len(ps) > 1 and isinstance(ps[1], dict) else None
        for o in opts if isinstance(opts, list) else []:
            if isinstance(o, dict) and o.get("key") == inputs.get(parent):
                sub = o.get("inputs") or {}
                return (sub.get("required") or {}).get(child) or (sub.get("optional") or {}).get(child)


def combo_opts(t, x):
    """The choices of a combo field: a plain list, 'COMBO' + options, or a dynamic combo with {key, inputs} options."""
    if isinstance(t, list): return t
    o = x.get("options")
    if isinstance(o, list) and o: return [(e.get("key", e.get("value", e.get("name"))) if isinstance(e, dict) else e) for e in o]


async def fields(n, c, label, o, setup=False):
    """Literal fields of an (Input)/(Setup) node, narrowed by [1,3] when given -> (entries, warnings)."""
    oi, out, ws = await info(c), [], []
    base, named = o["name"] or label, bool(o["name"])  # {Custom name} replaces the field/node name
    lits = {f: v for f, v in n["inputs"].items() if not link(v) and isinstance(v, (str, int, float))}
    if o["idx"]:  # counted from 1 over the node's own fields, in the order listed
        names = list(lits)
        ws = [f"{label}: has no field {i} (it has {len(names)})" for i in o["idx"] if not 1 <= i <= len(names)]
        lits = {names[i - 1]: lits[names[i - 1]] for i in o["idx"] if 1 <= i <= len(names)}
    tf = None if setup else next((f for f in TEXT_FIELDS if isinstance(lits.get(f), str)), None)
    if tf: out.append({"kind": "text", "field": tf, "label": base, "named": named, "value": lits.pop(tf)})
    for f, v in lits.items():
        sp = spec_of(oi, n["inputs"], f) or []
        t = sp[0] if sp else None
        x = sp[1] if len(sp) > 1 and isinstance(sp[1], dict) else {}
        opts = combo_opts(t, x)
        if opts: t = opts
        if isinstance(t, list) and not t: t = None
        ty = ("select" if isinstance(t, list) else "bool" if t == "BOOLEAN" or isinstance(v, bool) else
              "int" if t == "INT" or (t is None and isinstance(v, int)) else
              "float" if t == "FLOAT" or isinstance(v, float) else "text")
        e = {"kind": "param", "field": f, "type": ty, "value": v, "seed": f in SEEDS and not setup,
             "label": base if len(lits) == 1 else f"{base}: {f.replace('_', ' ')}", "named": named,
             "options": t if isinstance(t, list) else None, "min": x.get("min"), "max": x.get("max")}
        if ty in ("int", "float"):  # min / max / stp / dec in the title beat ComfyUI's own limits
            for kk in ("min", "max"):
                if o.get(kk) is not None: e[kk] = o[kk]
            e["step"] = x.get("step")  # ComfyUI's own step: the slider's default
            if o.get("stp"): e["stp"] = o["stp"]  # snap typed numbers to the closest multiple (counted from min)
            if o.get("dec") is not None: e["dec"] = 0 if ty == "int" else max(0, min(6, int(o["dec"])))
            e["slider"] = bool(o.get("slider"))
        if setup: e["error"] = chk(v, e["options"])
        out.append(e)
    return out, ws


async def parse(wid, g):
    ins, outs, setup, warns, credits, priced = [], [], [], [], {}, set()
    for nid, n in g.items():
        label, marks, rules = tags(n); c = n["class_type"]
        names = [f for f, v in n["inputs"].items() if not link(v) and isinstance(v, (str, int, float))]
        mine = []
        for o in marks:
            kind = o["kind"]
            if kind == "credits":  # (Credits) = a closed-source node, priced live; (Credits 351.6) = a fixed price instead
                priced.add(nid)
                if o.get("credits") is not None: credits[nid] = o["credits"]
                continue
            if kind == "output":
                outs.append({"node": nid, "kind": OUT.get(c) or next((k for k in ("video", "audio") if k in c.lower()), "image")})
            elif kind == "input" and c in MEDIA:
                e = {"node": nid, "kind": MEDIA[c][0], "field": MEDIA[c][1], "label": o["name"] or label,
                     "named": bool(o["name"]), "optional": o["optional"], "order": o["order"]}
                if o["group"]: e["group"], e["pos"], e["max"] = o["group"]  # (Input optional [image 2/10])
                mine.append(add(ins, e))
            else:
                es, ws = await fields(n, c, label, o, kind == "setup"); warns += ws
                for e in es:
                    kept = add(setup if kind == "setup" else ins, {"node": nid, "order": o["order"], **e})
                    if kind != "setup": mine.append(kept)
        for r in rules:  # {custom ratio} on [1]: those fields only show while that switch is on / off
            for e in mine:
                if not r["idx"] or (e["field"] in names and names.index(e["field"]) + 1 in r["idx"]):
                    e["showIf"] = {"name": r["name"], "on": r["on"]}
    for i in ins:  # a media input is "required" unless marked optional or the graph still runs without it
        if i["kind"] in ("image", "audio", "video"):
            i["required"] = not (i["optional"] or has_out(await prune(g, [i["node"]])))
    classes = {n["class_type"] for n in g.values()}
    for c in classes: await info(c)
    paid = bool(priced) or any(API.get(c) or PB.get(c) for c in classes)  # API (closed-source) nodes use credits
    for lst in (ins, setup):  # (1.Input) (2.Input): numbered ones first, the rest keep their order
        lst.sort(key=lambda e: (e["order"] is None, e["order"] or 0))
    return {"id": wid, "name": wid.replace("_", " "), "type": outs[0]["kind"] if outs else None,
            "inputs": ins, "outputs": outs, "warns": warns, "setup": setup, "credits": credits, "paid": paid, "priced": sorted(priced)}


def err_text(j):
    e = j.get("error")
    msg = e.get("message") if isinstance(e, dict) else str(e or "ComfyUI rejected the workflow")
    ne = [f'{v.get("class_type")}: {x.get("message")}' for v in (j.get("node_errors") or {}).values() for x in v.get("errors", [])]
    return "; ".join([msg] + ne[:3])


# ---------- routes ----------
async def models(req):
    t, res = req.query.get("type"), []
    for p in sorted(WF.glob("*.json")):
        try: m = await parse(p.stem, read_wf(p.stem))
        except Exception as e: m = {"id": p.stem, "name": p.stem, "type": None, "inputs": [], "error": str(e)}
        if not t or m["type"] == t: res.append(m)
    return web.json_response(res)


async def put_workflow(req):  # add new or replace an existing workflow (same name = update)
    d = await req.post(); f = d["file"]
    try: g = json.loads(f.file.read().decode("utf-8"))
    except ValueError: return web.json_response({"error": "File is not valid JSON."}, status=400)
    if "nodes" in g or not all(isinstance(n, dict) and "class_type" in n for n in g.values()):
        return web.json_response({"error": "Not an API workflow. In ComfyUI use Workflow > Export (API)."}, status=400)
    wid = slug(d.get("name") or Path(f.filename).stem) or "workflow"
    if not (await parse(wid, g))["outputs"]:
        return web.json_response({"error": "No node titled '(Output)'. Rename your Save node, e.g. 'Result (Output)'."}, status=400)
    (WF / f"{wid}.json").write_text(json.dumps(g), "utf-8")
    return web.json_response({"id": wid})


async def save_setup(req):  # body {"values": {"node.field": value}}, merged into the saved choices
    sf = SETUP / f"{Path(req.match_info['id']).name}.json"
    cur = json.loads(sf.read_text("utf-8")) if sf.exists() else {}
    cur.update((await req.json()).get("values", {})); sf.write_text(json.dumps(cur), "utf-8")
    return web.json_response({"ok": True})


async def rename(req):
    old, new = Path(req.match_info["id"]).name, slug((await req.json()).get("name", ""))
    if not new: return web.json_response({"error": "The name can't be empty."}, status=400)
    if new != old and (WF / f"{new}.json").exists():
        return web.json_response({"error": "A workflow with that name already exists."}, status=409)
    (WF / f"{old}.json").rename(WF / f"{new}.json")
    if (SETUP / f"{old}.json").exists(): (SETUP / f"{old}.json").rename(SETUP / f"{new}.json")
    return web.json_response({"id": new})


async def del_workflow(req):
    wid = Path(req.match_info["id"]).name
    (WF / f"{wid}.json").unlink(missing_ok=True); (SETUP / f"{wid}.json").unlink(missing_ok=True)
    return web.json_response({"ok": True})


async def generate(req):
    d = await req.post(); wid = Path(d["workflow"]).name
    g = read_wf(wid); m = await parse(wid, g); drop, ups = [], {}
    bad = [e["label"] for e in m["setup"] if e["error"]]
    if bad: return web.json_response({"error": "Setup needed for: " + ", ".join(bad) + ". Open Manager > Setup.", "setup": True}, status=400)
    for n in g.values():  # fresh seed every run, even on nodes that are not marked (Input)
        for f in SEEDS:
            if isinstance(n["inputs"].get(f), int): n["inputs"][f] = random.randint(0, 2**50)
    for i in m["inputs"]:
        k, v, n = f'{i["node"]}.{i["field"]}', d.get(f'{i["node"]}.{i["field"]}'), g[i["node"]]["inputs"]
        if i["kind"] == "text":
            if v is not None: n[i["field"]] = str(v)
        elif i["kind"] == "param":
            if i["seed"] and v in (None, "", "-1"): n[i["field"]] = random.randint(0, 2**50)
            elif v not in (None, ""):
                val = CAST.get(i["type"], str)(v); n[i["field"]] = fix_num(i, val) if i["type"] in ("int", "float") else val
        elif v is None or not hasattr(v, "file"):
            drop.append(i)  # left plain -> node is disabled
        else:
            # aiohttp cannot forward its temp-file wrapper, so send the bytes. The name is unique per upload,
            # so two queued jobs can never overwrite each other's inputs.
            v.file.seek(0)
            fd = aiohttp.FormData()
            fd.add_field("image", v.file.read(), filename=f"studio_{uuid.uuid4().hex[:10]}{Path(v.filename or '').suffix.lower()}",
                         content_type=v.content_type or "application/octet-stream")
            async with S.post(f"{COMFY}/upload/image", data=fd) as r:
                u = await r.json()
                if r.status != 200: return web.json_response({"error": f"ComfyUI refused {v.filename}: {u}"}, status=400)
            n[i["field"]] = (u["subfolder"] + "/" if u.get("subfolder") else "") + u["name"]
            ups[f'{i["node"]}.{i["field"]}'] = {"name": u["name"], "subfolder": u.get("subfolder", "")}  # lets the interface restore these inputs later
    g = await prune(g, [i["node"] for i in drop])
    if not has_out(g):
        need = ", ".join(dict.fromkeys(i.get("group") or i["label"] for i in drop)) or "an input"
        return web.json_response({"error": f"This model needs: {need}."}, status=400)
    async with S.post(f"{COMFY}/prompt", json={"prompt": g}) as r:
        j = await r.json()
        if r.status != 200: return web.json_response({"error": err_text(j)}, status=400)
    JOBS[j["prompt_id"]] = {o["node"] for o in m["outputs"]}
    return web.json_response({"id": j["prompt_id"], "uploads": ups})


async def job(req):
    pid = req.match_info["id"]
    async with S.get(f"{COMFY}/history/{pid}") as r: h = (await r.json()).get(pid)
    if not h: return web.json_response({"state": "running"})
    st = h.get("status", {})
    if st.get("status_str") == "error":
        msg = next((x[1].get("exception_message") for x in st.get("messages", []) if x[0] == "execution_error"), "Generation failed")
        return web.json_response({"state": "error", "error": msg})
    files = []
    for nid, o in h.get("outputs", {}).items():
        if pid in JOBS and nid not in JOBS[pid]: continue
        for v in o.values():
            for x in v if isinstance(v, list) else []:
                if isinstance(x, dict) and "filename" in x:
                    q = urlencode({k: x.get(k, "") for k in ("filename", "subfolder", "type")})
                    files.append({"url": "/api/view?" + q, "kind": file_kind(x["filename"])})
    return web.json_response({"state": "done", "files": files})


async def view(req):  # proxy ComfyUI /view with Range support so videos can seek
    hd = {"Range": req.headers["Range"]} if "Range" in req.headers else {}
    async with S.get(f"{COMFY}/view", params=req.query, headers=hd) as r:
        resp = web.StreamResponse(status=r.status, headers={k: r.headers[k] for k in
                                  ("Content-Type", "Content-Length", "Content-Range", "Accept-Ranges") if k in r.headers})
        await resp.prepare(req)
        async for c in r.content.iter_chunked(1 << 16): await resp.write(c)
        return resp


async def price(req):
    d = await req.json()
    return web.json_response({"credits": await price_of(Path(d["workflow"]).name, d.get("vals", {}), set(d.get("present", [])))})


async def guide(req): return web.FileResponse(ROOT / "Naming Guide.html")


async def clear(req):  # delete the files Studio generated (the browser sends the list it knows about)
    n = 0
    for f in (await req.json()).get("files", []):
        kind = f.get("type") if f.get("type") in ("temp", "input") else "output"
        name = Path(f.get("filename", "")).name
        if kind == "input" and not name.startswith("studio_"): continue  # never touch the user's own input files
        base = (COMFY_DIR / kind).resolve()
        p = (base / f.get("subfolder", "") / name).resolve()
        if base in p.parents and p.is_file():  # never touch anything outside ComfyUI's output folder
            try: p.unlink(); n += 1
            except OSError: pass
    return web.json_response({"deleted": n})


async def index(req): return web.FileResponse(ROOT / "index.html")


def tidy():  # remove our own uploads from ComfyUI's input folder after 30 days
    for p in (COMFY_DIR / "input").glob("studio_*"):
        try:
            if time.time() - p.stat().st_mtime > 2592000: p.unlink()
        except OSError: pass


@web.middleware
async def guard(req, handler):
    try: return await handler(req)
    except web.HTTPException: raise
    except aiohttp.ClientConnectionError:
        return web.json_response({"error": f"ComfyUI is not reachable at {COMFY}. Start it first."}, status=502)
    except Exception as e:  # show the real reason in the interface instead of "Internal Server Error"
        import traceback; traceback.print_exc()
        return web.json_response({"error": f"{type(e).__name__}: {e}"}, status=500)


async def up():
    try:
        async with S.get(f"{COMFY}/system_stats", timeout=aiohttp.ClientTimeout(total=2)) as r: return r.status == 200
    except (aiohttp.ClientError, asyncio.TimeoutError): return False


def comfy_cmd():
    """Command that starts ComfyUI like the user's own run_*.bat (same Python, flags and folder), plus 'no browser tab'."""
    extra = ["--disable-auto-launch", "--port", str(urlparse(COMFY).port or 8188)] + os.environ.get("COMFY_ARGS", "").split()
    root = COMFY_DIR.parent
    for b in sorted(root.glob("run*.bat"), key=lambda p: (p.name != "run_nvidia_gpu.bat", p.name)):
        for line in b.read_text("utf-8", "ignore").splitlines():
            if "main.py" in line and not line.strip().lower().startswith(("rem", "::")):
                toks = [t.strip('"') for t in shlex.split(line, posix=False)]
                exe = Path(toks[0]) if Path(toks[0]).is_absolute() else root / toks[0]
                if exe.exists(): return [str(exe.resolve())] + toks[1:] + extra, root
    return [sys.executable, "-s", "main.py"] + extra, COMFY_DIR


async def boot():
    """Start ComfyUI (terminal only, no browser tab) if it is not running yet, then open Studio."""
    global PROC
    if os.environ.get("COMFY_START", "1") != "0" and not await up():
        if (COMFY_DIR / "main.py").exists():
            cmd, cwd = comfy_cmd()
            print("Starting ComfyUI the same way your run_*.bat does. The first start can take a minute...")
            env = {k: v for k, v in os.environ.items() if k.upper() not in ("PYTHONHOME", "PYTHONPATH", "PYTHONOPTIMIZE", "PYTHONSTARTUP")}
            PROC = subprocess.Popen(cmd, cwd=cwd, env=env)
            while not await up():
                if PROC.poll() is not None:
                    print("\nComfyUI could not start (see the messages above).\nStart it the way you normally do; Comfy Studio will connect to it by itself.\n")
                    break
                await asyncio.sleep(1)
        else:
            print(f"ComfyUI is not running and no main.py was found in {COMFY_DIR}.")
    print(f"Comfy Studio is ready: http://127.0.0.1:{PORT}")
    webbrowser.open(f"http://127.0.0.1:{PORT}")


async def session(app):
    global S
    S = aiohttp.ClientSession(); tidy(); task = asyncio.create_task(boot())
    yield
    task.cancel()
    if PROC and PROC.poll() is None:  # stop the ComfyUI we started
        PROC.terminate()
        try: PROC.wait(15)
        except subprocess.TimeoutExpired: PROC.kill()
    await S.close()


app = web.Application(client_max_size=2 * 1024**3, middlewares=[guard])
app.cleanup_ctx.append(session)
app.add_routes([web.get("/", index),
                web.get("/api/models", models), web.post("/api/workflows", put_workflow),
                web.delete("/api/workflows/{id}", del_workflow), web.post("/api/workflows/{id}/rename", rename), web.put("/api/workflows/{id}/setup", save_setup), web.post("/api/clear", clear), web.post("/api/price", price), web.get("/guide", guide), web.post("/api/generate", generate),
                web.get("/api/jobs/{id}", job), web.get("/api/view", view)])

if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=PORT)
