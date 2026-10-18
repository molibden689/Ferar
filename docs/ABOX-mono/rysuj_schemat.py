import os
os.environ['MPLCONFIGDIR']='/tmp/abox-mpl'
import copy
import csv
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Polygon
from pathlib import Path

root=Path(__file__).resolve().parent
original='--oryginal' in sys.argv
reference=json.loads((root/'oryginal-polaczenia.json').read_text())
expected=copy.deepcopy(reference)
if not original:
 expected['source']='Wariant roboczy 100 W / 6 Ω, niezależnie wyprowadzony z oryginału; zmiany opisane w porownanie-z-oryginalem.md'
 expected['reference']='oryginal-polaczenia.json'
 expected['notes']=[
  'To modernizacja, nie kopia oryginału. Jawne zmiany opisano w porownanie-z-oryginalem.md.',
  'VP/VM są zewnętrznymi wejściami stabilizowanych ±40 V; nie dodano układu regulatorów. Kolektory T11/T15 korzystają z VP/VM.',
  'Jedna para końcowa, rezystory emiterowe i bazowe; kolektory T13/T17 oraz R20/R21 wracają do OUTI. Oryginał ma odrębne UP/LOW przed kolektorowymi R28/R29.',
  'R12=GND–IB2. R13=VB8–GND; wartość R13 nadal wymaga potwierdzenia. Nie zatwierdzono zamienników D4–D7.',
  'T13=2SA1930 PNP, T17=2SC5171 NPN zgodnie z wyborem użytkownika. Karta NPN potwierdza T17: 1=B, 2=C, 3=E. Karta PNP oraz dopuszczalna praca pary na gorąco pozostają do potwierdzenia.',
  'Zgodność grafu połączeń nie oznacza potwierdzenia stabilności, mocy, SOA ani bezpieczeństwa uruchomienia.'
 ]
 types={'T1':'2SC2240','T2':'2SC2240','T3':'KSC1845','T4':'KSA992','T5':'KSA992','T6':'KSA992','T7':'KSA992','T8':'2SA949','T9':'2SC2229','T10':'KSC1845','T11':'2SC2229','T12':'2SC2229','T13':'2SA1930','T15':'2SA949','T16':'2SA949','T17':'2SC5171'}
 for ref,typ in types.items():expected['components'][ref]['value']=typ
 for ref in ('R15','R16','R23','R24','R28','R29','T14','T18'):del expected['components'][ref]
 expected['components']['T11']['pins']['C']='VP'
 expected['components']['T15']['pins']['C']='VM'
 for ref in ('T13','T17'):expected['components'][ref]['pins']['C']='OUTI'
 for ref in ('R20','R21'):expected['components'][ref]['pins']['2']='OUTI'
 for upper,base,emit,rail,typ in [(True,'BU1','EP1','V+','2SA1943'),(False,'BL1','EN1','V-','2SC5200')]:
  ref='T14' if upper else 'T18'
  expected['components'][ref]={'kind':'Q','value':typ,'pins':{'B':base,'C':'OUTI','E':emit}}
  n=1 if upper else 2
  expected['components'][f'RE{n}']={'kind':'R','value':'0,22 Ω / 5 W','pins':{'1':rail if upper else emit,'2':emit if upper else rail}}
  expected['components']['RBU' if upper else 'RBL']={'kind':'R','value':'4,7 Ω','pins':{'1':'BU' if upper else 'BL','2':base}}
  expected['components']['R24' if upper else 'R23']={'kind':'R','value':'68 Ω','pins':{'1':emit if upper else base,'2':base if upper else emit}}
 expected['components']['R7']['value']='20,5 kΩ, wstępnie'
 expected['components']['R12']['value']='20,5 kΩ, wstępnie'
 expected['components']['R13']['value']='8,2 kΩ? — wartość do potwierdzenia'
prefix='oryginal' if original else 'schemat'
geometry={'segments':[],'junctions':[],'components':{},'labels':[]}
record_wires=True
def register(ref,kind,pins,value=''):
 if ref in geometry['components']:raise ValueError('Duplicate component '+ref)
 geometry['components'][ref]={'kind':kind,'pins':pins,'value':value}
def netlabel(name,point):geometry['labels'].append({'name':name,'point':point})
def value(ref,fallback):
 if original:
  overrides={'R13':'82k / 8k2 ?','T6':'BC157','T14':'TIP2955 / 2N6491','T18':'TIP3055 / 2N6488','R25':'2R49 / 0,5 W','R26':'2R49 / 0,5 W','R27':'0R62 / 2 W','C5':'47 µF / 16 V'}
  return overrides.get(ref,reference['components'][ref]['value'].split(';')[0])
 overrides={'R7':'20k5 *','R12':'20k5 *','R13':'8k2 ? *'}
 return overrides.get(ref,fallback)
fig,ax=plt.subplots(figsize=(32,16))
ax.set_xlim(-1,165);ax.set_ylim(-7,81);ax.axis('off')
col='#12243a'
def text(x,y,s,fs=8,**kw): ax.text(x,y,s,fontsize=fs,color=col,**kw)
def wire(*pts):
 ax.plot([p[0] for p in pts],[p[1] for p in pts],color=col,lw=1)
 if record_wires:
  geometry['segments'].extend([[a,b] for a,b in zip(pts,pts[1:]) if a!=b])
def dot(x,y):
 ax.add_patch(Circle((x,y),.18,color=col));geometry['junctions'].append((x,y))
def ground(x,y):
 netlabel('GND',(x,y))
 wire((x,y),(x,y-.8))
 for i,w in enumerate([1,.65,.3]):wire((x-w,y-.8-.35*i),(x+w,y-.8-.35*i))
def r(a,b,ref,val):
 val=value(ref,val)
 register(ref,'POT' if ref in ('Rc','Rd') else 'R',{'1':a,'2':b},val)
 x1,y1=a;x2,y2=b;mx=(x1+x2)/2;my=(y1+y2)/2
 if y1==y2:
  wire(a,(mx-1.4,my));wire((mx+1.4,my),b)
  ax.add_patch(Rectangle((mx-1.4,my-.45),2.8,.9,fill=False,edgecolor=col,lw=1))
  text(mx,my+1.1,ref+' '+val,7,ha='center')
 else:
  d=1 if y2>y1 else -1
  wire(a,(mx,my-d*1.4));wire((mx,my+d*1.4),b)
  ax.add_patch(Rectangle((mx-.45,my-1.4),.9,2.8,fill=False,edgecolor=col,lw=1))
  text(mx+1,my+3.5 if ref=='R14' else my,ref+'\n'+val,7,va='center')
def c(a,b,ref,val):
 val=value(ref,val);register(ref,'C',{'1':a,'2':b},val)
 x1,y1=a;x2,y2=b;mx=(x1+x2)/2;my=(y1+y2)/2
 if y1==y2:
  wire(a,(mx-.35,my));wire((mx+.35,my),b)
  wire((mx-.35,my-.9),(mx-.35,my+.9));wire((mx+.35,my-.9),(mx+.35,my+.9))
  text(mx,my+1.2,ref+' '+val,7,ha='center')
 else:
  d=1 if y2>y1 else -1
  wire(a,(mx,my-d*.35));wire((mx,my+d*.35),b)
  wire((mx-.9,my-.35),(mx+.9,my-.35));wire((mx-.9,my+.35),(mx+.9,my+.35))
  text(mx+1.1,my,ref+'\n'+val,7,va='center')
def diode(a,b,ref):
 ref=ref.split()[0]
 register(ref,'D',{'A':a,'K':b},expected['components'][ref]['value'])
 # a is anode, b is cathode.
 x1,y1=a;x2,y2=b;mx=(x1+x2)/2;my=(y1+y2)/2
 if x1==x2:
  d=1 if y2>y1 else -1
  wire(a,(mx,my-d*.7));wire((mx,my+d*.7),b)
  ax.add_patch(Polygon([(mx-.7,my-d*.7),(mx+.7,my-d*.7),(mx,my+d*.7)],fill=False,edgecolor=col))
  wire((mx-.8,my+d*.7),(mx+.8,my+d*.7));text(mx+1.2,my,ref,7,va='center')
 else:
  d=1 if x2>x1 else -1
  wire(a,(mx-d*.7,my));wire((mx+d*.7,my),b)
  ax.add_patch(Polygon([(mx-d*.7,my-.7),(mx-d*.7,my+.7),(mx+d*.7,my)],fill=False,edgecolor=col))
  wire((mx+d*.7,my-.8),(mx+d*.7,my+.8));text(mx,my+1.1,ref,7,ha='center')
def q(x,y,ref,typ,p):
 global record_wires
 typ=value(ref,expected['components'][ref]['value'])
 pins={'B':(x-2.5,y),'C':(x+1,y+3 if p=='N' else y-3),'E':(x+1,y-3 if p=='N' else y+3)}
 register(ref,'Q',pins,typ)
 record_wires=False
 # E at top for PNP; E at bottom for NPN.
 ax.add_patch(Circle((x,y),1.55,fill=False,edgecolor=col,lw=1))
 wire((x-.5,y-.8),(x-.5,y+.8));wire((x-2.5,y),(x-.5,y))
 wire((x-.5,y+.5),(x+1,y+1.2),(x+1,y+3))
 wire((x-.5,y-.5),(x+1,y-1.2),(x+1,y-3))
 if p=='N':a=(x+.05,y-.76);b=(x+.8,y-1.1)
 else:a=(x+.8,y+1.1);b=(x+.05,y+.76)
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=10,color=col,lw=1))
 tx,ty=(x+2,y+.4)
 if ref=='T3':tx,ty=x-7,y+2.3
 if ref=='T6':tx,ty=x+2,y-3
 text(tx,ty,ref+'\n'+typ,8,fontweight='bold',va='center')
 record_wires=True

text(1,78,'Radioelektronik — odtworzenie połączeń rys. 2, ±30 V' if original else 'ABOX — wariant roboczy 100 W / 6 Ω, jedna para końcowa',18,fontweight='bold')
text(1,75,'KONTROLA POŁĄCZEŃ, NIE DOKUMENTACJA WYKONAWCZA. R13 i dobór diod wymagają wyjaśnienia. Skrzyżowanie bez kropki = brak połączenia.',9)
if not original:
 text(1,73.5,'T17 2SC5171: 1=B, 2=C, 3=E wg karty. T13 2SA1930: karta do sprawdzenia. Gorące SOA, chłodzenie i kompensacja do potwierdzenia.',8)
# Main and filtered rails.
wire((1,72),(148,72));text(150,72,'+30 V' if original else '+50 V główne',11,va='center');netlabel('V+',(1,72))
wire((1,4),(148,4));text(150,4,'−30 V' if original else '−50 V główne',11,va='center');netlabel('V-',(1,4))
if original:
 r((3,72),(3,68),'R15','47 Ω');r((3,4),(3,8),'R16','47 Ω')
wire((3,68),(86 if not original else 77,68));text(5,69,'VP — filtrowane' if original else 'VP +40 V stabilizowane [zewnętrzne]',8);netlabel('VP',(3,68))
wire((3,8),(86 if not original else 77,8));text(5,9,'VM — filtrowane' if original else 'VM −40 V stabilizowane [zewnętrzne]',8);netlabel('VM',(3,8))
# Input and differential pair.
wire((0,36),(2,36));text(0,38,'IN',10)
r((2,36),(8,36),'R1','150 Ω **');c((8,36),(14,36),'C2','22 µF')
wire((14,36),(15.5,36));c((8,36),(8,30),'C1','2n2 **');ground(8,30)
r((14,36),(14,27),'R2','47 kΩ');ground(14,27)
q(18,36,'T1','2SC2240','N');q(37,36,'T2','2SC2240','N')
r((19,33),(19,27),'R3','120 Ω');r((38,33),(38,27),'R4','120 Ω')
wire((19,27),(38,27));dot(29,27);wire((29,27),(29,25))
q(28,22,'T3','KSC1845','N');r((29,19),(29,8),'R8','330 Ω');dot(29,8)
r((12,22),(23,22),'R7','25k5 / 1 W');ground(12,22);wire((23,22),(25.5,22))
diode((23,22),(23,15),'D2');diode((23,15),(23,8),'D1');dot(23,22);dot(23,8)
# Wilson mirror: literal connectivity from original.
q(18,58,'T5','KSA992','P');q(37,58,'T6','KSA992','P');q(28,48,'T4','KSA992','P')
r((19,61),(19,65),'R6','22 Ω');r((38,61),(38,65),'R5','22 Ω')
r((19,65),(38,65),'Rd','100 Ω, suwak → VP')
ax.add_patch(FancyArrowPatch((28.5,68),(28.5,65.45),arrowstyle='->',mutation_scale=9,color=col));dot(28.5,68)
geometry['components']['Rd']['pins']['W']=(28.5,68)
wire((19,55),(19,52),(29,52),(29,51));wire((15.5,58),(15,58),(15,52),(34,52),(34,58),(34.5,58))
dot(19,52);dot(29,52);text(26,53,'MIR',7)
wire((29,45),(29,43),(19,43),(19,39));text(20,41,'N1',7)
wire((38,55),(38,39));wire((25.5,48),(25,48),(25,46),(38,46));dot(38,46);text(39,45,'N2',7)
# Feedback connection, kept labelled to avoid a wire across the input circuit.
wire((34.5,36),(32,36));text(31.7,36,'FB',8,ha='right',va='center')
netlabel('FB',(32,36))
r((32,36),(32,30),'R9','2 kΩ');wire((32,30),(32,25));c((32,25),(32,19),'C5','47 µF');ground(32,19)
r((34,19),(42,19),'R10','47 kΩ');text(33,19,'FB',8,ha='right',va='center');text(43,19,'OUTI',8,va='center')
netlabel('FB',(34,19));netlabel('OUTI',(42,19))
# VAS with actual N1 wire and Miller compensation.
q(55,57,'T7','KSA992','P');q(55,49,'T8','2SA949','P')
wire((29,43),(41,43),(41,59),(51,59),(51,57),(52.5,57));dot(29,43)
diode((56,68),(56,60),'D3');dot(56,68)
wire((56,54),(56,52));wire((56,46),(64,46));text(64.3,46,'VH',8,va='center')
c((41,43),(56,43),'C6','39 pF *');wire((56,43),(56,46));dot(41,43);dot(56,46)
r((47,68),(47,46),'R14','820 Ω');wire((47,46),(47,49),(52.5,49));dot(47,68);dot(47,49)
r((44,40),(44,31),'R13','8k2 ? *');wire((44,40),(44,49),(47,49));ground(44,31)
c((41,68),(41,61),'C7','47 µF / 25 V');wire((41,61),(44,61),(44,49));dot(41,68);dot(44,49)
r((47,37),(47,22),'R12','20k5 *');wire((47,37),(50,37));ground(50,37)
q(70,22,'T9','2SC2229','N');q(64,14,'T10','KSC1845','N')
wire((47,22),(67.5,22));wire((65,17),(65,22));dot(65,22)
wire((71,19),(71,18),(60,18),(60,14),(61.5,14));dot(71,19)
r((71,19),(71,8),'R11','220 Ω');wire((65,11),(65,8));dot(65,8);dot(71,8)
c((47,22),(47,8),'C8','10 µF / 25 V');dot(47,22);dot(47,8)
# Original adjustable four-diode bias, explicitly not validated.
wire((64,46),(64,43));diode((64,43),(64,39),'D7 *');diode((64,39),(64,35),'D6 *')
diode((64,35),(64,31),'D5 *');diode((64,31),(64,27),'D4 *')
wire((64,27),(71,27),(71,25));text(71.5,27,'VL',8)
wire((64,35),(75,35));r((75,35),(75,27),'Rc','1 kΩ *');wire((75,27),(71,27));dot(64,35);dot(71,27)
geometry['components']['Rc']['pins']['W']=(78,29)
ax.add_patch(FancyArrowPatch((78,29),(75.55,31),arrowstyle='->',mutation_scale=9,color=col))
wire((78,29),(78,27),(75,27));dot(75,27)
# Buffers.
q(85,50,'T11','KSC3503','N');q(85,30,'T15','KSA1381','P')
wire((64,46),(78,46),(78,50),(82.5,50));dot(64,46)
wire((71,27),(78,27),(78,30),(82.5,30))
wire((86,53),(86,72 if original else 68));dot(86,72 if original else 68)
wire((86,27),(86,4 if original else 8));dot(86,4 if original else 8)
r((86,47),(86,40),'R18','220 Ω');r((86,40),(86,33),'R17','220 Ω')
# Compound output input transistors.
q(98,51,'T12','KSC3503','N');q(98,29,'T16','KSA1381','P')
wire((86,47),(92,47),(92,51),(95.5,51));dot(86,47)
wire((86,33),(92,33),(92,29),(95.5,29));dot(86,33)
r((99,48),(99,43 if original else 40),'R20','100 Ω')
r((99,32),(99,37 if original else 40),'R21','100 Ω')
if not original:
 wire((99,40),(147,40));dot(99,40)
else:
 wire((99,43),(127,43));wire((99,37),(127,37));wire((127,40),(147,40));dot(99,43);dot(99,37)
text(140,41,'OUTI',8);netlabel('OUTI',(140,40))
q(110,59,'T13','2SA1930','P');q(110,23,'T17','2SC5171','N')
wire((99,54),(99,59),(107.5,59));r((99,72),(99,59),'R19','1k2');dot(99,59);dot(99,72)
wire((99,26),(99,23),(107.5,23));r((99,23),(99,4),'R22','1k2');dot(99,23);dot(99,4)
# The reference keeps the separate UP / LOW nodes and collector resistors.
# The modern version is an explicitly documented topology change.
wire((111,56),(111,43 if original else 40))
wire((111,26),(111,37 if original else 40))
dot(111,43 if original else 40);dot(111,37 if original else 40)
if original:
 q(126,56,'T14','TIP2955','P');q(126,24,'T18','TIP3055','N')
 wire((111,62),(115,62),(115,56),(123.5,56))
 wire((111,20),(115,20),(115,24),(123.5,24))
 wire((127,72),(127,59));dot(127,72)
 wire((127,21),(127,4));dot(127,4)
 wire((127,53),(127,43));wire((127,27),(127,37))
 r((127,43),(127,40),'R28','0R22 / 5 W')
 r((127,37),(127,40),'R29','0R22 / 5 W')
 dot(127,43);dot(127,37);dot(127,40)
 for x,y,ref,n1,n2 in [(115,66,'R24','V+','BU'),(115,11,'R23','BL','V-')]:
  r((x-3,y),(x+3,y),ref,'68 Ω')
  text(x-3.4,y,n1,7,ha='right',va='center');text(x+3.4,y,n2,7,va='center')
  netlabel(n1,(x-3,y));netlabel(n2,(x+3,y))
 netlabel('BU',(115,62));netlabel('BL',(115,20))
else:
 q(126,56,'T14','2SA1943','P');q(126,24,'T18','2SC5200','N')
 wire((111,62),(115,62),(115,56))
 r((115,56),(121,56),'RBU','4R7 *');wire((121,56),(123.5,56))
 wire((111,20),(115,20),(115,26));r((115,26),(121,26),'RBL','4R7 *')
 wire((121,26),(121,24),(123.5,24))
 r((127,72),(127,59),'RE1','0R22 / 5 W');dot(127,72)
 wire((127,53),(127,40));dot(127,40)
 r((127,21),(127,4),'RE2','0R22 / 5 W');dot(127,4)
 wire((127,27),(127,40));dot(127,40)
 for x,y,ref,net1,net2 in [(115,66,'R24','EP1','BU1'),(115,11,'R23','BL1','EN1')]:
  r((x-3,y),(x+3,y),ref,'68 Ω');text(x-3.4,y,net1,7,ha='right',va='center');text(x+3.4,y,net2,7,va='center')
  netlabel(net1,(x-3,y));netlabel(net2,(x+3,y))
 for name,pt in [('EP1',(127,59)),('EN1',(127,21)),('BU1',(123.5,56)),('BL1',(123.5,24))]:
  netlabel(name,pt)
 text(127.5,59,'EP1',7);text(127.5,21,'EN1',7)
 text(121,57,'BU1',7);text(121,22,'BL1',7)
# Output filter and Zobel.
register('L1','L',{'1':(150,40),'2':(156.8,40)},'5 µH')
wire((147,40),(150,40))
for i in range(4):
 import numpy as np
 t=np.linspace(0,3.14159265,40);xx=150+i*1.7+1.7*t/3.14159265;yy=40+0.9*np.sin(t);ax.plot(xx,yy,color=col,lw=1)
wire((156.8,40),(163,40));text(154,38,'L1 5 µH' if original else 'L1 5 µH / ≥12 A *',7,ha='center');text(160,42,'OUT',11)
r((149,45),(158,45),'R27','0R62 / 5 W');wire((149,45),(149,40));wire((158,45),(158,40));dot(149,40);dot(158,40)
r((149,40),(149,33),'R26','2R49 / 2 W');r((149,33),(149,26),'R25','2R49 / 2 W');c((149,26),(149,18),'C9','220 nF / 250 V');ground(149,18)
text(159,36,'głośnik\n8 Ω' if original else 'głośnik\n6 Ω — cel',9);ground(163,30);wire((163,30),(163,32))
# Local bypass capacitors, connected by rail labels to keep readability.
for x,ref,top,bottom in [(11,'C3','VP','GND'),(48,'C4','GND','VM'),(84,'C10','V+','GND'),(121,'C11','GND','V−')]:
 c((x,-1),(x+9,-1),ref,'470 µF / 100 V');text(x-.5,-1,top,8,ha='right',va='center');text(x+9.5,-1,bottom,8,va='center')
 netlabel(top.replace('−','-'),(x,-1));netlabel(bottom.replace('−','-'),(x+9,-1))
text(1,-5,'R13: skan 82k / 8k2 — wartość niezatwierdzona. D1–D3: BAYP95; D6/D7: BAP811 wg skanu; D4/D5: typ do ustalenia. Nie zastępować automatycznie przez 1N4148.',8)
for ext in ['svg','pdf','png']:fig.savefig(root/f'{prefix}.{ext}',dpi=160,bbox_inches='tight')
svg_path=root/f'{prefix}.svg'
svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines())+'\n')
(root/f'{prefix}-geometria.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2)+'\n')
if not original:
 (root/'polaczenia.json').write_text(json.dumps(expected,ensure_ascii=False,indent=2)+'\n')
csv_path=root/('oryginal-tranzystory.csv' if original else 'tranzystory.csv')
with csv_path.open('w',newline='') as stream:
 writer=csv.writer(stream,lineterminator='\n')
 writer.writerow(['oznaczenie','typ','polaryzacja','baza','kolektor','emiter'])
 for ref,component in expected['components'].items():
  if component['kind']=='Q':
   name=component['value'].split(';')[0]
   pnp=ref in ('T4','T5','T6','T7','T8','T13','T14','T15','T16')
   writer.writerow([ref,name,'PNP' if pnp else 'NPN',component['pins']['B'],component['pins']['C'],component['pins']['E']])
