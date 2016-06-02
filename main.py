import ios, motion, plotting, os, gears, tooth
import tqdm, os

if __name__ == '__main__':
    leg = ios.leg()
    path = ios.path_2()
    angs = motion.gen_angs(path,leg)
    upper_angs = [a[0] for a in angs]
    lower_angs = [a[3] for a in angs]
    #plotting.plot_leg_motion(path,leg,angs, n_frames = 30)
    #plotting.plot_angs(angs)
    u_drive_rads, u_driven_rads, u_rads, u_rot = gears.gen_gear(upper_angs,1.0,1.5)
    #plotting.plot_gear(u_drive_rads, u_driven_rads, u_rads, u_rot, 'upper_joint', 1.5)
    l_drive_rads, l_driven_rads, l_rads, l_rot = gears.gen_gear(lower_angs,1.0,1.5)
    #plotting.plot_gear(l_drive_rads, l_driven_rads, l_rads, l_rot, 'lower_joint', 1.5)
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
    fpath = os.path.join(os.getcwd(),'imgs')
    l_fouts = []
    u_fouts = []
    for i in tqdm.tqdm(xrange(0,50)):
        l_inds_drive = gears.check_interior_angle(l_drive_rads)
        l_inds_driven = gears.check_interior_angle(l_driven_rads)
        l_out_motion = gears.calc_out_motion(l_drive_rads, l_driven_rads,1.0,1.5,l_inds_drive+l_inds_driven)
        # l_fout = os.path.join(fpath,'l_{}.png'.format(i))
        # l_fouts.append(l_fout)
        # plotting.plot_manufacturability(l_drive_rads,l_driven_rads,l_inds_drive+l_inds_driven,l_out_motion, 2.0,'lower',l_fout)
        l_drive_rads = gears.relax_gear(l_drive_rads,l_inds_drive,l_inds_driven,1.0)
        l_driven_rads = gears.gen_driven_gear(l_drive_rads,1.0)

        # u_inds_drive = gears.check_interior_angle(u_drive_rads)
        # u_inds_driven = gears.check_interior_angle(u_driven_rads)
        # u_out_motion = gears.calc_out_motion(u_drive_rads, u_driven_rads,1.0,1.5,u_inds_drive+u_inds_driven)
        # # u_fout = os.path.join(fpath,'u_{}.png'.format(i))
        # # u_fouts.append(u_fout)
        # # plotting.plot_manufacturability(u_drive_rads,u_driven_rads,u_inds_drive+u_inds_driven,u_out_motion, 2.0,'lower',u_fout)
        # u_drive_rads = gears.relax_gear(u_drive_rads,u_inds_drive,u_inds_driven,1.0)
        # u_driven_rads = gears.gen_driven_gear(u_drive_rads,1.0)

    #gen the gif
    # out_img = os.path.join(fpath,'compiled','lower_manufacturability.gif')
    # plotting.make_gif(l_fouts, out_img, 5)
    # out_img = os.path.join(fpath,'compiled','upper_manufacturability.gif')
    # plotting.make_gif(u_fouts, out_img, 5)
    # plotting.plot_gear(l_drive_rads, l_driven_rads, l_rads, l_rot, 'lower_joint', 1.5)
    # plotting.plot_gear(u_drive_rads, u_driven_rads, u_rads, u_rot, 'upper_joint', 1.5)

    #plotting.plot_manufacturability(l_driven_rads,inds_drive+inds_driven)
    #gears.relax_motion(out_motion, 1.0, 1.5, inds_drive+inds_driven)
    tooth.test_tootherpolate(l_drive_rads, l_driven_rads,100)
