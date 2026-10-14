import csv, math, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, Circle, Polygon
import matplotlib.transforms as mt
S = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(S, 'out')
rows = list(csv.DictReader(open(os.path.join(OUT, 'orga_v1_component_envelope.csv'))))
R, FY = 31.0, 26.0
fig, axs = plt.subplots(1, 2, figsize=(16, 8.6))
for ax, side in zip(axs, ['top', 'bottom']):
    a = math.degrees(math.asin(FY / R)); xf = math.sqrt(R*R - FY*FY)
    ax.add_patch(Arc((0, 0), 2*R, 2*R, theta1=180 - a, theta2=360 + a, lw=2, color='k'))
    ax.plot([-xf, xf], [FY, FY], 'k', lw=2)
    ax.add_patch(Rectangle((-24, FY), 48, 15, fc=(1, 0, 0, .12), ec='r', ls='--'))
    ax.text(0, FY + 7.5, 'ANTENNA KEEP-OUT (module courtyard)\nno metal / battery / steel band within 15 mm\nplastic shell only', ha='center', va='center', fontsize=8, color='r')
    for r in rows:
        x, y = float(r['box_cx']), float(r['box_cy'])
        if r['footprint'].startswith('MountingHole'):
            ax.add_patch(Circle((x, y), 1.1, fc='w', ec='k')); ax.text(x, y + 1.6, r['ref_orga_v1'] + ' M2', ha='center', fontsize=7)
            continue
        if r['side'] != side or not r['body_L']: continue
        L, W = float(r['body_L']), float(r['body_W']); rot = float(r['rot_deg'])
        if 'courtyard' in r['dim_source'] or 'PLACEHOLDER' in r['dim_source'] or 'JST' in r['dim_source']: rot = 0
        crit = bool(r['mech_interface'])
        p = Rectangle((x - L/2, y - W/2), L, W, fc=('#f4b183' if crit else '#d9d9d9'), ec='k', lw=.6 if not crit else 1.2)
        p.set_transform(mt.Affine2D().rotate_deg_around(x, y, rot) + ax.transData); ax.add_patch(p)
        if crit or L*W > 6:
            lab = r['ref_orga_v1'] + (f" ({r['ref_headset_orga']})" if r['ref_headset_orga'] and r['ref_headset_orga'] != r['ref_orga_v1'] else '')
            ax.text(x, y, lab + f"\nH{float(r['body_H']):.1f}", ha='center', va='center', fontsize=6.5 if crit else 5.5)
    for ref, (x, y) in {'MK1': (-16, -21.32), 'MK2': (15.5, 17.18), 'MK3': (-1.25, -4.78)}.items():
        ax.add_patch(Circle((x, y), .4, fc='b'));
    ax.annotate('USB-C mouth (−Y)', (0, -31.5), (0, -36), ha='center', fontsize=8, arrowprops=dict(arrowstyle='->'))
    ax.annotate('jack mouth (+X)', (28.7, -12), (35, -18), fontsize=8, arrowprops=dict(arrowstyle='->'))
    ax.annotate('POWER key (−X)', (-30.6, 0), (-44, 4), fontsize=8, arrowprops=dict(arrowstyle='->'))
    ax.annotate('MFB key (+X)', (30.4, -1), (33, 6), fontsize=8, arrowprops=dict(arrowstyle='->'))
    ax.set_xlim(-46, 46); ax.set_ylim(-40, 44); ax.set_aspect('equal'); ax.grid(alpha=.25)
    ax.set_xlabel('X_B [mm]'); ax.set_ylabel('Y_B [mm]')
    ax.set_title(f"{side.upper()} side ({'component side, viewed from top' if side=='top' else 'viewed from TOP (see-through); test pads, MK3, C33'})", fontsize=10)
    ax.arrow(-42, -36, 6, 0, head_width=1, color='k'); ax.arrow(-42, -36, 0, 6, head_width=1, color='k')
    ax.text(-35, -36.5, '+X_B', fontsize=8); ax.text(-43, -29, '+Y_B', fontsize=8)
fig.suptitle('ORGA v1 main board — MCAD envelope (reference placement orga-v1). Board frame B: origin = outline-circle centre, Z=0 PCB bottom, PCB 1.6 mm.\n'
             'Orange = mechanical-interface parts (ref orga-v1 (ref headset-orga)), H = body height above board surface [mm]. Blue dots = Ø0.8 mic ports. Outline: Ø62 circle cut flat at Y=+26.', fontsize=10)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'orga_v1_mech_drawing.png'), dpi=160)
print('ok')
