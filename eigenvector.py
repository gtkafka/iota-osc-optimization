#This takes the output ptc_twiss and transform the eigenvalues into a V matrix.
#knowing that the beam matrix is described as sig=VeVT
import numpy as np
import matplotlib.pyplot as plt

def write_to_file(x, y,filename):
    fileobj= open(filename,'a')
    print >> fileobj, 'x', ' ', 'z'
    for key, value in zip(x,y):
        print >> fileobj, key,value
    fileobj.close()

def read_eigen_vecs(input_file):
    ev,betx,bety,_s=[],[],[],[]
    with open(input_file) as f:
        data = f.read()
    data=data.split('\n')
    for row in data:
        if row.startswith('@') or row.startswith('*') \
            or row.startswith('$') or len(row)==0:continue
        else:
            w=" ".join(row.split())
            s=w.split()
            row.lstrip()
            _s.append(s[-5])
            if s[0]=='"OSC_IOTA$START"':
                for i in range(len(s)-1): #make sure only reading in 36 values
                    ev.append(s[i+1])
    print len(ev)
    return ev

def get_cov(dataset,ex,ey,ez):
    emat=np.matrix([[ex,0,0,0,0,0],[0,ex,0,0,0,0],[0,0,ey,0,0,0],\
        [0,0,0,ey,0,0],[0,0,0,0,ez,0],[0,0,0,0,0,ez]])
    evs=read_eigen_vecs(dataset)
    #einv=emat.I
    ev1=map(float,evs)
    ev2=np.asarray(ev1)
    v=(ev2.reshape(6,6))
    vt=v.transpose()
    mat=v*vt
    print "v*vt"; see(mat)
    a=emat*vt #beam=[V][e][V]T
    b=v*a
    print "v*e*vt"; see(b)
    #c=v*einv;d=c*a;see(d)
    return b

def see(matrix):
    np.set_printoptions(precision=3)
    print matrix

def make_beam(x,px,y,py,t,pt):
    for i in range(nparts):
        zeros.append(0); w.append(1)
        start.append('ptc_start,'); scom.append(';')
        sx.append('x='); sy.append(', y='); st.append(', t=')
        spx.append(', px='); spy.append(', py='); spt.append(', pt=')

    with open('input.beam99','w') as g:
        for g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14 \
            in zip(start, sx, x, spx, px, sy, y, spy, py, st, t, spt, pt, scom):
            print >> g, g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14

length=20

if length==10:
    emx=emy=7.318963355115351e-9/2

    sigt=1.485298218462403e-2
    sige=1.141732022041257e-4

if length==9:
    emx=4.22e-9
    emy=4.22e-9
    sigt=1.097736344328448e-2
    sige=1.176113371631837e-4

if length==14:
    emx=4.56e-9
    emy=4.56e-9
    sigt=1.-2
    sige=1.1e-4

if length==16:
    etot=5.0288727352898437e-9
    emx=emy=etot/2
    sigt=0.206399763034631
    sige=1.130313175371059E-004

if length==18:
    etot=3.97e-9
    emx=emy=etot/2
    sigt=0.1778
    sige=1.097e-4

if length==20:
    etot=3.98e-9
    emx=etot/2
    emy=emx
    #sigt=sige=0
    sigt=0.197236030163993
    sige=1.120662937626496e-4

if length==22:
    emx=1.85e-9
    emy=1.85e-9
    sigt=0.164459157255732
    sige=1.089775669002977e-4

if length==28:
    etot=3.549194715625540e-9
    emx=emy=etot/2
    sigt=0.1286
    sige=1.1057e-4

if length==30:
    etot=4.2e-9
    emx=emy=etot/2
    sigt=0.130435727328145
    sige=1.105967e-4

emz=sigt*sige

nparts=10000

V=get_cov('ptc_track',ex=emx,ey=emy,ez=emz)

#print "items",V.item(0),V.item(1),V.item(6),V.item(7)
points=np.random.multivariate_normal\
        ([0,0],[[V.item(0),V.item(1)],[V.item(6),V.item(7)]],nparts)

x,px,y,py,t,pt = np.random.multivariate_normal([0,0,0,0,0,0],V,nparts).T
print "stdx", np.std(x)
zeros,w,start,scom=[],[],[],[]
sx,sy,st,spx,spy,spt=[],[],[],[],[],[]
make_beam(x,px,y,py,t,pt)


tsquare=[i**2 for i in t]
ptsquare=[j**2 for j in pt]
trms=np.sqrt(np.mean(tsquare))
ptrms=np.sqrt(np.mean(ptsquare))
print "RMS(t)", trms, "RMS(pt)", ptrms

#plt.subplot(2,1,1)
#plt.plot(x,pt,'.')

#plt.subplot(2,1,2)
#plt.hist(t, histtype='step', bins=100, facecolor='blue')

#plt.savefig('beam.png')

#plt.show()

e= open('emittances.txt','w')
e.write(str(emx)+'\n'+str(emy)+'\n'+str(emz))

print "x", np.std(x),'\n',"px", np.std(px),'\n',"y",np.std(y),'\n',"py", np.std(py),\
    '\n',"t", np.std(t),'\n',"pt", np.std(pt)
print "created input99.beam"
