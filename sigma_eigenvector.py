#This takes the output ptc_twiss and transform the eigenvalues into a V matrix.
#knowing that the beam matrix is described as sig=VeVT
import numpy as np
from numpy import arctan
import ellipse_sort
#import ellipse_defs
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

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
    v=(ev2.reshape(6,6))  #v=(ev2.reshape(6,6,order='F'))
    vt=v.transpose()
    mat=v*vt;see(mat)
    a=emat*vt #beam=[V][e][V]T
    b=v*a
    see(b)
    #c=v*einv;d=c*a;see(d)
    return b

def see(matrix):
    np.set_printoptions(precision=3)
    print matrix

def make_beam(x,px,y,py,t,pt,nstd):
    zeros,w,start,scom=[],[],[],[]
    sx,sy,st,spx,spy,spt=[],[],[],[],[],[]
    for i in range(nparts):
        zeros.append(0); w.append(1)
        start.append('ptc_start,'); scom.append(';')
        sx.append('x='); sy.append(', y='); st.append(', t=')
        spx.append(', px='); spy.append(', py='); spt.append(', pt=')

    with open('input.beam'+str(nstd),'w') as g:
        for g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14 \
            in zip(start, sx, x, spx, px, sy, y, spy, py, st, t, spt, pt, scom):
            print >> g, g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14
    print "created input.beam",nstd

def get_axes(m11,m22,m12):

    xmaj=2**-0.5*np.sqrt(m11+m22+np.sqrt(m11**2+m22**2+4*(m12**2)-2*m11*m22))
    xmin=2**-0.5*np.sqrt(m11+m22-np.sqrt(m11**2+m22**2+4*(m12**2)-2*m11*m22))
    thet=0.5*np.arctan(2*m12/(m11-m22))
    print "thet", thet
    return xmaj, xmin, thet

def plot_dist(x,px,x0,px0,x1,px1,x2,px2):

    plt.figure()
    #plt.plot(x_,y_,'.',color='black')
    plt.plot(x,px,'y.',markersize=1.9)
    plt.plot(x0,px0,'.',color='black');
    plt.plot(x1,px1,'r.');plt.plot(x2,px2,'g.')
    #plt.plot(x3,px3,'b.');plt.plot(x4,px4,'m.')
    plt.savefig("sig_dist.jpeg")
    plt.close()
    plt.plot(x,pt,'y.',markersize=1.9)
    plt.plot(x0,pt0,'.',color='black');
    plt.plot(x1,pt1,'r.')
    plt.plot(x2,pt2,'g.')
    plt.savefig("x_pt.jpeg")
    return None

emx=emy=(3.98e-9)/2#1.2e-8
#emx=emy=0
emz=0.197236030163993*1.120e-4
#emz=0
nparts=1000000

#This creates a gaussian distribution, and then sorts using ellipse_sort
#into sigma bands.

V=get_cov('ptc_track',ex=emx,ey=emy,ez=emz)
x,px,y,py,t,pt = np.random.multivariate_normal([0,0,0,0,0,0],V,nparts).T

#GET THETA AND MAJOR AND MINOR AXES
xmaj,xmin,tht =   get_axes(V.item(0),V.item(7),V.item(6))

x0,px0,y0,py0,t0,pt0,x1,px1,y1,py1,t1,pt1,x2,px2,y2,py2,t2,pt2,=\
                ellipse_sort.get_sigma(x,px,y,py,t,pt,xmaj,xmin,tht)

plot_dist(x,px,x0,px0,x1,px1,x2,px2)

#make_beam(x4,px4,y4,py4,t4,pt4,5)
#make_beam(x3,px3,y3,py3,t3,pt3,4)
make_beam(x2,px2,y2,py2,t2,pt2,3)
make_beam(x1,px1,y1,py1,t1,pt1,2)
make_beam(x0,px0,y0,py0,t0,pt0,1)
#make_beam(x,px,y,py,t,pt,99)
e= open('emittances.txt','w')
e.write(str(emx)+'\n'+str(emy)+'\n'+str(emz))

#xmaj,xmin,tht=   get_axes(V.item(0),V.item(7),V.item(6))
#x1,px1       =   ellipse_defs.plot_twiss_ellipse(0,0,2*xmaj,2*xmin,tht*180/np.pi)
#x2,px2       =   ellipse_defs.plot_twiss_ellipse(0,0,2*xmaj,2*xmin,tht*180/np.pi)

#x3, px3, ellip3, mx,mpx = ellipse_defs.plot_point_cov(xpoints, nstd=3, alpha=0.3, color='green')
#x2, px2, ellip2,a,b = ellipse_defs.plot_point_cov(xpoints, nstd=2, alpha=0.3, color='red')
#x1, px1, ellip1,c,d = ellipse_defs.plot_point_cov(xpoints, nstd=1, alpha=0.3, color='yellow')
#x_5, px_5, ellip_5,e,f = ellipse_defs.plot_point_cov(xpoints, nstd=0.5, alpha=0.3, color='pink')

#make_beam(mx,mpx,y,py,t,pt,0)

#print "x", np.std(x),'\n',"px", np.std(px),'\n',"y",np.std(y),'\n',"py", np.std(py),\
#    '\n',"t", np.std(t),'\n',"pt", np.std(pt)
