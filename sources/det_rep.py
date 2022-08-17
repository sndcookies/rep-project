import lkeypoints
import numpy as np



# %% Start-mid-end representation

# 1) trace_prim gives keypoints per single concrete primitive


def create_start_mid_end_rep(all_prim):
    all_prim['0'] = all_prim[0]
    kp = 0
    abstract_discrete_primitives = {}
    concrete_primitives = []
    
    for prim_id in range(len(all_prim[kp])):
    
        # Store times and ptypes if needed
        prim_time = all_prim[str(kp)][prim_id][-2]
        prim_type = all_prim[str(kp)][prim_id][-1]
    
        single_primitives = lkeypoints.trace_prim(all_prim[str(kp)][prim_id], prim_time)
        concrete_primitives.append(single_primitives)
    
        # x and y are structured as lists of nb_prim arrays
        x = []
        y = []
    
        for point_id in range(len(single_primitives)):
            x.append(single_primitives[point_id][0])
            y.append(single_primitives[point_id][1])
            
    
        # Switching to arrays for broadcasting and such
        x = np.array(x)
        y = np.array(y)
        
    
        # Normalization
        max_x = np.max(x)
        max_y = np.max(y)
        min_x = np.min(x)
        min_y = np.min(y)
        
        if (max_x == min_x):
            x = np.zeros((len(x)))
        else :
            x = (x - min_x) / (max_x - min_x)
            
        if (max_y == min_y):
            y = np.zeros((len(y)))
        else :
            y = (y - min_y) / (max_y - min_y)
            
        print ('x =', x)
        print ('y =', y)
            
    
        # Translation
        x = x - x[0]
        y = y - y[0]
    
        # Store start, mid and end points
        abstract_discrete_primitives[prim_id] = {}
    
        start = ( x[0] , y[0] )
        mid = ( x[(len(single_primitives)-1)//2] , y[(len(single_primitives)-1)//2])
        end = ( x[-1] , y[-1] )
    
        abstract_discrete_primitives[prim_id]['start'] = start
        abstract_discrete_primitives[prim_id]['mid'] = mid
        abstract_discrete_primitives[prim_id]['end'] = end
        
    return abstract_discrete_primitives



# %% Clustering wrt end points 

def clustering_wrt_end_pts(abstract_discrete_primitives):
    
    nb_primitives = len(abstract_discrete_primitives)
    direction_dict = {'U' : [],'UR' : [],'R' : [],'DR' : [],'D' : [],'DL' : [],'L' : [],'UL' : []}
    
    for prim_id in range (nb_primitives):
        
        curr_end = abstract_discrete_primitives[prim_id]['end']
        
        if curr_end[1] == 1 :
            y_direction = 'U'
        elif curr_end[1] == -1 :
            y_direction = 'D'
        else :
            y_direction = ''
            
            
        if curr_end[0] == 1 :
            x_direction = 'R'
        elif curr_end[0] == -1 :
            x_direction = 'L'
        else :
            x_direction = ''
            
        if  y_direction + x_direction != '':
            direction_dict[ y_direction + x_direction ].append(prim_id)
            
        return direction_dict
  
  
  
# %% Switching into similarity matrix for easier implementation 

def create_sim_mat(direction_dict, abstract_discrete_primitives):
    
    nb_primitives = len(abstract_discrete_primitives)
    sim_mat = np.zeros((nb_primitives, nb_primitives))
    
    for value in direction_dict.values():    
        for p1 in value:
            for p2 in value:
                sim_mat[p1][p2] = 1
    
    return sim_mat



# %% Repetition detection 
           
def similarity(sim_mat, w1_start, w2_start, window_size):
    # Returns True if two windows of same size are similar 
    sim = True
    for i in range(window_size):
        if not sim_mat[w1_start + i][w2_start + i] :
            sim = False
    
    return sim

            
def repetition_detection(sim_mat, nb_primitives, window_size_max):
    # Uses similarity matrix in order to extablish repetition detection
    # by comparing windows for each window size
    
    all_reps = []
    
    for window_size in range(1, window_size_max):
        
        nb_windows = nb_primitives - window_size + 1
        reps_for_curr_window_size = np.zeros((nb_windows, nb_windows))
        
        for w1_start in range (nb_windows):
            for w2_start in range (nb_windows):
                reps_for_curr_window_size[w1_start, w2_start] = similarity(sim_mat, w1_start, w2_start, window_size)
    
                #print (reps_for_curr_window_size)
        all_reps.append(reps_for_curr_window_size)
            
    return all_reps 
              


   