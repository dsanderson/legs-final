from __future__ import division
import json, os, sys, collections, math
import numpy as np

def leg():
    Leg = collections.namedtuple('Leg',['center','lower_length','upper_length'])
    l = Leg(center=(0,0),lower_length=0.6,upper_length=0.9)
    return l

def path():
    p = gen_path(0.3,(0.5,-0.7))[:-2]
    return p

def gen_path(scale, trans):
    #make a unit ellipse
    npts = 30
    #make a circle
    t = np.linspace(0,2*math.pi,npts)
    xs = [math.cos(ti) for ti in t]
    ys = [math.sin(ti) for ti in t]
    #flatten top by 50%, bottom by 90%
    #ys = [y*0.5 for y in ys]
    ys_temp = []
    for y in ys:
        if y<0.0:
            ys_temp.append(y*0.2)
        else:
            ys_temp.append(y)
    ys = ys_temp
    #ys = [y*0.2 for y in ys if y<0.0]
    xs = [x*scale for x in xs]
    xs = [x+trans[0] for x in xs]
    ys = [y*scale for y in ys]
    ys = [y+trans[1] for y in ys]
    return zip(xs,ys)

def path_2(scale=0.3, trans=(0.5,-0.7)):
    pt_mult = 3
    #create top half
    npt_top = pt_mult*20
    xs_top = [math.cos(math.pi*i/npt_top) for i in range(0, npt_top)]
    ys_top = [0.5*math.sin(math.pi*i/npt_top) for i in range(0, npt_top)]
    #create bottom-left enterence
    npt_bl = pt_mult*5
    xs_bl = [0.1*math.cos(math.pi+((math.pi/2)*i/npt_bl))-0.9 for i in range(0, npt_bl)]
    ys_bl = [0.1*math.sin(math.pi+((math.pi/2)*i/npt_bl)) for i in range(0, npt_bl)]
    #create flat bottom
    npt_b = pt_mult*60
    xs_b = [-0.9+1.8*i/npt_b for i in range(0,npt_b)]
    ys_b = [-0.1 for i in range(0,npt_b)]
    #create bottom-right enterence
    npt_br = pt_mult*5
    xs_br = [0.1*math.cos(3*math.pi/2+((math.pi/2)*i/npt_br))+0.9 for i in range(0, npt_br)]
    ys_br = [0.1*math.sin(3*math.pi/2+((math.pi/2)*i/npt_br)) for i in range(0, npt_br)]

    #assemble
    xs = xs_top+xs_bl+xs_b+xs_br
    ys = ys_top+ys_bl+ys_b+ys_br

    xs = [x*scale for x in xs]
    xs = [x+trans[0] for x in xs]
    ys = [y*scale for y in ys]
    ys = [y+trans[1] for y in ys]

    return zip(xs,ys)
