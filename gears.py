from __future__ import division
import math
import svgwrite, plotting
from svgwrite import cm, mm

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
    #print pts
#     dwg = '''<?xml version="1.0" encoding="utf-8" ?>
# <svg baseProfile="full" height="100%" version="1.1" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs /><polyline points="'''
#     polyline = [p[0]+','+p[1] for p in pts]
#     polyline = " ".join(polyline)
#     dwg = dwg+polyline
#     dwg = dwg+'''" />'''
#     circle = '<circle cx="{}" cy="{}" r="{}" />'.format(str(shiftx)+'cm',str(shifty)+'cm',str(hole_rad)+'cm')
#     dwg = dwg+circle+'</svg>'
    for i in xrange(len(pts)-1):
        dwg.add(dwg.line(pts[i],pts[i+1]))
    dwg.add(dwg.line(pts[-1],pts[0]))
    dwg.add(dwg.circle(center=(shiftx*cm,shifty*cm),r=hole_rad*cm))
    dwg.save()
#    f = open(fname,'w')
#    f.write(dwg)
#    f.close()

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
    print angs_ccw
    return inds
