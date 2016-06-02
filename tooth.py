from __future__ import division
import os, sys, math
import matplotlib.pyplot as plt
import numpy as np
import copy
import plotting

def tootherpolate(drive_gear, driven_gear, tooth_height, tooth_width, n):
    poser = make_interp_gear_pose(drive_gear, driven_gear)
    #debugging
    drive_gear = []
    driven_gear = []
    for i in xrange(0,n):
        driveg, driveng = poser(2*math.pi*(i/n))
        drive_gear.append(copy.deepcopy(driveg))
        driven_gear.append(copy.deepcopy(driveng))
    return drive_gear, driven_gear


def make_interp_gear_pose(drive_gear, driven_gear):
    def interp_pose(ang):
        """returns the angle, radius of the gear at angle 'ang', and the angle, radius of the driven gear at that position"""
        #find the appropriate index of the driven gear that straddels the given angle
        i = 0
        while i<len(drive_gear)-1 and (drive_gear[i+1][0]<ang):
            i+=1
#        if i==len(drive_gear)-1 and (drive_gear[i+1][0]<ang):
#            i+=1
        drive_ang = ang
        drive_rad = drive_gear[i][1]
        #interpolate angle of driven gear
        driven_rad = driven_gear[i][1]
        driven_ang = driven_gear[i][0]-(ang-drive_gear[i][0])*drive_rad/driven_rad
        return (drive_ang, drive_rad), (driven_ang, driven_rad)
    return interp_pose

def test_tootherpolate(drive_gear, driven_gear, n):
    c_dist = 2.0
    rot = 0
    l = 1.5
    drive_angs = [d[0] for d in drive_gear]
    drive_rads = [d[1] for d in drive_gear]
    driven_angs = [d[0] for d in driven_gear]
    driven_rads = [d[1] for d in driven_gear]
    xs_drive, ys_drive = plotting.pol2cart([r for r in drive_angs], drive_rads) #+math.pi #used to be negative
    xs_drive.append(xs_drive[0])
    #xs_drive = [-x for x in xs_drive]
    ys_drive.append(ys_drive[0])
#        xs_driven, ys_driven = pol2cart([r+driven_angs[i]+math.pi for r in driven_angs], driven_rads)
    xs_driven, ys_driven = plotting.pol2cart([r-math.pi for r in driven_angs], driven_rads)
    xs_driven.append(xs_driven[0])
    ys_driven.append(ys_driven[0])
    xs_driven = [x+c_dist for x in xs_driven]
    #x_cable = math.cos(rot-driven_angs[i])+c_dist
    #y_cable = math.sin(rot-driven_angs[i])

    plt.plot(xs_drive,ys_drive,'b')
    plt.hold(True)
    plt.plot(xs_driven,ys_driven,'r')
    #plt.plot([x_cable,out_x],[y_cable,out_y],'g')
    plt.plot([0],[0],'bo')
    plt.plot([c_dist],[0],'ro')

    #path = os.getcwd()
    #path = os.path.join(path,'imgs')
    #path = os.path.join(path,'{}_gears.png'.format(i))
    #imgs.append(path)
    axes = [-c_dist,2*c_dist+l,-c_dist,c_dist]
    plt.axis(axes)

    drive_gear, driven_gear = tootherpolate(drive_gear, driven_gear, 0.0, 0.0, n)
    drive_angs = [d[0] for d in drive_gear]
    drive_rads = [d[1] for d in drive_gear]
    driven_angs = [d[0] for d in driven_gear]
    driven_rads = [d[1] for d in driven_gear]
    xs_drive, ys_drive = plotting.pol2cart([r for r in drive_angs], drive_rads) #+math.pi #used to be negative
    xs_drive.append(xs_drive[0])
    #xs_drive = [-x for x in xs_drive]
    ys_drive.append(ys_drive[0])
#        xs_driven, ys_driven = pol2cart([r+driven_angs[i]+math.pi for r in driven_angs], driven_rads)
    xs_driven, ys_driven = plotting.pol2cart([r-math.pi for r in driven_angs], driven_rads)
    xs_driven.append(xs_driven[0])
    ys_driven.append(ys_driven[0])
    xs_driven = [x+c_dist for x in xs_driven]
    #x_cable = math.cos(rot-driven_angs[i])+c_dist
    #y_cable = math.sin(rot-driven_angs[i])

    plt.plot(xs_drive,ys_drive,'r.')
    plt.hold(True)
    plt.plot(xs_driven,ys_driven,'b.')
    #plt.plot([x_cable,out_x],[y_cable,out_y],'g')
    plt.plot([0],[0],'bo')
    plt.plot([c_dist],[0],'ro')

    #path = os.getcwd()
    #path = os.path.join(path,'imgs')
    #path = os.path.join(path,'{}_gears.png'.format(i))
    #imgs.append(path)
    axes = [-c_dist,2*c_dist+l,-c_dist,c_dist]
    plt.axis(axes)

    plt.show()
