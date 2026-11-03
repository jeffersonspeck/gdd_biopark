# Zonas das trilhas modeladas a partir das fotos reais. Gera um .schem por zona.
import gzip, struct, os
OUT=os.getcwd()
class Cena:
    def __init__(s): s.G={}
    def box(s,b,x0,x1,y0,y1,z0,z1):
        for x in range(x0,x1+1):
            for y in range(y0,y1+1):
                for z in range(z0,z1+1): s.G[(x,y,z)]=b
    def set(s,b,x,y,z): s.G[(x,y,z)]=b
POST='iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]'
FENCE='dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]'
LAMP='sea_lantern'; SEAT='polished_blackstone_slab[type=bottom,waterlogged=false]'
TOPW='smooth_quartz_slab[type=top,waterlogged=false]'
def salvar(c,nome):
    G=c.G
    xs=[p[0] for p in G]; ys=[p[1] for p in G]; zs=[p[2] for p in G]
    x0,x1,y0,y1,z0,z1=min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
    W,H,L=x1-x0+1,y1-y0+1,z1-z0+1
    pal={'minecraft:air':0}; data=bytearray()
    for y in range(y0,y1+1):
        for z in range(z0,z1+1):
            for x in range(x0,x1+1):
                b=G.get((x,y,z)); k='minecraft:'+b if b else 'minecraft:air'
                i=pal.setdefault(k,len(pal))
                while i>=128: data.append((i&127)|128); i>>=7
                data.append(i)
    def s(t): e=t.encode(); return struct.pack('>H',len(e))+e
    def tag(t,n,v): return bytes([t])+s(n)+v
    pb=b''.join(tag(3,k,struct.pack('>i',v)) for k,v in pal.items())+b'\0'
    meta=tag(3,'WEOffsetX',struct.pack('>i',0))+tag(3,'WEOffsetY',struct.pack('>i',0))+tag(3,'WEOffsetZ',struct.pack('>i',0))+b'\0'
    body=(tag(3,'Version',struct.pack('>i',2))+tag(3,'DataVersion',struct.pack('>i',3955))
     +tag(2,'Width',struct.pack('>h',W))+tag(2,'Height',struct.pack('>h',H))+tag(2,'Length',struct.pack('>h',L))
     +tag(11,'Offset',struct.pack('>iiii',3,0,0,0))+tag(3,'PaletteMax',struct.pack('>i',len(pal)))
     +tag(10,'Palette',pb)+tag(7,'BlockData',struct.pack('>i',len(data))+bytes(data))+tag(10,'Metadata',meta)+b'\0')
    open(os.path.join(OUT,nome+'.schem'),'wb').write(gzip.compress(tag(10,'Schematic',body)))
    print(nome,W,H,L,len(G),len(pal))
def teto(c,x0,x1,z0,z1,h,piso,dx=8,dz=7):
    c.box(piso,x0,x1,-1,-1,z0,z1); c.box('white_concrete',x0,x1,h,h,z0,z1)
    for x in range(x0+3,x1-2,dx):
        for z in range(z0+3,z1-2,dz): c.box(LAMP,x,x+2,h,h,z,z+2)
def cadeira(c,x,z,dx,dz):
    c.set(FENCE,x,0,z); c.set(SEAT,x,1,z)
    c.set(FENCE,x+dx,1,z+dz); c.set(SEAT,x+dx,2,z+dz)

# ---- T1 Laboratorio de Hardware (foto: parede geometrica ao fundo, laranja a direita, quadro a esquerda)
def t1():
    c=Cena(); X,Z,H=26,50,8
    teto(c,0,X,0,Z,H,'polished_andesite')
    c.box('white_concrete',0,0,0,H-1,0,Z); c.box('orange_concrete',X,X,0,H-1,0,Z); c.box('white_concrete',0,X,0,H-1,Z,Z)
    for x in range(0,X+1):
        u=x/X
        for y in range(0,H):
            v=y/(H-1)
            if v>.62 and u<.48: b='green_concrete'
            elif v>.55 and u>=.48: b='blue_concrete'
            elif u<.18+.1*v or u>.72+.1*(1-v): b='orange_concrete'
            else: b='yellow_concrete'
            c.set(b,x,y,0)
    c.box('blue_concrete',1,3,0,H-1,6,9)                 # coluna azul
    c.box('black_concrete',4,10,0,3,1,1); c.box('gray_concrete',5,9,1,3,1,1)  # armario escuro
    c.box('black_concrete',0,0,2,5,24,40)                # quadro
    c.box('white_concrete',0,0,1,1,24,40)
    c.box('spruce_planks',X-1,X-1,0,1,2,Z-1); c.box('black_concrete',X-1,X-1,2,2,2,Z-1)  # armario e bancada
    for z0 in (10,18,26,34):
        c.box('white_concrete',11,11,0,1,z0,z0+3); c.box('white_concrete',17,17,0,1,z0,z0+3); c.box(TOPW,11,17,1,1,z0,z0+3)
        c.box('white_concrete',11,17,2,2,z0,z0+3) if False else None
        for x in (12,14,16):
            c.set(POST,x,0,z0+5); c.set(SEAT,x,1,z0+5)
        c.box(POST,14,14,2,H-1,z0+1,z0+1)
    # pecas gigantes do computador, na parede direita (y 3 a 7)
    c.box('green_concrete',X-1,X-1,3,7,12,16); c.box('black_concrete',X-1,X-1,4,6,13,15); c.box('gold_block',X-1,X-1,5,5,14,14)  # CPU
    c.box('green_concrete',X-1,X-1,4,6,19,25); c.box('gold_block',X-1,X-1,3,3,19,25)
    for z in (20,22,24): c.set('black_concrete',X-1,5,z)                                                                          # RAM
    c.box('gray_concrete',X-1,X-1,3,6,28,31); c.box('light_blue_concrete',X-1,X-1,4,5,29,30)                                       # SSD
    c.box('black_concrete',X-1,X-1,3,7,34,40); c.box('light_blue_concrete',X-1,X-1,4,6,35,39)                                      # monitor
    salvar(c,'trilha_t1_lab_hardware')
    return c,([3,4.2,49],[15,2.6,0]),'SALA',760

# ---- T2 Rua das Redes (foto lateral: ala amarela e branca, bancos, palmeiras, passarela de postes pretos)
def t2():
    c=Cena(); X0,X,Z=-6,76,34
    c.box('grass_block[snowy=false]',X0,X,-1,-1,-2,Z)
    c.box('terracotta',X0,X,-1,-1,11,16); c.box('blue_concrete',X0,X,-1,-1,13,14)
    c.box('terracotta',X0,X,-1,-1,23,27)
    c.box('yellow_concrete',X0,54,0,7,0,0); c.box('white_concrete',X0,54,8,13,0,0); c.box('white_concrete',X0,54,14,14,-2,0)
    # portal branco inclinado com letreiro
    for y in range(0,18):
        f=8+(4*y)//17; c.box('white_concrete',55,58,y,y,0,f); c.box('white_concrete',72,75,y,y,0,f)
    c.box('white_concrete',55,75,17,17,0,12); c.box('blue_concrete',59,71,11,15,9,9); c.box('white_concrete',59,71,8,10,0,8)
    c.box('blue_concrete',59,71,7,7,8,8); c.box('yellow_concrete',59,71,0,6,2,2)
    # passarela coberta
    for x in range(8,X,6):
        c.box(FENCE,x,x,0,6,20,20); c.box(FENCE,x,x,0,6,29,29)
    c.box('polished_blackstone_slab[type=top,waterlogged=false]',6,X,6,6,19,30)
    # cobertura metalica ate a entrada
    c.box('smooth_stone_slab[type=bottom,waterlogged=false]',60,66,5,5,9,19)
    # bancos e palmeiras
    for x,z in ((4,8),(9,9),(16,7),(36,8),(43,9)):
        c.box('polished_andesite_slab[type=top,waterlogged=false]',x,x+2,0,0,z,z); c.set('polished_andesite',x,0,z); c.set('polished_andesite',x+2,0,z)
    for x,z in ((2,5),(22,6),(30,7),(48,6),(52,8)):
        c.set('stripped_spruce_log[axis=y]',x,0,z)
        for dx,dz,y in ((0,0,1),(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,1),(-1,-1,1),(1,-1,1),(-1,1,1),(0,0,2)):
            c.set('azalea_leaves[distance=1,persistent=true,waterlogged=false]',x+dx,y,z+dz)
    # estacoes (voltadas para quem vem pela calcada)
    c.box('black_concrete',12,12,2,6,2,7); c.box('light_blue_concrete',12,12,3,5,3,6); c.box('gray_concrete',12,12,0,1,4,5)          # computador
    c.box('white_concrete',27,27,0,2,2,7); c.set('lime_concrete',27,1,3); c.set('lime_concrete',27,1,5); c.box('black_concrete',27,27,3,6,2,2); c.box('black_concrete',27,27,3,6,7,7)  # roteador
    c.box('black_concrete',42,42,0,8,2,7)
    for y in (1,3,5,7):
        c.box('gray_concrete',42,42,y,y,3,6); c.set('lime_concrete',42,y,3); c.set(LAMP,42,y,6)                                       # servidor
    salvar(c,'trilha_t2_rua_redes')
    return c,([-5,4.5,17],[60,5,4]),'FORA',720

# ---- T3 Sala Hexagonal (foto: parede bordo ao fundo, janelas a esquerda, visor a direita)
def hexmesa(c,cx,cz):
    for dx in range(-7,8):
        for dz in range(-4,5):
            m=abs(dx)+abs(dz)*.8
            if m<=7 and not (abs(dx)+abs(dz)*.8<=3.4 and abs(dz)<=1):
                c.set(TOPW,cx+dx,1,cz+dz)
    for dx,dz in ((-6,0),(6,0),(-3,-4),(3,-4),(-3,4),(3,4)):
        c.set(FENCE,cx+dx,0,cz+dz); c.set(FENCE,cx+dx,1,cz+dz) if False else None
    for dx,dz,ax,az in ((-9,0,-1,0),(9,0,1,0),(-3,-6,0,-1),(3,-6,0,-1),(-3,6,0,1),(3,6,0,1)):
        cadeira(c,cx+dx,cz+dz,ax,az)
def t3():
    c=Cena(); X,Z,H=46,38,8
    teto(c,0,X,0,Z,H,'polished_diorite',dx=9,dz=8)
    c.box('red_concrete',0,X,0,H-1,0,0)
    c.box('white_concrete',0,0,0,H-1,0,Z); c.box('white_concrete',X,X,0,H-1,0,Z); c.box('white_concrete',0,X,0,H-1,Z,Z)
    c.box('red_concrete',X,X,0,2,0,Z)
    for z in range(2,Z-1):
        if z%5: c.box('glass',0,0,3,6,z,z)
    for z in (6,16,26): c.box('white_concrete',1,2,0,H-1,z,z); c.box('red_concrete',1,2,0,1,z,z)
    c.box('white_concrete',X,X,3,6,6,20); c.box('glass',X,X,4,5,7,19)
    # paineis: texto, planilha, slides
    c.box('white_concrete',3,6,2,5,1,1); c.box('gray_concrete',4,5,5,5,1,1); c.box('light_gray_concrete',4,5,3,3,1,1)
    c.box('white_concrete',8,11,2,5,1,1); c.set('lime_concrete',9,3,1); c.set('lime_concrete',10,4,1); c.set('light_gray_concrete',9,4,1); c.set('light_gray_concrete',10,3,1)
    c.box('white_concrete',13,16,2,5,1,1); c.box('orange_concrete',14,15,4,5,1,1); c.box('light_gray_concrete',14,15,2,2,1,1)
    hexmesa(c,14,25); hexmesa(c,14,12) ; hexmesa(c,33,17)
    salvar(c,'trilha_t3_sala_hexagonal')
    return c,([38,5,37],[17,2.2,2]),'SALA',700

# ---- T4 Painel (foto: laboratorio com parede azul, laranja, colunas amarelas e mesas de madeira)
def t4():
    from gerar_painel import G
    c=Cena()
    c.G.update(G); X0,X1,Z,H=-10,50,52,24
    teto(c,X0,X1,-2,Z,H,'polished_andesite',dx=9,dz=8)
    c.box('blue_concrete',X0,X0,0,H,-2,Z); c.box('orange_concrete',X1,X1,0,H,-2,Z)
    c.box('white_concrete',X0,X1,0,H,-2,-2); c.box('white_concrete',X0,X1,0,H,Z,Z)
    c.box('yellow_concrete',X0+1,X0+4,0,H-1,-1,2); c.box('yellow_concrete',X1-4,X1-1,0,H-1,-1,2)
    # estante e mesas de madeira, como na foto
    c.box('spruce_planks',X1-1,X1-1,0,8,8,20)
    for y in (2,5): c.box('dark_oak_planks',X1-1,X1-1,y,y,9,19)
    for x0,x1 in ((-6,14),(26,46)):
        for z0 in (24,36):
            c.box('spruce_planks',x0,x0,0,1,z0,z0+5); c.box('spruce_planks',x1,x1,0,1,z0,z0+5)
            c.box('oak_slab[type=top,waterlogged=false]',x0,x1,1,1,z0,z0+5)
            for x in range(x0+2,x1-1,4): cadeira(c,x,z0-2,0,-1)
    salvar(c,'trilha_t4_painel')
    return c,([20,8,51],[20,7.5,0]),'SALA',860
CENAS=dict(t1=t1,t2=t2,t3=t3,t4=t4)
NPCS=dict(t1=[(21,22)],t2=[(20,12)],t3=[(25,27)],t4=[(16,9)])
ROUPA=dict(t1='white_concrete',t2='cyan_concrete',t3='magenta_concrete',t4='orange_concrete')
if __name__=='__main__':
    for k,f in CENAS.items(): f()
