# 09 — CAD Workflow and Conventions

## 1. Toolchain

- **Primary: code-CAD in Python, CadQuery 2.x or build123d (OpenCascade kernel).**
  - Fully parametric, diff-able, reproducible.
  - Claude can write, run and revise it.
  - Exports exact B-rep STEP that opens in Fusion 360, Onshape, FreeCAD, SolidWorks and KiCad.
- **Viewing/editing:** FreeCAD or Onshape (free) to inspect STEP, measure and make quick sections. Slicer (Bambu/Prusa/Cura) for print prep.
- **Rendering for the portfolio:** STEP → Blender, or KeyShot/Fusion render.
- **ECAD:** KiCad 10 (`headset-orga`).

## 2. Repository layout (in `C:\ORLANDO\Lab\kicad\headset-orga\mech\`)

```text
mech/
  params/orga_params.py     ← single source of truth for every dimension (with source tags)
  src/                      ← one script per part: cup_left.py, cup_right.py, baffle.py, keys.py, headband.py, assembly.py
  ref/                      ← imported references: board STEP from KiCad, purchased-part STEPs
  out/                      ← generated STEP / STL / 3MF / DXF (never edit by hand)
  renders/                  ← PNG renders and section views for review
  log.md                    ← iteration log: rev, change, print result
```

The `orga_v1_mainboard_envelope.*` files and `orga_v1_board_outline.dxf` go into `ref/`. The scripts `gen_envelope.py` and `draw.py` regenerate them.

## 3. Units, frames, naming

- **Units:** millimetres, degrees.
- **Frames:**
  - head frame **H**: X forward, Y left, Z up, origin at the interaural centre;
  - board frame **B** (file 03 §1);
  - each part is modelled in its own local frame, then placed in H by the assembly script.
- **Part names:** `ORGA-M-<part>-<rev>`, e.g. `ORGA-M-CUPL-OUT-A` (left cup outer shell, rev A). Revisions are A, B, C…, plus a print iteration suffix `.1`, `.2` if needed.
- **Files:** `ORGA-M-CUPL-OUT-A.step`, `.stl`, plus `ORGA-M-ASM-A.step` for the full assembly.
- **Dimension tags** in `orga_params.py`: `# src: datasheet <file>` / `# src: measured <date>` / `# src: assumed VERIFY`.

## 4. ECAD ↔ MCAD round-trip

1. **MCAD → ECAD**
   - Export the outline + holes DXF in frame B (layers `OUTLINE`, `HOLES`, `PORTS_AND_OPENINGS`, `KEEPOUT_TOP_hX.X`, `KEEPOUT_BOT_hX.X`).
   - In KiCad: File → Import → Graphics. Put `OUTLINE` on **Edge.Cuts**, the shell inner wall on **User.1** and keep-outs on **User.2**. Set the origin so KiCad (100, 100) = B origin, to keep the mapping in file 03.
2. **ECAD → MCAD**
   - In KiCad: File → Export → STEP (board + components, with 3D models), saved to `mech/ref/`.
   - Re-run the interference check (file 07 V0).
3. Each loop gets a line in `log.md`.

## 5. What a CAD iteration delivers (definition of done)

- Updated `orga_params.py` (with source tags).
- STEP (assembly + parts) and STL/3MF (printable parts, oriented for printing).
- 3 PNG renders (iso, exploded, section through the left cup).
- The V0 check report (interference, clearances, alignment, mass) as a short table.
- A list of anything the electronics side must change (outline, part moves), as DXF + table.
