import sys
import numpy as np
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../sources')
import create_synthetic
import det_rep
import visu
import seg_traj


def cat_traj(time, signal):
    return np.reshape(np.concatenate((time,signal)),(2,len(time)))

def test_seg(time, signal, signal_title, seg_criteria, parameters):
    visu.plot_synthetic(time, signal, signal_title, 1)
    traj = cat_traj(time, signal)
    [segments,seg_pts] = seg_traj.segmentation(traj, seg_criteria, parameters)  
    print( f"{signal_title} segmentation points :", seg_pts)
    visu.plot_seg_result(segments, seg_pts, seg_criteria)
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
    
    return after_third_filter, all_patterns


# %% Parameters
stat_thresh = 1
neigh_thresh = 5
criteria_thresh = 0.7
seg_criteria = 'improved_heading'

window_size_max = 10

# %% Handcrafted
x, y = create_synthetic.generate_signal_manually()
visu.plot_synthetic(x, y, 'Handcrafted', 1)
segments, seg_pts = test_seg(x, y, 'Handcrafted', seg_criteria, [stat_thresh, neigh_thresh, criteria_thresh])
final_result_handcrafted = test_rep(segments)


# %% Real signal : HeadBanging_20_data | Keypoint : Nose

xr, yr = seg_traj.load_data_cube(r'C:\Users\Salma Ferjani\Dev\rep_project\data\data_cubes\HeadBanging_20_data.mat', 1)
visu.plot_synthetic(xr, yr, 'HeadBanging_20', 1)
segments_r, seg_pts_r = test_seg(xr, yr, 'HeadBanging_20', seg_criteria, [stat_thresh, neigh_thresh, criteria_thresh])
final_result_HeadBanging_20, all_patterns = test_rep(segments_r)
