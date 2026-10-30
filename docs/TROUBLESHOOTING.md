# Troubleshooting

Comfy Studio is deliberately small, so most problems are one of three things: **ComfyUI is not reachable**, **a model/custom node is missing**, or **a workflow is not marked up correctly**.

---

## Start here

1. Is ComfyUI running? Open <http://127.0.0.1:8188> in your browser.
2. Is Comfy Studio running? Open <http://127.0.0.1:7860>.
3. Does the workflow run inside ComfyUI itself?
4. Does the Comfy Studio Manager show any **Setup needed** or **No output** warnings?

If the answer to 3 is no, fix the workflow in ComfyUI first. Comfy Studio cannot run a workflow that ComfyUI itself cannot run.

---

## “ComfyUI is not reachable at http://127.0.0.1:8188”

- Start ComfyUI.
- Or use `Start Comfy Studio.bat`, which starts ComfyUI for you.
- If ComfyUI is on a different port, set `COMFY_URL`.

```powershell
$env:COMFY_URL = "http://127.0.0.1:8189"
python studio.py
```

- If ComfyUI is on another machine, use `COMFY_START=0` and the remote URL. Make sure the port is reachable and not blocked by a firewall.

```bash
COMFY_URL="http://192.168.1.50:8188" COMFY_START=0 python3 studio.py
```

---

## “ComfyUI could not start”

The automatic launcher looks for:

1. `..\..\python_embeded\python.exe` (portable build)
2. `..\venv\Scripts\python.exe`
3. `..\.venv\Scripts\python.exe`
4. `python` on PATH

If none of these is right, start ComfyUI yourself and use `Start Studio Only.bat`, or set `COMFY_DIR` to the folder containing `main.py`:

```powershell
$env:COMFY_DIR = "C:\path\to\ComfyUI"
$env:COMFY_START = "0"
python studio.py
```

The launcher reads `run*.bat` files to copy the same Python flags ComfyUI normally uses. If your ComfyUI uses a custom launcher, set `COMFY_ARGS` or start it manually.

---

## “Not an API workflow. In ComfyUI use Workflow > Export (API).”

You uploaded a regular UI workflow. The file contains a `"nodes"` array and links, not the flat API format.

In ComfyUI:

1. Open the workflow.
2. Choose **Workflow → Export (API)**.
3. Save the JSON.
4. Upload that file in Comfy Studio.

The API file looks like this:

```json
{
  "3": {
    "class_type": "KSampler",
    "inputs": { "...": "..." }
  }
}
```

It does **not** start with `{"nodes": [...]}`.

---

## “No node titled ‘(Output)’”

No node has the `(Output)` marker. Rename your save or preview node:

```text
Save Image (Output)
Video Combine (Output)
Preview Audio (Output)
```

Then export the API workflow again.

If your output node class is unusual, Studio still uses the `(Output)` marker. The kind is inferred from the class; unknown classes fall back to image.

---

## “Setup needed for: …”

A workflow has one or more `(Setup)` fields that are empty or point to a file ComfyUI does not have.

1. Open **Manager**.
2. Click **⚠ Setup** on the workflow.
3. Choose the correct file for each field.
4. Click **Save setup**.
5. Generate again.

If the dropdown is empty, the model is not installed in ComfyUI. See [`MODELS.md`](MODELS.md).

---

## The Generate button stays disabled

The workflow is waiting for something:

- A **required** image/video/audio input is empty.
- There is no prompt and no optional media.
- The workflow has a Setup error.
- The selected workflow has no output.

Add the required input, type a prompt, or mark the media input `optional` in the workflow title.

---

## An uploaded file is ignored

The loader class must be one of:

- Images: `LoadImage`, `LoadImageMask`
- Audio: `LoadAudio`, `VHS_LoadAudio`
- Video: `LoadVideo`, `VHS_LoadVideo`

If you use a custom loader, add it to `MEDIA` in `studio.py`:

```python
MEDIA = {
    "LoadImage": ("image", "image"),
    "MyLoader": ("image", "image_path"),
}
```

Restart Studio after editing `studio.py`.

---

## A field is missing from the app

- The field may be connected to another node. Linked inputs are not exposed.
- You may have used `[1,3]` and skipped it. Check the field order in ComfyUI.
- It may be a `(Setup)` field. Look in **Manager → Setup**, not the composer.
- It may be hidden by a visibility rule. Check the switch state.

---

## A switch does not show or hide anything

- The rule must be in the **same node title** as the fields it controls.
- The switch name must match exactly (case-insensitive), including spaces.
- The rule’s bracket uses field positions on that node, not the order of exposed controls.

See [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md#visibility-rules).

---

## “Naming guide” opens a blank page or 404

`Naming Guide.html` must sit next to `studio.py`. It is included in this repo. If you renamed or moved it, either restore it or change the `guide` route in `studio.py`:

```python
async def guide(req):
    return web.FileResponse(ROOT / "Naming Guide.html")
```

---

## `ModuleNotFoundError: No module named 'aiohttp'`

Install the dependency with the same Python that runs Studio:

```bash
python -m pip install -r requirements.txt
```

For the Windows portable build:

```powershell
..\..\python_embeded\python.exe -m pip install aiohttp
```

If you use a venv, activate it first.

---

## Port 7860 is already in use

Set a different port:

```powershell
$env:PORT = "7861"
python studio.py
```

Then open <http://127.0.0.1:7861>.

---

## ComfyUI starts, but the first generation takes forever

Model loading can take minutes on the first run. Watch the ComfyUI terminal. Large video models such as MiniMax H3 are especially slow to load.

Tips:

- Generate a small image first to confirm the connection.
- Keep ComfyUI’s terminal visible; it prints model loading and errors.
- For video, start with 3–5 seconds and a small resolution.
- Use `COMFY_ARGS=--lowvram` if you are short on VRAM.

---

## Out of memory / CUDA errors

- Lower the resolution or duration.
- Close other GPU apps (games, browsers with hardware acceleration, other AI tools).
- Try `--lowvram` or `--normalvram`.
- For MiniMax H3, use the GGUF text encoder and a shorter clip.
- Check the ComfyUI terminal for the exact node that ran out of memory.

Comfy Studio does not manage VRAM; ComfyUI does.

---

## Video result does not play or seek

Studio proxies ComfyUI’s `/view` endpoint and forwards Range requests, so seeking should work in modern browsers. If it does not:

- Try Chrome or Edge.
- Check that the output file is a valid MP4.
- Open the file directly from ComfyUI’s `output/` folder to confirm it plays.

---

## “Remove all generations” did not delete files

This is intentional. Studio only deletes:

- files in ComfyUI’s `output/` or `temp/` folders that the gallery knows about, and
- input files whose names start with `studio_`.

It never touches your own input files or anything outside ComfyUI’s folders.

---

## Browser shows an old version

Hard-refresh:

- Windows: `Ctrl + F5`
- macOS: `Cmd + Shift + R`

Studio’s history and settings are kept in `localStorage`. Clearing site data resets the gallery and saved model choices (but not `setup/*.json`).

---

## Workflow imports but the app looks wrong

- Rename nodes in ComfyUI and re-export.
- Use the **API** export.
- Check the Manager warnings.
- Make sure the workflow has one `(Output)`.
- Test the workflow in ComfyUI with the same inputs.

---

## “Internal Server Error” with no useful message

The Studio terminal prints the traceback. Look there first. If it is an aiohttp/client error, the message usually tells you which ComfyUI endpoint failed.

Common causes:

- ComfyUI crashed or restarted mid-generation.
- A custom node raised an exception.
- The workflow references a model that is no longer installed.
- The upload was larger than the configured limit (2 GB).

---

## Security note

Comfy Studio is designed for **local use**. It has no login, no user accounts, and no CSRF protection. Do **not** expose port 7860 directly to the public internet without putting authentication and HTTPS in front of it (for example, a reverse proxy with a password). The same applies to ComfyUI’s port 8188.

If you deploy a public demo for the challenge, add authentication and usage limits.

---

## Still stuck?

Open an issue on the GitHub repo with:

- your OS and Python version,
- the ComfyUI version,
- the exact error message,
- the workflow name,
- the relevant part of the Studio and ComfyUI terminals.

Do not paste API keys, tokens, or private file paths.
