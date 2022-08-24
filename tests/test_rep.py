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

# %% Parameters
criteria_thresh = 10
stat_thresh = 5
seg_criteria = 'heading'


# %%

x_synth, y_synth = create_synthetic.build_signal_blocks( [['funky_line', [10,5,150,20,20]],                                 # Attention double list [[]]
                    ['stationary', [150, 20, 8]], ['funky_line', [10,150,10,20,200]],
                    ['stationary', [10, 200, 10]], ['funky_line', [10,10,170,200,200] ] ], 10)

segments, seg_pts = test_seg(x_synth, y_synth, 'Synthetic', seg_criteria, [stat_thresh,criteria_thresh])