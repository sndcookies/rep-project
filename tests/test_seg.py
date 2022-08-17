import numpy as np
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../sources')
import seg_traj
import visu


def synthetic_traj(traj_size):

    traj = np.zeros((2,traj_size))
    
    for i in range (traj_size//2):
        traj[0,i] = i
        traj[1,i] = i
    
    for i in range (traj_size//2, traj_size ):
        traj[0,i] = i
        traj[1,i] = traj_size - i - 1
    
    traj = traj.astype(int) 
    traj = np.concatenate((traj[:,0:-1],traj),axis=1)
    traj[0, traj_size -1 :2  * traj_size] = traj[0, traj_size -1  :2   * traj_size] + traj_size -1
        
    
    return traj


traj_size = 11
traj = synthetic_traj(traj_size)
[segments,seg_pts] = seg_traj.segmentation(traj)
print(seg_pts)  
visu.plot_seg_result(segments,'heading')
