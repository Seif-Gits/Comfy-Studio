# Models and custom nodes

Comfy Studio does **not** bundle model weights. The workflows in `workflows/` reference the filenames below. Install the models in ComfyUI, then use **Manager → Setup** in Comfy Studio to point each workflow at the files you actually have.

> Model weights are large and have their own licenses. Download them from the model author's official page or from a trusted ComfyUI repack, and check the license before commercial use.

---

## Where files go

ComfyUI loads each file type from a specific folder:

| Loader field | ComfyUI folder |
| --- | --- |
| `unet_name` (`UNETLoader`) | `ComfyUI/models/diffusion_models/` (older installs may use `models/unet/`) |
| `clip_name` (`CLIPLoader`, `CLIPLoaderGGUF`) | `ComfyUI/models/text_encoders/` (older installs may use `models/clip/`) |
| `vae_name` (`VAELoader`) | `ComfyUI/models/vae/` |
| `lora_name` (`LoraLoaderModelOnly`) | `ComfyUI/models/loras/` |
| `LoadImage` / `LoadAudio` / `VHS_LoadVideo` inputs | `ComfyUI/input/` |

Subfolders inside those folders are allowed. The workflow strings include them, for example `Minimax/minimax_h3_...safetensors`.

---

## Qwen Image 2.1 workflows

Files: `workflows/Qwen_2.1.json`, `workflows/Qwen_2.1_5.json`, `workflows/Qwen_2.1_6.json`

| File | Put it in | Used by |
| --- | --- | --- |
| `Qwen Image/qwen_image_2.1_int8_convrot.safetensors` | `models/diffusion_models/` | `UNETLoader` |
| `qwen3vl_8b_int8_convrot.safetensors` | `models/text_encoders/` | `CLIPLoader` |
| `qwen_image_2.1_vae_bf16.safetensors` | `models/vae/` | `VAELoader` |

The nodes `QwenImage21Cache`, `TextEncodeQwenImage21`, `SaveImageAdvanced`, `ImageCompare`, and `ResolutionSelector` are part of recent ComfyUI builds. Update ComfyUI if they are missing.

**Setup entries in the app:** the diffusion model, CLIP, and VAE loaders are marked `(Setup)`. Choose the actual files in **Manager → Setup**.

---

## Krea 2 workflows

Files: `workflows/Krea-2.json`, `workflows/Krea-2_T2I_again.json`

| File | Put it in | Used by |
| --- | --- | --- |
| `krea2_raw_int8_convrot.safetensors` | `models/diffusion_models/` | `UNETLoader` |
| `qwen3vl_4b_fp8_scaled.safetensors` | `models/text_encoders/` | `CLIPLoader` |
| `qwen_image_vae.safetensors` | `models/vae/` | `VAELoader` |
| `Krea 2/krea2_turbo_lora_rank_64_bf16.safetensors` | `models/loras/` | `Power Lora Loader (rgthree)` |
| `Krea 2/Krea2-realism-V2.safetensors` | `models/loras/` | `Power Lora Loader (rgthree)` |

Install **rgthree-comfy** for the `Power Lora Loader (rgthree)` node. The workflow has two LoRAs enabled by default; you can turn either off in ComfyUI before exporting, or remove the LoRA from the graph.

---

## MiniMax H3 reference-to-video workflow

File: `workflows/Minimax_H3_Ref2Va.json`

| File | Put it in | Used by |
| --- | --- | --- |
| `Minimax/minimax_h3_ref2va_pruned_int8_convrot.safetensors` | `models/diffusion_models/` | `UNETLoader` |
| `Minimax/minimax_h3_video_vae_int8_convrot.safetensors` | `models/vae/` | `VAELoader` (video VAE) |
| `Minimax/minimax_h3_audio_vae_fp32.safetensors` | `models/vae/` | `VAELoader` (audio VAE) |
| `Minimax/qwen3vl-32B-MiniMax-H3-Q2_K.gguf` | `models/text_encoders/` | `CLIPLoaderGGUF` |
| `Minimax H3/minimax_h3_ref2v_lightx2v_turbo_4step_v0.1_resized_avg_rank_20_bf16.safetensors` | `models/loras/` | `LoraLoaderModelOnly` |

This is the heaviest workflow in the repo. MiniMax H3 is a large video model; a 24 GB GPU is a realistic starting point. If you run out of VRAM, try a shorter duration, a lower resolution, the GGUF text encoder, or start ComfyUI with `--lowvram`.

The workflow also uses:

- `CLIPLoaderGGUF` from [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF)
- `VHS_VideoCombine` and `VHS_LoadVideo` from [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)
- `ComfyMathExpression` from [ComfyMath](https://github.com/evanspearman/ComfyMath)
- `VRAM_Debug` from [ComfyUI-KJNodes](https://github.com/kijai/ComfyUI-KJNodes)
- `LTXVSeparateAVLatent`, `VAEDecodeAudio`, `MiniMaxH3ReferenceToVideo`, `ResolutionSelector`, and `SaveImageAdvanced` from recent ComfyUI builds

---

## Optional partner workflow

File: `examples/partner-workflows/GPT_2.5.json`

This workflow uses `OpenAIGPTImageNodeV2` — a ComfyUI **API/partner node** for OpenAI GPT Image 2.5. It does **not** download a local model. It uses ComfyUI API credits and an API key configured in ComfyUI. It is kept out of the default `workflows/` folder so the main submission stays open-weights only.

To try it, drag the JSON into Comfy Studio’s Manager. To remove it from an open-weights build, simply do not add it.

---

## Quick install checklist

1. Download the files above.
2. Put each file in the matching `ComfyUI/models/...` folder.
3. Start ComfyUI.
4. Open **Manager → Install Missing Custom Nodes** and install anything the workflow reports.
5. Restart ComfyUI.
6. Open Comfy Studio → **Manager → Setup** and choose the model files.
7. Generate a small test image/video.

If a model filename is slightly different on your machine, that is fine: the Setup panel lists the files ComfyUI actually sees. Pick the matching one.

---

## Licensing notes

- The **Comfy Studio code** is MIT-licensed (see `LICENSE`).
- **Model weights** keep their own licenses. Qwen, Krea, MiniMax, and OpenAI models may have different terms for commercial use, redistribution, and derivatives. Read the model card before publishing outputs or a hosted demo.
- **Custom node packs** keep their own licenses. The links above point to their repositories.
- The example workflows include prompts written for this project. Replace them with your own when you publish example outputs.
