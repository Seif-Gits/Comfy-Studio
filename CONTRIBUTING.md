# Contributing

Thanks for helping make Comfy Studio better. This project is intentionally small: one Python backend, one HTML frontend, and workflow JSON files.

## Ways to contribute

- Report a bug with steps to reproduce.
- Improve the docs or the naming guide.
- Add a workflow that demonstrates a new model or UI pattern.
- Improve the interface or the backend.
- Share an example output (SFW, with the prompt and workflow).

## Development setup

1. Install ComfyUI and make sure it runs.
2. Put this repo inside your ComfyUI folder, next to `main.py`.
3. Install the one Python dependency:

```bash
python -m pip install -r requirements.txt
```

4. Start the app:

```bash
python studio.py
```

5. Open <http://127.0.0.1:7860>.

There is no build step. Edit `index.html` or `studio.py` and refresh the browser. Restart `studio.py` after backend changes.

## Code style

- Python: keep the existing compact style. Four-space indentation. No new dependencies without a good reason.
- JavaScript: vanilla JS, no framework, no bundler.
- CSS: keep it in `index.html` with the existing custom properties.
- Workflows: API format only. Add a short note in `workflows/README.md`.
- Docs: clear, short sentences. Explain terms for non-coders.

## Adding a workflow

1. Build and test it in ComfyUI.
2. Mark at least one output with `(Output)`.
3. Mark model loaders with `(Setup)`.
4. Mark optional media with `(Input optional)`.
5. Export with **Workflow → Export (API)**.
6. Add the JSON to `workflows/`.
7. Update the table in `workflows/README.md` and `docs/MODELS.md`.
8. Test it in Comfy Studio with a small prompt.

Do **not** commit model weights, generated outputs larger than a few MB, API keys, or private data.

## Pull requests

1. Fork the repo.
2. Create a branch: `git checkout -b my-change`.
3. Make the change and test it.
4. Run the checks:

```bash
python -m py_compile studio.py
python scripts/validate_workflows.py
```

5. Open a pull request with:
   - what changed,
   - how you tested it,
   - screenshots for UI changes.

## License

By contributing, you agree your contribution is released under the repository’s MIT License. Workflow files and docs are included under the same license unless stated otherwise.

## Code of conduct

Be kind, be specific, and assume good intent. Harassment, hate speech, and sharing private or non-consensual material are not welcome.
