import scipy as sp
import pylab as py
#import get_m56
import labeling
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt,pi
import scipy.special as special
from scipy import stats
from scipy.stats import norm
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

def read_file(datafile,obsv):

    x=[];y=[];t=[];pt=[];z=[];px=[];py=[] #l is the t coordinate, z is the obs location
    for o in range(obsv):
        x.append([]);y.append([]);t.append([])
        px.append([]);py.append([]);pt.append([])
    with open(datafile) as f:
        data = f.read()
    data=data.split('\n')
    print "data length:", (len(data))
    n=0;i=0
    nparts= (len(data)-8)/obsv

    for row in data:
        if row.startswith('@') or row.startswith('*') \
            or row.startswith('$') or row.startswith('#')\
            or len(row)==0: continue
        else:
            i+=1
            w=" ".join(row.split())
            s=w.split()
            x[n].append(float(s[2]))
            px[n].append(float(s[3]))
            y[n].append(float(s[4]))
            py[n].append(float(s[5]))
            t[n].append(float(s[6]))
            pt[n].append(float(s[7]))
            if i%nparts==0:
                z.append(float(s[8]))
                i=0;n+=1

    return x,px,y,py,t,pt,z

def test_plot_bunch_lengths(*args):
    bunch_plot=0;ypy_plot=0;yz_plot=0;ptz_plot=1;y3d=0;y_chic_plot=0;
    fig=plt.gcf()
    fig.set_size_inches(30,20)
    for beam in enumerate(args):
        n =0;l_=0
        x= beam[1][0];px=beam[1][1]
        y= beam[1][2];py=beam[1][3]
        t= beam[1][4];pt=beam[1][5]
        z=beam[1][6]
        print "NUMBER OF OBSERVATION POINTS",len(x)
        dl=[];dl2=[]
        print y
        for obs in (0,2,4,6,8,9):
            dl.append([p-q for p,q in zip(t[obs],t[0])])
            dl2.append([g*h for g,h in zip(dl[l_],dl[l_])])
            l_+=1

        if (bunch_plot==1):
            for obs in (0,2,4,6,8,9):
                dl=[p-q for p,q in zip(t[obs],t[0])]
                plt.subplot(2,3,n+1)
                plt.hist(dl, histtype='step', bins=100, facecolor='blue')
                plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0),fontsize=20)


                plt.tight_layout()
                plt.savefig('bunhch.png')
                #3std=3*np.std(dl)
                #print np.sqrt(np.sum(dl2)/1000)

        if (ypy_plot==1):
            for obs in (0,2,4,6,8,9):
                plt.subplot(2,3,n+1);n+=1
                plt.plot(x[obs],px[obs],'.')
                set_plots(n,'xy (MeV)','x (m)','X_PX.png')

        if (yz_plot==1):
            for obs in (0,2,4,6,8,9):
                plt.subplot(2,3,n+1)
                plt.plot(x[obs],dl[n],'.');n+=1
                set_plots(n,'z (m)','x (m)','X_Z.png')

        if (ptz_plot==1):
            for obs in (0,2,4,6,8,9):
                plt.subplot(2,3,n+1)
                plt.plot(dl[n],pt[obs],'.');n+=1
                set_plots(n,'$\delta$','z (m)','PT_Z.png')

        if (y3d==1):
            fig=plt.figure()
            for obs in (0,2,4,6,8,9):
                print obs
                ax=fig.add_subplot(2,3,n+1,projection='3d')
                ax.scatter(x[obs],px[obs],dl[n]);n+=1
                ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0),fontsize=5)
                ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0),fontsize=5)
                plt.tight_layout()
                plt.savefig('xz3d.png')

        if (y_chic_plot==1):
            fig=plt.figure()
            for obs in range(10):
                plt.plot(z[obs],y[obs][0],'.');n+=1
                plt.savefig('y_z.png')
    #plt.show()

def set_plots(n,y,x,name):
    label=['Pick-up','Dipole 1','Dipole 2','Dipole 3','Dipole 4','Kicker']
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0),fontsize=20)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0),fontsize=20)
    plt.title(label[n-1],fontsize=30)
    plt.rcParams.update({'font.size':22})
    plt.ylabel(y)
    plt.xlabel(x)
    plt.tight_layout()
    plt.savefig(name)

    print 'created:', name

"""
def plot_bunch_lengths(in1,in3,in5):
        coeffs=np.polyfit(x0,_l0,6)
        #x=np.arrange(-0.001,0.001)

def get_label():
    ######NOW LABEL THE PLOT WITH APPROPRIATE EMITTANCES######
    en=[]
    infile=open('emittances.txt')
    outfile=open('emit.txt','w')
    replace={'.':''}
    for line in open('emittances.txt'):
        for src, target in replace.iteritems():
            line = line.replace(src, target)
            outfile.write(line)
    outfile.close()
    infile.close()

    with open('emit.txt') as f:
        file = f.read()
    file=file.split('\n')
    for row in file:
        en.append(row)
    file_string= 'z_'+str(en[0])+'_'+str(en[1])+'_'+str(en[2])+'.jpeg'
    return file_string
"""
#_s,_betx,_alfx,_gamx =  get_m56.get_values('ptc_abc')
n_obsv=11
beam0=read_file('../0trackone',obsv=n_obsv)
#print "beam file", len(beam0)

beam1=read_file('../1trackone',obsv=n_obsv)
#print "beam file", len(beam1)

beam15=read_file('../1.5trackone',obsv=n_obsv)
#print "beam file", len(beam15)

#beam2=read_file('../2trackone',obsv=n_obsv)
#print "beam file", len(beam2)

#beam25=read_file('../2.5trackone',obsv=n_obsv)
#print "beam file", len(beam25)

#beam99=read_file('../realtrackone',obsv=n_obsv)
#print "beam file", len(beam99)

#test_plot_bunch_lengths(beam99)
test_plot_bunch_lengths(beam0,beam15,beam1)
#plot_bunch_lengths(beam0,beam1_5,beam2_5)

#s,m51,m52,m56,m56p   =  get_m56.get_M5s(_s,_M51,_M52,_M56)
#sigE,sigP,tot_ds,m56label     =  get_m56.get_bunch_lengths(_betx,_alfx,_gamx,_M51,_M52,_M56,ex=1.22e-8,sigP=0.000123)
#print m56label
######READ IN TRACKONE FROM MADX BYPASS OUTPUT######
#plot_bunch_lengths(beam,plot_of='diff',s=s,dl=tot_ds,mlabel=m56label)