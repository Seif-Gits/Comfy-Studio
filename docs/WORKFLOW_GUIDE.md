# Workflow naming guide

Comfy Studio does not need a custom workflow format. It reads **node titles** in a normal ComfyUI API workflow and turns the marked nodes into app controls.

The fastest way to understand it: open a workflow in ComfyUI, rename the nodes you care about using the markers below, then choose **Workflow → Export (API)** and upload the JSON in Comfy Studio’s **Manager**.

> **Important:** upload the **API** workflow, not the regular UI workflow. The API file is a flat object of node IDs. The UI file contains a `"nodes"` array and is rejected with a helpful error.

---

## The five-minute version

Rename these nodes in ComfyUI:

```text
Prompt                  ->  Prompt (Input)
Load Image              ->  Load Image (Input optional [Image 1/10])
Resolution Selector     ->  Resolution Selector (Input [1,2])
Duration                ->  Duration (Input {Seconds})
Steps                   ->  Steps (Slider {Steps} [2] min:1/max:50 step:1)
Custom ratio            ->  Custom ratio (Switch {Custom ratio} [1])
Model loader            ->  Model (Setup)
Save Image              ->  Save Image (Output)
```

Export the API workflow and upload it. The app now has:

- a main prompt box,
- a 10-slot reference image strip,
- resolution controls,
- a duration field,
- a steps slider,
- a custom-ratio toggle,
- a Setup entry for the model,
- an image output card.

---

## Marker reference

A marker is a parenthesised instruction in a node title. A title can contain several markers, plus optional visibility rules.

### `(Output)`

Marks a node whose result should appear in the gallery.

```text
Save Image (Output)
Video Combine (Output)
Preview Audio (Output)
```

The output kind is inferred from the node class. If the class is unknown, Studio guesses from the class name and falls back to image. A workflow needs at least one `(Output)` node.

### `(Input)`

Exposes the node’s literal (unconnected) input fields as app controls.

```text
Prompt (Input)
Resolution Selector (Input)
Duration (Input)
```

- Text-like fields (`text`, `prompt`, `value`, `string`) become the prompt box or a text field.
- Numbers become number controls.
- Combo/list fields become dropdowns. Supported dynamic combos expose the selected variant’s sub-fields using ComfyUI’s node metadata.
- Booleans become switches.
- Fields named `seed` or `noise_seed` become random-seed controls.

### `(2.Input)` — order

The number before `Input` sets the order in the composer. Numbered inputs come first, in ascending order; unnumbered inputs keep their workflow order.

```text
Prompt (1.Input)
Reference (2.Input)
Resolution (3.Input)
```

### `(Input [1,3])` — pick fields

By default, every literal field on the node is exposed. Use a bracketed list to expose only specific fields, counted from 1 in the node’s own input order.

```text
Resolution Selector (Input [1,2])
```

This exposes fields 1 and 2 only. A warning is shown in the Manager if the node has fewer fields than requested.

You can combine order and field selection:

```text
Resolution Selector (1.Input [1,2])
```

### `(Input {Label})` — rename

`{Label}` replaces the field or node name in the app.

```text
Duration (Input {Seconds})
Prompt (Input {Your idea})
Load Image (Input {Start frame} [Image 1/10])
```

For a node with several exposed fields, the label becomes `Label: field name`.

### `(Input optional)`

Marks a **media** input as optional. If the user leaves it empty, Studio disables that branch of the workflow instead of blocking the Generate button.

```text
Load Image (Input optional)
```

Without `optional`, a media input is required unless Studio can prove the graph still produces an output without it.

### `(Input optional [Image 1/10])` — grouped media

This creates one growing strip of upload slots instead of ten separate boxes.

```text
Load Image (Input optional [Image 1/10])
Load Image (Input optional [Image 2/10])
...
Load Image (Input optional [Image 10/10])
```

The syntax is:

```text
[<group name> <position>/<max>]
```

- The **kind** comes from the loader class (`LoadImage` = image, `LoadAudio` = audio, `VHS_LoadVideo` = video).
- The **group name** is shown in the UI.
- The **position** controls the order.
- The **max** is the number of slots.

All members of a group must share the same kind and group name. The UI lets users drag to reorder, replace individual files, and remove files; empty trailing slots are optional.

A group can be required by leaving out `optional`:

```text
Load Image (Input [Image 1/4])
Load Image (Input [Image 2/4])
Load Image (Input [Image 3/4])
Load Image (Input [Image 4/4])
```

### `(Switch {Name} [1])`

Exposes a boolean field as a toggle and gives it a name that visibility rules can reference.

```text
Custom ratio (Switch {Custom ratio} [1])
```

- The node must have a boolean literal field.
- `[1]` selects the field (1-based).
- The switch is **on** when the user’s value differs from the workflow’s stored value. This is intentional: the workflow’s own default is treated as “off”.
- Use the switch name in a rule to show or hide other fields.

### `(Slider {Name} [2] min:0/max:10 step:1)`

Renders a numeric field as a range slider. The displayed number is clickable, so the user can type an exact value; the value is constrained by the configured minimum and maximum.

```text
Steps (Slider {Steps} [2] min:1/max:50 step:1)
```

- `[2]` selects the field.
- `min:`, `max:`, and `step:` override ComfyUI’s own limits.
- `{Name}` is the label.

### `(Setup)`

Hides technical fields from the composer and moves them into **Manager → Setup**. Use this for model files, VAEs, text encoders, and LoRAs that a user should choose once, not on every generation.

```text
Load Diffusion Model (Setup)
Load CLIP (Setup)
Load VAE (Setup)
Load LoRA (Setup)
```

Setup fields are validated:

- empty values show “This is empty. Choose a value.”
- values not found in ComfyUI show “was not found in ComfyUI”.

Saved Setup choices live in `setup/<workflow>.json` and are git-ignored.

### `(Credits)` and `(Credits 351.6)`

`(Credits)` explicitly marks a paid/API node. The workflow receives a crown in the model list and Manager. Studio also recognizes API nodes from ComfyUI metadata when available, even if the mark is omitted. When ComfyUI provides a `price_badge` formula, Studio estimates the current credit cost from the workflow settings and connected inputs.

```text
Some API Node (Credits)
```

Use a number, such as `(Credits 351.6)`, to set a fixed credit price when a formula is unavailable or cannot be evaluated. The formula-based estimate is only as accurate as the information provided by the installed ComfyUI version.

### Visibility rules: `{switch} on [1,2]`

Rules hide fields while a named switch is on or off. Put the rule **in the same node title** as the fields it controls.

The bracket in a rule is a list of **field positions** on that same node. If you leave the bracket out, the rule applies to every exposed field on that node.

```text
Preset (Input [1]) {custom ratio} off [1]
Custom width (Input [1]) {custom ratio} on [1]
```

- `Preset` is visible while the switch named **custom ratio** is off.
- `Custom width` is visible while **custom ratio** is on.

The switch itself is a separate boolean node, for example:

```text
Custom ratio (Switch {Custom ratio} [1])
```

One node can carry several rules:

```text
Resolution Selector (1.Input [1]) (2.Input [2]) {custom ratio} off [1] {custom ratio} on [2]
```

This shows field 1 while the switch is off, and field 2 while it is on.

Rules are evaluated in the browser. Hidden fields are not sent with the generation request.

---

## Multiple markers on one node

A single title can carry several marks and a rule:

```text
Resolution Selector (1.Input [1,2]) (3.Input [3]) {custom ratio} on [1]
```

This exposes fields 1, 2, and 3; orders them at position 1; and applies the rule to field 1. More commonly you will use one or two markers per node.

---

## What Studio can expose

| ComfyUI value | Studio control |
| --- | --- |
| Text / multiline text | Prompt box or text field |
| `INT` | Number field |
| `FLOAT` | Number field |
| `BOOLEAN` | Toggle |
| `COMBO` / list | Dropdown |
| `seed`, `noise_seed` | Random seed control |
| `LoadImage`, `LoadImageMask` | Image upload slot |
| `LoadAudio`, `VHS_LoadAudio` | Audio upload slot |
| `LoadVideo`, `VHS_LoadVideo` | Video upload slot |
| `SaveImage`, `PreviewImage`, animated image saves | Image output |
| `SaveVideo`, `VHS_VideoCombine` | Video output |
| Audio save/preview nodes | Audio output |

If you use a custom loader class that is not in this table, add it to the `MEDIA` dictionary in `studio.py`:

```python
MEDIA = {
    "LoadImage": ("image", "image"),
    "MyCustomImageLoader": ("image", "image_path"),
    ...
}
```

---

## Output classes

Studio recognises these output nodes by default:

- Images: `SaveImage`, `PreviewImage`, `SaveAnimatedWEBP`, `SaveAnimatedPNG`
- Video: `SaveVideo`, `VHS_VideoCombine`
- Audio: `SaveAudio`, `SaveAudioMP3`, `SaveAudioOpus`, `PreviewAudio`

Any node with `(Output)` is also treated as an output. Unknown classes fall back to image, or to video/audio if the class name contains those words.

---

## Complete example

A MiniMax-style reference-to-video workflow could use:

```text
Prompt (1.Input)
Load Image (1.Input optional [Image 1/10])
Load Image (1.Input optional [Image 2/10])
...
Load Image (1.Input optional [Image 10/10])
Load Video (Upload) (2.Input optional [Video 1/3])
Load Video (Upload) (2.Input optional [Video 2/3])
Load Video (Upload) (2.Input optional [Video 3/3])
Load Audio (2.Input optional [Audio 1/3])
Load Audio (2.Input optional [Audio 2/3])
Load Audio (2.Input optional [Audio 3/3])
Duration(Second) (Input {Seconds})
Resolution Selector (Input [1,2])
Load Diffusion Model (1.Setup)
Load CLIP (2.Setup)
Load Video VAE (3.Setup)
Load Audio VAE (4.Setup)
Load LoRA (Setup)
Video Combine (Output)
```

The app shows a prompt, a 10-image strip, a 3-video strip, a 3-audio strip, duration and resolution controls, a Setup panel for four model files and a LoRA, and a video output.

---

## Common mistakes

**“Not an API workflow.”**
You exported the normal workflow. Use **Workflow → Export (API)**.

**“No node titled ‘(Output)’.”**
No node has `(Output)`. Rename your save/preview node.

**“Setup needed.”**
A `(Setup)` field is empty or points to a model that is not installed. Open **Manager → Setup**.

**A field is missing from the app.**
The field may be connected to another node (links are not exposed), or you used `[1,3]` and skipped it. Check the field order in ComfyUI.

**A switch does not show or hide anything.**
The rule must be in the same node title as the fields it controls, and the switch name must match exactly (case-insensitive).

**The Generate button stays disabled.**
A required media input is empty, or the workflow has no prompt and no optional media. Add the required input or mark it `optional`.

**An uploaded file is ignored.**
The loader class must be in the `MEDIA` table above. Add your custom class to `studio.py`.

---

## Testing checklist

Before uploading a workflow:

- [ ] It runs end-to-end in ComfyUI with the API-style inputs.
- [ ] At least one node is marked `(Output)`.
- [ ] Every `(Input)` node has values that make sense as defaults.
- [ ] Model loaders are marked `(Setup)`, not exposed as free-text fields.
- [ ] Optional media inputs are marked `optional`.
- [ ] Grouped media uses the same group name and kind for every member.
- [ ] Switch names in rules match the `(Switch {Name} …)` exactly.
- [ ] The workflow name is descriptive; it becomes the model name in the app.
- [ ] The JSON file is small enough to commit (workflows are usually a few KB).
