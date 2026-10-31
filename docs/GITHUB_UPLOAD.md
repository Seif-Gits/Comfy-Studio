# How to put this folder on GitHub

You have three options. **GitHub Desktop is the easiest for beginners.** Pick one.

---

## Option A — GitHub Desktop (recommended)

### 1. Create a GitHub account

Go to <https://github.com/join> and sign up. Verify your email.

### 2. Install GitHub Desktop

Download it from <https://desktop.github.com/> and sign in with the account you just created.

### 3. Add this folder

1. Open GitHub Desktop.
2. Choose **File → Add Local Repository**.
3. Select this folder (`comfy-studio`).
4. If GitHub Desktop says it is not a Git repository, click **create a repository**.
5. Keep the name `comfy-studio`, choose `main` as the branch, and click **Create Repository**.

### 4. Make the first commit

1. You should see all the files in the **Changes** tab.
2. At the bottom left, type the summary:

```text
Initial commit: Comfy Studio
```

3. Click **Commit to main**.

### 5. Publish it

1. Click **Publish repository** at the top.
2. Name: `comfy-studio`
3. Description: `A Higgsfield-style studio for your own ComfyUI workflows.`
4. **Uncheck “Keep this code private.”** The challenge needs a public repo.
5. Click **Publish repository**.

### 6. Check it

Open `https://github.com/YOUR-USERNAME/comfy-studio` in your browser.

- [ ] README renders with the banner.
- [ ] `LICENSE` is visible.
- [ ] The repo says **Public** at the top.
- [ ] `workflows/` contains the JSON files.

---

## Option B — Upload through the GitHub website

Use this if you do not want to install anything.

### 1. Create an empty repository

1. Go to <https://github.com/new>.
2. Repository name: `comfy-studio`
3. Description: `A Higgsfield-style studio for your own ComfyUI workflows.`
4. Choose **Public**.
5. Do **not** check “Add a README file” (you already have one).
6. Click **Create repository**.

### 2. Upload the files

1. On the empty repo page, click **uploading an existing file**.
2. Open this folder in File Explorer.
3. Select **all files and folders** inside `comfy-studio-github` — not the folder itself.
4. Drag them into the GitHub upload box.
5. Wait for the upload to finish. Folders are supported by dragging in Chrome or Edge.
6. In the “Commit changes” box, type:

```text
Initial commit: Comfy Studio
```

7. Click **Commit changes**.

### 3. Check it

- [ ] The README shows.
- [ ] `LICENSE` is visible.
- [ ] The repo is **Public**.

**Do not upload the hidden `.git` folder.** It is not needed for the website method and can confuse the uploader. If you do not see it, that is normal — Windows hides it.

**File size:** GitHub’s web uploader rejects files over 25 MB. If a demo clip is larger, upload it to YouTube and link it instead of committing it.

---

## Option C — Command line

Use this if you are comfortable with a terminal.

```bash
cd "path/to/comfy-studio-github"

git init -b main
git add .
git commit -m "Initial commit: Comfy Studio"

# Create an empty public repo on github.com first, then:
git remote add origin https://github.com/YOUR-USERNAME/comfy-studio.git
git push -u origin main
```

If GitHub asks for a password, use a **personal access token**, not your account password:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic).
2. Generate a token with `repo` scope.
3. Paste the token when Git asks for a password.

---

## After publishing (5 minutes)

Do these from the repo page:

1. **About** (top right) → click the gear.
2. Description:

```text
A Higgsfield-style studio for your own ComfyUI workflows. Open source, local, MIT.
```

3. Topics (add one at a time):

```text
comfyui
comfyui-workflows
ai-video
ai-image
higgsfield
open-source-higgsfield
python
aiohttp
```

4. **Settings → General → Social preview** → upload `assets/banner.png` (or `assets/banner.svg` if accepted).
5. **Settings → General → Features** → enable **Issues** if you want feedback.
6. Pin the repo on your GitHub profile (optional).

---

## Common problems

**“Repository not found” when pushing**
The repo may be private, the URL may have a typo, or you may not be signed in. Check the URL and your permissions.

**“Nothing to commit”**
You may already have committed the files. Check the **History** tab in GitHub Desktop.

**“File is too large”**
GitHub rejects files over 100 MB (25 MB through the web uploader). Move large videos to YouTube and link them. Do not commit model weights.

**The README images are broken**
Make sure the `assets/` folder was uploaded and that filenames match exactly. GitHub is case-sensitive.

**The repo is private but I need it public**
Repo → **Settings → General → Danger Zone → Change visibility → Change to public**.

**I uploaded the folder itself, so the repo has `comfy-studio-github/` inside it**
That still works, but the README will be one level deep. To fix it, move the contents to the repo root using GitHub Desktop or re-upload them at the root.

---

## What a good repo looks like

```text
comfy-studio/
├── README.md              <- what it is, screenshots, quick start
├── LICENSE                <- MIT
├── studio.py
├── index.html
├── workflows/             <- the workflow files
├── docs/                  <- setup, models, demo script, submission
├── examples/              <- example outputs, prompts
└── assets/                <- banner, screenshots
```

That is exactly what this folder contains. You are ready to publish.
