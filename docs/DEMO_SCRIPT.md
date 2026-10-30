# 2-minute demo video script

The challenge asks for a **demo video of two minutes or less**. Comfy Org says they are judging the work, not your editing: “The best demo shows your work in action with an explanation of how it was built.”

This script is designed to be recorded in one take with a screen recorder. Read the lines naturally; do not rush.

---

## Before you record

- [ ] ComfyUI and Comfy Studio are already running.
- [ ] The `Qwen_2.1` workflow is set up and tested with one prompt.
- [ ] The `Minimax_H3_Ref2Va` workflow is set up (or use a second image workflow if your GPU is small).
- [ ] Your desktop is clean: close private tabs, notifications, and chat apps.
- [ ] Browser zoom is 100–110%; the UI is readable at 1080p.
- [ ] Record at **1920×1080** or **2560×1440**, 30 fps.
- [ ] Use a microphone. A cheap headset is fine; clear audio matters more than video quality.
- [ ] Do **not** use copyrighted music, film clips, celebrity faces, or unlicensed likenesses.
- [ ] Keep every generated example **SFW**.
- [ ] Have the GitHub repo page open in a second tab for the final shot.

**Suggested tools:** OBS Studio (free, Windows/macOS/Linux), or Xbox Game Bar on Windows (`Win + G`), or Loom.

---

## The script

### 0:00–0:15 — What it is

**Show:** The Comfy Studio home screen with the model picker and prompt box.

**Say:**

> “This is Comfy Studio, an open-source, Higgsfield-style front end for ComfyUI. It turns any ComfyUI API workflow into a simple app: pick a model, type an idea, add references, and generate. No node graph required.”

### 0:15–0:35 — Why it is different

**Show:** Click the model picker, then open **Manager** briefly to show the workflow list and the Setup panel. Close it.

**Say:**

> “The app reads the workflow’s node titles to build the interface automatically. A node marked Input becomes a control. A node marked Output becomes a result card. Setup fields become one-time model choices. That means creators can add their own workflows without writing front-end code.”

### 0:35–1:05 — Image generation

**Show:** Select **Qwen 2.1**. Type a prompt. Change the aspect ratio or megapixels. Add one reference image if you have a clean, SFW example. Press **Generate**.

**Say:**

> “Let’s make an image with Qwen Image 2.1, running locally in ComfyUI. I can type a prompt, choose a resolution, and add reference images. The app uploads the files to ComfyUI, queues the workflow, and streams the result back into the gallery.”

**Show:** The finished image card. Open it. Show the prompt and settings on the right. Click **Download** or **Copy inputs**.

**Say:**

> “Every result keeps its prompt, settings, and input files, so I can reuse the recipe or download the output.”

### 1:05–1:35 — Video generation

**Show:** Switch to **Video**, select **Minimax H3 Ref2Va**. Add one image and type a short motion prompt. Keep the duration short (3–5 seconds). Press **Generate**.

**Say:**

> “The same interface handles video and audio. MiniMax H3 takes reference images and a prompt, and returns a video with its own soundtrack. The controls come from the workflow itself: duration, resolution, reference slots, and model setup.”

**Show:** The finished video playing in the card, then open it.

**Say:**

> “The original audio is kept, and the result can be downloaded or reused.”

> If MiniMax is too slow for your GPU, substitute a second image workflow and say: “The same pattern works for any output type — image, video, or audio.”

### 1:35–1:50 — How it is built

**Show:** The GitHub repo page. Scroll to the README’s architecture diagram and the workflow guide link.

**Say:**

> “Under the hood it is one Python file and one HTML file. The backend talks to ComfyUI’s local HTTP API, uploads inputs, queues prompts, and polls for results. The repo includes the app, six local workflows, an MIT license, and a naming guide so other people can add their own models.”

### 1:50–2:00 — Close

**Show:** The studio again, then the repo URL.

**Say:**

> “It runs entirely on your own machine with open-weight models. The code is MIT-licensed and the repo is linked below. Thanks for watching.”

---

## After recording

1. Trim the start and end so the video is **under 2:00**.
2. Export at 1080p, H.264 MP4. Keep the file under ~500 MB.
3. Upload to **YouTube** (public or unlisted), Vimeo, or X. Do not upload a 2-minute video directly to GitHub unless it is small.
4. Copy the video URL into `docs/SUBMISSION.md`.
5. Post the video on at least one of Reddit, X, Instagram, LinkedIn, YouTube, or TikTok with **#OpenSourceHiggsfield**.
6. Put the social post URL in `docs/SUBMISSION.md` too.
7. Submit the Typeform before **October 30, 9am PT**.

---

## Backup plan if a model will not run

You do not need to show every workflow. A convincing demo can use **one image workflow** and **one video workflow**, or even two image workflows with different models. The important parts are:

- the app working end-to-end,
- the interface being usable,
- the workflow-to-app idea being clear,
- the repo and license being visible,
- the demo being under two minutes.

If generation is slow, cut to a previously generated result and say so. Do not fake a live result.
