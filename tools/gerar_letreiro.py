from PIL import Image, ImageDraw, ImageFont
SS=3; W,H=5376*SS,640*SS
BG=(28,61,150); WT=(243,243,240); YL=(231,170,20)
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
F='C:/Windows/Fonts/ARLRDBD.TTF'  # Arial Rounded Bold; troque se usar outro sistema
# posicoes medidas na foto retificada (fracao do painel)
fx=lambda f:int(f*W); fy=lambda f:int(f*H)
tf=ImageFont.truetype(F,fy(.9))
txt='Donaduzzi'; bb=d.textbbox((0,0),txt,font=tf); tw=bb[2]-bb[0]; th=bb[3]-bb[1]
lay=Image.new('L',(tw+20,th+20),0); ImageDraw.Draw(lay).text((-bb[0]+10,-bb[1]+10),txt,font=tf,fill=255)
lay=lay.resize((fx(.851)-fx(.353),fy(.92)-fy(.24)),Image.LANCZOS)
im.paste(WT,(fx(.353),fy(.24)),lay)
cf=ImageFont.truetype(F,fy(.17)); d.text((fx(.462),fy(.045)),'C O L \u00c9 G I O',font=cf,fill=(220,222,225))
# simbolo: anel com metade esquerda amarela, metade direita branca e traco central
cx,cy,R=fx(.274),fy(.56),fy(.36); t=int(R*.34)
d.arc((cx-R,cy-R,cx+R,cy+R),90,270,fill=YL,width=t)
d.arc((cx-R,cy-R,cx+R,cy+R),270,90,fill=WT,width=t)
d.rounded_rectangle((cx-int(R*.42),cy-int(R*.15),cx+int(R*.60),cy+int(R*.15)),radius=int(R*.06),fill=WT)
im=im.resize((5376,640),Image.LANCZOS); im.save('letreiro_donaduzzi_42x5.png')
