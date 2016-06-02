import os, subprocess, math
import tqdm
import matplotlib.pyplot as plt
import numpy as np

def plot_leg_motion(path,leg,angs,n_frames):
    plt.figure()
    pxs = [p[0] for p in path]
    pxs.append(pxs[0])
    pys = [p[1] for p in path]
    pys.append(pys[0])
    plotnames = []
    plotpath = os.path.join(os.getcwd(),'imgs')
    step = int(len(angs)/n_frames)
    for i,a in tqdm.tqdm(enumerate(angs)):
        if i%step!=0:
            continue
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

def plot_gear(drive_gear, driven_gear, rads, rot, label, l):
    n_rots = 30
    c_dist = 2*1.0
    out_x = c_dist+l
    out_y = 0
    plt.figure()
    imgs = []
    drive_angs = [d[0] for d in drive_gear]
    drive_rads = [d[1] for d in drive_gear]
    driven_angs = [d[0] for d in driven_gear]
    driven_rads = [d[1] for d in driven_gear]
    # plt.figure()
    # plt.hold(True)
    # plt.plot(drive_angs,'b')
    # plt.plot(driven_angs,'r')
    # plt.title('angles')
    # plt.figure()
    # plt.hold(True)
    # plt.plot(drive_rads,'b')
    # plt.plot(driven_rads,'r')
    # plt.title('radii')
    # plt.show()
    #for i in tqdm.tqdm(xrange(0,n_rots)):
    frame_ct = int(len(drive_gear)/n_rots)
    for i in tqdm.tqdm(xrange(len(drive_gear))):
        if i%frame_ct!=0:
            continue
        #shift = drive_angs[i]#2*math.pi*i/n_rots
#        xs_drive, ys_drive = pol2cart([-r-drive_angs[i] for r in drive_angs], drive_rads) #+math.pi #used to be negative
        xs_drive, ys_drive = pol2cart([r-drive_angs[i] for r in drive_angs], drive_rads) #+math.pi #used to be negative
        xs_drive.append(xs_drive[0])
        #xs_drive = [-x for x in xs_drive]
        ys_drive.append(ys_drive[0])
#        xs_driven, ys_driven = pol2cart([r+driven_angs[i]+math.pi for r in driven_angs], driven_rads)
        xs_driven, ys_driven = pol2cart([r-driven_angs[i]-math.pi for r in driven_angs], driven_rads)
        xs_driven.append(xs_driven[0])
        ys_driven.append(ys_driven[0])
        xs_driven = [x+c_dist for x in xs_driven]
        x_cable = math.cos(rot-driven_angs[i])+c_dist
        y_cable = math.sin(rot-driven_angs[i])

        plt.plot(xs_drive,ys_drive,'b')
        plt.hold(True)
        plt.plot(xs_driven,ys_driven,'r')
        plt.plot([x_cable,out_x],[y_cable,out_y],'g')
        plt.plot([0],[0],'bo')
        plt.plot([c_dist],[0],'ro')

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

def plot_manufacturability(drive_gear, driven_gear, fail_ids, out_motion, c_dist = 2.0, name = '', fout = None):
    drive_angs = [d[0] for d in drive_gear]
    drive_rads = [d[1] for d in drive_gear]
    driven_angs = [d[0]+math.pi for d in driven_gear]
    driven_rads = [d[1] for d in driven_gear]
    drive_angs_fail = [d[0] for i,d in enumerate(drive_gear) if i in fail_ids]
    drive_rads_fail = [d[1] for i,d in enumerate(drive_gear) if i in fail_ids]
    driven_angs_fail = [d[0]+math.pi for i,d in enumerate(driven_gear) if i in fail_ids]
    driven_rads_fail = [d[1] for i,d in enumerate(driven_gear) if i in fail_ids]
    drive_xs, drive_ys = pol2cart(drive_angs,drive_rads)
    drive_xs_fail, drive_ys_fail = pol2cart(drive_angs_fail,drive_rads_fail)
    driven_xs, driven_ys = pol2cart(driven_angs,driven_rads)
    driven_xs_fail, driven_ys_fail = pol2cart(driven_angs_fail,driven_rads_fail)
    #xs.append(xs[0])
    #ys.append(ys[0])
    driven_xs = [d+c_dist for d in driven_xs]
    driven_xs_fail = [d+c_dist for d in driven_xs_fail]
    plt.subplot(1,2,1)
    plt.title(name)
    plt.hold(False)
    plt.plot(drive_xs,drive_ys,'b')
    plt.hold(True)
    plt.plot(driven_xs,driven_ys,'b')
    plt.plot(drive_xs_fail,drive_ys_fail,'r.')
    plt.plot(driven_xs_fail,driven_ys_fail,'r.')
    plt.axis('equal')
    #plot the stretching plot, with bad zones in red
    plt.subplot(1,2,2)
    xs = [o[0] for o in out_motion]
    ys = [o[1] for o in out_motion]
    plt.hold(False)
    plt.plot(xs,ys,'b')
    plt.hold(True)
    xs_fails = [d for i, d in enumerate(xs) if i in fail_ids]
    ys_fails = [d for i, d in enumerate(ys) if i in fail_ids]
    plt.plot(xs_fails, ys_fails, 'r.')
    # plt.subplot(1,3,3)
    # plt.hold(True)
    # # for i in xrange(len(drive_angs)):
    # #     xs = [drive_angs[i],driven_angs[i]]
    # #     ys = [1,0]
    # #     if i in fail_ids:
    # #         plt.plot(xs,ys,'r')
    # #     else:
    # #         plt.plot(xs,ys,'b')
    # # d_angs = [driven_angs[i+1]-driven_angs[i] for i in xrange(len(driven_angs)-1)]
    # # d_angs.append(2*math.pi+driven_angs[0]-driven_angs[-1])
    # # plt.plot(driven_angs, d_angs, 'bo')
    # plt.plot()
    # for i in xrange(len(driven_angs)):
    #     if i in fail_ids:
    #         plt.plot(driven_angs[i],d_angs[i],'ro')
    if fout == None:
        plt.show()
    else:
        plt.savefig(fout, bbox_inches='tight')

def make_gif(images, outimg, length):
    delay = length*100/float(len(images))
    command = ['convert', '-delay', str(int(delay)), '-dispose', 'none']
    for i in images:
        #command.append('-page')
        command.append(i)
    command.append(outimg)
    subprocess.call(command)
