import numpy as np
from rep_project.sources import seg_traj


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


def test_synthetic():
    traj = synthetic_traj(11)
    cutting_points = seg_traj.segmentation(traj)
    print(cutting_points)
    
test_synthetic()