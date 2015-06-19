__author__ = 'kafka'
import matplotlib.pyplot as plt
from math import sqrt
def get_values(datafile,a,b,c,d):
    sl=[];m51l=[];m52l=[];m56l=[]
    with open(datafile) as f:
        data = f.read()
    data=data.split('\n')
    print "data length:", (len(data))
    for row in data:
        if row.startswith('@') or row.startswith('*') \
            or row.startswith('$') or row.startswith('#')\
            or len(row)==0: continue
        if row.startswith(' "OEND"'):
            print "oend"
            break
        else:

            w=" ".join(row.split())
            s=w.split()
            sl.append(float(s[a]))
            m51l.append(float(s[b]))
            m52l.append(float(s[c]))
            m56l.append(float(s[d]))

    #print v0, '\n',v1, '\n',v2, '\n',v3
    #print len(v1)
    #print m52l
    return sl,m51l, m52l, m56l

def get_t_values(datafile):
    t511=[];t512=[];t516=[];t522=[];t526=[];t566=[];
    with open(datafile) as f:
        data = f.read()
    data=data.split('\n')
    #print "data length:", (len(data))
    for row in data:
        if row.startswith('@') or row.startswith('*') \
            or row.startswith('$') or row.startswith('#')\
            or len(row)==0: continue
        if row.startswith(' "OEND"'):

            break
        else:

            w=" ".join(row.split())
            s=w.split()
            t511.append(float(s[1]))
            t512.append(float(s[2]))
            t516.append(float(s[3]))
            t522.append(float(s[4]))
            t526.append(float(s[5]))
            t566.append(float(s[6]))

    return t511, t512, t522

def get_M5s(_s,M51,M52,M56):
    ones=[];DX=[];DXP=[];deltap=[]
    dx=-1.324131;dxp=1.1390845
    for i in range(0,106):
        deltap.append(0.000123)
        ones.append(-1)
        DX.append(dx);DXP.append(dxp)
    #FLIP SIGNS
    _m51=[y*z for y, z in zip(M51, ones)]
    _m52=[v*x for v, x in zip(M52, ones)]
    _m56=[s*t for s, t in zip(M56, ones)]

    #########compute partial slip##########

    M51Dx  =[a*b for a, b in zip(_m51, DX)]
    M52Dxp =[c*d for c, d in zip(_m52, DXP)]
    M56dp  =[e*f for e, f in zip(_m56,deltap)]
    _m56p  =[m+n+o for m,n,o in zip(M51Dx, M52Dxp, _m56)]

    #_m56p=[m+n+o for m,n,o in zip(M51Dx, M52Dxp, M56dp)]

    return _s,_m51,_m52,_m56,_m56p

def get_T5s():
    T511,T512,T522=get_t_values('ptc_tmatrix')
    bylen=len(T511)
    s,betx,alfx,gam=get_values('ptc_abc',1,2,6,13)
    betx=betx[1];alfx=alfx[1];gamx=(1+alfx**2)/betx
    del s[bylen:]
    for t in range(len(T511)):
        T511T522=[a*b for a, b in zip(T511,T522)]
    print "T511t522",T511T522
    sigma=[]
    ex=(3.97e-9)/2
    for n in range(len(T511)):
        sigma.append(sqrt(ex**2*(2*(T511[n]*betx-T512[n]*alfx+T522[n]*gamx)**2+(T512[n]**2-4*T511T522[n]))))
    print "secondsigma", sigma
    return sigma


def get_bunch_lengths(betx,alfx,gamx,m51, m52, m56, ex, sigP):
    betx=betx[1];alfx=alfx[1];gamx=(1+alfx**2)/betx
    dx=-0.456708189 ;dxp=0.4047374021
    sigE_ds=[];sigP_ds=[];tot_ds=[]
    for i in range(100):
        #print "m51", m51[i], "m52", m52[2], "m56", m56[i]
        #es=sqrt(ex*(betx*m51[i]**2-2*alfx*m51[i]*m52[i]+gamx*m56[i]**2))
        #ds=sqrt(sigP**2*(m51[i]*dx+m52[i]*dxp+m56[i])**2)

        sigE_ds.append(sqrt(abs(ex*(betx*m51[i]**2-2*alfx*m51[i]*m52[i]+gamx*m52[i]**2))))
        sigP_ds.append(sqrt(abs(sigP**2*(m51[i]*dx+m52[i]*dxp+m56[i])**2)))
        #print sigE_ds[i], m51[i], m52[i], m56[i]
    for j in range(100):
        tot_ds.append(sqrt(sigP_ds[j]**2+sigE_ds[j]**2))
    #print "length_E", sigE_ds[len(m51)-1]
    #print "length_tot", tot_ds[100],tot_ds[100]
    #label=str(tot_ds[len(m51)-1])
    return sigE_ds, sigP_ds, tot_ds, 'label'


#_s,_betx,_alfx,_gamx =  get_values('ptc_abc',1,2,6,13)

#_s,_M51,_M52,_M56    =  get_values('ptc_rmatrix',1,2,3,4)

#s,m51,m52,m56,m56p   =  get_M5s(_s,_M51,_M52,_M56)
#sigE,sigP,tot_ds,label     =  get_bunch_lengths(_betx,_alfx,_gamx,_M51,_M52,_M56, 1.1e-8, 0.000123)

#plt.subplot(1,1,1)
#plt.plot(s,m51,'-',color='r')
#plt.plot(s,m52,'-',color='orange')
#plt.plot(s,m56,'-',color='r')
#plt.plot(s,M51Dx,'-',color='magenta')
#plt.plot(s,M52Dxp,'-',color='purple')
#plt.plot(s,m56p,'-',color='blue')

#plt.plot(s,sigE,'-',color='cyan')
#plt.plot(s,sigP,'-',color='blue')
#plt.plot(s,tot_ds,'-',color='r')
#plt.title('sigma='+label)
#plt.savefig('M56.jpeg')
#print "created file:", label