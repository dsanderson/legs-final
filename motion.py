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

def gen_gear(angs,R=1.0,l=1.5):
    #given the gear radius and output length, calculate the non-normalized change of length as a function of rotation
    ts = np.linspace(0, 2*math.pi, 120)
    raw_angs = []
    for t in ts:
        raw_angs.append(math.sqrt((l-R*math.cos(t))**2+(R*math.sin(t))**2))
    raw_angs = normalize_angs(raw_angs)
    rots, rot = calc_rots(angs,raw_angs)
    #print vs
    #convert relative velocities into matched gear sets, and their initial rotation
    # rads = [(rot+(2*math.pi*i/len(vs)))%(2*math.pi) for i in range(0,len(vs))]
    # drive_rads = [2*r/(v+1) for v in vs]
    # driven_rads = [(2*r)-rad for rad in drive_rads]
    #print rots
    d_out = [rots[i+1][0]-rots[i][0] for i,_ in enumerate(rots[:-1])]
    d_in = [rots[i+1][1]-rots[i][1] for i,_ in enumerate(rots[:-1])]
    r_ins = [(2*R*d_out[i])/(d_in[i]+d_out[i]) for i in range(len(d_out))]
    # plt.figure()
    # plt.plot(r_ins)
    # plt.show()
    #produce the drive gear, as a pair (angle, radius)
    drive_gear = []
    for i,r in enumerate(rots[:-1]):
        drive_gear.append((r[0],r_ins[i]))
    #produce the driven gear, as a pair (angle, radius)
    driven_gear = []
    for i,r in enumerate(rots[:-1]):
        driven_gear.append((r[1],2*R-r_ins[i]))
    rotations = rots
    return drive_gear, driven_gear, rotations, rot



def normalize_angs(angs):
    #normalize the change in length from zero to one
    raw_angs = copy.deepcopy(angs)
    trans = min(raw_angs)
    raw_angs = [a-trans for a in raw_angs]
    scale = max(raw_angs)
    raw_angs = [a/scale for a in raw_angs]
    return raw_angs

def calc_rots(out_angs, in_angs):
    out_angs = normalize_angs(out_angs)
    in_angs = normalize_angs(in_angs)
    in_peak_index = [i for i in xrange(len(in_angs)) if in_angs[i] == max(in_angs)][0]
    #print in_peak_index
    out_peak_index = [i for i in xrange(len(out_angs)) if out_angs[i] == max(out_angs)][0]
    #print out_peak_index

    #rotate in_angs to match out_angs
    in_angs = [in_angs[int((i+in_peak_index)%len(in_angs))] for i in range(0,len(in_angs))]
    out_angs = [out_angs[int((i+out_peak_index)%len(out_angs))] for i in range(0,len(out_angs))]
    in_min_index = [i for i in xrange(len(in_angs)) if in_angs[i] == min(in_angs)][0]
    #print in_min_index
    out_min_index = [i for i in xrange(len(out_angs)) if out_angs[i] == min(out_angs)][0]
    #print out_min_index

    stretch_indecies = [(0,0.0)]
    #extend out_angs and in_angs by 1

    for i,val in enumerate(out_angs[1:]):
        if i == out_min_index:
            stretch_indecies.append((in_min_index,0.0))
        elif i < out_min_index:
            stretch_indecies.append(find_index_down(val,in_angs))
        elif i > out_min_index:
            stretch_indecies.append(find_index_up(val,in_angs))
    # plt.figure()
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

    #using the previously calculated stretch_indecies, convert to paired relative angles on both gears
    theta_out_in = []
    for i, s in enumerate(stretch_indecies):
        if s!=None:
            t_out = 2*math.pi*(i/len(out_angs))
            t_in = 2*math.pi*(s[0]+s[1])/len(in_angs)
            theta_out_in.append((t_out,t_in))
    #plot the two angles
    # plt.figure()
    # plt.hold(True)
    # plt.plot([t[0] for t in theta_out_in],'b')
    # plt.plot([t[1] for t in theta_out_in],'r')
    # plt.show()


    # #convert the stretch indecies to relative speed
    # v_avg = 1.0/len(out_angs)
    # vs = []
    # #stretch_indecies.append(stretch_indecies[0])
    # stretch_indecies.append((len(in_angs),0.0))
    # print stretch_indecies, len(stretch_indecies)
    # for i in xrange(0,len(stretch_indecies)-1):
    #     #print stretch_indecies[i+1]
    #     d = ((stretch_indecies[i+1][0]+stretch_indecies[i+1][1])-(stretch_indecies[i][0]+stretch_indecies[i][1]))/len(in_angs)
    #     v_rel = d/v_avg
    #     vs.append(v_rel)
    rot = (out_peak_index/(len(out_angs)-1))*2*math.pi
    return theta_out_in, rot

def find_index_up(val, vals, start=0):
    for i in xrange(start,len(vals)-1):
        if (vals[i]<=val and vals[i+1]>val):
            #linearly interpolate between the two points
            return (i, (val-vals[i])/(vals[i+1]-vals[i]))
    #print val

def find_index_down(val, vals, start=0):
    for i in xrange(start,len(vals)-1):
        if (vals[i]>=val and vals[i+1]<val):
            #linearly interpolate between the two points
            return (i, (val-vals[i])/(vals[i+1]-vals[i]))
    #print val, 'down'

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
