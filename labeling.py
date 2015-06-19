def get_label():
    ######NOW LABEL THE PLOT WITH APPROPRIATE EMITTANCES######
    en=[]
    infile=open('emittances.txt')
    outfile=open('emit.txt','w')
    replace={'.':''}
    for line in open('emittances.txt'):
        for src, target in replace.iteritems():
            line = line.replace(src, target)
            line = line[3:]
            outfile.write(line)
    outfile.close()
    infile.close()

    with open('emit.txt') as f:
        file = f.read()
    file=file.split('\n')
    for row in file:
        en.append(row)
    emits= 'z_'+str(en[0])+'_'+str(en[1])+'_'+str(en[2])+'__'
    grfile=[]
    with open('gradients') as g:
        grad = g.read()
    grad=grad.split('\n')
    for row in grad:
        if len(row)==0: continue
        w=" ".join(row.split())
        s=w.split()
        el=s[0][:2]
        gr=s[2][:6]
        grads=str(el+gr)
        grfile.append(grads)
        #print el, gr
    glabel=''
    for i in range(len(grfile)):
        glabel=glabel+grfile[i]+'_'
    tot_string=emits+glabel+'.png'
    #print tot_string
    return tot_string
