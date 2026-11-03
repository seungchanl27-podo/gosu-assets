import numpy as np, cv2, sys
gray=np.load(sys.argv[1]+'/gray.npy').astype(np.float32)
SC=8
def build(weight=0, soften=0, track=0, sharp=False):
    big=cv2.resize(gray,None,fx=SC,fy=SC,interpolation=cv2.INTER_CUBIC)
    big=cv2.GaussianBlur(big,(0,0),SC*1.1)
    m=(big<172).astype(np.uint8)
    if sharp:   # replace rounded right ends of ㅗ/ㅜ bars with a slanted sharp cut (like ㅕ/ㅓ stem ends)
        for top,bot,xe in [(228.5,248.4,262),(169.0,188.75,537)]:
            T,B=int(round(top*SC)),int(round(bot*SC)); X=xe*SC
            m[T-2*SC:B+2*SC, X-16*SC:X+4*SC]=0
            cv2.fillPoly(m,[np.array([[X-16*SC,T],[X+2*SC,T],[X-9*SC,B],[X-16*SC,B]],np.int32)],1)
    if weight>0: m=cv2.dilate(m,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*weight+1,)*2))
    if soften>0:
        k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*soften+1,)*2)
        m=cv2.morphologyEx(m,cv2.MORPH_OPEN,k); m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,k)
    m=(cv2.GaussianBlur(m.astype(np.float32),(0,0),SC*1.2)>0.5).astype(np.uint8)
    cuts=[0,271*SC,548*SC,797*SC,m.shape[1]]
    parts=[m[:,cuts[i]:cuts[i+1]] for i in range(4)]
    pad=int(track*SC)
    out=np.zeros((m.shape[0], m.shape[1]+3*pad+40),np.uint8); x=0
    for p in parts:
        out[:,x:x+p.shape[1]]|=p; x+=p.shape[1]+pad
    return out
from scipy.signal import savgol_filter
def smooth(p, win=61, k=28, thr=0.55):
    n=len(p)
    if n<win+2: return p
    sm=np.stack([savgol_filter(p[:,i],win,2,mode='wrap') for i in (0,1)],1)
    a=np.roll(p,k,0)-p; b=np.roll(p,-k,0)-p          # corner detection by angle
    cos=(a*b).sum(1)/(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1)+1e-9)
    corner=cos>-np.cos(thr*np.pi/2)                   # sharper than ~130deg
    w=np.ones(n)
    idx=np.where(corner)[0]
    for i in idx: w[np.arange(i-k,i+k+1)%n]=0
    w=np.convolve(np.r_[w[-15:],w,w[:15]],np.ones(31)/31,'same')[15:-15]
    return p*(1-w[:,None])+sm*w[:,None]
def to_svg(m,*_):
    cs,_h=cv2.findContours(m,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    d=[]
    for c in cs:
        if cv2.contourArea(c)<50: continue
        a=smooth(c.reshape(-1,2).astype(float))
        a=cv2.approxPolyDP(a.astype(np.float32).reshape(-1,1,2),0.8,True).reshape(-1,2)
        d.append("M"+" L".join(f"{x},{y}" for x,y in a)+"Z")
    ys,xs=np.where(m>0)
    return xs.min(),xs.max(),ys.min(),ys.max()," ".join(d)
