# Challenge submission

This file is the copy-paste sheet for the **Open Source Higgsfield** challenge. Fill in the two placeholders, submit the form, and keep this file in the repo (or delete it before publishing if you prefer).

Official pages:

- Challenge: <https://comfy.org/open-source-higgsfield/>
- Sign up: <https://form.typeform.com/to/Ayn9Cwfj>
- Submit: <https://form.typeform.com/to/V1dSQrkS>
- Deadline: **October 30, 2026, 9:00am PT**
- Winners announced: **November 6, 2026**

---

## Fill these in

| Field | Your value |
| --- | --- |
| Public GitHub repo | `https://github.com/YOUR-USERNAME/comfy-studio` |
| Demo video (≤ 2 min) | `PASTE_YOUR_VIDEO_URL_HERE` |
| Social post | `PASTE_YOUR_POST_URL_HERE` |
| Optional live demo | `PASTE_A_DEPLOYED_LINK_OR_LEAVE_BLANK` |

After filling them in, update the same links in the **Challenge** section of `README.md` if you want them visible to visitors.

---

## One-line description

> Comfy Studio is an open-source, Higgsfield-style web app that turns any ComfyUI API workflow into a prompt-first creative studio for images, video, and audio.

## Short description

> Comfy Studio is a local web app that sits in front of ComfyUI. It reads API-exported workflows and builds a clean interface from their node titles: a prompt box, model picker, reference image/video/audio slots, sliders, toggles, setup fields, a result gallery, and a workflow manager. It runs entirely on your own machine with open-weight models, has no build step, and is MIT-licensed. The repo includes six ready-to-use workflows for Qwen Image 2.1, Krea 2, and MiniMax H3, a naming guide for adding more, and a two-minute demo script.

## Built with

- ComfyUI (local HTTP API)
- Python 3 / aiohttp
- Vanilla HTML, CSS, and JavaScript
- Qwen Image 2.1
- Krea 2
- MiniMax H3
- MIT License

## Category notes

| Category | Fit |
| --- | --- |
| Best Overall | Yes — working app, example workflows, docs, license |
| Most Innovative | Yes — a workflow-to-app UI generated from node-title markers, not another workflow dump |
| Most Viral | Strong — prompt-first UI, one-click launch, results gallery |
| Open Weights Only | Yes — the default `workflows/` folder is open weights only; the GPT partner workflow is kept in `examples/` and is not used in the demo |
| VFX / LTX bonus | No — LTX is not the core model |
| FLUX bonus | No — FLUX 3 is not the core model |
| MiniMax H3 bonus | Yes, if the demo shows the MiniMax H3 workflow. MiniMax H3 is the core video model in `Minimax_H3_Ref2Va.json` |

> If you demo MiniMax H3, say clearly in the video that MiniMax H3 is the core video model. That is the condition for the MiniMax H3 bonus.

---

## Requirement checklist

Copied from the official page and mapped to this repo:

- [x] **Built with ComfyUI** — uses ComfyUI’s local HTTP API (`/upload/image`, `/prompt`, `/history`, `/view`).
- [x] **Runs however you like** — local ComfyUI, with a documented path to Comfy Cloud / Developer Platform if you adapt `COMFY_URL`.
- [x] **Open-source license** — [`LICENSE`](../LICENSE) (MIT).
- [x] **Enough setup detail** — [`README.md`](../README.md), [`docs/MODELS.md`](MODELS.md), [`docs/TROUBLESHOOTING.md`](TROUBLESHOOTING.md).
- [x] **App code + workflow files in one repo** — `studio.py`, `index.html`, `workflows/`.
- [x] **Demo video ≤ 2 minutes** — script in [`docs/DEMO_SCRIPT.md`](DEMO_SCRIPT.md).
- [x] **Any extra tools/models explained** — [`docs/MODELS.md`](MODELS.md), README.
- [x] **Lawful and SFW** — example prompts are SFW; no bundled celebrity likenesses or unlicensed IP.
- [x] **Feature permission** — by submitting, you agree ComfyUI, Runpod, LTX, Black Forest Labs, and MiniMax may feature your work with credit. Read the official page before submitting.
- [x] **One submission per person** — keep it to one entry.

---

## Submission form answers

Use these as a starting point. Adjust the wording to sound like you.

**Project name**

```text
Comfy Studio
```

**Tagline**

```text
A Higgsfield-style studio for your own ComfyUI workflows.
```

**What did you build?**

```text
Comfy Studio is a local, open-source web app that turns ComfyUI API workflows into a prompt-first creative studio. Users pick a workflow, type a prompt, add reference images/video/audio, adjust the generated controls, and get images, video, or audio back. It includes a workflow manager, per-workflow model Setup, a result gallery, and a naming system that lets creators add new workflows without writing front-end code.
```

**How does it use ComfyUI?**

```text
It talks to a local ComfyUI server over its HTTP API. The backend uploads input files, queues API-format workflows with /prompt, polls /history, and proxies results through /view. The UI is generated from node titles in the workflow JSON. The included workflows use Qwen Image 2.1, Krea 2, and MiniMax H3, all running locally with open-weight models.
```

**What is innovative about it?**

```text
Most open-source ComfyUI apps are fixed front ends or workflow dumps. Comfy Studio is a generic workflow-to-app layer: a creator marks nodes with small title markers like (Input), (Output), (Setup), (Slider), and (Switch), exports the API workflow, and the app builds a usable interface automatically. That makes it a reusable app builder, not a single demo.
```

**Anything else?**

```text
The repo includes six local example workflows, an in-app naming guide, a model/setup guide, an MIT license, and a two-minute demo script. The default workflow set is open weights only; an optional GPT Image 2.5 partner workflow is kept out of the default folder so the main submission stays eligible for the Open Weights Only category.
```

---

## Social post template

Post the demo video on one of Reddit, X, Instagram, LinkedIn, YouTube, or TikTok. Tag **#OpenSourceHiggsfield**.

```text
I built Comfy Studio for the #OpenSourceHiggsfield challenge: an open-source, Higgsfield-style studio for your own ComfyUI workflows.

Pick a model, type a prompt, add references, generate. It reads API workflows and builds the UI from node titles, so creators can add new models without writing front-end code.

Local ComfyUI · open weights · MIT

Repo: https://github.com/YOUR-USERNAME/comfy-studio
Demo: PASTE_YOUR_VIDEO_URL_HERE
```

Keep the post SFW. Do not use copyrighted music, film clips, or celebrity likenesses.

---

## Final 10-minute check

- [ ] The repo is **public** and the README renders.
- [ ] `LICENSE` is visible in the repo root.
- [ ] The demo video is **under 2:00** and plays without logging in.
- [ ] The video shows the app generating at least one real result.
- [ ] The video explains that it is built with ComfyUI.
- [ ] The repo link in the video/description is correct.
- [ ] The social post uses **#OpenSourceHiggsfield**.
- [ ] The Typeform is submitted before **9:00am PT**.
- [ ] You kept a copy of the confirmation email/screenshot.
