import ios, motion, plotting, os, gears

if __name__ == '__main__':
    leg = ios.leg()
    path = ios.path_2()
    angs = motion.gen_angs(path,leg)
    upper_angs = [a[0] for a in angs]
    lower_angs = [a[3] for a in angs]
    #plotting.plot_leg_motion(path,leg,angs, n_frames = 30)
    #plotting.plot_angs(angs)
    u_drive_rads, u_driven_rads, rads, rot = gears.gen_gear(upper_angs,1.0,1.5)
    #plotting.plot_gear(drive_rads, driven_rads, rads, rot, 'upper_joint', 1.5)
    l_drive_rads, l_driven_rads, rads, rot = gears.gen_gear(lower_angs,1.0,1.5)
    #plotting.plot_gear(drive_rads, driven_rads, rads, rot, 'lower_joint', 1.5)
    # hole_rad = 0.5
    # fname_path = os.getcwd()
    # fname_path = os.path.join(fname_path,'imgs','compiled')
    # fname = os.path.join(fname_path, 'upper_drive.svg')
    # gears.write_gear(fname,u_drive_rads,hole_rad)
    #
    # fname = os.path.join(fname_path, 'upper_driven.svg')
    # gears.write_gear(fname,u_driven_rads,hole_rad)
    #
    # fname = os.path.join(fname_path, 'lower_drive.svg')
    # gears.write_gear(fname,l_drive_rads,hole_rad)
    #
    # fname = os.path.join(fname_path, 'lower_driven.svg')
    # gears.write_gear(fname,l_driven_rads,hole_rad)
    for i in xrange(0,3):
        inds_drive = gears.check_interior_angle(l_drive_rads)
        inds_driven = gears.check_interior_angle(l_driven_rads)
        out_motion = gears.calc_out_motion(l_drive_rads, l_driven_rads,1.0,1.5,inds_drive+inds_driven)
        plotting.plot_manufacturability(l_drive_rads,l_driven_rads,inds_drive+inds_driven,out_motion)
        l_driven_rads = gears.gen_driven_gear(l_drive_rads,1.0)
        out_motion = gears.calc_out_motion(l_drive_rads, l_driven_rads,1.0,1.5,inds_drive+inds_driven)
        plotting.plot_manufacturability(l_drive_rads,l_driven_rads,inds_drive+inds_driven,out_motion)
        l_drive_rads = gears.relax_gear(l_drive_rads,inds_drive,inds_driven,1.0)
        l_driven_rads = gears.gen_driven_gear(l_drive_rads,1.0)

    #plotting.plot_manufacturability(l_driven_rads,inds_drive+inds_driven)
    #gears.relax_motion(out_motion, 1.0, 1.5, inds_drive+inds_driven)
