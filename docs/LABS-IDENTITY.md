# Labs identity

The home, benchmark index and migration index use the charcoal and fluorescent-green Labs design. Individual reports retain their own visual designs, content and figures. All 17 current and archived HTML pages share the PNG test-tube favicon.

## Artwork

The user selected the first 2D cartoon test tube. `public/labs/identity/tube-hero.png` is the selected transparent 1024×1536 master, displayed responsively without CSS glow effects. The separate `tube-icon-master.png` simplifies that selected illustration for favicon use. PNG variants are 16, 32, 48, 180, 192 and 512 pixels; `public/favicon.ico` provides a conventional fallback.

Generated with the built-in image generation tool, then copied into the publication repository. Native master resolution is retained; it has not been artificially upscaled. JetBrains Mono is locally hosted with its OFL license. Static assets belong to the public branch; HTML source and shared favicon declarations belong to stage.

## Final prompts

Hero:

Use case: illustration-story. Asset type: premium TWO-DIMENSIONAL CARTOON brand illustration for Nift Labs, transparent PNG. One test tube holding bright fluorescent green liquid. IMPORTANT STYLE: completely 2D, elegant flat cartoon, crisp graphic shapes, deliberate bold contours, simple cel shading, sophisticated illustrated mascot-object quality. NOT 3D, NOT photoreal, NOT a realistic glass render. Think beautifully art-directed editorial cartoon object on a premium hacker website. Shape: a moderately broad test tube tilted slightly diagonally, simple elliptical open rim, straight sides, rounded closed bottom, lower half bright green liquid with a gently curved surface and two simple circular bubbles. Glass indicated ONLY by a pale warm-white outline and two clean flat reflection stripes, with charcoal-tinted translucent interior. Green fill uses two or three clean flat tones, not realistic light or bloom. Strong recognizable silhouette, polished proportions, confident smooth lines, simple enough for a brand identity but richer than generic chemistry clip-art. Transparent alpha background, full object centered, ample margins. No surrounding aura, no textures, no complex gradients, no realism, no photography, no 3D material, no chrome, no scientific apparatus, no text, no logos, no blue or purple. Make it unmistakably illustrated, playful but elegant, high quality rather than childish.

Favicon:

Use case: logo-brand. Input image is the SELECTED first cartoon Labs test tube, preserve this design and angle exactly. Make a favicon adaptation of THIS tube, not a different tube: same left-tilted broad oval rim, cream border, dark charcoal glass, vivid lime green liquid in lower half, rounded bottom. Two-dimensional cartoon. Simplify only the fine inner reflections and bubbles for legibility at 16 pixels; keep the outline, proportions, rim and liquid shape recognizable from the reference. Square transparent PNG with comfortable margins, no glow halo, no background, no text. Do not redesign or change the silhouette.

## Build and publication

Run `nift build --all`, then `nift build`, `python3 scripts/validate.py` and `python3 scripts/check_storage_policy.py`. Push source stage before publication main, as specified in the Labs redesign brief. No benchmark reruns or evidence changes are part of this work.

## Verification, 10 October 2026

- Full build: 14 tracked routes; incremental build reports all up to date.
- Publication validator: 17 HTML pages and 378 local references pass.
- Universal favicon audit: all 17 HTML pages reference the same 16/32/48 PNGs and 180 touch icon, with correct dimensions and existing assets.
- Browser viewport checks: home, benchmark collection, migration collection, Shell, Capgo and TanStack at 1440, 390 and 320 pixels. No page-width overflow or broken images. Desktop and mobile visual inspection retain distinct report typography and layouts.
- Preservation audit against the pre-redesign snapshot: 69 report bodies/assets are byte-identical. Temporal and TanStack report bodies differ only in Nift-generated whitespace. All retained figures, tables, styles, evidence links and numerical datasets are unchanged.
- Storage policy passes; both PNG masters remain below the individual-file limit.
