# 고수영어 custom lettering — drawn from scratch with primitive strokes
import math, sys
def rect_v(x0,x1,y0,y1,cut=10):   # vertical stem, bottom slanted: left lower
    return f"M{x0},{y0} L{x1},{y0} L{x1},{y1-cut} L{x0},{y1+cut*0.0} Z" if False else \
           f"M{x0},{y0} L{x1},{y0} L{x1},{y1-cut} L{x0},{y1} Z"
def rect_h(x0,x1,y0,y1,r=0):      # horizontal bar, right end softly rounded
    if not r: return f"M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} Z"
    return f"M{x0},{y0} L{x1-r},{y0} Q{x1},{y0} {x1},{(y0+y1)/2} Q{x1},{y1} {x1-r},{y1} L{x0},{y1} Z"
def ring(cx,cy,rx,ry,ts,tt):      # ㅇ: sides thickness ts, top/bottom tt
    o=f"M{cx-rx},{cy} A{rx},{ry} 0 1 0 {cx+rx},{cy} A{rx},{ry} 0 1 0 {cx-rx},{cy} Z"
    ix,iy=rx-ts,ry-tt
    i=f"M{cx-ix},{cy} A{ix},{iy} 0 1 1 {cx+ix},{cy} A{ix},{iy} 0 1 1 {cx-ix},{cy} Z"
    return o+" "+i
def bez(p0,p1,p2,t): return [(1-t)**2*p0[k]+2*(1-t)*t*p1[k]+t*t*p2[k] for k in (0,1)]
def curve(p0,p1,p2,w0,w1,n=24):   # tapered quadratic stroke
    L=[];R=[]
    for i in range(n+1):
        t=i/n; x,y=bez(p0,p1,p2,t)
        dx=2*(1-t)*(p1[0]-p0[0])+2*t*(p2[0]-p1[0]); dy=2*(1-t)*(p1[1]-p0[1])+2*t*(p2[1]-p1[1])
        l=math.hypot(dx,dy); nx,ny=-dy/l,dx/l; w=(w0+(w1-w0)*t)/2
        L.append((x+nx*w,y+ny*w)); R.append((x-nx*w,y-ny*w))
    pts=L+R[::-1]
    return "M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)+" Z"

V=25; H=18; C=11   # vertical / horizontal weight, slant cut
P=dict(V=V,H=H)
def glyphs(V=V,H=H,C=C,T=27,TT=18):
    g=[]
    # 고
    g.append(rect_h(28,200+V/2,72,72+H))
    g.append(curve((200,72),(201,150),(188,214),V,V-2))           # ㄱ vertical, slight left bend
    g.append(rect_v(95,95+V-2,163,268))                          # ㅗ stub
    g.append(rect_h(6,248,266,266+H,r=8))                          # ㅗ base
    # 수
    g.append(rect_h(376,376+V-2,60,98))                            # ㅅ top stub (merged)
    g.append(curve((386,92),(362,148),(290,174),V-2,H-3))          # ㅅ left sweep
    g.append(curve((390,100),(425,140),(505,168),H+2,H-6))         # ㅅ right
    g.append(rect_h(276,530,204,204+H,r=8))                        # ㅜ bar
    g.append(rect_v(388,388+V,204+H-2,320,C))                      # ㅜ stem
    # 영
    g.append(ring(622,128,66,67,T,TT))
    g.append(rect_h(684,752,101,101+H-2)); g.append(rect_h(684,752,150,150+H-2))
    g.append(rect_v(748,748+V,50,200,C))
    g.append(ring(697,262,68,56,T,TT))
    # 어
    g.append(ring(879,147,64,76,T,TT))
    g.append(rect_h(936,1016,132,132+H))
    g.append(rect_v(1012,1012+V,50,322,C))
    return g
if __name__=="__main__":
    col=sys.argv[2] if len(sys.argv)>2 else "#666"
    d="".join(f'<path d="{x}"/>' for x in glyphs())
    open(sys.argv[1],"w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1086 360"><g fill="{col}" fill-rule="evenodd">{d}</g></svg>')
