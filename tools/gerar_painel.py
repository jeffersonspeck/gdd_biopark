# Painel gigante de circuitos (40 x 18) + 3 bancadas de portas logicas funcionais (AND, OR, NOT)
import gzip, struct, random
G={}
def box(b,x0,x1,y0,y1,z0,z1):
    for x in range(x0,x1+1):
        for y in range(y0,y1+1):
            for z in range(z0,z1+1):
                G[(x,y,z)]=b
random.seed(26)
box('polished_andesite',-3,42,-1,-1,-2,11)
box('gray_concrete',-1,40,0,18,-1,-1)
box('green_concrete',0,39,0,17,0,0)
box('black_concrete',-1,40,18,18,0,0); box('black_concrete',-1,-1,0,17,0,0); box('black_concrete',40,40,0,17,0,0)
TR='gold_block'
chips=[(3,3,5,3),(13,2,6,3),(26,3,5,3),(33,6,4,3),(5,9,6,4),(17,7,7,5),(29,11,6,3),(3,14,5,2),(14,14,6,2),(25,14,4,2)]
centers=[(x+w//2,y+h//2) for x,y,w,h in chips]
def route(a,b):
    (x0,y0),(x1,y1)=a,b
    for x in range(min(x0,x1),max(x0,x1)+1): G[(x,y0,0)]=TR
    for y in range(min(y0,y1),max(y0,y1)+1): G[(x1,y,0)]=TR
for a,b in [(0,1),(1,2),(2,3),(0,4),(1,5),(2,5),(3,6),(4,5),(5,6),(4,7),(5,8),(6,9),(7,8),(8,9)]:
    route(centers[a],centers[b])
for x,y,w,h in chips:
    box('black_concrete',x,x+w-1,y,y+h-1,0,0)
    for i in range(x,x+w,2):
        for yy in (y-1,y+h):
            if 0<=yy<=17: G[(i,yy,0)]='iron_block'
    G[(x+w-1,y+h-1,0)]='sea_lantern'
for _ in range(26):
    x,y=random.randrange(1,39),random.randrange(1,17)
    if G[(x,y,0)]=='green_concrete': G[(x,y,0)]=random.choice(['sea_lantern','redstone_block','lime_concrete','iron_block'])
W='white_concrete'; LAMP='redstone_lamp[lit=false]'
LEV='lever[face=wall,facing=south,powered=false]'
def wire(e='none',w='none',n='none',s='none',p=0): return f'redstone_wire[east={e},north={n},power={p},south={s},west={w}]'
# --- AND
a=4; base='yellow_concrete'
box(base,a,a+2,0,0,6,6); G[(a,0,7)]=LEV; G[(a+2,0,7)]=LEV
G[(a,1,6)]='redstone_torch[lit=true]'; G[(a+2,1,6)]='redstone_torch[lit=true]'
G[(a+1,1,6)]=wire(e='side',w='side',n='side',p=15)
G[(a+1,1,5)]=W; G[(a+1,1,4)]='redstone_wall_torch[facing=north,lit=false]'; G[(a+1,2,4)]=LAMP
# --- OR
b=18; base='light_blue_concrete'
G[(b,0,6)]=base; G[(b+2,0,6)]=base; G[(b,0,7)]=LEV; G[(b+2,0,7)]=LEV
G[(b,0,5)]=wire(e='side'); G[(b+2,0,5)]=wire(w='side'); G[(b+1,0,5)]=wire(e='side',w='side',n='side'); G[(b+1,0,4)]=LAMP
# --- NOT
c=32; base='red_concrete'
G[(c,0,6)]=base; G[(c,0,7)]=LEV; G[(c,0,5)]='redstone_wall_torch[facing=north,lit=true]'; G[(c,1,5)]='redstone_lamp[lit=true]'
xs=[p[0] for p in G]; ys=[p[1] for p in G]; zs=[p[2] for p in G]
x0,x1,y0,y1,z0,z1=min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
Wd,H,L=x1-x0+1,y1-y0+1,z1-z0+1
pal={'minecraft:air':0}; data=bytearray()
for y in range(y0,y1+1):
    for z in range(z0,z1+1):
        for x in range(x0,x1+1):
            b_=G.get((x,y,z)); k='minecraft:'+b_ if b_ else 'minecraft:air'
            i=pal.setdefault(k,len(pal))
            while i>=128: data.append((i&127)|128); i>>=7
            data.append(i)
def s(t): e=t.encode(); return struct.pack('>H',len(e))+e
def tag(t,n,v): return bytes([t])+s(n)+v
pb=b''.join(tag(3,k,struct.pack('>i',v)) for k,v in pal.items())+b'\0'
meta=tag(3,'WEOffsetX',struct.pack('>i',0))+tag(3,'WEOffsetY',struct.pack('>i',0))+tag(3,'WEOffsetZ',struct.pack('>i',0))+b'\0'
body=(tag(3,'Version',struct.pack('>i',2))+tag(3,'DataVersion',struct.pack('>i',3955))
 +tag(2,'Width',struct.pack('>h',Wd))+tag(2,'Height',struct.pack('>h',H))+tag(2,'Length',struct.pack('>h',L))
 +tag(11,'Offset',struct.pack('>iiii',3,0,0,0))+tag(3,'PaletteMax',struct.pack('>i',len(pal)))
 +tag(10,'Palette',pb)+tag(7,'BlockData',struct.pack('>i',len(data))+bytes(data))+tag(10,'Metadata',meta)+b'\0')
open('painel_circuitos.schem','wb').write(gzip.compress(tag(10,'Schematic',body)))
print('dims',Wd,H,L,'blocos',len(G),'paleta',len(pal))
