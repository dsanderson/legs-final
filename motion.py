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
