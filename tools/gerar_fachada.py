# Fachada Colegio Donaduzzi - 1 bloco ~ 0,6 m. x -> direita, y -> cima, z -> frente (fachada olha p/ +z = sul)
# Medidas ajustadas pela foto: portal 48 x 18, profundidade 4 (chao) a 6 (topo), alas com 14 de altura.
import gzip, struct
G={}
def box(b,x0,x1,y0,y1,z0,z1):
    for x in range(x0,x1+1):
        for y in range(y0,y1+1):
            for z in range(z0,z1+1):
                G[(x,y,z)]=b
WH='white_concrete'; BL='blue_concrete'; YE='yellow_concrete'; SO='light_gray_concrete'
LV='smooth_stone_slab[type=double,waterlogged=false]'; FLOOR='gray_concrete'
GLW='light_gray_stained_glass_pane'; DG='black_stained_glass_pane'; DK='black_concrete'
XMIN,XMAX,ZMIN,ZMAX=-46,76,-10,24
box('grass_block[snowy=false]',XMIN,XMAX,-1,-1,ZMIN,ZMAX)
box('terracotta',XMIN,XMAX,-1,-1,14,17)           # calcada de concreto vermelho
box('terracotta',26,31,-1,-1,5,13)                # acesso a entrada
box(FLOOR,3,44,-1,-1,-4,4)
def front(y): return 4+(3*y)//17                  # pilar inclinado: z=4 no chao, z=6 no topo
# ---- alas e fundo (atras do plano z=0)
def wing(x0,x1,back=-9):
    box(YE,x0,x1,0,7,0,0); box(WH,x0,x1,8,13,0,0)
    box(WH,x0,x1,14,14,back,0); box(WH,x0,x1,0,13,back,back)
    for x in (x0,x1): box(WH,x,x,0,13,back,0)
    box(WH,x0,x1,4,5,0,0)
    for x in range(x0+1,x1):
        if (x-x0)%4: box(GLW,x,x,4,5,0,0)
    box(DK,x0+1,x1-1,4,5,-1,-1)
wing(48,76); wing(-27,-1)
box(WH,3,44,14,14,-9,-1); box(WH,0,47,0,17,-9,-9); box(WH,0,47,17,17,-9,0)
# ---- pilares (3 de largura, inclinados em profundidade) e viga superior
for y in range(0,17):
    f=front(y); box(WH,0,2,y,y,-9,f); box(WH,45,47,y,y,-9,f)
box(WH,0,47,17,17,0,6)
for xr in ((-1,3),(44,48)):
    box('smooth_quartz_slab[type=bottom,waterlogged=false]',xr[0],xr[1],0,0,5,5)
# ---- letreiro, faixa branca, marquise
box(WH,3,44,8,16,-3,3)
box(BL,3,44,11,15,4,4)
box(SO,3,44,16,16,4,4)
box(BL,3,44,7,7,3,3); box(SO,3,44,7,7,-4,2)
# ---- parede A (janelas) z=0, retorno x=12, parede das portas z=-4
box(YE,3,12,0,6,-4,0)
box(WH,3,12,4,5,0,0)
for x in (4,5,7,8,10,11): box(GLW,x,x,4,5,0,0)
box(DK,4,11,4,5,-1,-1)
box(YE,13,44,0,6,-4,-4)
box(LV,13,44,5,6,-4,-4)
box('yellow_terracotta',13,18,0,3,-5,-5); box(DK,19,33,0,3,-5,-5); box(DK,37,40,0,4,-5,-5)
box(WH,13,18,0,3,-4,-4)
for x in (14,16,17): box('yellow_stained_glass_pane',x,x,0,3,-4,-4)
box(WH,19,33,0,3,-4,-4)
for x in (20,21,23,24,25,27,28,30,31,32): box(DG,x,x,0,3,-4,-4)
box(WH,37,40,0,4,-4,-4)
for x in (38,39): box(GLW,x,x,0,3,-4,-4)
# porta lateral da ala esquerda
box(WH,-18,-14,0,3,0,0)
for x in (-17,-16,-15): box(DG,x,x,0,3,0,0)
box(DK,-17,-15,0,3,-1,-1)
# ---- torre: coluna branca, caixa de vidro azul, laje
box(WH,-35,-28,0,15,-3,5)
box('blue_stained_glass',-43,-36,9,15,0,6)
box(WH,-44,-28,16,16,-3,7)
# ---- arvores jovens (tronco fino, copa rala), bancos e palmeiras
def tree(x,z,h=7):
    for y in range(0,h): G[(x,y,z)]='spruce_fence'
    for y in range(h-2,h+3):
        for dx in range(-3,4):
            for dz in range(-3,4):
                if abs(dx)+abs(dz)+abs(y-h)*1.2<=3.2 and (dx*7+dz*11+y*13)%5>1:
                    G.setdefault((x+dx,y,z+dz),'oak_leaves[distance=1,persistent=true,waterlogged=false]')
for x,z in [(46,9),(58,9),(5,7),(-9,6),(-25,12)]: tree(x,z)
def bench(x,z):
    box('polished_andesite_slab[type=top,waterlogged=false]',x,x+2,0,0,z,z)
    for xx in (x,x+2): G[(xx,0,z)]='polished_andesite'
bench(-9,10); bench(-5,12); bench(-14,12)
def palm(x,z):
    G[(x,0,z)]='stripped_spruce_log[axis=y]'
    for d in [(0,0,1),(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(0,0,2)]:
        G.setdefault((x+d[0],d[2],z+d[1]),'azalea_leaves[distance=1,persistent=true,waterlogged=false]')
for x,z in [(-3,8),(8,9),(16,10),(22,10),(-17,8)]: palm(x,z)
# ---- conexoes de painel de vidro / cerca
def solid(p):
    b=G.get(p); return b is not None and not b.startswith(('spruce_fence','oak_leaves','azalea'))
out={}
for p,b in G.items():
    if b.endswith('_pane'):
        x,y,z=p; e=solid((x+1,y,z)); w=solid((x-1,y,z))
        b=f'{b}[east={str(e).lower()},north=false,south=false,waterlogged=false,west={str(w).lower()}]'
    elif b=='spruce_fence':
        b='spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]'
    out[p]=b
xs=[p[0] for p in out]; ys=[p[1] for p in out]; zs=[p[2] for p in out]
x0,x1,y0,y1,z0,z1=min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
W,H,L=x1-x0+1,y1-y0+1,z1-z0+1
pal={'minecraft:air':0}; data=bytearray()
for y in range(y0,y1+1):
    for z in range(z0,z1+1):
        for x in range(x0,x1+1):
            b=out.get((x,y,z)); k='minecraft:'+b if b else 'minecraft:air'
            i=pal.setdefault(k,len(pal))
            while i>=128: data.append((i&127)|128); i>>=7
            data.append(i)
# NBT minimo - Sponge Schematic v2
def s(t): e=t.encode(); return struct.pack('>H',len(e))+e
def tag(t,n,v): return bytes([t])+s(n)+v
pb=b''.join(tag(3,k,struct.pack('>i',v)) for k,v in pal.items())+b'\0'
meta=tag(3,'WEOffsetX',struct.pack('>i',0))+tag(3,'WEOffsetY',struct.pack('>i',0))+tag(3,'WEOffsetZ',struct.pack('>i',0))+b'\0'
body=(tag(3,'Version',struct.pack('>i',2))+tag(3,'DataVersion',struct.pack('>i',3955))
 +tag(2,'Width',struct.pack('>h',W))+tag(2,'Height',struct.pack('>h',H))+tag(2,'Length',struct.pack('>h',L))
 +tag(11,'Offset',struct.pack('>iiii',3,0,0,0))
 +tag(3,'PaletteMax',struct.pack('>i',len(pal)))
 +tag(10,'Palette',pb)+tag(7,'BlockData',struct.pack('>i',len(data))+bytes(data))+tag(10,'Metadata',meta)+b'\0')
open('fachada_colegio_donaduzzi.schem','wb').write(gzip.compress(tag(10,'Schematic',body)))
print('dims',W,H,L,'blocos',len(out),'paleta',len(pal))
