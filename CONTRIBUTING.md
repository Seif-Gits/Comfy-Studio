# Contributing

Thanks for helping! Comfy Studio is one small Python file (`studio.py`, an aiohttp server) and one HTML file (`index.html`, no build step, no dependencies). That is on purpose, so please keep it that way.

## Run it while you work

```
python studio.py            # starts ComfyUI if needed, then opens the interface
COMFY_START=0 python studio.py   # Studio only (ComfyUI already running)
```

Use the same Python that runs ComfyUI. On the Windows portable build that is `python_embeded\python.exe`.

## Run the tests

```
python -m unittest discover -s tests -v
```

The tests cover the title-mark parser, the field/combo detection, the pruning of empty inputs and the credits formula evaluator. They need no GPU and no running ComfyUI.

## Ideas that would help

- A progress bar and a cancel button (Studio polls `/history`, it does not use the websocket yet)
- Support for custom-node widgets that hold several values, such as rgthree's Power Lora Loader
- More supported node types and interface controls, with tests in `tests/`
- Translations

## Pull requests

Describe what a person sees differently, and add a test if you touch the parser or the credits code. For interface changes, a short screen recording is the best proof.
