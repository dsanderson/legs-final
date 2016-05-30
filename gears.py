from __future__ import division
import math
import svgwrite, plotting
from svgwrite import cm, mm
import matplotlib.pyplot as plt

def write_gear(fname, gear, hole_rad, base_rad_cm=2, cable_pt = None):
    dwg = svgwrite.Drawing(fname, profile='full')

    angs = [d[0] for d in gear]
    rads = [d[1] for d in gear]
    xs, ys = plotting.pol2cart(angs, [r*base_rad_cm for r in rads])
    shiftx = -min(xs)
    shifty = -min(ys)
    xs = [(x+shiftx)*cm for x in xs]
    ys = [(y+shifty)*cm for y in ys]
    pts = zip(xs,ys)
    for i in xrange(len(pts)-1):
        dwg.add(dwg.line(pts[i],pts[i+1]))
    dwg.add(dwg.line(pts[-1],pts[0]))
    dwg.add(dwg.circle(center=(shiftx*cm,shifty*cm),r=hole_rad*cm))
    dwg.save()

def check_interior_angle(gear, threshold = (30/180)*math.pi):
    '''checks if the interior angle around a point is less than threshold.  Returns the indecies of points which failt that criterion'''
    #assumes angs in montonically increasing
    angs = [p[0] for p in gear]
    rads = [p[1] for p in gear]
    inds = []
    #angs.append(angs[0])
    #rads.append(rads[0])
    #inspect each point
    #semi_thresh = math.sin(threshold/2)
    for i in xrange(len(angs)):
        #construct list of semi-angles from clockwise dir first
        d_ang = 0
        j = i
        angs_cw = []
        while d_ang<threshold:
            j -= 1
            d_ang = abs(angs[i]-angs[j])
            d_ang = min(d_ang, 2*math.pi-d_ang)
            #ang = math.sin(d_ang)*rads[j]/(rads[j]-rads[i])
            #print 180*d_ang/math.pi, ang, rads[j], rads[i]
            #ang = math.atan(ang)
            ang = math.atan2(math.sin(d_ang)*rads[j%len(angs)],rads[j%len(angs)]-rads[i])
            angs_cw.append(ang)
        d_ang = 0
        j = i
        angs_ccw = []
        while d_ang<threshold:
            j += 1
            d_ang = abs(angs[i]-angs[j%len(angs)])
            d_ang = min(d_ang, 2*math.pi-d_ang)
#            if d_ang<0:
#                print d_ang
            #ang = math.sin(d_ang)*rads[j%len(angs)]/(rads[j%len(angs)]-rads[i])
            #ang = math.atan(ang)
            ang = math.atan2(math.sin(d_ang)*rads[j%len(angs)],rads[j%len(angs)]-rads[i])
            angs_ccw.append(ang)
        #check if any on the angles, summed, give you less than threshold
        found = False
        for cw in angs_cw:
            if found:
                break
            for ccw in angs_ccw:
                if ccw+cw<threshold and ccw+cw>0:
                    found = True
                    inds.append(i)
                    break
    #print angs_ccw
    return inds

def calc_out_motion(drive_gear, driven_gear, R, l, fail_inds):
    #calculate (normalized) output motion from the gear and geometry data
    xs = [d[0] for d in drive_gear]
    ys = [math.sqrt((l-R*math.cos(d[0]))**2+(R*math.sin(d[0]))**2) for d in driven_gear]
    #plt.plot(xs,ys,'b')
    #plt.hold(True)
    #xs_fails = [d for i, d in enumerate(xs) if i in fail_inds]
    #ys_fails = [d for i, d in enumerate(ys) if i in fail_inds]
    #plt.plot(xs_fails, ys_fails, 'r.')
    #plt.show()
    return zip(xs,ys)

def relax_motion(out_motion, R, l, fail_inds, relax_width=math.pi/16, relax_pct = 0.25):
    angs = [o[0] for o in out_motion]
    target_dists = [o[1] for o in out_motion]
    cable_dists = [math.sqrt((l-R*math.cos(a))**2+(R*math.sin(a))**2) for a in angs]
    new_dists = []
    for i in xrange(0, len(angs)):
        rad = min([abs(angs[f]-angs[i]) for f in fail_inds])
        new_dist = target_dists[i] - (target_dists[i]-cable_dists[i])*(1.0/(1.0+(rad/relax_width)))*relax_pct
        new_dists.append(new_dist)
    plt.plot(angs, target_dists, 'b')
    plt.hold(True)
    plt.plot(angs, cable_dists, 'r')
    plt.plot(angs, new_dists, 'g')
    plt.show()
