#!/usr/bin/env python3
"""Gera as ilustrações das 13 missões de docs/ATIVIDADES.md.

Uso: python gerar_imagens_atividades.py PASTA_DAS_TEXTURAS PASTA_DE_SAIDA [m0 t1_1 ...]

As imagens são ilustrações do que cada atividade propõe, não registros de sessões.
Os objetos acrescentados aqui, como quadros e botões, servem só para a imagem e não fazem parte dos .schem.
"""
import os, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent; RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
sys.dont_write_bytecode = True
FONTE = 'C:/Windows/Fonts/ARLRDBD.TTF'


def fonte(t):
    try:
        return ImageFont.truetype(FONTE, t)
    except OSError:
        return ImageFont.load_default(t)


def quadro(linhas, fundo=(250, 250, 248), cor=(30, 30, 30), w=1200, h=600, t=70, centro=True):
    im = Image.new('RGBA', (w, h), fundo); d = ImageDraw.Draw(im)
    alt = int(t * 1.35); y = (h - alt * len(linhas)) // 2 if centro else 40
    for l in linhas:
        txt, tam = (l, t) if isinstance(l, str) else l
        f = fonte(tam); bb = d.textbbox((0, 0), txt, font=f)
        d.text(((w - (bb[2] - bb[0])) // 2 if centro else 50, y), txt, font=f, fill=cor); y += alt
    return im


def planilha():
    im = Image.new('RGBA', (1200, 600), (250, 250, 248)); d = ImageDraw.Draw(im); f = fonte(44)
    linhas = [('Cor', 'Blocos'), ('Branco', '120'), ('Azul', '45'), ('Amarelo', '80'), ('Total', '=SOMA(B2:B4)')]
    for i, (a, b) in enumerate(linhas):
        y = 60 + i * 95
        d.rectangle((50, y, 300, y + 95), outline=(90, 90, 90), width=3); d.rectangle((300, y, 660, y + 95), outline=(90, 90, 90), width=3)
        d.text((65, y + 20), a, font=f, fill=(30, 30, 30)); d.text((315, y + 20), b, font=f, fill=(30, 30, 30))
    for x, v, c in ((770, 120, (190, 190, 190)), (900, 45, (40, 70, 170)), (1030, 80, (230, 170, 20))):
        d.rectangle((x, 500 - v * 3, x + 90, 500), fill=c)
    d.line((740, 500, 1150, 500), fill=(60, 60, 60), width=4)
    return im


def tabela():
    im = Image.new('RGBA', (1200, 800), (250, 250, 248)); d = ImageDraw.Draw(im); f = fonte(52)
    d.text((60, 30), 'Tabela-verdade', font=fonte(64), fill=(30, 30, 30))
    linhas = ['A  B  |  AND  OR', '0  0  |    0     0', '0  1  |    0     1', '1  0  |    0     1', '1  1  |    1     1', 'NOT:  0 -> 1    1 -> 0']
    for i, l in enumerate(linhas):
        d.text((60, 140 + i * 105), l, font=f, fill=(30, 30, 30))
    return im


def painel(G, x0, x1, y0, y1, z, bloco='gray_concrete'):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            G[(x, y, z)] = bloco


def limpar(G, x0, x1, z0, z1):
    """Tira móveis da frente da câmera, mantendo piso e teto."""
    for p in [p for p in G if x0 <= p[0] <= x1 and z0 <= p[2] <= z1 and 0 <= p[1] <= 6]:
        del G[p]


def atividades():
    import gerar_cenarios as C, render_voxel as RV
    base = {k: f()[0].G for k, f in C.CENAS.items()}
    import gerar_fachada
    fachada = dict(gerar_fachada.out)
    letreiro = Image.open(RAIZ / 'assets' / 'letreiro_donaduzzi_42x5.png')
    L = {}

    def add(nome, G, cam, alvo, modo, ov=None, f=820, npcs=()):
        G = dict(G)
        for x, z, r in npcs: RV.npc(G, x, z, r)
        L[nome] = (G, cam, alvo, modo, ov, f)

    add('m0', fachada, (30, 6, 50), (24, 7, 0), 'FORA', [(letreiro, 3, 45, 11, 16, 5)], 900, [(27, 10, 'light_blue_concrete')])
    add('t1_1', base['t1'], (11, 4.5, 26), (25, 4.2, 20), 'SALA', None, 620, [(21, 22, 'white_concrete')])
    G = dict(base['t1']); limpar(G, 4, 24, 9, 45); ov = []
    for i, txt in enumerate(('ENTRADA', 'PROCESSAMENTO', 'ARMAZENAMENTO', 'SAÍDA')):
        x = 5 + i * 5; painel(G, x, x + 3, 1, 6, 9); ov.append((quadro([(txt, 64)]), x, x + 4, 3, 7, 10))
        G[(x + 1, 2, 9)] = 'lime_concrete'; G[(x + 2, 2, 9)] = 'lime_concrete'
    add('t1_2', G, (14.5, 4, 28), (14.5, 3.6, 9), 'SALA', ov, 760, [(22, 14, 'white_concrete')])
    G = dict(base['t1']); limpar(G, 4, 24, 9, 45); ov = [(quadro([('O sistema operacional', 66), ('é um programa?', 66)]), 5, 23, 5, 8, 10), ]
    painel(G, 5, 23, 0, 7, 9, 'white_concrete')
    for x, cor in ((7, 'lime_concrete'), (16, 'red_concrete')):
        painel(G, x, x + 4, 0, 3, 9, 'black_concrete'); painel(G, x, x + 4, 4, 4, 9, cor)
    ov += [(quadro([('SIM', 80)]), 7, 12, 4, 5, 10), (quadro([('NÃO', 80)]), 16, 21, 4, 5, 10)]
    add('t1_3', G, (14.5, 4, 28), (14.5, 3.8, 9), 'SALA', ov, 760, [(22, 13, 'white_concrete')])
    add('t2_1', base['t2'], (14, 3.6, 13), (40, 3.2, 4), 'FORA', None, 620, [(22, 12, 'cyan_concrete')])
    G = dict(base['t2']); ov = []
    for x, txt in ((14, '123456'), (22, 'maria2012'), (30, 'Bloco-Azul!Rio7-Lanche')):
        painel(G, x, x + 5, 0, 5, 9, 'white_concrete'); painel(G, x + 1, x + 4, 0, 3, 9, 'black_concrete')
        ov.append((quadro([(txt, 60 if len(txt) < 12 else 46)], w=1200, h=300), x, x + 6, 4, 6, 10))
    add('t2_2', G, (25, 3.6, 18.4), (25, 3, 9), 'FORA', ov, 330, [(37, 13, 'cyan_concrete')])
    G = dict(base['t2']); ov = []
    msgs = (('Você ganhou um celular!', 'Clique em 5 minutos.', 'GOLPE', (200, 40, 40)),
            ('Calendário publicado', 'no site oficial.', 'SEGURO', (40, 150, 60)),
            ('Envie sua senha agora', 'ou perderá o perfil.', 'GOLPE', (200, 40, 40)))
    for i, (a, b, r, c) in enumerate(msgs):
        x = 14 + i * 8; painel(G, x, x + 6, 0, 5, 9, 'spruce_planks')
        ov.append((quadro([(a, 60), (b, 60), (r, 92)], w=1400, h=800, cor=(30, 30, 30)), x, x + 7, 1, 5, 10))
    add('t2_3', G, (25, 3.6, 18.4), (25, 3, 9), 'FORA', ov, 330, [(38, 13, 'cyan_concrete')])
    logo = Image.open(RAIZ / 'assets' / 'logo_faculdade_12x4.png')

    def sala(nome, img):
        G = dict(base['t3']); painel(G, 24, 40, 1, 6, 3, 'white_concrete')
        add(nome, G, (32, 4.2, 14), (32, 3.5, 3), 'SALA', [(img, 24, 41, 1, 7, 4)], 560, [(26, 6, 'magenta_concrete')])
    sala('t3_1', quadro([('Relatório da visita', 90), ('O mapa reproduz espaços reais.', 54), ('• Laboratório', 54), ('• Sala Hexagonal', 54)], t=60))
    sala('t3_2', planilha())
    sala('t3_3', quadro([('O que aprendi', 100), ('Circuitos, redes e segurança', 56), ('início  •  meio  •  fim', 50)], fundo=(255, 240, 225)))
    add('t4_1', base['t4'], (20, 3.2, 13), (19.5, 1.2, 5), 'SALA', None, 560, [(24, 7, 'orange_concrete')])
    add('t4_2', base['t4'], (20, 7, 28), (20, 5, 4), 'SALA', [(tabela(), 13, 27, 7, 17, 1)], 640, [(13, 10, 'orange_concrete')])
    G = dict(base['t4']); limpar(G, -4, 26, 14, 34)
    W = 'redstone_wire[east=side,north=none,power=0,south=none,west=side]'
    for x in range(10, 17): G[(x, 0, 20)] = W
    painel(G, 8, 9, 0, 1, 20, 'white_concrete'); painel(G, 17, 18, 0, 1, 20, 'white_concrete')
    G[(9, 1, 21)] = 'prop_botao'; G[(17, 1, 21)] = 'prop_botao'
    painel(G, 13, 14, 0, 3, 16, 'iron_block'); painel(G, 12, 15, 4, 4, 16, 'white_concrete')
    add('t4_3', G, (13.5, 5, 32), (13.5, 1.6, 17), 'SALA', None, 760, [(7, 24, 'light_blue_concrete'), (20, 24, 'lime_concrete')])
    return L


def main(texturas, saida, quais):
    os.environ['BIOPARK_TEXTURAS'] = str(Path(texturas).resolve())
    saida = Path(saida).resolve(); saida.mkdir(parents=True, exist_ok=True)
    os.chdir(tempfile.mkdtemp())   # os geradores de .schem escrevem na pasta atual
    import render_voxel as RV
    for nome, (G, cam, alvo, modo, ov, f) in atividades().items():
        if quais and nome not in quais: continue
        RV.render(G, cam, alvo, modo, str(saida / f'{nome}.jpg'), ov, f)
        print('ok', nome, flush=True)


if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
