import sys
sys.path.insert(0, sys.argv[1]); import letter
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
mode,out,c1,c2=sys.argv[2:6]; bg=sys.argv[6] if len(sys.argv)>6 else None
paths="".join(f'<path d="{d}"/>' for d in letter.glyphs())
X0,X1,Y0,Y1=6,1037,50,322; ww=X1-X0; wh=Y1-Y0
def en(path,text,size,track):
    f=TTFont(path); gs=f.getGlyphSet(); cm=f.getBestCmap(); s=size/f['head'].unitsPerEm
    items=[];x=0
    for ch in text:
        g=gs[cm[ord(ch)]]
        if ch!=' ':
            b=BoundsPen(gs); g.draw(b); items.append((x,g,b.bounds))
        x+=g.width*s+track*size
    l=items[0][0]+items[0][2][0]*s; r=items[-1][0]+items[-1][2][2]*s
    top=max(b[3] for *_,b in items)*s
    def draw(dx,base):
        o=[]
        for x,g,_ in items:
            p=SVGPathPen(gs); g.draw(TransformPen(p,(s,0,0,-s,dx+x,base))); o.append(p.getCommands())
        return " ".join(o)
    return r-l,l,top,draw
pad=110 if bg else 12
s=[]
if mode=="word":
    W=ww+2*pad; H=wh+2*pad
    s.append(f'<g fill="{c1}" fill-rule="evenodd" transform="translate({pad-X0},{pad-Y0})">{paths}</g>')
else:
    ew,el,et,draw=en(sys.argv[1]+"/f2/Montserrat-500.ttf","GOSU ENGLISH",62,0.42)
    W=max(ww,ew)+2*pad; cx=W/2
    rule_y=pad+wh+60; base=rule_y+50+et; H=base+pad
    s.append(f'<g fill="{c1}" fill-rule="evenodd" transform="translate({cx-ww/2-X0},{pad-Y0})">{paths}</g>')
    s.append(f'<rect x="{cx-110}" y="{rule_y}" width="220" height="4" fill="{c2}"/>')
    s.append(f'<path fill="{c2}" d="{draw(cx-ew/2-el,base)}"/>')
hdr=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W/2:.0f}" height="{H/2:.0f}">'
if bg: hdr+=f'<rect x="-2" y="-2" width="{W+4:.0f}" height="{H+4:.0f}" fill="{bg}"/>'
open(out,"w").write(hdr+"".join(s)+"</svg>")
