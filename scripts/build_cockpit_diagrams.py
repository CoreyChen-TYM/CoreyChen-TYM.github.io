"""Rebuild English SVG versions of the cockpit article's original block diagrams."""
from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).resolve().parents[1] / 'articles/cockpit-audio-hardware/images'
BLUE = '#527bda'
PALE = '#e6edff'

class SVG:
    def __init__(self, width, height, title):
        self.width, self.height = width, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title><rect width="100%" height="100%" fill="white"/><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto-start-reverse"><path d="M1 1L7 4.5L1 8" fill="none" stroke="#8c96a4" stroke-width="1.5"/></marker></defs><g font-family="Arial, sans-serif" fill="#1e2530">']
    def box(self,x,y,w,h,label='',fill=PALE,stroke=BLUE,size=19):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        if label:self.text(x+w/2,y+h/2+6,label,size,'middle')
    def text(self,x,y,text,size=18,anchor='start',weight='normal',color='#1e2530'):
        lines=text.split('\n')
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">')
        for i,line in enumerate(lines):self.parts.append(f'<tspan x="{x}" dy="{0 if i==0 else size*1.35}">{escape(line)}</tspan>')
        self.parts.append('</text>')
    def wire(self,points,label='',x=0,y=0,digital=False,both=False,arrow=True,color='#8c96a4'):
        pts=' '.join(f'{a},{b}' for a,b in points)
        extra=(' stroke-dasharray="3 6"' if digital else '')+(' marker-end="url(#arrow)"' if arrow else '')+(' marker-start="url(#arrow)"' if both else '')
        self.parts.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.2"{extra}/>')
        if label:self.text(x,y,label,16)
    def port(self,x,y,name):self.box(x,y,40,30,name,'#fff36b','#39404c',14)
    def save(self,name):
        self.parts.append('</g></svg>');ROOT.mkdir(parents=True,exist_ok=True);(ROOT/name).write_text(''.join(self.parts),encoding='utf-8')

def head(s,mode):
    s.box(25,150,1090,1140,'','white')
    s.text(42,180,'Head unit',24,weight='bold')
    s.box(70,245,390,700,'')
    s.text(85,275,'Main SoC: Qualcomm SA8295',21,weight='bold')
    s.box(85,300,360,335,'','#ffffce','#d4c947')
    s.text(100,330,'Multiple CPU cores',20,weight='bold')
    s.text(110,370,'Android',21,weight='bold')
    s.text(110,400,'Graphical interfaces: navigation,\nQQ Music, and so on—much like\na smartphone.',17)
    s.wire([(90,475),(440,475)],digital=True,arrow=False,color='#80b651')
    s.text(110,505,'QNX',21,weight='bold')
    s.text(110,535,'Android runs as a virtual machine\non QNX. QNX handles tasks that\nmust not crash: vehicle communication,\nreversing camera, warning sounds, etc.\nBasic vehicle functions remain available\neven if Android crashes.',14)
    for x,label,fill,stroke in [(85,'gDSP','#e0f4df','#7eb76b'),(205,'cDSP','#fae6e5','#dc8c85'),(325,'aDSP','#fff0da','#dda658')]:s.box(x,645,120,280,label,fill,stroke,21)
    s.box(70,1090,170,80,'MCU')
    s.wire([(145,945),(145,1085)],'SPI: internal communication',165,1025,both=True)
    s.box(720,175,170,80,'BT / Wi-Fi')
    s.box(720,30,170,70,'Owner’s phone')
    s.wire([(805,100),(805,175)],'Antenna',820,140,digital=True,arrow=False,color='#333')
    s.wire([(460,385),(520,385),(520,215),(715,215)],'UART: Bluetooth music\nand information to the\nAndroid Bluetooth stack',495,167,both=True)
    s.wire([(460,700),(545,700),(545,275),(750,275),(750,260)],'I2S: Bluetooth call uplink / downlink',550,310,both=True)
    s.box(720,370,170,90,'ADC')
    s.wire([(715,415),(590,415),(590,735),(465,735)],'TDM8\n5-seat: first 4 slots active\n7-seat: first 6 slots active',620,495)
    for i,t in enumerate(['Driver analog mic','Passenger analog mic','Second-row left mic','Second-row right mic']):
        y=383+i*20;s.wire([(890,y),(940,y)],arrow=False,color='#242424');s.text(950,y+5,t,14)
    if mode=='internal':
        s.box(720,605,170,85,'Amplifier_A');s.box(720,780,170,85,'Amplifier_B')
        s.wire([(460,780),(630,780),(630,645),(715,645)],'TDM8',550,755)
        s.wire([(630,780),(630,820),(715,820)])
        s.text(705,575,'AMP_A: first 4 slots',16)
        s.text(705,750,'AMP_B: last 4 slots',16)
        labels=[['Front-left tweeter','Front-left mid / woofer','Front-right tweeter','Front-right mid / woofer'],['Front center speaker','Rear-left speaker','Rear-right speaker','Exterior pedestrian warning']]
        for y,group in [(620,labels[0]),(795,labels[1])]:
            for i,t in enumerate(group):
                yy=y+i*18;s.wire([(890,yy),(935,yy)],arrow=False,color='#242424');s.text(945,yy+5,t,13)
        s.text(730,900,'Typical 5.0 audio system',17)
    else:
        s.box(720,610,170,105,'A2B')
        s.port(725,650,'A');s.port(845,650,'B')
        s.wire([(460,780),(605,780),(605,690),(715,690)],'6-wire TDM16: 32 channels down\nand 32 channels up simultaneously',480,755,both=True)
        s.wire([(460,455),(660,455),(660,595),(805,595),(805,605)],'I2C',670,565)
    # The remaining peripherals occupy their own lower rows.
    for cy,chip,external,digital in [(990,'AM / FM tuner','Antenna',False),(1085,'DAB receiver','Antenna',True),(1180,'Deserializer','Nintendo console',True),(1260,'ADC','T-Box',False)]:
        s.box(720,cy-35,170,65,chip,size=17)
        lane=490+(cy-990)*.18
        s.wire([(715,cy),(lane,cy),(lane,885+(cy-990)*.12),(465,885+(cy-990)*.12)],'I2S',620,cy-10)
        s.wire([(890,cy),(965,cy)],digital=digital,arrow=False,color='#242424');s.text(975,cy+5,external,15)
    s.text(35,1335,'External connections: solid = analog; dotted = digital. Internal buses are labeled.',17)

def internal():
    s=SVG(1150,1380,'Head unit with built-in amplifiers');head(s,'internal');s.save('built-in-amplifier.svg')

def external(booster=False):
    s=SVG(1150,1950,'Head unit with a booster amplifier' if booster else 'Head unit with an external amplifier')
    head(s,'booster' if booster else 'external')
    s.box(250,1440,850,440,'','white');s.text(270,1475,'Booster external amplifier' if booster else 'External amplifier (typically 7.1.4)',24,weight='bold')
    s.box(280,1530,150,95,'A2B');s.port(285,1545,'B');s.port(285,1590,'A')
    s.wire([(865,665),(1125,665),(1125,1400),(260,1400),(260,1558),(280,1558)],'A2B: multichannel PCM',620,1390,digital=True,both=True)
    if not booster:
        s.box(520,1515,165,190,'DSP',size=23)
        s.wire([(435,1560),(515,1560)],'6-wire TDM16: 32 down / 32 up',440,1500,both=True)
        s.box(280,1750,150,70,'MCU')
        s.wire([(435,1785),(600,1785),(600,1710)],'SPI: volume, headrest mode, etc.',450,1830,both=True)
        s.wire([(150,1175),(150,1910),(355,1910),(355,1825)],'CAN: volume, headrest mode, etc.',210,1900,digital=True,both=True)
        source_x,source_y=690,1580
    else:
        source_x,source_y=435,1575
    for y,label in [(1525,'Amplifier_A'),(1780,'Amplifier_N')]:
        s.box(780,y,160,70,label,size=17)
        lane=725 if not booster else 670
        s.wire([(source_x,source_y),(lane,source_y),(lane,y+35),(775,y+35)],'TDM',lane+8,y+5)
    if booster:
        s.wire([(435,1600),(580,1600),(580,1495),(860,1495),(860,1520)],'I2C: remote AMP register control',500,1510)
        s.wire([(580,1600),(580,1860),(860,1860),(860,1855)])
    s.text(860,1680,'⋮',35,'middle')
    for y,label in [(1560,'Cabin speakers × N'),(1670,'Headrest speakers × N'),(1815,'Exterior speakers × N')]:
        s.wire([(945,y),(980,y)],arrow=False,color='#242424');s.text(990,y+5,label,13)
    if booster:s.text(275,1925,'No MCU or DSP: all routing and control are handled by the head unit.',15)
    s.save('booster-amplifier.svg' if booster else 'external-amplifier.svg')

def chain():
    s=SVG(1540,780,'A2B chain linking front and rear head units, an amplifier, and microphones')
    s.text(250,40,'Front / rear audio downstream; amplifier references and cabin microphones upstream',19)
    def node(x,y,label,second=False):
        s.box(x,y,205,170,'','white');s.text(x+102,y+32,label,17,'middle');s.box(x,y+65,205,80,'A2B_2' if second else 'A2B_1' if 'head unit' in label else 'A2B',size=18);s.port(x+4,y+90,'A');s.port(x+161,y+90,'B')
    for x,label in [(35,'Front head unit'),(300,'Rear head unit')]:
        s.box(x,120,205,420,'','white');s.text(x+102,152,label,17,'middle')
        for y,label2 in [(185,'A2B_1'),(435,'A2B_2')]:
            s.box(x,y,205,80,label2,size=18);s.port(x+4,y+25,'A');s.port(x+161,y+25,'B')
    node(565,120,'External amplifier')
    for i in range(3):node(830+i*235,120,'Cabin mic × 2')
    for x1,x2 in [(240,300),(505,565),(770,830),(1035,1065),(1270,1300)]:s.wire([(x1,225),(x2-5,225)],both=True)
    
    s.wire([(240,475),(295,475)],both=True)
    for i in range(3):node(565+i*270,535,'Exterior mic × 2')
    s.wire([(505,475),(535,475),(535,640),(560,640)],both=True)
    s.wire([(770,640),(830,640)],both=True);s.wire([(1040,640),(1100,640)],both=True)
    s.wire([(265,95),(265,235)],digital=True,arrow=False,color='#69a64e')
    s.wire([(265,475),(265,600)],digital=True,arrow=False,color='#69a64e')
    s.text(35,650,'Rear-head-unit audio and exterior-mic audio\nare sent upstream to the front head unit.',18)
    s.save('a2b-network.svg')

def surround():
    s=SVG(600,480,'5.1-channel speaker layout')
    cx,cy,r=300,250,180
    s.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="#61766e" stroke-width="1.5" stroke-dasharray="8 7" fill="none"/>')
    for deg,label in [(-30,'L'),(0,'C'),(30,'R'),(-110,'LS'),(110,'RS')]:
        rad=math.radians(deg);x=cx+r*math.sin(rad);y=cy-r*math.cos(rad)
        s.wire([(cx,cy),(x,y)],digital=True,arrow=False,color='#58736b');s.box(x-15,y-20,30,38,'','#fafafa','#8b9691');s.text(x,y-31,label,18,'middle')
    s.box(360,30,55,48,'Sub','#fafafa','#8b9691',16)
    s.parts.append('<circle cx="300" cy="250" r="20" fill="#202724"/><path d="M275 282Q300 300 325 282" stroke="#202724" fill="none" stroke-width="12"/>')
    s.text(285,120,'30°',17);s.text(350,230,'110°',17);s.text(400,310,'100°',17);s.text(210,400,'120°',17)
    s.save('surround-5-1.svg')

if __name__=='__main__':
    internal();external();external(True);chain();surround()
    print('Wrote five English SVG diagrams.')
