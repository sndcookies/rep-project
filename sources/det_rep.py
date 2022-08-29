import numpy as np
import copy


# %% Start-end representation

def create_start_end_rep(segments):    
    start_end_rep = {}
    
    for prim_id in range (len(segments)):   
        x = [segments[prim_id][0][0], segments[prim_id][0][-1]]
        y = [segments[prim_id][1][0], segments[prim_id][1][-1]] 
    
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
            
        # Translation
        x = x - x[0]
        y = y - y[0]
    
        # Store start, mid and end points
        start_end_rep[prim_id] = {}    
        start = ( x[0] , y[0] )
        end = ( x[-1] , y[-1] )   
        start_end_rep[prim_id]['start'] = start
        start_end_rep[prim_id]['end'] = end
        
    return start_end_rep, len(start_end_rep)



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

            
def repetition_detection(sim_mat, nb_primitives, window_size_max = 10):
    # Uses similarity matrix in order to extablish repetition detection
    # by comparing windows for each window size    
    all_reps = []    
    for window_size in range(1, window_size_max):       
        nb_windows = nb_primitives - window_size + 1
        reps_for_curr_window_size = np.zeros((nb_windows, nb_windows))       
        for w1_start in range (nb_windows):
            for w2_start in range (nb_windows):
                reps_for_curr_window_size[w1_start, w2_start] = similarity(sim_mat, w1_start, w2_start, window_size)
        all_reps.append(reps_for_curr_window_size)          
    return all_reps 
              
# %% Create pattern dictionary

def fetch_primitives(rep_matrix) :
    patterns_list_curr_window_size = []    
    nb_rows, nb_cols = rep_matrix.shape
    for i in range(nb_rows):
        innerlist = []
        for j in range(nb_cols):
            if rep_matrix[i][j]:
                innerlist.append(j)
        patterns_list_curr_window_size.append(innerlist)
    return patterns_list_curr_window_size
    

def patterns_curr_window_size(rep_matrix):
    # Compares rows of rep_matrix, if they are equal, it means there's a new repetition pattern.
    # Delete all redundant patterns, and rows that contain 0 or 1 window patterns. 
    # Returns resulting list, containing all patterns for one window size.
    
    nb_rows = len(rep_matrix)
    i = 0
    while i < nb_rows :                                                                      # Loop through i rows
        curr_row = np.array(rep_matrix[i])       
        #print('curr_row', curr_row)  
        #print('sum', np.sum(curr_row > 0))                                                            
        if np.sum(curr_row > 0) > 1 :                                                        # If i row is not empty or composed of a single occurence, process :          
            #print('keep')
            j = i + 1
            while j < nb_rows :                                                              # Loop through j rows
                if not (np.mean(abs(rep_matrix[j] - rep_matrix[i]))):                        # If i row and j row contain the same pattern
                    rep_matrix = np.delete(rep_matrix, j, 0)                                 # Delete repeting row (j row)                    
                    j = j - 1
                    nb_rows = len(rep_matrix)                                                                         
                j = j + 1 
            i = i + 1
        
        else :                                                                               # Else delete row 
            #print('delete')
            rep_matrix = np.delete(rep_matrix, i, 0)                                         
            nb_rows = len(rep_matrix)
          
    patterns_list_curr_window_size = fetch_primitives(rep_matrix)                            # Fetch primitives
    return patterns_list_curr_window_size


def create_patterns_dict(all_reps_list):
    nb_window_sizes = len(all_reps_list)
    all_patterns = {}
                    
    for window_size in range(nb_window_sizes):
        rep_matrix = all_reps_list[window_size]
        all_patterns[f'{window_size}'] = patterns_curr_window_size(rep_matrix)
        
    return all_patterns


# %% Great filters

# 1) Keep longest pattern -> If window is included in bigger window, eliminate

def reframe_window_from_pattern(all_patterns, window_size, pattern_index):
    # Returns the list of primitives forming a window
    true_window_size = window_size + 1
    window_start = all_patterns[f'{window_size}'][pattern_index][0]
    window = list(range(window_start, true_window_size + window_start))      
    return window


def compare_patterns(sim_mat, bp, sp) :                                                             
    # Compares 2 lists of primitives, to see if small window is included in bigger window   
    for i in range(len(bp)-len(sp) + 1) :                                                                # IL FAUT RAJOUTER +1 !!!!!!!! 
        if sim_mat[bp[i]][sp[0]]:
            j = 0
            while j < len(sp) and sim_mat[bp[i+j]][sp[j]] :
                j = j + 1
            if j == len(sp) :
                return True
    return False


def first_filter(all_patterns, sim_mat): 
    all_patterns_temp = copy.deepcopy(all_patterns)    
    nb_window_sizes = len(all_patterns_temp)    
    for window_size_sp in range (nb_window_sizes - 1):
        nb_sp = len(all_patterns_temp[f'{window_size_sp}'])
        sp_index = 0      
        while sp_index < (nb_sp):            
            for window_size_bp in range (window_size_sp+1, nb_window_sizes):
                nb_bp = len(all_patterns_temp[f'{window_size_bp}'])
                found_bigger = False
                for bp_index in range(nb_bp):
                    sp_start = all_patterns_temp[f'{window_size_sp}'][sp_index][0]
                    bp_start = all_patterns_temp[f'{window_size_bp}'][bp_index][0]
                    true_window_size_sp = window_size_sp + 1
                    true_window_size_bp = window_size_bp + 1
                    prim_in_sp = list(range(sp_start, true_window_size_sp + sp_start))                     # Create primitives list contained in small pattern window
                    prim_in_bp = list(range(bp_start, true_window_size_bp + bp_start))                     # Create primitives list contained in big pattern window                    
                    
                    '''print('window_size_sp', window_size_sp, 'prim_in_sp',prim_in_sp)
                    print('window_size_bp', window_size_bp, 'prim_in_bp',prim_in_bp)
                    print('include ?', compare_patterns(sim_mat, prim_in_bp, prim_in_sp))'''
                    if compare_patterns(sim_mat, prim_in_bp, prim_in_sp):                                           # If sp is included in bp, delete sp 
                        del all_patterns_temp[f'{window_size_sp}'][sp_index]
                        nb_sp = nb_sp - 1  
                        sp_index = sp_index - 1
                        found_bigger = True
                        break;
                if found_bigger :
                    break;
                    '''
                else :
                    print('window_size_sp', window_size_sp, 'prim_in_sp',prim_in_sp)
                    print('window_size_bp', window_size_bp, 'prim_in_bp',prim_in_bp) '''       
            sp_index = sp_index + 1                                  
    return all_patterns_temp


# %% 2) For every window size, we eliminate patterns that present overlapping windows

def check_overlap(pattern, ws):
    # Checks if input pattern presents overlapping windows    
    for i in range(len(pattern) - 1):
        if (pattern[i+1] - pattern[i]) <= ws :
            return True 


def second_filter(all_patterns):
    
    all_patterns_temp = copy.deepcopy(all_patterns)
    for window_size in range (len(all_patterns_temp)):                                                # For every window                 
        nb_patterns_curr_ws = len(all_patterns_temp[f'{window_size}'])  
        pattern_ind = 0   
        
        while pattern_ind < nb_patterns_curr_ws :                                                     # For every pattern          
            if check_overlap(all_patterns_temp[f'{window_size}'][pattern_ind], window_size) :
                del all_patterns_temp[f'{window_size}'][pattern_ind]
                nb_patterns_curr_ws = nb_patterns_curr_ws - 1
                pattern_ind = pattern_ind - 1    
            pattern_ind = pattern_ind + 1
                         
    return all_patterns_temp

   
# %% 3) If for the same window size, we have the same repetition but in a different order, keep the one with the most windows 

def is_circular(arr1, arr2):
    # Checks if 2 patterns are circularly indentical 
    
    if len(arr1) != len(arr2):
        return False
    str1 = ' '.join(map(str, arr1))
    str2 = ' '.join(map(str, arr2))
    if len(str1) != len(str2):
        return False
    return str1 in str2 + ' ' + str2


def third_filter(all_patterns):
    
    all_patterns_temp = copy.deepcopy(all_patterns)
    for window_size in range (len(all_patterns_temp)):
        nb_patterns = len(all_patterns_temp[f'{window_size}']) 
        
        if nb_patterns :                                                       # debug
            p1_ind = 0
            
            while p1_ind < (nb_patterns - 1):
                p2_ind = p1_ind + 1
                
                while p2_ind < nb_patterns:
                    #print('p1_ind', p1_ind)
                    #print('p1', all_patterns_temp[f'{window_size}'][p1_ind])
                    p1 = all_patterns_temp[f'{window_size}'][p1_ind]
                    p2 = all_patterns_temp[f'{window_size}'][p2_ind]
                    w1_start = p1[0]                                        # Create function for this part ? retrace_window(window_size, pattern index)
                    w2_start = p2[0]
                  
                    true_window_size = window_size + 1
                    w1 = list(range(w1_start, true_window_size + w1_start))
                    w2 = list(range(w2_start, true_window_size + w2_start))
                    
                    w1 = [(s - w1[0]) % true_window_size for s in w1]
                    w2 = [(s - w1[0]) % true_window_size for s in w2]
                           
                    if is_circular(w1,w2):                                  # If windows are circularly indentical then delete the pattern with min nb of windows
                        if len(p1)<len(p2):
                            del all_patterns_temp[f'{window_size}'][p1_ind]
                            p1_ind = p1_ind - 1
                            nb_patterns = nb_patterns - 1
                        elif len(p1)>len(p2):
                            del all_patterns_temp[f'{window_size}'][p2_ind]
                            p2_ind = p2_ind - 1
                            nb_patterns = nb_patterns - 1
                    p2_ind = p2_ind + 1   
                p1_ind = p1_ind + 1                          
                
    return all_patterns_temp