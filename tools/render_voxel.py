"""Renderizador simples de blocos para ilustrar zonas e atividades.

Usa as texturas do jogo, extraídas localmente do .jar do cliente. As texturas não são versionadas.
Para ilustrar elementos que não são blocos, use nomes com prefixo npc_ ou prop_.
"""
import os
import numpy as np
from PIL import Image

TEX = os.environ.get('BIOPARK_TEXTURAS', 'tex')
MAPA = {'grass_block': 'grass_block_top', 'smooth_quartz_slab': 'quartz_block_bottom', 'smooth_quartz': 'quartz_block_bottom',
        'smooth_stone_slab': 'smooth_stone_slab_side', 'polished_andesite_slab': 'polished_andesite',
        'polished_blackstone_slab': 'polished_blackstone', 'dark_oak_fence': 'dark_oak_planks', 'spruce_fence': 'spruce_planks',
        'oak_slab': 'oak_planks', 'redstone_wall_torch': 'redstone_torch', 'redstone_wire': 'redstone_dust_dot',
        'npc_legs': 'blue_concrete', 'npc_head': 'sandstone_top', 'prop_botao': 'stone'}


def textura(b):
    n = b.split('[')[0]
    if n.startswith('npc_') and n not in MAPA:
        return n[4:]
    return MAPA.get(n, n.replace('_pane', ''))


def caixa(b):
    if b.startswith(('dark_oak_fence', 'spruce_fence')): return (.375, 0, .375, .625, 1, .625)
    if b.startswith('iron_bars'): return (.44, 0, .44, .56, 1, .56)
    if '_pane' in b: return (0, 0, .44, 1, 1, .56)
    if b.startswith('redstone_wire'): return (0, 0, 0, 1, .08, 1)
    if b.startswith('prop_botao'): return (.3, .35, .75, .7, .65, 1)
    if 'type=top' in b: return (0, .5, 0, 1, 1, 1)
    if 'type=bottom' in b: return (0, 0, 0, 1, .5, 1)
    if b == 'npc_legs': return (.28, 0, .36, .72, 1, .64)
    if b == 'npc_head': return (.2, 0, .2, .8, .6, .8)
    if b.startswith('npc_'): return (.22, 0, .34, .78, 1, .66)
    return (0, 0, 0, 1, 1, 1)


def carregar(n):
    t = np.asarray(Image.open(os.path.join(TEX, n + '.png')).convert('RGBA').crop((0, 0, 16, 16)), float).copy()
    if n == 'grass_block_top': t[..., :3] *= [.52, .72, .33]
    if n == 'oak_leaves': t[..., :3] *= [.40, .62, .25]
    if n == 'azalea_leaves': t[..., :3] *= [.62, .74, .72]
    return t


def npc(G, x, z, roupa='orange_concrete'):
    G[(x, 0, z)] = 'npc_legs'; G[(x, 1, z)] = 'npc_' + roupa; G[(x, 2, z)] = 'npc_head'


def render(G, cam, alvo, modo, saida, overlay=None, f=820, w=960, h=640):
    """modo: SALA (interno) ou FORA (externo). overlay: (imagem, x0, x1, y0, y1, plano_z), na face voltada para +z."""
    cam = np.array(cam, float); alvo = np.array(alvo, float)
    xs = [p[0] for p in G]; ys = [p[1] for p in G]; zs = [p[2] for p in G]
    x0, y0, z0 = min(xs), min(ys), min(zs); dim = np.array([max(xs) - x0 + 1, max(ys) - y0 + 1, max(zs) - z0 + 1])
    ids = {}; texs = [np.zeros((16, 16, 4))]; caixas = [(0, 0, 0, 1, 1, 1)]; V = np.zeros(dim, int)
    for (x, y, z), b in G.items():
        k = (textura(b), caixa(b))
        if k not in ids:
            ids[k] = len(texs); texs.append(carregar(k[0])); caixas.append(k[1])
        V[x - x0, y - y0, z - z0] = ids[k]
    T = np.stack(texs); B = np.array(caixas, float)
    GL = [i for k, i in ids.items() if 'glass' in k[0]]
    LUZ = [i for k, i in ids.items() if k[0] == 'sea_lantern']
    lo = np.array([x0, y0, z0], float); hi = lo + dim

    def uvs(P, n):
        uv = np.where(n[:, None] == 0, P[:, [2, 1]], np.where(n[:, None] == 1, P[:, [0, 2]], P[:, [0, 1]]))
        q = (uv - np.floor(uv)) * 16
        return q[:, 0].astype(int).clip(0, 15), (15 - q[:, 1].astype(int)).clip(0, 15)

    def trace(o, d, sem_vidro=False):
        n = len(d); inv = 1 / np.where(np.abs(d) < 1e-9, 1e-9, d)
        t0 = (lo - o) * inv; t1 = (hi - o) * inv
        tn = np.minimum(t0, t1).max(1); tf = np.maximum(t0, t1).min(1)
        hit = np.zeros(n, int); ht = np.full(n, np.inf); nor = np.zeros(n, int)
        a = np.where(tf > np.maximum(tn, 0))[0]
        t = np.maximum(tn[a], 0) + 1e-5
        c = np.floor(o[a] + d[a] * t[:, None]).astype(int)
        st = np.where(d[a] > 0, 1, -1); tm = (c + (st > 0) - o[a]) * inv[a]; dl = np.abs(inv[a])
        for _ in range(500):
            if len(a) == 0: break
            i = c - [x0, y0, z0]; ok = ((i >= 0) & (i < dim)).all(1)
            val = np.zeros(len(a), int); val[ok] = V[i[ok, 0], i[ok, 1], i[ok, 2]]
            if sem_vidro: val[np.isin(val, GL)] = 0
            hh = np.where(val > 0)[0]; done = np.zeros(len(a), bool); done[~ok] = True
            if len(hh):
                b = B[val[hh]]; oo = o[a[hh]]; dd = d[a[hh]]; iv = inv[a[hh]]
                ta = (c[hh] + b[:, :3] - oo) * iv; tb = (c[hh] + b[:, 3:] - oo) * iv
                tn2 = np.minimum(ta, tb); tf2 = np.maximum(ta, tb).min(1)
                ax = np.argmax(tn2, 1); tt = tn2[np.arange(len(hh)), ax]
                good = (tf2 >= tt) & (tf2 > 0)
                P = oo + dd * np.maximum(tt, 0)[:, None]
                u, v = uvs(P, ax); al = T[val[hh], v, u, 3]
                good &= (al > 10) | np.isin(val[hh], GL)
                g = hh[good]; hit[a[g]] = val[g]; ht[a[g]] = np.maximum(tt[good], 0); nor[a[g]] = ax[good]; done[g] = True
            keep = ~done
            a = a[keep]; c = c[keep]; tm = tm[keep]; dl = dl[keep]; st = st[keep]
            if len(a) == 0: break
            ax = np.argmin(tm, 1); r = np.arange(len(a)); c[r, ax] += st[r, ax]; tm[r, ax] += dl[r, ax]
        return hit, ht, nor

    z = cam - alvo; z /= np.linalg.norm(z); xx = np.cross([0, 1, 0], z); xx /= np.linalg.norm(xx); R = np.stack([xx, np.cross(z, xx), z])
    u, v = np.meshgrid(np.arange(w) + .5, np.arange(h) + .5)
    d = (np.stack([(u - w / 2) / f, -(v - h / 2) / f, -np.ones_like(u)], -1) @ R).reshape(-1, 3)
    d /= np.linalg.norm(d, axis=1, keepdims=True); o = np.tile(cam, (len(d), 1))
    hit, t, nor = trace(o, d)
    img = np.tile(np.array([186, 190, 195.]), (len(d), 1)) + d[:, [1]] * 40
    m = hit > 0; P = o[m] + d[m] * t[m, None]; n = nor[m]; ix = np.arange(m.sum())
    sn = -np.sign(d[m][ix, n]); N = np.zeros_like(P); N[ix, n] = sn
    ui, vi = uvs(P, n); col = T[hit[m], vi, ui, :3].copy()
    col[np.isin(hit[m], GL)] = np.array([205, 222, 235.])
    for im, xa, xb, ya, yb, zf in (overlay or []):
        arr = np.asarray(im.convert('RGBA'), float)
        s = (n == 2) & (sn > 0) & (np.abs(P[:, 2] - zf) < 1e-3) & (P[:, 0] >= xa) & (P[:, 0] < xb) & (P[:, 1] >= ya) & (P[:, 1] < yb)
        yy = ((yb - P[s, 1]) / (yb - ya) * (arr.shape[0] - 1)).astype(int); xi = ((P[s, 0] - xa) / (xb - xa) * (arr.shape[1] - 1)).astype(int)
        al = arr[yy, xi, 3:] / 255; col[s] = col[s] * (1 - al) + arr[yy, xi, :3] * al
    if modo == 'SALA':
        amb = np.where(n == 1, 1.02, np.where(n == 0, .9, .97)); vis = np.zeros(len(P))
        for off in ((.6, .3, .2), (-.6, .3, -.2), (.2, .3, .6), (-.2, .3, -.6), (.5, .8, -.5), (-.5, .8, .5)):
            dr = N + np.array(off); dr /= np.linalg.norm(dr, axis=1, keepdims=True)
            h2, t2, _ = trace(P + N * .03, dr, True); vis += ~((h2 > 0) & (t2 < 3.0))
        luz = amb * (.74 + .26 * vis / 6)
        col[np.isin(hit[m], LUZ)] = np.array([250, 250, 240.]); luz[np.isin(hit[m], LUZ)] = 1
        img[m] = col * luz[:, None]
    else:
        sol = np.array([.45, .7, .55]); sol /= np.linalg.norm(sol)
        amb = np.where(n == 1, .92, np.where(n == 0, .74, .84))
        h2, _, _ = trace(P + N * .02, np.tile(sol, (len(P), 1))); dif = np.maximum((N * sol).sum(1), 0) * (h2 == 0)
        img[m] = col * (amb * .72 + dif * .36)[:, None]
    Image.fromarray(img.reshape(h, w, 3).clip(0, 255).astype('uint8')).save(saida, quality=92)
