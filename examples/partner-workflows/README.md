# Optional partner workflow

`GPT_2.5.json` is an **optional** ComfyUI workflow that uses the OpenAI GPT Image 2.5 API node (`OpenAIGPTImageNodeV2`).

It is kept in this folder — not in `workflows/` — for two reasons:

1. It needs a ComfyUI API key and credits.
2. The default workflow set stays **open weights only**, so the main demo is eligible for the Open Weights Only category.

## Try it

1. Configure ComfyUI’s API nodes and your API key.
2. Open Comfy Studio → **Manager**.
3. Drag `GPT_2.5.json` into the Manager, or use **Add workflow files**.
4. Select the workflow and generate.

The app shows an estimated credit price when ComfyUI publishes a price badge for the node.

## Remove it from an open-weights build

If you want the repository to contain only open-weight workflows, delete this folder before publishing. The app does not need it.

## License

The workflow JSON is part of this MIT-licensed repo. The OpenAI model and API are governed by OpenAI’s terms. Do not commit API keys.
