# 02 — Mechanical System Architecture

## 1. Partitioning (V1)

```text
                       ┌──────────── headband (adjustable sliders, cushion) ────────────┐
                       │                2-wire twisted pair: HPR_P, HPR_N               │
                       │                (floating differential — never to GND)          │
   LEFT CUP (main) ◄───┘                                                                └───► RIGHT CUP
   • main PCB (ESP32-S3 module, codec, charger, buck-boost, IMU)                                • right driver (40 mm)
   • left driver (40 mm)                                                                         • driver wires → harness
   • battery 1S Li-Po ~1000 mAh                                                                  • (V2 option: battery here
   • MEMS mics MK1 (voice) and MK2 (reference); MK3 inner (DNP)                                    for balance, +3 wires)
   • USB-C, boom-mic 3.5 mm jack, POWER, MFB, thumbwheel, RGB + charge LED
   • antenna end of the module at the TOP of the cup
```

The right cup holds no electronics in V1, only the driver and the harness. Design doc §5.1 keeps the PDM mic clock out of the harness.

## 2. Electrical-to-mechanical interface list

| Interface | Connector (ref headset-orga / orga-v1) | Mechanical consequence |
|---|---|---|
| USB-C charge + data | J1 / J1, GCT USB4105-GF-A, top-mount | Shell opening; plug overmold recess; back-stop rib |
| Boom mic | J4 / J3, CUI SJ2-3593D-SMT 3.5 mm 3-pole with switch | Shell opening toward the mouth; plug retention |
| Battery | J3 / J2, JST SH 3-pin (BAT+, GND, NTC) | Cable routing from the battery pocket; cell needs a 10 kΩ NTC lead |
| Left driver | J5 / J4, JST SH 2-pin | Short pigtail from the driver tabs |
| Right-cup harness | J6 / J5, JST SH 2-pin | Cable entry with strain relief at the left cup–headband junction |
| POWER key | SW1, Panasonic EVQ-P7A side-push | Shell key or plunger on the rim |
| MFB key | SW4, EVQ-P7A side-push | Shell key or plunger on the rim |
| Thumbwheel | SW3, PEC09 **placeholder** | Real roller encoder TBD (decision M4). Slot in the rim. |
| BOOT | SW2, Omron B3U-1000P top-push | Service access only |
| RGB status LED | D7 / D6, Würth 150141M173100 PLCC4 top-view | Light pipe to the shell window |
| Charge LED | D3 / D2, 0603 red | Share the light pipe with the RGB (move next to D6) |
| Voice mic | MK1, IM73D122V01 bottom-port | Shell port + gasket + mesh, front-lower |
| Reference mic | MK2, IM73D122V01 bottom-port | Shell port + gasket + mesh, top/rear |
| Inner mic (DNP) | MK3, IM73D122V01 bottom-port | Only hears the cavity behind the driver (see issue I-6 in file 08) |
| IMU | U9 / U8, LSM6DSV16X | Rigid board mount; record axis orientation vs head frame H (HRTF head tracking) |
| Antenna | U2 / U6, ESP32-S3-WROOM-1 PCB antenna | Plastic window, ≥ 15 mm from metal |

## 3. Left-cup internal stack (outward → ear). Concept; to be sized in CAD

The driver is mounted **in** the baffle. Its magnet/body projects backward into the electronics (rear) cavity, and its diaphragm faces the ear through the front volume.

| Layer (outward → ear) | Thickness (first estimate) | Notes |
|---|---|---|
| Outer shell wall | 2.0 mm | FDM ≥ 1.6 mm. Plastic over the antenna. |
| Clearance | 0.5 mm | |
| Top-side components | 5.0 mm (jack), 3.3 (USB), 3.1 (module); thumbwheel TBD | Height map in file 03 (M1-A: top faces out) |
| PCB | 1.6 mm | 4-layer |
| Bottom-side parts + cable space | 1.5–2.5 mm | MK1/MK2 move here under M1-A (1.2 mm) |
| Battery (if stacked behind the PCB) | 6.0 mm + 10 % swell | Better **beside** the driver body than over it (decision M3) |
| Driver body projecting into the rear cavity | 5–10 mm (VERIFY with part) | Overlaps the battery zone if the battery sits beside it |
| Baffle | 1.5–2.0 mm | Seals the front volume from the electronics cavity |
| Front volume + grille | 2–5 mm | |
| Ear pad | 18–25 mm uncompressed, ≈ 10–15 mm compressed | Inner opening: file 06 |

- **Rear/electronics cavity** (shell outer face → baffle): ≈ 16–20 mm with the battery stacked, ≈ 12–15 mm with the battery beside the driver body.
- **Ear clearance:** pinna protrusion (15–25 mm) + ≥ 5 mm clearance means head skin to grille ≈ 20–30 mm. A compressed pad gives only 10–15 mm, so the baffle must be **recessed (or angled) into the cup** by roughly another 10–15 mm, or the pad must be deeper.
- **Total cup depth** including the pad: ≈ 35–50 mm. Iterate in CAD.

## 4. Purchased mechanical / off-board parts list (to source)

| Item | Spec / candidate | Status |
|---|---|---|
| Drivers ×2 | 40 mm dynamic, 32 Ω, ≥ 100 dB/mW, with dimensional drawing | **TBD (design doc D1)**. CAD needs OD, flange and depth. |
| Battery | 1S Li-Po ~1000 mAh, 603450 class (~6 × 34 × 50 mm + PCM), 3-wire with 10 kΩ NTC, JST SH 3p | TBD; measure the actual cell |
| Ear pads ×2 | Off-the-shelf over-ear replacement pads (oval), inner opening per file 06 | TBD (decision M7) |
| Headband | Spring-steel band + 3D-printed sliders, or fully printed. Cushion. | TBD (decision M6) |
| Boom mic | Detachable 3.5 mm mono electret boom (3-pole TRS plug, mic on tip) | TBD. Check plug pinout vs. the SJ2-3593D 3-pole jack. |
| Fasteners | M2 screws + M2 heat-set inserts (brass, ~Ø3.2–3.6 × 3–4 mm) | Standard |
| Light pipe | Ø2–3 mm PC/PMMA rod or off-the-shelf pipe; length = PCB-to-shell distance | TBD |
| Mic gaskets + mesh | Die-cut PORON/silicone ring gasket, acoustic mesh/membrane ~Ø3–4 mm | TBD |
| Thumbwheel encoder | Low-profile side-actuated roller encoder (replaces the PEC09 placeholder) | TBD (decision M4) |
| Harness wire | 2-core twisted pair, ~28–30 AWG, flexible (silicone/PTFE), plus JST SH crimp housings | TBD |
| USB-C cable (test) | 2–3 cables with different overmold sizes, for the fit test | Have on hand |
