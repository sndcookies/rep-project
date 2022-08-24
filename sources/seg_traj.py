import numpy as np
import criteria
  
def test_criteria(traj, start, end, attribute, parameters):                        
    # For given trajectory, start and end indices, creates a subtrajectory
    # For given attribute, tests if corresponding critera is satisfied on 
    # said trajectory. Returns True if it is, False if it's not.
    
    centroid = [np.mean(traj[0, start:end]), np.mean(traj[1, start:end])]
    stationary = True
    for i in range (start, end):
        if np.linalg.norm(traj[:,i] - centroid) > parameters[0]:
            stationary = False
    
    if stationary :   
        return True                                            
        
    if attribute == 'heading':     
        for i in range(start+1, end):
            x0 = traj[0, i-1]
            x1 = traj[0, i]
            x2 = traj[0, i+1]
            y0 = traj[1, i-1]
            y1 = traj[1, i]
            y2 = traj[1, i+1]
            vector_1 = [ ( x1 - x0 ) ,  ( y1 - y0 ) ]
            vector_2 = [ ( x2 - x1 ) ,  ( y2 - y1 ) ]
            if criteria.angle(vector_1, vector_2) > parameters[1]:
                return False
        return True

    elif attribute == 'improved_heading':
        if start + parameters[1] < min(end, len(traj[0])- 1- parameters[1]):
            for i in range(start+parameters[1], min(end,len(traj[0])-parameters[1])):
                x1 = traj[0, i-parameters[1]:i]
                y1 = traj[1, i-parameters[1]:i]
                a1, b1, fitting_error = criteria.fitting_error(x1, y1)

                x_2 = traj[0, i:i+parameters[1]]
                y_2 = traj[1, i:i+parameters[1]]
                a2, b2, fitting_error = criteria.fitting_error(x_2, y_2)

                vector_1 = [ ( x1[-1] - x1[0] ) ,  ( a1 * x1[-1] + b1 - a1 * x1[0] + b1 ) ]
                vector_2 = [ ( x_2[-1] - x_2[0] ) ,  ( a2 * x_2[-1] + b2 - a2 * x_2[0] + b2 ) ]
                
                if criteria.angle(vector_1, vector_2) > parameters[2]:
                    return False
        return True

    elif attribute == 'fitting_error':
        if end - start <= 4:
            print('< 2', 'end', end)
            return True
        a, b, fitting_error = criteria.fitting_error(traj[0, start:end], traj[1, start:end])
        if fitting_error > parameters[1]:
            return False
        else:
            return True
        
        
# %%   
                                      
def bin_search(traj, start, end, seg_criteria, parameters):    
    n = len(traj[0])   
    low = start
    high = end
    mid = 0
    
    while low <= high:
        mid = (high + low) // 2
        t_mid = test_criteria(traj, start, mid, seg_criteria, parameters)
        t_mid_moins_1 =  test_criteria(traj, start, mid - 1, seg_criteria, parameters)
        if t_mid_moins_1 and (mid == n-1 or not t_mid):
            return mid
        elif t_mid:            
            low = mid + 1  
        else:           
            high = mid - 1    
    return mid


# %% 

def segmentation(traj, seg_criteria, parameters):
    # Segments trajectory
    
    n = len(traj[0])
    s = 0
    seg_pts = []
    
    while  (s < n-1):
        a = 1

        while (s + a < n) and test_criteria(traj, s, s + a, seg_criteria, parameters):
            a = 2 * a   
           
        j = bin_search(traj, s, min( s + a, n-1), seg_criteria, parameters)   
        seg_pts.append(j-1)      
        s = j
        
    segments = [] 
    segments.append(traj[:, 0:seg_pts[0]])
    
    for i in range (len(seg_pts) - 1) :
        segments.append(traj[:,seg_pts[i]:seg_pts[i+1]])
    segments[-1]= np.concatenate((segments[-1],np.reshape(traj[:,-1],(2,1))),axis=1)                   # Manually adding missing last point    
            
    return segments,seg_pts

