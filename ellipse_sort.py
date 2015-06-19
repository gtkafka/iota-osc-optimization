import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos,pi
def get_sigma(x,px,y,py,t,pt,xmaj,xmin,th):

    print len(x)
    #th=tht*180/pi
    xa=[];x0=[];x1=[];x2=[];x3=[]
    pxa=[];px0=[];px1=[];px2=[];px3=[]

    ya=[];y0=[];y1=[];y2=[];y3=[]
    pya=[];py0=[];py1=[];py2=[];py3=[]

    ta=[];t0=[];t1=[];t2=[];t3=[]
    pta=[];pt0=[];pt1=[];pt2=[];pt3=[]
    for i in range(len(x)):

        x_= x[i];px_=px[i]
        y_= y[i];py_=py[i]
        t_= t[i];pt_=pt[i]

        ellips=[]
        ellips0=[]
        for j in (1.,1.005, 2.,2.005, 3,3.01):#, 4.,4.02, 5.,5.03):
            print i,j
            ellips.append(((x_*cos(-th)-px_*sin(-th))**2/((j*xmaj)**2))+
                          ((x_*sin(-th)+px_*cos(-th))**2/((j*xmin)**2)))

        if ellips[0]>1 and ellips[1]<1:
            x0.append(x_);px0.append(px_)
            y0.append(y_);py0.append(py_)
            t0.append(t_);pt0.append(pt_)

        if ellips[2]>1 and ellips[3]<1:
            x1.append(x_);px1.append(px_)
            y1.append(y_);py1.append(py_)
            t1.append(t_);pt1.append(pt_)

        if ellips[4]>1 and ellips[5]<1:
            x2.append(x_);px2.append(px_)
            y2.append(y_);py2.append(py_)
            t2.append(t_);pt2.append(pt_)
        """
        if ellips[6]>1 and ellips[7]<1:
            x3.append(x_);px3.append(px_)
            y3.append(y_);py3.append(py_)
            t3.append(t_);pt3.append(pt_)

        if ellips[8]>1 and ellips[9]<1:
            xa.append(x_);pxa.append(px_)
            ya.append(y_);pya.append(py_)
            ta.append(t_);pta.append(pt_)
    """

    return x0,px0,y0,py0,t0,pt0,x1,px1,y1,py1,t1,pt1,\
           x2,px2,y2,py2,t2,pt2#,x3,px3,y3,py3,t3,pt3,xa,pxa,ya,pya,ta,pta
"""
    while True:
        if ellips < 1:
            ithEllipse = count
            break
        count+=1
        if count >= len(rads):
            ithEllipse = None
            break

    return ithEllipse

rads = zip(np.arange(.5,10,.5),np.arange(.5,10,.5))
print rads
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-15,15)
ax.set_ylim(-15,15)

# plot Ellipses
for rx,ry in rads:
    ellipse = patches.Ellipse((0,0),rx*2,ry*2,angle=70,fc='none',ec='red')
    ax.add_patch(ellipse)
v=[[1,0],[1,0]]
a,b=np.random.multivariate_normal((0,0),v,1000).T

x=1.3
y=2.4
idx = inWhichEllipse(x,y,rads,70)
rx,ry = rads[idx]
ellipse = patches.Ellipse((0,0),rx*2,ry*2,angle=70,fc='none',ec='blue')
ax.add_patch(ellipse)

if idx != None:
    circle = patches.Circle((x,y),.05)
    ax.add_patch(circle)
plt.plot(x,y,'.',markersize=1.9)
plt.show()

"""