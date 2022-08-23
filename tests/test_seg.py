import numpy as np
from scipy.signal import savgol_filter
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../sources')
import create_synthetic
import seg_traj
import visu





def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def cat_traj(time, signal):
    return np.reshape(np.concatenate((time,signal)), (2, len(time)))

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
seg_criteria = 'fitting_error'   

# %% Triangle

traj_size = 11
traj = create_synthetic.triangle(traj_size)
[segments,seg_pts] = seg_traj.segmentation(traj, seg_criteria, [stat_thresh, criteria_thresh])   
visu.plot_seg_result(segments, seg_pts, seg_criteria)


# %% Testing noisy stationary signal 
'''
end = 100
time_line, line_block = create_synthetic.line_block(0, end-1, end, 0, 5)
visu.plot_synthetic(line_block, time_line, 'line block')
noisy_line = create_synthetic.add_noise(time_line, line_block, 3)
segments, seg_pts = test_seg(time_line, noisy_line, 'Noisy line', seg_criteria, [stat_thresh, criteria_thresh])

'''


# %% Testing sinusoidal 

sinusoid, time_sin = create_synthetic.sinusoid()
segments, seg_pts = test_seg(time_sin, sinusoid, 'Sinusoid', seg_criteria, [stat_thresh,criteria_thresh])


# %%
noisy_sinusoid = create_synthetic.add_noise(sinusoid, time_sin, 4)
segments, seg_pts = test_seg(time_sin, sinusoid, 'Noisy sinusoid', seg_criteria, [stat_thresh,criteria_thresh])

# %% Synthetic

time1, block1 = create_synthetic.funky_line(100,5,150,200,200)
time3, block3 = create_synthetic.funky_line(100,5,170,200,20)
time4, block4 = create_synthetic.funky_line(120,170,10,20,20)
time2, block2 = create_synthetic.stationary(10, 200, 20)
time2, block2 = create_synthetic.add_noise(time2, block2, 20)
time5, block5 = create_synthetic.stationary(170, 20, 20)
time5, block5 = create_synthetic.add_noise(time5, block5, 20)
synth_signal = list(block1) + list(block2) + list(block3) + list(block4) + list(block5) 
synth_time = list(time1) + list(time2) + list(time3)+ list(time4) + list(time5) 
segments, seg_pts = test_seg(synth_time, synth_signal, 'Synthetic', seg_criteria, [stat_thresh,criteria_thresh])


# %% Synthetic

x_synth, y_synth = create_synthetic.build_signal_blocks( [['funky_line', [10,5,150,20,20]],                                 # Attention double list [[]]
                    ['stationary', [150, 20, 8]], ['funky_line', [10,150,10,20,200]],
                    ['stationary', [10, 200, 10]], ['funky_line', [10,10,170,200,200] ] ], 10)

segments, seg_pts = test_seg(x_synth, y_synth, 'Synthetic', seg_criteria, [stat_thresh,criteria_thresh])

# %% Synthetic random

x_synth, y_synth = create_synthetic.build_signal_blocks( [], 2)

segments, seg_pts = test_seg(x_synth, y_synth, 'Synthetic', seg_criteria, [stat_thresh,criteria_thresh])
visu.display_fitted_line(segments)