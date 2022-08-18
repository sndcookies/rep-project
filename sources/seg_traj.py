import numpy as np
import criteria
import lglobalvars

def test_criteria(traj, start, end, attribute, parameters):                        # No need for parameters to be a dict right ?
    # For given trajectory, start and end indices, creates a subtrajectory
    # For given attribute, tests if corresponding critera is satisfied on 
    # said trajectory. Returns True if it is, False if it's not.
                                            
    
    if attribute == 'heading':     
        for i in range(start+1, end ):
            x0 = traj[0, i-1]
            x1 = traj[0, i]
            x2 = traj[0, i+1]
            y0 = traj[1, i-1]
            y1 = traj[1, i]
            y2 = traj[1, i+1]
            vector_1 = [ ( x1 - x0 ) ,  ( y1 - y0 ) ]
            vector_2 = [ ( x2 - x1 ) ,  ( y2 - y1 ) ]
            if criteria.angle(vector_1, vector_2) > parameters[0]:
                return False
        return True                                   

def bin_search(traj, start, end):    
    n = len(traj[0])
    
    low = start
    high = end
    mid = 0
    
    while low <= high:
        mid = (high + low) // 2
        t_mid = test_criteria(traj, start, mid, 'heading', [.5])
        t_mid_moins_1 =  test_criteria(traj, start, mid - 1, 'heading', [.5])
        if t_mid_moins_1 and (mid == n-1 or not t_mid):
            return mid
        elif t_mid:
            low = mid + 1            
        else:
            high = mid - 1
            
    return high

def segmentation(traj):
    # Segments trajectory
    
    n = len(traj[0])
    s = 0
    seg_pts = []
    
    while  (s < n-1):
        a = 1

        while (s + a < n) and test_criteria(traj, s, s + a, 'heading', [0.5]):
            a = 2 * a   
            
        j = bin_search(traj, s, min( s + a, n-1))
        seg_pts.append(j)      
        s = j
        
    segments = [] 
    segments.append(traj[:,0:seg_pts[0]])
    
    for i in range (len(seg_pts) - 1) :
        segments.append(traj[:,seg_pts[i]:seg_pts[i+1]])
    segments[-1]= np.concatenate((segments[-1],np.reshape(traj[:,-1],(2,1))),axis=1)                   # Manually adding missing last point    
            
    return segments,seg_pts


# %% Computing concrete primitives 

''' type_fit = "dp_all"
synt_args = {"points_pp": 1, "stat_thres": 0.2, \
            "span_thres": 10, "r_penalty": True, \
            "no_acc": False, "REG": -1, 'cores': 1, \
            "window": 25}
lglobalvars.synt_args = synt_args



for j in range(1) :
    keypoint = {0 : keypoints[j]}
    
    all_prim = lkeypoints.generate_all_primitives(keypoint, type_fit, synt_args)
    print(all_prim)
    # display_funky_primitives(keypoints, 0, base_prim)
    new_keypoints, color_codes = lkeypoints.trace_funky_primitives(all_prim)
        
        
    # color_codes into better better color_codes
color_ind = 0
primitives_start_end_ind = [0]
for i in range (1,len(color_codes)):
    if color_codes[i] != color_codes[i-1]:
        primitives_start_end_ind.append(i)
        primitives_start_end_ind.append(i)
primitives_start_end_ind.append(len(color_codes))'''