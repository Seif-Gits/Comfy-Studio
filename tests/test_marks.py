"""Logic tests for Comfy Studio. They need no ComfyUI.   Run:  python -m unittest discover -s tests -v"""
import asyncio, json, sys, types, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
try:
    import aiohttp  # noqa: F401
except ImportError:  # lets the tests run on a machine without ComfyUI's Python
    a = types.ModuleType("aiohttp"); a.ClientError = a.ClientConnectionError = type("E", (Exception,), {})
    w = types.ModuleType("web"); w.middleware = lambda f: f; a.web = w
    sys.modules.update({"aiohttp": a, "aiohttp.web": w})
ns = {"__file__": str(ROOT / "studio.py")}
exec((ROOT / "studio.py").read_text("utf-8").split("# ---------- routes")[0], ns)  # everything except the web routes
run = asyncio.run
T = lambda title, cls="X", inputs=None: {"class_type": cls, "inputs": inputs or {}, "_meta": {"title": title}}
ns["OI"].update({c: {} for c in ("LoadImage", "SaveImage", "SaveVideo", "CLIPTextEncode")})


class Marks(unittest.TestCase):
    def test_titles(self):
        label, marks, rules = ns["tags"](T("Load Image (Input optional {Reference photos} [image 2/10])"))
        m = marks[0]
        self.assertEqual((label, m["kind"], m["name"], m["optional"], m["group"]), ("Load Image", "input", "Reference photos", True, ("image", 2, 10)))
        m = ns["tags"](T("N (2.Slider {Seconds} [5] min:3/max:15 step:2)"))[1][0]
        self.assertEqual((m["order"], m["slider"], m["idx"], m["min"], m["max"], m["step"]), (2, True, [5], 3.0, 15.0, 2.0))
        self.assertEqual(len(ns["tags"](T("Switch (Input {A} [1]) (Input [2])"))[1]), 2)
        self.assertEqual(ns["tags"](T("Seedance (Credits)"))[1][0]["kind"], "credits")

    def test_show_rule(self):
        label, marks, rules = ns["tags"](T("Resolution (Input [1,2]) {Custom ratio} on [1]"))
        self.assertEqual((label, rules), ("Resolution", [{"name": "custom ratio", "on": True, "idx": [1]}]))

    def test_slug_keeps_dots(self):
        self.assertEqual(ns["slug"]("Qwen 2.1"), "Qwen_2.1")
        self.assertEqual(ns["slug"](".."), "")


class Graphs(unittest.TestCase):
    def setUp(self):
        ns["OI"]["Pick"] = {"required": {"mode": [["a", "b"], {}], "n": ["INT", {"min": 1, "max": 9}], "flag": ["BOOLEAN", {}]}}
        ns["OI"]["Dyn"] = {"required": {"fmt": ["COMFY_DYNAMICCOMBO_V3", {"options": [{"key": "png", "inputs": {"required": {"depth": [["8", "16"], {}]}}}]}]}}
        ns["OI"]["Join"] = {"required": {"a": ["IMAGE"]}, "optional": {"b": ["IMAGE"]}}

    def test_fields_and_dedupe(self):
        g = {"1": T("Pick (Input) (Switch {Fast mode} [3])", "Pick", {"mode": "a", "n": 3, "flag": True}), "2": T("Save (Output)", "SaveImage")}
        m = run(ns["parse"]("t", g))
        f = {e["field"]: e for e in m["inputs"]}
        self.assertEqual(f["mode"]["options"], ["a", "b"]); self.assertEqual(f["n"]["type"], "int"); self.assertEqual(f["n"]["max"], 9)
        self.assertEqual((f["flag"]["label"], f["flag"]["named"]), ("Fast mode", True))
        self.assertEqual(len([e for e in m["inputs"] if e["field"] == "flag"]), 1)  # marked twice, shown once

    def test_dynamic_combo(self):
        g = {"1": T("Dyn (Input)", "Dyn", {"fmt": "png", "fmt.depth": "8"}), "2": T("Save (Output)", "SaveImage")}
        f = {e["field"]: e for e in run(ns["parse"]("t", g))["inputs"]}
        self.assertEqual((f["fmt"]["options"], f["fmt.depth"]["options"]), (["png"], ["8", "16"]))

    def test_empty_optional_upload_is_pruned(self):
        g = {"1": T("L (Input optional)", "LoadImage", {"image": "a.png"}), "2": T("L2 (Input optional)", "LoadImage", {"image": "b.png"}),
             "3": T("Join", "Join", {"a": ["1", 0], "b": ["2", 0]}), "4": T("Save (Output)", "SaveImage", {"images": ["3", 0]})}
        self.assertTrue(ns["has_out"](run(ns["prune"](g, ["2"]))))                  # optional input: the link is just cut
        self.assertFalse(ns["has_out"](run(ns["prune"](g, ["1"]))))                 # required input gone: nothing can run

    def test_group_members_and_order(self):
        g = {str(i): T(f"L (Input optional [image {i}/3])", "LoadImage", {"image": "x.png"}) for i in (1, 2, 3)}
        g["9"] = T("Save (Output)", "SaveImage"); g["8"] = T("P (1.Input)", "CLIPTextEncode", {"text": "hi"})
        m = run(ns["parse"]("t", g))
        self.assertEqual(m["inputs"][0]["kind"], "text")                               # 1. puts the prompt first
        self.assertEqual(sorted(e["pos"] for e in m["inputs"] if e.get("group")), [1, 2, 3])


class Credits(unittest.TestCase):
    ev = staticmethod(lambda e, w=None: ns["jeval"](ns["JP"](ns["jlex"](e)).parse(), {}, {"widgets": w or {}, "inputs": {}, "input_groups": {}}))

    def test_formulas(self):
        self.assertEqual(self.ev('({"type":"usd","usd": $lookup({"720p":0.5,"1080p":1.2}, widgets.r) * widgets.d})', {"r": "720p", "d": 5}), {"type": "usd", "usd": 2.5})
        self.assertEqual(self.ev('($p := widgets.a ? 0.3 : 0.2; {"usd": $round(widgets.d * $p, 2)})', {"a": True, "d": 5}), {"usd": 1.5})
        self.assertEqual(self.ev('$contains(widgets.m, "pro") ? 1 : 2', {"m": "x pro"}), 1)
        self.assertEqual(self.ev('-(1+2)*3'), -9)
        self.assertEqual(ns["usd_range"]({"type": "list_usd", "usd": [0.1, 0.3]}), (0.1, 0.3))

    def test_live_price_follows_inputs(self):
        ns["OI"]["Api"] = {"required": {"d": ["INT", {}]}, "optional": {"image_1": ["IMAGE"]}}
        ns["PB"]["Api"] = {"expr": '({"type":"usd","usd": widgets.d * 0.1 * (inputs.image_1.connected ? 2 : 1)})', "depends_on": {}}
        g = {"1": T("L (Input optional)", "LoadImage", {"image": "a.png"}), "2": T("Api (Input [1]) (Credits)", "Api", {"d": 5, "image_1": ["1", 0]}),
             "3": T("Save (Output)", "SaveVideo", {"v": ["2", 0]})}
        path = ns["WF"] / "_test_price.json"; path.write_text(json.dumps(g))
        try:
            self.assertEqual(run(ns["price_of"]("_test_price", {}, [])), [105.5, 105.5])             # no image: 0.5 USD x 211
            self.assertEqual(run(ns["price_of"]("_test_price", {}, ["1.image"])), [211.0, 211.0])   # image connected: doubled
            self.assertEqual(run(ns["price_of"]("_test_price", {"2.d": "10"}, ["1.image"])), [422.0, 422.0])
            self.assertTrue(run(ns["parse"]("_test_price", g))["paid"])
        finally: path.unlink()


if __name__ == "__main__":
    unittest.main()
