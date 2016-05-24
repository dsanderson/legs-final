import ios, motion, plotting

if __name__ == '__main__':
    leg = ios.leg()
    path = ios.path()
    angs = motion.gen_angs(path,leg)
    upper_angs = [a[0] for a in angs]
    lower_angs = [a[3] for a in angs]
    drive_rads, driven_rads, rads, rot = motion.gen_gear(upper_angs,1.0,1.5)
    plotting.plot_gear(drive_rads, driven_rads, rads, rot, 'upper_joint', 1.5)
    drive_rads, driven_rads, rads, rot = motion.gen_gear(lower_angs,1.0,1.5)
    plotting.plot_gear(drive_rads, driven_rads, rads, rot, 'lower_joint', 1.5)
    #plotting.plot_leg_motion(path,leg,ang)
    #plotting.plot_angs(ang)
