"""Lightweight shaded renders (painter's algorithm) and section plots for review PNGs."""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from build123d import Box, Pos


def mesh(shape, tol=0.25):
    """Triangulate with OCP directly; skips faces that fail to mesh instead of aborting."""
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED
    from OCP.BRep import BRep_Tool
    from OCP.TopLoc import TopLoc_Location
    from OCP.TopoDS import TopoDS
    w = shape.wrapped
    BRepMesh_IncrementalMesh(w, tol, False, 0.35, True)
    Vs, Ts, off = [], [], 0
    ex = TopExp_Explorer(w, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face(ex.Current()); loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(f, loc)
        if tri is not None:
            tr = loc.Transformation()
            pts = [tri.Node(i).Transformed(tr) for i in range(1, tri.NbNodes() + 1)]
            Vs += [(p.X(), p.Y(), p.Z()) for p in pts]
            rev = f.Orientation() == TopAbs_REVERSED
            for i in range(1, tri.NbTriangles() + 1):
                a, b, c = tri.Triangle(i).Get()
                Ts.append((off + a - 1, off + c - 1, off + b - 1) if rev else (off + a - 1, off + b - 1, off + c - 1))
            off += len(pts)
        ex.Next()
    return np.array(Vs, float).reshape(-1, 3), np.array(Ts, int).reshape(-1, 3)


def view_matrix(azim, elev):
    a, e = math.radians(azim), math.radians(elev)
    # camera looks along -d where d is the direction from target to eye
    d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    up = np.array([0, 0, 1.0])
    r = np.cross(up, d); r /= np.linalg.norm(r)
    u = np.cross(d, r)
    return np.vstack([r, u, d])


def shade(items, azim=-60, elev=22, ax=None, light=(0.4, -0.5, 0.8), edge=False):
    """items: list of (shape, rgb). Returns the axes."""
    M = view_matrix(azim, elev)
    Ld = M.T @ np.array(light); Ld /= np.linalg.norm(Ld)
    polys, cols, depth = [], [], []
    for shp, rgb in items:
        V, T = mesh(shp)
        if len(T) == 0:
            continue
        P = V @ M.T
        tri = P[T]
        n = np.cross(V[T][:, 1] - V[T][:, 0], V[T][:, 2] - V[T][:, 0])
        nl = np.linalg.norm(n, axis=1); ok = nl > 1e-12
        n[ok] /= nl[ok][:, None]
        vis = (n @ M[2]) > -0.05
        lam = np.clip(np.abs(n @ Ld), 0, 1)
        k = 0.5 + 0.5 * lam
        c = np.clip(np.outer(k, rgb), 0, 1)
        polys.append(tri[vis][:, :, :2]); cols.append(c[vis]); depth.append(tri[vis][:, :, 2].mean(1))
    polys = np.concatenate(polys); cols = np.concatenate(cols); depth = np.concatenate(depth)
    order = np.argsort(depth)
    if ax is None:
        fig, ax = plt.subplots(figsize=(11, 9))
    pc = PolyCollection(polys[order], facecolors=cols[order], edgecolors=cols[order] * 0.9 if not edge else "k",
                        linewidths=0.15)
    ax.add_collection(pc)
    ax.autoscale_view(); ax.set_aspect("equal"); ax.axis("off")
    return ax


def section_yz(items, x=0.0, ax=None, big=600):
    """Fill the cut faces of each shape on the plane X = x (2D: horizontal = Z, vertical = Y)."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    slab = Pos(x, 0, 0) * Box(0.02, big, big)
    for shp, rgb, label in items:
        try:
            cut = shp & slab
        except Exception:
            continue
        if cut is None or cut.volume < 1e-6:
            continue
        V, T = mesh(cut, 0.1)
        tri = V[T][:, :, [2, 1]]
        area = 0.5 * np.abs((tri[:, 1, 0] - tri[:, 0, 0]) * (tri[:, 2, 1] - tri[:, 0, 1]) -
                            (tri[:, 2, 0] - tri[:, 0, 0]) * (tri[:, 1, 1] - tri[:, 0, 1]))
        tri = tri[area > 1e-6]
        ax.add_collection(PolyCollection(tri, facecolors=[rgb], edgecolors=[rgb], linewidths=0.2, label=label))
    ax.autoscale_view(); ax.set_aspect("equal"); ax.grid(alpha=0.25)
    return ax
