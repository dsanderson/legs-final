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
