import sys, json
S=sys.argv[1]; mode,out,c1,c2=sys.argv[2:6]; bg=sys.argv[6] if len(sys.argv)>6 else None
sys.path.insert(0,S); import importlib.util
spec=importlib.util.spec_from_file_location('l2',S+'/lockup2.py')
J=json.load(open(S+'/trace/mod.json')); x,y,ww,wh=J['vb']; x+=20;y+=20;ww-=40;wh-=40
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
def en(path,text,size,track):
    f=TTFont(path); gs=f.getGlyphSet(); cm=f.getBestCmap(); s=size/f['head'].unitsPerEm
    items=[];X=0
    for ch in text:
        g=gs[cm[ord(ch)]]
        if ch!=' ':
            b=BoundsPen(gs); g.draw(b); items.append((X,g,b.bounds))
        X+=g.width*s+track*size
    l=items[0][0]+items[0][2][0]*s; r=items[-1][0]+items[-1][2][2]*s; top=max(b[3] for *_,b in items)*s
    def draw(dx,base):
        o=[]
        for X,g,_ in items:
            p=SVGPathPen(gs); g.draw(TransformPen(p,(s,0,0,-s,dx+X,base))); o.append(p.getCommands())
        return " ".join(o)
    return r-l,l,top,draw
K=ww/4160; pad=(430 if bg else 40)*K
s=[]
if mode=="word":
    W=ww+2*pad; H=wh+2*pad
    s.append(f'<path fill="{c1}" fill-rule="evenodd" transform="translate({pad-x},{pad-y})" d="{J["d"]}"/>')
else:
    ew,el,et,draw=en(S+"/f2/Montserrat-500.ttf","GOSU ENGLISH",245*K,0.42)
    W=max(ww,ew)+2*pad; cx=W/2; rule_y=pad+wh+230*K; base=rule_y+200*K+et; H=base+pad
    s.append(f'<path fill="{c1}" fill-rule="evenodd" transform="translate({cx-ww/2-x},{pad-y})" d="{J["d"]}"/>')
    s.append(f'<rect x="{cx-430*K}" y="{rule_y}" width="{860*K}" height="{14*K}" fill="{c2}"/>')
    s.append(f'<path fill="{c2}" d="{draw(cx-ew/2-el,base)}"/>')
hdr=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W/8/K:.0f}" height="{H/8/K:.0f}">'
if bg: hdr+=f'<rect x="-8" y="-8" width="{W+16:.0f}" height="{H+16:.0f}" fill="{bg}"/>'
open(out,"w").write(hdr+"".join(s)+"</svg>")
