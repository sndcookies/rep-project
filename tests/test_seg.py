import numpy as np
from scipy.signal import savgol_filter
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../sources')
import create_synthetic
import seg_traj
import visu



def cat_traj(time, signal):
    return np.reshape(np.concatenate((time,signal)),(2,len(time)))

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def test_seg(time, signal, signal_title = ''):
    visu.plot_synthetic(signal, time, signal_title, 1)
    traj = cat_traj(time, signal)
    [segments,seg_pts] = seg_traj.segmentation(traj)  
    print( f"{signal_title} segmentation points :", seg_pts)
    visu.plot_seg_result(segments, seg_pts, 'heading')
    

# %% Triangle

traj_size = 11
traj = create_synthetic.triangle(traj_size)
[segments,seg_pts] = seg_traj.segmentation(traj)  
visu.plot_seg_result(segments, seg_pts,'heading')


# %% Testing noisy stationary signal 

end = 100
line_block, time_line = create_synthetic.create_line_block(0, end-1, end, 0, 5)
visu.plot_synthetic(line_block, time_line, 'line block')
noisy_line = create_synthetic.add_noise(line_block, 0, .1)
test_seg(time_line, noisy_line, 'Noisy line')


# %% Smoothing 1st try

smooth_noisy_line_1 = smooth(noisy_line,50)
test_seg(time_line, smooth_noisy_line_1, 'Smoothed noisy line 1st try')

# %% Smoothing 2nd try

smooth_noisy_line_2 = savgol_filter(noisy_line, 51, 3) # window size 51, polynomial order 3
test_seg(time_line, smooth_noisy_line_2, 'Smoothed noisy line 1nd try')



# %% Testing sinusoidal 

sinusoid, time = create_synthetic.sinusoid()
test_seg(time, sinusoid, 'Sinusoid')

# %%
noisy_sinusoid = create_synthetic.add_noise(sinusoid, 0, .1)
test_seg(time, sinusoid, 'Noisy sinusoid')