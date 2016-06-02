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

def calc_gear_length(gear):
    l = 0.0
    for i, d in enumerate(gear[:-1]):
        l+=d[1]*abs(d[0]-gear[i+1][0])
    l+=gear[-1][1]*abs(2*math.pi-abs(gear[-1][0]))
    return l[0]

def interpolate_tooth_angles(gear,n_teeth,is_driven):
    l = calc_gear_length(gear)
    space = l/n_teeth
    ls = []
    for i,_ in enumerate(gear):
        if i==0:
            ls.append(0)
            continue
        ls.append((ls[-1]+abs(gear[i][0]-gear[i-1][0])*gear[i-1][1])[0])
    ls.append(l)
    #print l, space, ls
    #iterate over the gear surface, identifying the angular location to place each tooth
    poses = []
    for i in xrange(n_teeth):
        dist = i*space
        #print dist
        for j, el in enumerate(ls[:-1]):
            if el<=dist and ls[j+1]>dist:
                break
        d_dist = dist-ls[j]
        ang = gear[j][0]+d_dist/gear[j][1]
        #if is_driven:
            #ang = -ang
        poses.append((j,ang[0],gear[j][1][0]))
    #print poses
    return poses

def design_teeth(gear, n_teeth):
    '''estimate a height and width for teeth based on gear size and number of teeth'''
    l = calc_gear_length(gear)
    space = l/n_teeth
    tooth_width = 0.6*space
    tooth_height = tooth_width*1.25
    return tooth_height, tooth_width

def gen_teeth(drive_gear, driven_gear, tooth_height, tooth_width, n_teeth):
    p_drive = interpolate_tooth_angles(drive_gear,n_teeth,False)
    p_driven = interpolate_tooth_angles(driven_gear,n_teeth,True)
    toothed_drive = gear_2_teeth(p_drive, tooth_height, tooth_width, False)
    toothed_driven = gear_2_teeth(p_driven, tooth_height, tooth_width, True)
    return toothed_drive, toothed_driven

def gear_2_teeth(poses, tooth_height, tooth_width, is_driven):
    under_pct = 0.1
    new_gear = []
    for p in poses:
        rad_under = p[2]-((tooth_height/2)*(1+under_pct))
        rad_over = p[2]+(tooth_height/2)
        quarter_ang = (tooth_width/4)/p[2]
        if is_driven:
            new_gear.append((p[1]+quarter_ang,rad_under))
            new_gear.append((p[1]-quarter_ang,rad_over))
            new_gear.append((p[1]-3*quarter_ang,rad_under))
        else:
            new_gear.append((p[1]-3*quarter_ang,rad_under))
            new_gear.append((p[1]-quarter_ang,rad_over))
            new_gear.append((p[1]+quarter_ang,rad_under))
    return new_gear

def test_calc_gear_length(gear1, gear2):
    print calc_gear_length(gear1), calc_gear_length(gear2)

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

def test_interpolate_tooth_angles(drive_gear, driven_gear, n):
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

    p_drive = interpolate_tooth_angles(drive_gear,n,False)
    p_driven = interpolate_tooth_angles(driven_gear,n,True)

    drive_angs = [d[1] for d in p_drive]
    drive_rads = [d[2] for d in p_drive]
    driven_angs = [d[1] for d in p_driven]
    driven_rads = [d[2] for d in p_driven]
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
