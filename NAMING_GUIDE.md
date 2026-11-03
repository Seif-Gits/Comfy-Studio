# Naming guide

You tell Comfy Studio what to show by typing short **marks** into node titles in ComfyUI. Double-click a node's title, add the mark after the name, and export with **Workflow → Export (API)**.

A mark is always in parentheses and starts with a keyword: `(Input)`, `(Switch)`, `(Slider)`, `(Setup)`, `(Output)` or `(Credits)`. Capital letters don't matter, and one title can hold several marks.

## The marks

| Mark | Put it on | What the user gets |
|---|---|---|
| `(Input)` | any node | every simple field of the node becomes a setting. Load Image / Audio / Video nodes become upload boxes, and the first text field becomes the prompt box |
| `(Input Switch)` | a node with a true/false field | a toggle that starts **off**. Off means "whatever the workflow says"; on sends the opposite. `(Switch)` on its own works too |
| `(Input Slider min=0/max=10)` | a node with a number field | a slider with a live number. Clicking the number lets you type an exact value. `(Slider)` on its own works too |
| `(Setup)` | model, VAE, CLIP and LoRA loaders | not shown while generating. It appears in **Manager → Setup**, so each person picks the model files on their own computer. Missing or empty files are highlighted in red |
| `(Output)` | the Save node | marks the result. Its type decides the tab: Image, Video or Audio |
| `(Credits)` | a closed-source (API) node | a crown in the model list, and the live credits the node will charge, shown on the Generate button. `(Credits 351.6)` sets a fixed price instead |

## Add-ons

Write these inside the same parentheses, in any order, unless it says otherwise.

| Add-on | What it does |
|---|---|
| `{Custom ratio}` | the name shown instead of the field name (no parentheses inside the braces) |
| `[1,3]` | only the 1st and 3rd field, counted from the top, skipping fields that have a wire. Settings appear in the order you list them |
| `optional` | the upload may stay empty. An empty upload switches its node off |
| `[image 2/10]` | a group of uploads sharing one box; this node is slot 2 of 10. Pictures are assigned in the order the user arranges them. Works with `image`, `audio` and `video` |
| `min=256/max=2048` | the lowest and highest number; typed numbers are pulled back inside (`min:256` works too) |
| `stp=32` | numbers move in steps of 32, counted from the minimum. A typed number snaps to the closest step (1000 becomes 992 when the minimum is 256) |
| `dec=0` or `dec=2` | how many decimals the number accepts: `dec=0` whole numbers, `dec=2` two decimals like 1.12. Whole-number fields are always `dec=0` |
| `Slider` / `Switch` | the kind of control, as a plain word inside `(Input …)` |
| `(2.Input)` | a number before the keyword sets the order. Numbered settings come first, then the rest. The model picker always stays first |
| `{Custom ratio} on [1]` | a **show rule**, written *outside* the parentheses: field 1 of this node only appears while the switch named "Custom ratio" is on. Use `off` for the opposite. Hidden fields are not sent |

**Putting it together.** After the keyword (`Input`, `1.Input`, `2.Input` …) the rest can be in any order. `(Input Slider [1] {Height} min=256/max=2048/stp=32/dec=0)` and `(Input {Height} max=2048/stp=32/min=256/dec=0 Slider [1])` give the same result: a slider called "Height" on the node's first field, from 256 to 2048, in steps of 32, with no decimals.

## Examples

| Node title | Result |
|---|---|
| `CLIP Text Encode (Input)` | the prompt box |
| `Load Image (Input optional {Start frame})` | an optional upload box called "Start frame" |
| `Load Image (Input optional [image 1/10])` … `[image 10/10]` | one growing box with draggable numbered thumbnails |
| `Resolution Selector (Input [1,2])` | aspect ratio and megapixels; the third field is left out |
| `If/Else Switch (Switch {Custom ratio} [1])` | a toggle called "Custom ratio" |
| `Resolution Selector (Input [1,2]) {Custom ratio} on [1]` | aspect ratio only shows while "Custom ratio" is on |
| `Empty Latent (Input Slider [1] {Height} min=256/max=2048/stp=32/dec=0)` | a "Height" slider from 256 to 2048 in steps of 32, whole numbers only |
| `KSampler (Input Slider {Steps} [2] min=1/max=50)` | a "Steps" slider from 1 to 50 |
| `KSampler (Input {Guidance} [3] min=1/max=10/dec=1)` | a "Guidance" number box, 1 to 10, one decimal |
| `Load Diffusion Model (Setup {Main model} [1])` | a "Main model" drop-down in Manager → Setup |
| `Save Video (Output)` | the result; the workflow appears under Video |
| `Seedance Reference to Video (Credits)` | a crown and the live price on the Generate button |

## Good to know

- **Switches start off.** Off always means the value saved in the workflow. To make "on" mean what you want, export with the opposite value.
- **Prompt.** The first text field whose name doesn't contain "negative" becomes the prompt box. Other text fields appear as settings.
- **Empty uploads** switch their node off, and so is anything that cannot run without it. Studio decides on its own whether a box is "Required"; `optional` forces it to be optional.
- **Seeds** (`seed`, `noise_seed`) get a new random value on every run, even when unmarked.
- **A field marked twice**, for example `(Input) (Switch {Custom ratio} [1])`, shows once, with the name you gave it.
- **Dropdowns** are filled from ComfyUI's own list of options, so people never have to guess a value.

## Credits and the crown

Closed-source API nodes in ComfyUI carry a price formula, the same one that draws the "credits/Run" badge on the node. Studio reads it, works out the price for the exact settings and uploads, and recalculates after every change. Several API nodes are added up, and a price that varies shows as a range.

- If a price can't be worked out, the button says "uses credits" and the terminal explains which node and why. A very old ComfyUI may not provide formulas; use `(Credits 351.6)` there.
- Credits are dollars × 211. Set `COMFY_CREDITS_PER_USD` if your rate differs.

## If something looks wrong

- Open **Manager**. A workflow without `(Output)` is rejected, and a field number that doesn't exist is listed in red.
- A red **⚠ Setup needed** next to the model picker means a model file is empty or not found.
- Re-uploading a workflow with the same file name replaces it and keeps its Setup choices.
