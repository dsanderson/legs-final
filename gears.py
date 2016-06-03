from __future__ import division
import math
import svgwrite, plotting
#from svgwrite import cm, mm
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize
import copy, os, tqdm

def write_layers(folder_name, gear, cable_pt = None, is_driven=False):
    shiftx, shifty = find_shift(gear)
    keys = gear.keys()
    for k in tqdm.tqdm(keys):
        fname = os.path.join(folder_name, 'layer_{}.svg'.format(k))
        if k==0:
            write_gear(fname, gear[k], 0.1, shiftx, shifty, 1, cable_pt, is_driven)
        else:
            write_gear(fname, gear[k], 0.1, shiftx, shifty, 1, None, is_driven)

def find_shift(gear):
    shiftx = 0
    shifty = 0
    for k in gear.keys():
        angs = [d[0] for d in gear[k]]
        rads = [d[1] for d in gear[k]]
        xs, ys = plotting.pol2cart(angs, [r for r in rads])
        shiftx = min(shiftx, min(xs))
        shifty = min(shifty, min(ys))
    return -shiftx, -shifty

def write_gear(fname, gear, hole_rad, shiftx, shifty, base_rad_cm=1, cable_pt = None, is_driven=False):
    dwg = svgwrite.Drawing(fname, profile='full')
    cm = 100.0
    if is_driven:
        angs = [d[0] for d in gear]
    else:
        angs = [d[0] for d in gear]
    rads = [d[1] for d in gear]
    xs, ys = plotting.pol2cart(angs, [r*base_rad_cm for r in rads])
    #shiftx = -min(xs)
    #shifty = -min(ys)
    xs = [(x+shiftx)*cm for x in xs]
    ys = [(y+shifty)*cm for y in ys]
    pts = zip(xs,ys)
    for i in xrange(len(pts)-1):
        dwg.add(dwg.line(pts[i],pts[i+1],stroke=svgwrite.rgb(100, 0, 0, '%')))
    dwg.add(dwg.line(pts[-1],pts[0],stroke=svgwrite.rgb(100, 0, 0, '%')))
    dwg.add(dwg.circle(center=(shiftx*cm,shifty*cm),r=hole_rad*cm,stroke=svgwrite.rgb(100, 0, 0, '%')))
    #add verical line through circle
    dwg.add(dwg.line((shiftx*cm,(shifty+hole_rad)*cm),(shiftx*cm,(shifty-hole_rad)*cm),stroke=svgwrite.rgb(100, 0, 0, '%')))
    if cable_pt != None:
        dwg.add(dwg.circle(center=((shiftx+cable_pt[0])*cm,(shifty+cable_pt[1])*cm),r=hole_rad*cm,stroke=svgwrite.rgb(100, 0, 0, '%')))
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

def relax_motion(angs, rotations, R, l, fail_inds, relax_width=math.pi/16, relax_pct = 0.25):
    drive_angs = [o[0] for o in rotations]
    target_dists = [o[1] for o in rotations]
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

def gen_driven_gear(drive_gear, R):
    rads = [d[1] for d in drive_gear]
    angs = [d[0] for d in drive_gear]
    driven_angs = [0]
    driven_rads = [2*R-rads[0]]
    for i in xrange(1,len(rads)):
        d_ang = -((angs[i]-angs[i-1])*rads[i-1])/driven_rads[i-1]
        driven_angs.append(driven_angs[i-1]+d_ang)
        driven_rads.append(2*R-rads[i])
    return zip(driven_angs,driven_rads)

def relax_gear(drive_gear, drive_fails, driven_fails, R, relax_pct = 0.05):
    rads = [d[1] for d in drive_gear]
    angs = [d[0] for d in drive_gear]
    new_rads = copy.deepcopy(rads)
    for i in xrange(len(rads)):
        if i in drive_fails or i in driven_fails:
            diff = rads[i]-(rads[i-1]+rads[(i+1)%len(rads)])/2.0
            diff = diff*relax_pct
            new_rads[i] = rads[i]-diff
    #normalize the new radii
    scale = find_scale(zip(angs, new_rads), R)
    #R/(sum(new_rads)/len(new_rads))
    new_rads = [scale*r for r in new_rads]
    #print sum(new_rads)/len(new_rads)
    #assert(sum(new_rads)/len(new_rads)==R)
    return zip(angs,new_rads)

def find_scale(drive_gear, R):
    '''normalizes the radii of the drive gear to ensure the driven gear rotates 1:1'''
    angs = [d[0] for d in drive_gear]
    rads = [d[1] for d in drive_gear]
    d_angs = [angs[i+1]-angs[i] for i in xrange(0, len(angs)-1)]
    d_angs.append(2*math.pi-angs[-1])
    #print d_angs
    assert(len(d_angs)==len(angs))
    def score_func(x):
        s = x[0]
        score = 0.0
        for i in xrange(len(d_angs)):
            score += (d_angs[i]*rads[i]*s)/(2*R-rads[i]*s)
        return (score-2*math.pi)**2
    #print score_func(0),score_func(1)
    res = scipy.optimize.minimize(score_func, [1.0])
    return res.x

def gen_gear(angs,R=1.0,l=1.5):
    #given the gear radius and output length, calculate the non-normalized change of length as a function of rotation
    ts = np.linspace(0, 2*math.pi, 120)
    raw_angs = []
    for t in ts:
        raw_angs.append(math.sqrt((l-R*math.cos(t))**2+(R*math.sin(t))**2))
    angs = normalize_angs(angs)
    raw_angs = normalize_angs(raw_angs)
    rots, rot = calc_rots(angs,raw_angs)

    d_driven = [rots[i+1][1]-rots[i][1] for i,_ in enumerate(rots[:-1])]
    d_driven.append(2*math.pi-rots[-1][1])
    d_drive = [rots[i+1][0]-rots[i][0] for i,_ in enumerate(rots[:-1])]
    d_drive.append(2*math.pi-rots[-1][0])
    r_drive = [(2*R*d_driven[i])/(d_drive[i]+d_driven[i]) for i in range(len(d_driven))]
    # plt.figure()
    # plt.plot(r_ins)
    # plt.show()
    #produce the drive gear, as a pair (angle, radius)
    drive_gear = []
    for i,r in enumerate(rots):
        drive_gear.append((r[0],r_drive[i]))
    driven_gear = gen_driven_gear(drive_gear,R)
    #produce the driven gear, as a pair (angle, radius)
    #driven_gear = []
    #for i,r in enumerate(rots[:-1]):
#        driven_gear.append((r[1],2*R-r_ins[i]))
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
    #using the previously calculated stretch_indecies, convert to paired relative angles on both gears
    theta_out_in = []
    for i, s in enumerate(stretch_indecies):
        if s!=None:
            t_out = 2*math.pi*(i/len(out_angs))
            t_in = 2*math.pi*(s[0]+s[1])/len(in_angs)
            theta_out_in.append((t_out,t_in))

    rot = (out_peak_index/(len(out_angs)-1))*2*math.pi
    # plt.plot([t[0] for t in theta_out_in],'b')
    # plt.hold(True)
    # plt.plot([t[1] for t in theta_out_in],'r')
    # plt.show()
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

def check_interference(gear_1, gear_2, pose, tooth_rad):
    '''checks if, between gear_1 and gear_2, in pose, there are any interferening points'''
    pass

def splitter(gear, inds):
    '''splits the gear into distinct layers at the indicated indicies'''
    pass

def uniform_splitter(gear, n_layers, is_driven, tooth_gap):
    '''splits the gear into distinct layers by alternating teeth'''
    tooth_list_length = 3
    n_teeth = int(len(gear)/tooth_list_length)
    for i in xrange(0, n_teeth):
        for j in xrange(0, tooth_list_length):
            pass
    layers = {}
    for l in xrange(n_layers):
        layers[l]=[]
    l = 0
    for t in xrange(n_teeth):
        if is_driven:
            extras = []
            norm = []
        else:
            extras = None
        for p in xrange(tooth_list_length):
            #add an escape
            if is_driven:
                norm.append(gear[t*tooth_list_length+p])
                #layers[l].append(gear[t*tooth_list_length+p])
                dang = tooth_gap/gear[t*tooth_list_length][1]
                extras.append((gear[t*tooth_list_length+p][0]+dang, gear[t*tooth_list_length+p][1]))
            else:
                if p==0:
                    new_rad = gear[t*tooth_list_length+p][1]
                    new_ang = gear[t*tooth_list_length+p][0]-math.pi*2/180.0
                    layers[l].append((new_ang, new_rad))
                layers[l].append(gear[t*tooth_list_length+p])
                if p==tooth_list_length-1:
                    new_rad = gear[t*tooth_list_length+p][1]
                    new_ang = gear[t*tooth_list_length+p][0]+math.pi*2/180.0
                    layers[l].append((new_ang, new_rad))
        if is_driven:
            for e in extras:
                layers[l].append(e)
            for n in norm:
                layers[l].append(n)
        l += 1
        l = l%n_layers
    return layers

def rotate_split(gear, ang):
    for k in gear.keys():
        angs = [g[0]+ang for g in gear[k]]
        rads = [g[1] for g in gear[k]]
        gear[k] = zip(angs,rads)
    return gear
