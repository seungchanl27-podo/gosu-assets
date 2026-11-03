import numpy as np, cv2, potrace, sys
gray=np.load(sys.argv[1]+'/gray.npy').astype(np.float32)
SC=4
def build(weight=0, soften=0, track=0, ring=1.0):
    big=cv2.resize(gray,None,fx=SC,fy=SC,interpolation=cv2.INTER_CUBIC); big=cv2.GaussianBlur(big,(0,0),SC*0.9)
    m=(big<172).astype(np.uint8)
    if weight>0: m=cv2.dilate(m,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*weight+1,)*2))
    if soften>0:   # round off sharp corners slightly
        k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*soften+1,)*2)
        m=cv2.morphologyEx(m,cv2.MORPH_OPEN,k); m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,k)
    # split syllables at gaps and re-space
    cuts=[0,271*SC,548*SC,797*SC,m.shape[1]]
    parts=[m[:,cuts[i]:cuts[i+1]] for i in range(4)]
    pad=int(track*SC)
    out=np.zeros((m.shape[0], m.shape[1]+3*pad+40),np.uint8); x=0
    for i,p in enumerate(parts):
        out[:,x:x+p.shape[1]]|=p; x+=p.shape[1]+pad
    return out
def to_svg(m,path,col,bg=None):
    bm=potrace.Bitmap(m==0); pl=bm.trace(turdsize=200,alphamax=1.1,opticurve=True,opttolerance=0.6)
    d=[]
    for c in pl:
        s=c.start_point; d.append(f"M{s.x:.1f},{s.y:.1f}")
        for seg in c.segments:
            if seg.is_corner: d.append(f"L{seg.c.x:.1f},{seg.c.y:.1f} L{seg.end_point.x:.1f},{seg.end_point.y:.1f}")
            else: d.append(f"C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}")
        d.append("Z")
    ys,xs=np.where(m>0); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    return x0,x1,y0,y1," ".join(d)
