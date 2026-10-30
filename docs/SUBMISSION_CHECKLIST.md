# Submission checklist for beginners

You do **not** need to be a programmer to submit this. Follow the steps in order. The challenge deadline is **October 30, 2026, 9:00am PT**.

> **Time-saving tip:** if you are close to the deadline, do steps 1, 3, 4, and 6 first. A working repo, a 2-minute video, and the Typeform matter most. Example screenshots and a polished README can be improved later.

---

## Step 0 — Check what you have (5 minutes)

- [ ] ComfyUI runs on your computer.
- [ ] At least one of the included workflows runs in ComfyUI (Qwen Image 2.1 is the easiest).
- [ ] This folder (`comfy-studio-github`) is on your computer.
- [ ] You have a GitHub account. If not, create one free at <https://github.com/join>.
- [ ] You have a screen recorder (OBS, Xbox Game Bar, or Loom).

---

## Step 1 — Test Comfy Studio locally (15–30 minutes)

1. Put this folder inside your ComfyUI folder, next to `main.py`:

```text
ComfyUI_windows_portable\
├── ComfyUI\
│   ├── main.py
│   ├── comfy-studio-github\   <-- this folder
│   └── ...
└── python_embeded\
```

2. Double-click **`Start Comfy Studio.bat`**.
3. Your browser should open `http://127.0.0.1:7860`.
4. Pick **Qwen 2.1**, type a simple prompt, and press **Generate**.
5. If it works, you are ready. If not, see [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

**Important:** the folder name in the tree is `comfy-studio-github`; you can rename it to `comfy-studio` before uploading. The repo name on GitHub can be `comfy-studio` either way.

---

## Step 2 — Add one real screenshot and one example output (10–20 minutes)

Judges like seeing the app and its results without running it.

1. While the app is open, take a screenshot of the main screen with a finished result. Save it as:

```text
docs/screenshots/main.png
```

2. Generate 1–3 good, SFW examples (image or video). Save small versions in:

```text
examples/
```

Use clear names like `qwen-portrait.png`, `krea-product.png`, or `minimax-cafe.mp4`.

3. Open `README.md` and replace the illustration line with your real screenshot:

```markdown
![Comfy Studio](docs/screenshots/main.png)
```

4. Add a short `examples/README.md` table listing what each example is and which workflow made it.

Keep files small. GitHub’s web uploader has a 25 MB limit per file, and the repo is easier to clone when it stays light. For video, a 5–10 second compressed clip is enough, or just link the demo video.

---

## Step 3 — Put the folder on GitHub (10 minutes)

Follow the detailed guide: [`GITHUB_UPLOAD.md`](GITHUB_UPLOAD.md).

The short version with **GitHub Desktop**:

1. Install GitHub Desktop: <https://desktop.github.com/>
2. Sign in with your GitHub account.
3. **File → Add Local Repository**.
4. Choose this folder (`comfy-studio-github`).
5. If it says it is not a Git repository, click **create a repository** and accept the defaults.
6. Write the summary `Initial commit` and click **Commit to main**.
7. Click **Publish repository**.
8. **Uncheck “Keep this code private.”** The challenge needs a public repo.
9. Name it `comfy-studio` and publish.

Then open the repo in your browser and check:

- [ ] The README shows.
- [ ] The `LICENSE` file is visible.
- [ ] The `workflows` folder is there.
- [ ] The repo is **Public** (the repo name at the top has a “Public” label).

---

## Step 4 — Record the 2-minute demo (30–45 minutes)

Use the script: [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md).

Minimum viable demo:

1. Show the app.
2. Generate one image live.
3. Show the result and its prompt/settings.
4. Show the GitHub repo and say it is MIT-licensed.
5. Keep it under 2:00.

Upload the video to YouTube (unlisted is fine) or Vimeo. Copy the link.

**Do not:**
- use copyrighted music,
- show private information,
- use celebrity faces or unlicensed characters,
- go over 2 minutes.

---

## Step 5 — Post the demo on social (5 minutes)

Post the video on **one** of: Reddit, X, Instagram, LinkedIn, YouTube, or TikTok.

Include:

```text
#OpenSourceHiggsfield
```

and the repo link. Use the template in [`SUBMISSION.md`](SUBMISSION.md).

Copy the post URL.

---

## Step 6 — Submit the Typeform (5 minutes)

Open the official form: <https://form.typeform.com/to/V1dSQrkS>

Fill in:

- your name and email,
- the public GitHub repo URL,
- the demo video URL,
- the social post URL,
- the short description from [`SUBMISSION.md`](SUBMISSION.md),
- the categories you want to be considered for.

Submit **before 9:00am PT on October 30**. Take a screenshot of the confirmation page.

---

## Step 7 — After submitting (optional)

- [ ] Add the demo video link to the top of `README.md`.
- [ ] Add the social post link.
- [ ] Add a “Try it” section if you deploy it.
- [ ] Reply to comments on your social post.
- [ ] Keep the repo public until winners are announced on **November 6**.

---

## If you are running out of time

Do these in order:

1. **Make the repo public** with the current files. A repo with no examples is still a valid entry.
2. **Record a 90-second demo** with one real generation.
3. **Submit the Typeform** with the repo and video links.
4. **Post on social** with `#OpenSourceHiggsfield`.
5. Improve screenshots/examples afterward if the form allows edits.

Missing polish is better than missing the deadline.

---

## Common beginner questions

**Do I need to pay for anything?**
No. GitHub is free. ComfyUI is free. The included local workflows use open-weight models. You only pay for hardware/electricity, or if you choose to use API/partner nodes.

**Do I need a website?**
No. A public GitHub repo is enough. The “link to try it” is optional.

**Can I use a private repo?**
The challenge requires an open-source license and setup instructions. Use a **public** repo.

**Can I submit more than one project?**
The rules say one submission per person. Submit this one.

**Does the repo need a license?**
Yes. This repo includes MIT in [`LICENSE`](../LICENSE). Keep it.

**Can I use partner models?**
Yes for the main prizes. Only the **Open Weights Only** category requires open weights with no partner nodes. This repo keeps the GPT partner workflow out of the default set, so the main demo is open weights.

**What if my GPU cannot run MiniMax H3?**
Demo Qwen or Krea instead. You can still enter the main categories. The MiniMax H3 bonus requires MiniMax H3 as the core video model, so skip that bonus if you cannot run it.

**Will my entry be featured?**
Winning entries are featured on `comfy.org/hub` with credit. By submitting, you agree ComfyUI, Runpod, LTX, Black Forest Labs, and MiniMax may feature your work with credit.
