#!/usr/bin/env python3
"""ORGA v1 main-board MCAD envelope: STEP/STL/DXF/CSV/PNG from the reference placement (orga-v1).
Board frame B: origin = centre of the Ø62 outline circle, +X right, +Y toward the flat (antenna) edge,
viewed from the TOP (component) side; Z = 0 at PCB bottom surface, PCB top surface at Z = +1.6 mm."""
import json, math, csv, sys, os
import cadquery as cq

S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, 'out'); os.makedirs(OUT, exist_ok=True)
fps = json.load(open(os.path.join(S, 'orga_v1_fps.json')))['fps']          # KiCad footprint extraction (orga-v1)
DNP = {r for r, d in json.load(open(os.path.join(S, 'orga_v1_design_nets.json'))).items() if d.get('dnp')}
T = 1.6; R = 31.0; FLAT_Y = 26.0          # outline: circle R31 cut by chord at Y=+26
C0 = (100.0, 100.0)                        # KiCad coords of the circle centre
def bx(x): return round(x - C0[0], 3)
def by(y): return round(-(y - C0[1]), 3)

# user-schematic (headset-orga) reference for each orga-v1 reference (mechanically relevant parts)
USER_REF = {'D2':'D3','D6':'D7','J1':'J1','J2':'J3','J3':'J4','J4':'J5','J5':'J6','L1':'L1','MK1':'MK1','MK2':'MK2','MK3':'MK3',
            'Q1':'Q1','SW1':'SW1','SW2':'SW2','SW3':'SW3','SW4':'SW4','U1':'U7','U2':'U1','U3':'U3','U4':'U4','U5':'U5',
            'U6':'U2','U7':'U8','U8':'U9','Y1':'Y1','D1':'D1','D3':'D4','D4':'D6','D5':'D5','H1':'(add)','H2':'(add)'}

# body envelope: (L along footprint X, W along footprint Y, H above board surface) in mm; source tag
BODY = {
 'ESP32-S3-WROOM-1': (18.0, 25.5, 3.1, 'Espressif datasheet §10.1 (18 × 25.5 × 3.1)'),
 'USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal': (8.94, 7.35, 3.31, 'GCT USB4105 drawing (8.94 × 7.35, H 3.31) — verify'),
 'Jack_3.5mm_CUI_SJ2-3593D-SMT_Horizontal': (None, None, 5.0, 'courtyard; H ≈5.0 — VERIFY against SJ2-3593D-SMT drawing'),
 'RotaryEncoder_Bourns_Horizontal_PEC09-2xxxF-Nxxxx': (None, None, 7.5, 'PLACEHOLDER part (PEC09); real thumbwheel TBD'),
 'SW_SPST_EVQP7A': (3.5, 2.9, 1.35, 'Panasonic EVQ-P7 side-push — VERIFY'),
 'SW_SPST_B3U-1000P': (3.0, 2.5, 1.6, 'Omron B3U-1000P top-push — VERIFY'),
 'JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal': (None, None, 2.95, 'JST SH horizontal, H 2.95 + mated plug — VERIFY'),
 'JST_SH_SM03B-SRSS-TB_1x03-1MP_P1.00mm_Horizontal': (None, None, 2.95, 'JST SH horizontal, H 2.95 + mated plug — VERIFY'),
 'L_Wuerth_MAPI-3015': (3.0, 3.0, 1.5, 'Würth 74438335022 (3.0 × 3.0 × 1.5)'),
 'Infineon_PG-LLGA-5-3_IM73D122': (4.0, 3.0, 1.2, 'Infineon IM73D122V01 (4 × 3 × 1.2), bottom port Ø0.8 PCB hole'),
 'LED_RGB_Wuerth-PLCC4_3.2x2.8mm_150141M173100': (3.2, 2.8, 1.9, 'Würth 150141M173100 PLCC4, H ≈1.9 — VERIFY'),
 'Texas_RHB0032E_VQFN-32-1EP_5x5mm_P0.5mm_EP3.45x3.45mm_ThermalVias': (5.0, 5.0, 1.0, 'TI RHB QFN-32'),
 'VQFN-16-1EP_3x3mm_P0.5mm_EP1.6x1.6mm_ThermalVias': (3.0, 3.0, 1.0, 'TI RGT QFN-16'),
 'Texas_DRC0010J_ThermalVias': (3.0, 3.0, 1.0, 'TI DRC SON-10'),
 'LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y': (3.0, 2.5, 0.86, 'ST LSM6DSV16X LGA-14'),
 'Oscillator_SMD_Abracon_ASE-4Pin_3.2x2.5mm': (3.2, 2.5, 1.2, 'Abracon ASE (DNP)'),
 'SOT-23': (2.9, 2.4, 1.45, 'SOT-23 max'), 'SOT-23-5': (2.9, 2.8, 1.45, 'SOT-23-5 max'), 'SOT-23-6': (2.9, 2.8, 1.45, 'SOT-23-6 max'),
 'D_SMF': (2.8, 1.9, 1.1, 'SMF'),
 'R_0402_1005Metric': (1.0, 0.5, 0.4, 'chip'), 'C_0402_1005Metric': (1.0, 0.5, 0.55, 'chip'), 'D_0402_1005Metric': (1.0, 0.5, 0.6, 'chip'),
 'R_0603_1608Metric': (1.6, 0.8, 0.5, 'chip'), 'C_0603_1608Metric': (1.6, 0.8, 0.9, 'chip'), 'L_0603_1608Metric': (1.6, 0.8, 0.9, 'chip'),
 'LED_0603_1608Metric': (1.6, 0.8, 0.8, 'chip LED'),
 'R_0805_2012Metric': (2.0, 1.25, 0.6, 'chip'), 'C_0805_2012Metric': (2.0, 1.25, 1.35, 'chip'),
 'TestPoint_Pad_D1.0mm': (1.0, 1.0, 0.05, 'pad only (pogo-pin target)'),
 'MountingHole_2.2mm_M2': (0, 0, 0, 'M2 hole Ø2.2'),
}
MECH = {'J1':'USB-C port (shell opening, plug overmold clearance)','J3':'Boom-mic 3.5 mm jack (shell opening)',
        'SW1':'POWER side-push (shell key)','SW4':'MFB side-push (shell key)','SW3':'Thumbwheel encoder (PLACEHOLDER, shell slot)',
        'SW2':'BOOT (internal access only)','D6':'RGB status LED (light pipe)','D2':'Charge LED (light pipe, share with D6)',
        'MK1':'Voice mic port (shell hole + gasket + mesh)','MK2':'Reference mic port (shell hole + gasket + mesh)',
        'MK3':'Inner-cup mic (DNP) port','U6':'ESP32-S3 module — antenna end at flat edge, no metal ≥15 mm',
        'J2':'Battery cable (JST SH 3p)','J4':'Left driver cable (JST SH 2p)','J5':'Right-cup harness (JST SH 2p)',
        'H1':'M2 mounting hole','H2':'M2 mounting hole','U8':'IMU — record axis orientation in assembly'}

rows = []; solids = []
board = (cq.Workplane('XY').circle(R).extrude(T)
         .intersect(cq.Workplane('XY').center(0, (FLAT_Y - 40) / 2).rect(80, FLAT_Y + 40).extrude(T)))
drills = []
for f in fps:
    name = f['fp'].split(':')[-1]
    L, W, H, src = BODY.get(name, (None, None, 1.0, 'default envelope'))
    x, y, rot = bx(f['x']), by(f['y']), f['rot']
    top = f['side'] == 'top'
    if L is None:  # use courtyard bbox, shrink 0.25 mm per side
        cb = f['court']; L = (cb[2] - cb[0]) - 0.5; W = (cb[3] - cb[1]) - 0.5
        ccx, ccy = bx((cb[0] + cb[2]) / 2), by((cb[1] + cb[3]) / 2); boxrot = 0
    else:
        ccx, ccy = x, y; boxrot = rot
    if name == 'ESP32-S3-WROOM-1':   # body sits flush to the flat edge (Y = +26 .. +0.5)
        L, W = 18.0, 25.5; ccx, ccy, boxrot = 0.0, FLAT_Y - 25.5 / 2, 0
    for h in f['holes']:
        if max(h['d'], h['dy']) < 0.5: continue      # skip thermal/stitch vias
        drills.append((bx(h['x']), by(h['y']), max(h['d'], h['dy']) if not h['npth'] else h['d']))
    if H > 0 and L > 0:
        z0 = T if top else -H
        s = (cq.Workplane('XY').workplane(offset=z0).center(ccx, ccy)
             .rect(L, W).extrude(H))
        if boxrot: s = s.rotate((ccx, ccy, 0), (ccx, ccy, 1), boxrot)
        solids.append((f['ref'], s))
    rows.append(dict(ref_orga_v1=f['ref'], ref_headset_orga=USER_REF.get(f['ref'], ''), value=f['val'], footprint=name,
                     x_mm=x, y_mm=y, box_cx=round(ccx, 2), box_cy=round(ccy, 2), rot_deg=round(rot, 1), side=f['side'],
                     body_L=round(L, 2) if L else '', body_W=round(W, 2) if W else '', body_H=H,
                     z_top_mm=round((T + H) if top else -H, 2), mech_interface=MECH.get(f['ref'], ''), dnp=f['ref'] in DNP, dim_source=src))
for x, y, d in drills:
    board = board.cut(cq.Workplane('XY').center(x, y).circle(d / 2).extrude(T))

asm = cq.Assembly(name='ORGA_v1_mainboard_envelope')
asm.add(board, name='PCB_1.6mm', color=cq.Color(0.1, 0.45, 0.2))
for ref, s in solids:
    col = cq.Color(0.75, 0.75, 0.78) if ref.startswith(('U6', 'J1', 'J3')) else cq.Color(0.2, 0.2, 0.22)
    asm.add(s, name=ref, color=col)
# antenna keep-out marker (non-physical): 18 x 15 mm beyond the flat edge, translucent
ko = cq.Workplane('XY').workplane(offset=-3).center(0, FLAT_Y + 7.5).rect(48, 15).extrude(T + 6.1)   # = module footprint keep-out courtyard
asm.add(ko, name='KEEPOUT_antenna_no_metal_marker', color=cq.Color(1, 0, 0, 0.25))
asm.save(os.path.join(OUT, 'orga_v1_mainboard_envelope.step'))
comp = board
for _, s in solids: comp = comp.union(s, clean=False)
cq.exporters.export(comp, os.path.join(OUT, 'orga_v1_mainboard_envelope.stl'), tolerance=0.05)

# DXF outline (board frame, mm) + holes on layer HOLES
import ezdxf
doc = ezdxf.new(dxfversion='R2010'); doc.units = ezdxf.units.MM; msp = doc.modelspace()
doc.layers.add('OUTLINE'); doc.layers.add('HOLES'); doc.layers.add('PORTS_AND_OPENINGS')
a = math.degrees(math.asin(FLAT_Y / R)); xf = math.sqrt(R * R - FLAT_Y * FLAT_Y)
msp.add_line((-xf, FLAT_Y), (xf, FLAT_Y), dxfattribs={'layer': 'OUTLINE'})
msp.add_arc((0, 0), R, 180 - a, a, dxfattribs={'layer': 'OUTLINE'})   # CCW from 123° through 270° to 57°
for x, y, d in drills:
    msp.add_circle((x, y), d / 2, dxfattribs={'layer': 'HOLES'})
doc.saveas(os.path.join(OUT, 'orga_v1_board_outline.dxf'))

with open(os.path.join(OUT, 'orga_v1_component_envelope.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader()
    for r in sorted(rows, key=lambda r: (r['mech_interface'] == '', r['ref_orga_v1'])): w.writerow(r)
print('solids', len(solids), 'drills', len(drills), 'rows', len(rows))
