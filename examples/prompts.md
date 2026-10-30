# Example prompts

These are starting points for the included workflows. They are original, SFW, and free of copyrighted characters. Replace them with your own ideas.

---

## Qwen Image 2.1 / Krea 2 — image prompts

**Cinematic portrait**

```text
A cinematic close-up portrait of a young astronomer in a worn canvas jacket, standing in a greenhouse at blue hour, soft rain on the glass, warm practical lights, shallow depth of field, natural skin texture, 50mm lens, muted teal and amber palette
```

**Product shot**

```text
A minimalist ceramic skincare bottle on a slab of dark stone, a single eucalyptus leaf, soft morning window light from the left, deep shadows, subtle mist, editorial product photography, 85mm lens, clean composition
```

**Environment**

```text
A quiet desert research station at dusk, solar panels and antennae, distant mesa, dust in the air, long shadows, a single lit window, wide-angle cinematic still, natural color grade
```

**Food**

```text
An overhead shot of a rustic breakfast table: sourdough bread, olives, labneh, mint tea in a small glass, linen napkin, warm side light, film grain, cookbook photography
```

**Abstract**

```text
A sculptural study of folded translucent paper, soft gradients of pearl white and pale lime, studio lighting, subtle shadows, macro detail, minimal background, high-end 3D render
```

**Reference-image edit**

Use one clean reference image, then prompt:

```text
Keep the subject's face and clothing exactly the same. Place them in a quiet library with warm afternoon light, add a shallow depth of field, keep the original expression and pose, photorealistic
```

> Only use reference images you have the right to use. Do not upload celebrity photos or other people's private images without permission.

---

## MiniMax H3 Ref2Va — video prompts

MiniMax H3 uses reference images plus a text prompt. Describe the subject, the action, the camera, and the sound.

**Café push-in**

```text
A slow, steady push-in on a quiet neighborhood café in the early morning. The owner wipes down a small table, steam rises from a glass of tea, warm sunlight cuts through the window. Natural ambient sound: distant traffic, birds, the clink of cups. Keep the café's colors and layout consistent with the reference image.
```

**Portrait turn**

```text
The subject turns slowly toward the camera and gives a small, tired smile. Soft window light, shallow depth of field, subtle handheld drift. Quiet room tone and a faint breeze. Preserve the subject's face, hair, and clothing from the reference image.
```

**Product rotation**

```text
A slow 180-degree orbit around the product on a stone pedestal, soft studio light, gentle reflections, a wisp of mist in the background. Clean ambient hum, no music. Keep the label and packaging exactly as in the reference image.
```

**Landscape**

```text
A slow aerial glide over a desert canyon at golden hour, long shadows, dust drifting in the wind, distant birds. Natural wind and a low ambient drone. Keep the rock formations and lighting consistent with the reference image.
```

**Camera notes**

- Say “slow push-in”, “orbit”, “handheld drift”, or “static shot”.
- Keep clips short (3–5 seconds) for the first test.
- Describe the sound you want; the workflow outputs audio.
- Mention what must stay consistent with the reference image.

---

## Optional GPT Image 2.5 — partner workflow

`examples/partner-workflows/GPT_2.5.json` uses a ComfyUI API node. It needs an API key and credits.

```text
A clean editorial photo of a glass of iced tea on a sunlit windowsill, condensation on the glass, a linen curtain moving in the breeze, soft shadows, minimal composition
```

---

## Prompt tips

- **Be concrete:** subject, setting, light, lens, mood, color.
- **Use references for identity:** say what must stay the same.
- **Do not ask for logos, celebrities, or copyrighted characters.**
- **Keep it SFW.**
- **Iterate one change at a time** so you can tell what worked.
