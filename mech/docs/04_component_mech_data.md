# 04 — Mechanical Data of Interface Parts

Confidence: **D** = taken from the manufacturer datasheet in `headset-orga/orga-v1/datasheets/`. **K** = KiCad footprint (courtyard-derived). **V** = typical value, **VERIFY** against the drawing or measure with calipers before freezing CAD.

## On-board parts that touch the enclosure

| Part (ref headset-orga) | MPN | Body L × W × H [mm] | Interface data | Conf. |
|---|---|---|---|---|
| ESP32-S3 module (U2) | ESP32-S3-WROOM-1-N16R8 | 18.0 × 25.5 × 3.1 | PCB antenna at one short end; keep-out per Espressif (no copper under or beside it, no metal nearby) | D |
| USB-C (J1) | GCT USB4105-GF-A, top-mount, 16-pin USB 2.0 | 8.94 × 7.35 × 3.31 | Receptacle opening ≈ 8.34 × 2.56; 4 shell THT tabs + 2 NPTH pegs Ø0.65. Insertion/extraction forces typically ~5–20 N: needs a shell back-stop. | D (body), V (forces) |
| 3.5 mm jack (J4) | CUI/Same Sky SJ2-3593D-SMT, 3-conductor + 2 switches | courtyard 20.6 × 11.2; H ≈ 5.0 | 2 locating pegs Ø1.7; plug axis parallel to the PCB; shell hole sized for the boom-plug **overmold**, ≈ Ø7.5–8 (VERIFY with the actual boom plug) | K / VERIFY |
| Side-push switch ×2 (SW1, SW4) | Panasonic EVQ-P7A01P | ≈ 3.5 × 2.9 × 1.35 | Actuator on the board edge; travel ≈ 0.2 mm; force ≈ 1.6 N | VERIFY |
| Top-push switch (SW2 BOOT) | Omron B3U-1000P | ≈ 3.0 × 2.5 × 1.6 | Service only | VERIFY |
| Thumbwheel (SW3) | **placeholder** Bourns PEC09-2125K-N0012 | 9.7 wide, H ≈ 7.5 incl. shaft | Will be replaced: low-profile side-actuated roller encoder, decision M4 | D (placeholder) |
| RGB LED (D7) | Würth 150141M173100, PLCC4, top-view, common anode | 3.2 × 2.8 × ≈1.9 | Viewing angle wide (top-view); needs a light pipe to the shell | D (L×W), VERIFY (H) |
| Charge LED (D3) | 0603 red (part TBD) | 1.6 × 0.8 × 0.8 | Share the light pipe with D7 | V |
| MEMS mic ×3 (MK1–3) | Infineon IM73D122V01 | 4.0 × 3.0 × 1.2 | **Bottom port**: the sound inlet is on the solder side, through a Ø0.8 PCB hole. The acoustic path must be sealed from the PCB hole to the shell port (gasket). | D |
| JST SH 2p ×2 (J5, J6) | SM02B-SRSS-G-TB, horizontal | courtyard ≈ 5.8 × 6.6, H 2.95 | Mated plug adds ≈ 4 mm along the cable axis; wire bend radius ≥ 3 mm | K / VERIFY |
| JST SH 3p (J3) | SM03B-SRSS-TB, horizontal | courtyard ≈ 6.8 × 6.6, H 2.95 | As above | K / VERIFY |
| Inductor (L1) | Würth 74438335022 | 3.0 × 3.0 × 1.5 | Magnetic; keep away from the mic ports (electrical) | D |
| IMU (U9) | ST LSM6DSV16X LGA-14 | 3.0 × 2.5 × 0.86 | Axis marking on the package: record its orientation in frame H | D |

## Off-board parts (dimensions drive the cup design)

| Part | Spec | Key dimensions | Conf. |
|---|---|---|---|
| Driver ×2 | 40 mm dynamic, 32 Ω, ≥ 100 dB/mW | OD ≈ 40 (frame/flange often 40–42), depth ≈ 5–10, rear vents on the back | **TBD**: pick a part with a drawing (decision D1 of design doc) |
| Battery | 1S Li-Po ~1000 mAh, 603450 class, PCM + 10 kΩ NTC, 3 wires | ≈ 6.0 × 34 × 50 (+3–5 mm PCM/tab end); mass ≈ 18–22 g; swell allowance ≥ 10 % thickness | V, measure the real cell |
| Ear pads | Over-ear replacement pads | Inner opening: target ≈ 75 × 48 (covers ≈95th-percentile pinna 70 mm + clearance); ≥ 65 × 45 absolute minimum (large ears will touch, file 06); thickness 18–25 uncompressed; attach by lip/flange or clip ring | **TBD** (decision M7) |
| Headband | Spring steel band or printed band + sliders | Adjustment ≥ 25 mm per side (≥ 50 mm total, file 06). A steel band must end ≥ 15 mm from the antenna (I-11). | TBD (M6) |
| Boom mic | Detachable 3.5 mm mono electret, gooseneck | Plug body ≈ Ø5–7 × 10–15 mm; check the plug pinout matches tip = mic, sleeve = GND | V |
| USB-C cable plugs | Assorted overmolds | Overmold widths vary (≈ 8.5–12.5 mm) and heights (≈ 5–7 mm): test with real cables | V |
| Fasteners | M2 × 4–6 mm screws, M2 heat-set inserts | Insert OD ≈ 3.2–3.6, length 3–4 (use the insert vendor's recommended hole) | V |
| Light pipe | Ø2–3 mm PC/PMMA | Length = LED top to shell outer surface (≈ 3–6 mm) | V |

## Mass budget (first estimate, for MR-001 / MR-002)

| Item | Left cup [g] | Right cup [g] | Headband [g] |
|---|---|---|---|
| Shell + baffle (printed, ~2 mm walls) | 35–45 | 30–40 | — |
| Driver | 10–15 | 10–15 | — |
| Ear pad | 10–15 | 10–15 | — |
| PCB assembly | 8–12 | — | — |
| Battery 1000 mAh | 18–22 | — | — |
| Screws, pipe, gaskets | 3 | 2 | — |
| Headband + sliders + cushion + harness | — | — | 60–90 |
| **Subtotal** | **84–112** | **52–72** | **60–90** |

The total is about 196–274 g, which fits under 300 g. The left/right difference is about 30–40 g, at the limit of MR-002. The options are to move the battery to the right cup (V2) or to add a counterweight (not recommended).
