# 05 — Enclosure Design Guidelines (prototype, 3D-printed)

Values are starting points for prototypes. Calibrate them with a tolerance test print on the actual printer or service before printing full shells.

## 1. Process choice

| Process | Use for | Typical accuracy | Notes |
|---|---|---|---|
| FDM (PETG / ASA / PLA+) | Early fit checks, brackets | ±0.2–0.3 mm | Cheap and fast. Layer lines are visible; avoid as the final portfolio finish. |
| SLA / resin (tough or ABS-like) | Shells, keys, fine features | ±0.1 mm | Best surface. Brittle resins crack at snap-fits and screw bosses, so use a "tough" resin. |
| MJF / SLS (PA12) | Final prototype shells, headband parts | ±0.2 mm | Strong, isotropic, matte; good for snap-fits and hinges. Available from online print services. |

Recommendation: FDM for iterations 1–2, then MJF PA12 (structure) and SLA (keys and light window) for the portfolio build.

## 2. Geometry rules

| Feature | FDM | SLA / MJF |
|---|---|---|
| Wall thickness | ≥ 1.6 mm (4 perimeters @ 0.4 nozzle); 2.0 typical | ≥ 1.2 mm; 1.5–2.0 typical |
| Rib thickness | 0.6–0.8 × wall | 0.6 × wall |
| Clearance, sliding fit (per side) | 0.25–0.3 mm | 0.10–0.15 mm |
| Clearance, PCB in pocket (per side) | 0.3 mm | 0.2 mm |
| Shell over tallest component | ≥ 0.5 mm | ≥ 0.3 mm |
| Minimum hole | Ø1.0, print undersize and drill | Ø0.5 |
| Inside corner fillet | ≥ 0.5 mm; outside cosmetic radius ≥ 1.0 mm | same |
| Overhangs without support (FDM) | ≤ 45°; design the parting/print orientation early | n/a |

## 3. Fastening and PCB retention

- **M2 heat-set inserts** in bosses. Use the insert vendor's hole size (typically about Ø3.2 × 4 mm deep for a short M2 insert). Boss OD ≥ 2 × insert OD; tie bosses to the wall with ribs.
- **PCB mounting:** ≥ 3 points (MR-011), one within 10 mm of USB-C. Standoff height sets the PCB-to-shell gap. Keep a Ø7 mm part-free zone around each hole on both sides. For FDM bosses, Ø2.4–2.5 board holes absorb position error.
- **USB-C back-stop:** a rib behind the receptacle body, touching or within ≤ 0.1 mm, so plug insertion force goes into the shell. Do the same for the 3.5 mm jack. ≤ 0.1 mm is only holdable in SLA/MJF. In FDM, use a crush rib (small sacrificial bump that deforms on assembly) or a shim.
- **Shell halves:** outer cover + inner baffle/frame, closed with 3–4 M2 screws from the ear-pad side (hidden under the pad), or with snap-fits plus 2 screws.
- **Snap-fit (MJF PA12):** design strain ≤ 2–3 %; cantilever length ≥ 5 × thickness. Avoid snaps in SLA standard resin.

## 4. User controls

| Control | Design rule |
|---|---|
| Side-push switches (POWER, MFB) | A printed key or plunger in a slot. Pre-travel gap 0.05–0.1 mm to the actuator (SLA/MJF only; in FDM use a compliant flexure key that preloads lightly onto the actuator); total key travel = switch travel (≈ 0.2 mm, VERIFY) + gap. Add an over-travel stop in the shell so the user can't crush the switch. Make the keys tactilely different (shape or bump) so the user can tell POWER from MFB blind. |
| Thumbwheel | Wheel protrudes ≈ 1.5–2.5 mm from the rim. Knurled, ≈ 0.3 mm clearance gap all round, dust lip. Final geometry depends on the encoder chosen (M4). |
| Light pipe | Pipe end ≤ 0.3 mm above the LED. Opaque sleeve or shell boss around the pipe to stop light leaking into the cavity. Frosted outer window. One window for RGB and charge LED: either a ≈ 6 × 3 mm slot light guide/diffuser over both LEDs placed side by side, or two Ø2 pipes merging into one frosted window. |
| BOOT | Ø1.2 pin-hole under the ear pad, or accessible only with the cover off |

## 5. Acoustic design

- **Driver:** clamp or glue to the baffle with a closed-cell foam gasket so the **front volume** (driver to ear) is sealed from the cup interior. Follow the driver vendor's rear-vent guidance; a small damped vent (mesh/felt) in the rear cavity tunes bass.
- **Electronics cavity** = driver rear volume in V1. Keep it free of rattling cables (tie down the battery and harness). Its volume affects bass, so note the volume in CAD (useful for later tuning).
- **MEMS mic ports:**
  - shell hole Ø1.0–1.5 mm (Ø0.8 is not reliably printable; drill it after printing if needed);
  - acoustic channel as short as possible (≤ 2–3 mm) to keep the Helmholtz resonance well above the voice band;
  - compressed ring gasket (PORON or silicone, 1.5–2 mm thick, 25–35 % compression, i.e. 0.4–0.7 mm, which absorbs print tolerance) between the PCB (around the Ø0.8 port) and the shell;
  - acoustic mesh or membrane over the outer hole (dust, and wind for the voice mic);
  - keep the path airtight: leaks from the cavity make the mic hear the driver (echo).
- **Voice mic MK1:** port toward the mouth (front-lower). **Reference mic MK2:** port on the outer shell, top/rear, away from the voice direction.
- **Inner mic MK3:** see issue I-6 (file 08).

## 6. RF / antenna

- Plastic only over the antenna end of the module. No metallic paint, metal inserts, screws, battery, driver magnet or metal headband/yoke parts within 15 mm of the antenna end and sides (VERIFY with Espressif guidelines). The current baseline does **not** yet guarantee this (issue I-11): H1 is ≈ 13 mm away, the placeholder encoder's metal body ≈ 11 mm, a yoke/steel band usually attaches at the top of the cup, a battery stacked behind the module would sit under it, and the right-cup harness must leave toward the top.
- The antenna faces up (top of the cup, +Z_H) and away from the head where possible. Measure RSSI in the assembled cup (file 07). If the range is poor → fall back to a WROOM-1U module with an external FPC antenna on the inner shell wall (design doc D6).

## 7. ESD, safety, thermal

- Any exposed metal (jack sleeve, USB shell) is already ESD-protected on the PCB. Avoid other exposed metal near the board. If metal trim or a headband is used, keep it ≥ 2 mm from internal conductors or ground it through a defined path.
- Speaker wires and the harness: insulated, routed away from sharp edges. Never touch GND (floating differential outputs).
- Battery: no pressure on the cell; foam pad; ≥ 0.5 mm clearance and ≥ 10 % swell room; no screws or sharp ribs pointing at the cell; keep it away from the charger IC area (warm, about 0.6 W while charging).
- Venting for heat is not required. The charger dissipation is small, but avoid enclosing it in foam.

## 8. Assembly sequence (target)

1. Driver + gasket → baffle.
2. Battery → pocket (foam pad) → plug its JST.
3. PCB → standoffs (screws). Plug the driver and harness JSTs. Fit the mic gaskets.
4. Light pipe and keys → outer shell.
5. Outer shell → baffle (screws under the pad).
6. Ear pad → clip/lip.
7. Cup → yoke/headband (swivel). Harness through the band.

Every step must be reversible for service (MR-031).

## 9. Cosmetic / portfolio

- Consistent fillet language (e.g., R1 small, R3 shell edges).
- A recessed "ORGA" logo area on the outer shell.
- The parting line hidden under the pad edge.
- Print orientation chosen so the outer face is the best surface.
- Render the CAD for the portfolio (exploded view + section through the cup showing the PCB, battery and driver stack).
