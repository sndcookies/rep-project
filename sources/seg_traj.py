import criteria



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
             
    return seg_pts