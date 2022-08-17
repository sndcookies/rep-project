# %% Great filters

# 1) Keep longest pattern -> If window is included in bigger window, eliminate

def reframe_window_from_pattern(all_patterns_dict, window_size, pattern_index):
    # Returns the list of primitives forming a window
    true_window_size = window_size + 1
    window_start = all_patterns_dict[f'{window_size}'][pattern_index][0]
    window = list(range(window_start, true_window_size + window_start))      
    return window


def compare_patterns(sim_mat, bp, sp) :                                                               # We're comparing windows not patterns ?
    # Compares 2 lists of primitives, to see if small window is included in bigger window
    
    for i in range(len(bp)-len(sp)) :
        if sim_mat[bp[i]][sp[0]]:                                                                     # First position found
            j = 0
            while j < len(sp) and sim_mat[bp[i+j]][sp[j]] :
                j = j + 1
            if j == len(sp) :
                return True
    return False


def first_filter(all_patterns_dict):                                                                                
    
    nb_window_sizes = len(all_patterns_dict)
    
    for window_size in range (nb_window_sizes - 1):
        print("window_size",window_size,"\n")
        
        nb_sp = len(all_patterns_dict[f'{window_size}'])
        sp_index = 0
        while sp_index < (nb_sp):
            
            nb_bp = len(all_patterns_dict[f'{window_size + 1}'])
            print("nb_bp",nb_bp)
            print("nb_sp", nb_sp)
            print("sp_index",sp_index,"\n")
            for bp_index in range(nb_bp):
                sp_start = all_patterns_dict[f'{window_size}'][sp_index][0]
                bp_start = all_patterns_dict[f'{window_size + 1}'][bp_index][0]
                print("sp_start",sp_start,)
                print("bp_start",bp_start,"\n")
                true_window_size = window_size + 1
                prim_in_sp = list(range(sp_start, true_window_size + sp_start))                          # Create primitives list contained in small pattern window
                prim_in_bp = list(range(bp_start, true_window_size + 1 + bp_start))                      # Create primitives list contained in big pattern window
                
                if compare_patterns(prim_in_bp, prim_in_sp):                                             # If sp is included in bp, delete sp 
                    del all_patterns_dict[f'{window_size}'][sp_index]
                    nb_sp = nb_sp - 1  
                    sp_index = sp_index - 1
                    break;
            sp_index = sp_index + 1 
                                  
    return all_patterns_dict


# %% 2) For every window size, we eliminate patterns that present overlapping windows

def check_overlap(pattern, ws):
    # Checks if input pattern presents overlapping windows    
    for i in range(len(pattern) - 1):
        if (pattern[i+1] - pattern[i]) <= ws :
            return True 


def second_filter(all_patterns_dict):
    
    for window_size in range (len(all_patterns_dict)):                                                    # For every window                 
        nb_patterns_curr_ws = len(all_patterns_dict[f'{window_size}'])  
        pattern_ind = 0   
        
        while pattern_ind < nb_patterns_curr_ws :                                                         # For every pattern   
        
            if check_overlap(all_patterns_dict[f'{window_size}'][pattern_ind], window_size) :
                del all_patterns_dict[f'{window_size}'][pattern_ind]
                nb_patterns_curr_ws = nb_patterns_curr_ws - 1
                pattern_ind = pattern_ind - 1
                
            pattern_ind = pattern_ind + 1
           
                
    return all_patterns_dict


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

def third_filter(all_patterns_dict):
    
    for window_size in range (len(all_patterns_dict)):
        nb_patterns = len(all_patterns_dict[f'{window_size}']) 
        p1_ind = 0
        while p1_ind < (nb_patterns - 1):
            p2_ind = p1_ind + 1
            while p2_ind < nb_patterns:
                p1 = all_patterns_dict[f'{window_size}'][p1_ind]
                p2 = all_patterns_dict[f'{window_size}'][p2_ind]
                w1_start = p1[0]                                        # Create function for this part ? retrace_window(window_size, pattern index)
                w2_start = p2[0]
                
                true_window_size = window_size + 1
                w1 = list(range(w1_start, true_window_size + w1_start))
                w2 = list(range(w2_start, true_window_size + w2_start))
                
                w1 = [(s - w1[0]) % true_window_size for s in w1]
                w2 = [(s - w1[0]) % true_window_size for s in w2]
                       
                if is_circular(w1,w2):                                  # If windows are circularly indentical then delete the pattern with min nb of windows
                    if len(p1)<len(p2):
                        del all_patterns_dict[f'{window_size}'][p1_ind]
                        p1_ind = p1_ind - 1
                        nb_patterns = nb_patterns - 1
                    elif len(p1)>len(p2):
                        del all_patterns_dict[f'{window_size}'][p2_ind]
                        p2_ind = p2_ind - 1
                        nb_patterns = nb_patterns - 1
                p2_ind = p2_ind + 1   
                print(p2_ind)
            p1_ind = p1_ind + 1                          
                
    return all_patterns_dict