import sys
import numpy as np
import scipy 
import scipy.ndimage
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../sources')
import create_synthetic
import det_rep
import visu
import seg_traj


def cat_traj(time, signal):
    return np.reshape(np.concatenate((time,signal)),(2,len(time)))

def test_seg(time, signal, signal_title, seg_criteria, parameters):
    visu.plot_synthetic(time, signal, signal_title, 0)
    traj = cat_traj(time, signal)
    [segments,seg_pts] = seg_traj.segmentation(traj, seg_criteria, parameters)      
    #visu.plot_seg_result(segments, seg_pts, seg_criteria)
    visu.display_fitted_line(segments)
    print( f"{signal_title} segmentation points :", seg_pts)
    return segments, seg_pts

def test_rep(segments):
    # Start_end representations
    start_end_rep, nb_primitives = det_rep.create_start_end_rep(segments)
    
    # Repetition detection
    direction_dict = det_rep.clustering_wrt_end_pts(start_end_rep)
    sim_mat = det_rep.create_sim_mat(direction_dict, start_end_rep)
    all_reps = det_rep.repetition_detection(sim_mat, nb_primitives, window_size_max)
    all_patterns = det_rep.create_patterns_dict(all_reps)
    
    # Filtrage
    after_second_filter = det_rep.second_filter(all_patterns)   
    after_first_filter = det_rep.first_filter(after_second_filter, sim_mat)   
    after_third_filter = det_rep.third_filter(after_first_filter)
    visu.repetition_display(after_third_filter, segments) 
    visu.rep_display_with_fitted_line(after_third_filter, segments)
    return after_third_filter, all_patterns


# %% Parameters
stat_thresh = 5
neigh_thresh = 15
criteria_thresh = 0.7
seg_criteria = 'improved_heading'

window_size_max = 10
cube_name = 'Rocking_000000000000_no_smoothing'
kp = 1   
# %% Handcrafted
x, y = create_synthetic.generate_signal_manually()
visu.plot_synthetic(x, y, 'Handcrafted', 1)
segments, seg_pts = test_seg(x, y, 'Handcrafted', seg_criteria, [stat_thresh, neigh_thresh, criteria_thresh])
final_result_handcrafted, all_patterns = test_rep(segments)


# %% Real signal | Keypoint : Nose

path = 'C:\\Users\\Salma Ferjani\\Dev\\rep_project\\data\\data_cubes\\' + cube_name + '.mat'                    # Use os.path.join()
x_init, y_init = seg_traj.load_data_cube(path, kp)
visu.plot_synthetic(x_init, y_init, 'Signal original', 0)
#traj = scipy.signal.medfilt2d((np.vstack((x_init,y_init))), kernel_size=3)
#traj = scipy.signal.medfilt(np.vstack((x_init,y_init)), kernel_size=3)
traj = scipy.ndimage.median_filter(np.vstack((x_init,y_init)),3)
xr = traj[0,:]
yr = traj[1,:]
visu.plot_synthetic(xr, yr, 'Signal après smoothing', 0)
#segments_r, seg_pts_r = test_seg(xr, yr, cube_name, seg_criteria, [stat_thresh, neigh_thresh, criteria_thresh])
#final_result, all_patterns = test_rep(segments_r)

# %%
x_synth, y_synth = create_synthetic.build_signal_blocks( [['funky_line', [10,5,150,20,20]],                                 # Attention double list [[]]
                    ['stationary', [150, 20, 8]], ['funky_line', [10,150,10,20,200]],
                    ['stationary', [10, 200, 10]], ['funky_line', [10,10,170,200,200] ] ], 10)

segments, seg_pts = test_seg(x_synth, y_synth, 'Synthetic', seg_criteria, [stat_thresh, neigh_thresh, criteria_thresh])
