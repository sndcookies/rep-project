import lkeypoints
import numpy as np



# %% Start-mid-end representation

# 1) trace_prim gives keypoints per single concrete primitive


def create_start_end_rep(segments):
    
    start_end_rep = {}
    for prim_id in range (len(segments)):   
        x = segments[prim_id][0]
        y = segments[prim_id][1]    
    
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
        start_end_rep[prim_id] = {}
    
        start = ( x[0] , y[0] )
        end = ( x[-1] , y[-1] )
    
        start_end_rep[prim_id]['start'] = start
        start_end_rep[prim_id]['end'] = end
        
    return start_end_rep



# %% Clustering wrt end points 

def clustering_wrt_end_pts(start_end_rep):
    
    nb_primitives = len(start_end_rep)
    direction_dict = {'U' : [],'UR' : [],'R' : [],'DR' : [],'D' : [],'DL' : [],'L' : [],'UL' : []}
    
    for prim_id in range (nb_primitives):
        
        curr_end = start_end_rep[prim_id]['end']
        
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

def create_sim_mat(direction_dict, start_end_rep):
    
    nb_primitives = len(start_end_rep)
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
              


   