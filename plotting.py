import os, subprocess, math

import matplotlib.pyplot as plt
import numpy as np

def plot_leg_motion(path,leg,angs):
    plt.figure()
    pxs = [p[0] for p in path]
    pxs.append(pxs[0])
    pys = [p[1] for p in path]
    pys.append(pys[0])
    plotnames = []
    plotpath = os.path.join(os.getcwd(),'imgs')
    for i,a in enumerate(angs):
        a_upper_raw = a[0]
        a_lower_raw = a[2]
        p_mid = (leg.center[0]+leg.upper_length*math.cos(a_upper_raw),
                    leg.center[1]+leg.upper_length*math.sin(a_upper_raw))
        p_foot = (p_mid[0]+leg.lower_length*math.cos(a_lower_raw),
                    p_mid[1]+leg.lower_length*math.sin(a_lower_raw))
        plt.plot(pxs,pys,'r')
        plt.hold(True)
        legx = (leg.center[0],p_mid[0],p_foot[0])
        legy = (leg.center[1],p_mid[1],p_foot[1])
        plt.plot(legx,legy,'b')
        #save the plot
        axes = [-1,1,-1,1]
        plt.axis(axes)
        fpath = os.path.join(plotpath,'{}.png'.format(i))
        plotnames.append(fpath)
        plt.savefig(fpath, bbox_inches='tight')
    #produce gif
    outimg = os.path.join(plotpath,'compiled')
    outimg = os.path.join(outimg,'OUT.gif')
    make_gif(plotnames,outimg,3.0)

def plot_angs(angs):
    plt.figure()
    plt.subplot(3,1,1)
    plt.title('upper leg angle, rad')
    a_uppers = [a[0] for a in angs]
    a_lower_raws = [a[2] for a in angs]
    a_lower_rels = [a[3] for a in angs]
    plt.plot(a_uppers)
    plt.subplot(3,1,2)
    plt.title('lower absolute leg angle, rad')
    plt.plot(a_lower_raws)
    plt.subplot(3,1,3)
    plt.title('lower relative leg angle, rad')
    plt.plot(a_lower_rels)
    path = os.getcwd()
    path = os.path.join(path,'imgs')
    path = os.path.join(path,'compiled')
    path = os.path.join(path,'OUT_angs.png')
    plt.savefig(path)#, bbox_inches='tight')

def pol2cart(angs,rads):
    xs = []
    ys = []
    for i in xrange(0,len(angs)):
        rad = rads[i]
        ang = angs[i]
        xs.append(rad*math.cos(ang))
        ys.append(rad*math.sin(ang))
    return xs,ys

def plot_gear_single(drive_rads, driven_rads, rads, rot, label, l):
    c_dist = 2*1.0
    out_x = c_dist+l
    out_y = 0
    plt.figure()
    imgs = []
    shift = 0.0
    xs_drive, ys_drive = pol2cart([r+shift+math.pi for r in rads], drive_rads)
    xs_drive.append(xs_drive[0])
    ys_drive.append(ys_drive[0])
    xs_driven, ys_driven = pol2cart([r+shift for r in rads], driven_rads)
    xs_driven.append(xs_driven[0])
    ys_driven.append(ys_driven[0])
    xs_driven = [x+c_dist for x in xs_driven]
    x_cable = math.cos(rot+shift)+c_dist
    y_cable = math.sin(rot+shift)

    plt.plot(xs_drive,ys_drive,'b')
    plt.hold(True)
    plt.plot(xs_driven,ys_driven,'r')
    plt.plot([x_cable,out_x],[y_cable,out_y],'g')
    plt.show()

def plot_gear(drive_rads, driven_rads, rads, rot, label, l):
    n_rots = 30
    c_dist = 2*1.0
    out_x = c_dist+l
    out_y = 0
    plt.figure()
    imgs = []
    for i in xrange(0,n_rots):
        shift = 2*math.pi*i/n_rots
        xs_drive, ys_drive = pol2cart([r-shift+math.pi for r in rads], drive_rads)
        xs_drive.append(xs_drive[0])
        ys_drive.append(ys_drive[0])
        xs_driven, ys_driven = pol2cart([r+shift for r in rads], driven_rads)
        xs_driven.append(xs_driven[0])
        ys_driven.append(ys_driven[0])
        xs_driven = [x+c_dist for x in xs_driven]
        x_cable = math.cos(rot+shift)+c_dist
        y_cable = math.sin(rot+shift)

        plt.plot(xs_drive,ys_drive,'b')
        plt.hold(True)
        plt.plot(xs_driven,ys_driven,'r')
        plt.plot([x_cable,out_x],[y_cable,out_y],'g')

        path = os.getcwd()
        path = os.path.join(path,'imgs')
        path = os.path.join(path,'{}_gears.png'.format(i))
        imgs.append(path)
        axes = [-c_dist,2*c_dist+l,-c_dist,c_dist]
        plt.axis(axes)
        plt.savefig(path, bbox_inches='tight')
        plt.hold(False)
    outimg = os.path.join(os.getcwd(),'imgs','compiled')
    outimg = os.path.join(outimg,'OUT_{}.gif'.format(label))
    make_gif(imgs,outimg,3.0)



def make_gif(images, outimg, length):
    delay = length*100/float(len(images))
    command = ['convert', '-delay', str(int(delay)), '-dispose', 'none']
    for i in images:
        #command.append('-page')
        command.append(i)
    command.append(outimg)
    subprocess.call(command)
