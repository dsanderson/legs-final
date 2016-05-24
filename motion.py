from __future__ import division
import math, collections, os, subprocess, json, copy
import numpy as np
import matplotlib.pyplot as plt
import plotting

def dist(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def ang(p1,p2):
    return math.atan2(p2[1]-p1[1],p2[0]-p1[0])

def circs_to_ang(p,leg):
    d = dist(leg.center,p)
    ra = leg.upper_length
    rb = leg.lower_length
    segment = (d**2+ra**2-rb**2)/(2*d)
    ang = math.acos(segment/ra)
    return ang

def gen_gears(leg,angs):
    pass

def gen_gear(angs,r=1.0,l=1.5):
    #given the gear radius and output length, calculate the non-normalized change of length as a function of rotation
    ts = np.linspace(0, 2*math.pi, 120)
    raw_angs = []
    for t in ts:
        raw_angs.append(math.sqrt((l-r*math.cos(t))**2+(r*math.sin(t))**2))
    raw_angs = normalize_angs(raw_angs)
    vs, rot = calc_vels(angs,raw_angs)
    print vs
    #convert relative velocities into matched gear sets, and their initial rotation
    rads = [(rot+(2*math.pi*i/len(vs)))%(2*math.pi) for i in range(0,len(vs))]
    drive_rads = [2*r/(v+1) for v in vs]
    driven_rads = [(2*r)-rad for rad in drive_rads]
    return drive_rads, driven_rads, rads, rot



def normalize_angs(angs):
    #normalize the change in length from zero to one
    raw_angs = copy.deepcopy(angs)
    trans = min(raw_angs)
    raw_angs = [a-trans for a in raw_angs]
    scale = max(raw_angs)
    raw_angs = [a/scale for a in raw_angs]
    return raw_angs

def calc_vels(out_angs, in_angs):
    out_angs = normalize_angs(out_angs)
    in_angs = normalize_angs(in_angs)
    in_peak_index = [i for i in xrange(len(in_angs)) if in_angs[i] == max(in_angs)][0]
    print in_peak_index
    out_peak_index = [i for i in xrange(len(out_angs)) if out_angs[i] == max(out_angs)][0]
    print out_peak_index

    #rotate in_angs to match out_angs
    in_angs = [in_angs[int((i+in_peak_index)%len(in_angs))] for i in range(0,len(in_angs))]
    out_angs = [out_angs[int((i+out_peak_index)%len(out_angs))] for i in range(0,len(out_angs))]
    in_min_index = [i for i in xrange(len(in_angs)) if in_angs[i] == min(in_angs)][0]
    print in_min_index
    out_min_index = [i for i in xrange(len(out_angs)) if out_angs[i] == min(out_angs)][0]
    print out_min_index

    stretch_indecies = []
    ind_mult = len(in_angs)/len(out_angs)
    for i,val in enumerate(out_angs):
        if i == out_min_index:
            stretch_indecies.append((in_min_index,0.0))
        elif i < out_min_index:
            stretch_indecies.append(find_index_down(val,in_angs))
        elif i > out_min_index:
            stretch_indecies.append(find_index_up(val,in_angs))
    # plt.plot([i/len(in_angs) for i in xrange(0,len(in_angs))],in_angs,'b')
    # plt.hold(True)
    # plt.plot([i/len(out_angs) for i in xrange(0,len(out_angs))],[o+2 for o in out_angs],'r')
    # for i,v in enumerate(out_angs):
    #     try:
    #         xs = [i/len(out_angs),stretch_indecies[i][0]/len(in_angs)]
    #         ys = [v+2,in_angs[stretch_indecies[i][0]]]
    #         plt.plot(xs,ys,'g')
    #     except:
    #         pass
    # plt.show()

    #convert the stretch indecies to relative speed
    v_avg = 1.0/len(out_angs)
    vs = []
    stretch_indecies.append(stretch_indecies[0])
    for i in xrange(0,len(stretch_indecies)-2):
        #print stretch_indecies[i+1]
        d = ((stretch_indecies[i+1][0]+stretch_indecies[i+1][1])-(stretch_indecies[i][0]+stretch_indecies[i][1]))/len(in_angs)
        v_rel = d/v_avg
        vs.append(v_rel)
    rot = (out_peak_index/(len(out_angs)-1))*2*math.pi
    return vs, rot

def find_index_up(val, vals, start=0):
    for i in xrange(start,len(vals)-1):
        if (vals[i]<=val and vals[i+1]>val):
            #linearly interpolate between the two points
            return (i, (val-vals[i])/(vals[i+1]-vals[i]))

def find_index_down(val, vals, start=0):
    for i in xrange(start,len(vals)-1):
        if (vals[i]>=val and vals[i+1]<val):
            #linearly interpolate between the two points
            return (i, (val-vals[i])/(vals[i+1]-vals[i]))

def interpolate_gear(leg):
    #generate an interpolation function for the gear
    pass

def gen_angs(path, leg):
    '''consumes a path and determines leg motion to produce that path, taking the minimum possible distance between any two steps'''
    angs = []
    for p in path:
        d = dist(p,leg.center)
        a = ang(leg.center,p)
        #calculate the side length for semi-triangle
        #a_upper_rel = math.acos(d/(2*leg.upper_length))
        a_upper_rel = circs_to_ang(p,leg)
        a_upper_raw = a+a_upper_rel
        #calculate the angle for the lower leg
        p_mid = (leg.center[0]+leg.upper_length*math.cos(a_upper_raw),
                    leg.center[1]+leg.upper_length*math.sin(a_upper_raw))
        #assert that the distance between the path an p_mid is close to the lower leg length
        assert(abs(dist(p_mid,p)-leg.lower_length)<0.001)
        a_lower_raw = ang(p_mid,p)
        a_lower_rel = a_lower_raw-a_upper_raw
        angs.append((a_upper_raw,a_upper_rel,a_lower_raw,a_lower_rel))
    return angs
