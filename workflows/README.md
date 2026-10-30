# Workflows

These are **API-format** ComfyUI workflows. Comfy Studio reads them and builds the app controls from their node titles.

| File | Output | Model | Notes |
| --- | --- | --- | --- |
| `Qwen_2.1.json` | Image | Qwen Image 2.1 | Text-to-image, up to 10 reference images, resolution selector |
| `Qwen_2.1_5.json` | Image | Qwen Image 2.1 | Alternate control layout |
| `Qwen_2.1_6.json` | Image | Qwen Image 2.1 | Alternate layout with a custom-ratio switch |
| `Krea-2.json` | Image | Krea 2 | Text-to-image with turbo + realism LoRAs |
| `Krea-2_T2I_again.json` | Image | Krea 2 | Alternate Krea 2 layout |
| `Minimax_H3_Ref2Va.json` | Video + audio | MiniMax H3 | Reference-to-video, up to 10 images, 3 videos, 3 audio clips |

The optional partner workflow is in [`../examples/partner-workflows/`](../examples/partner-workflows/).

## What “API format” means

An API workflow is a flat object:

```json
{
  "3": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 123,
      "steps": 20,
      "model": ["4", 0]
    },
    "_meta": {
      "title": "Sampler (Input)"
    }
  }
}
```

It is **not** the regular UI workflow, which contains `"nodes"` and `"links"` arrays. In ComfyUI, use **Workflow → Export (API)**.

## How to load one

1. Start Comfy Studio.
2. Open **Manager**.
3. Click **Add workflow files (.json)** and choose one of these files, or drag it onto the page.
4. If the workflow shows **Setup needed**, open **Manager → Setup** and choose the model files installed on your machine.
5. Generate.

Uploading a file with the same name replaces the workflow but keeps the saved Setup choices.

## Naming markers in these files

The titles contain markers such as:

```text
Prompt (Input)
Load Image (Input optional [Image 1/10])
Resolution Selector (1.Input [1,2])
Duration(Second) (Input {Seconds})
Load Diffusion Model (Setup)
Save Image (Output)
```

The full syntax is in [`../docs/WORKFLOW_GUIDE.md`](../docs/WORKFLOW_GUIDE.md) and in the in-app **Manager → Naming guide**.

## Model files

The exact filenames each workflow expects are listed in [`../docs/MODELS.md`](../docs/MODELS.md). If a filename differs on your machine, use **Manager → Setup** to pick the file you have.

## Adding your own

1. Build and test the workflow in ComfyUI.
2. Rename the important nodes with markers.
3. Export **API** JSON.
4. Upload it in the Manager.
5. Test it with a small prompt.

Keep workflow JSON files small. Do not commit model weights or output media here.
