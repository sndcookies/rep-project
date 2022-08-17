import numpy as np
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../sources')
import create_synthetic_signals
import seg_traj
import visu




traj_size = 11
traj = create_synthetic_signals.synthetic_traj(traj_size)
[segments,seg_pts] = seg_traj.segmentation(traj)
print(seg_pts)  
visu.plot_seg_result(segments,'heading')
