import matplotlib.pyplot as plt   
import numpy as np


def uniqueish_color():  
    """There're better ways to generate unique colors, but this isn't awful."""
    return plt.cm.gist_ncar(np.random.random())


def plot_traj(traj):    
    plt.figure
    plt.plot(traj[0,:], traj[1,:])
    plt.show()
    
    
def plot_synthetic(signal, time, title = '', close_all = 0):
    if close_all:
        plt.close('all')   
    plt.figure
    plt.plot(time, signal)
    plt.title(title)
    plt.ylim([min(signal) - 10 , max(signal) + 10])
    plt.show()
    
    
def scatter_traj(traj):    
    plt.figure
    plt.scatter(traj[0,:], traj[1,:])
    plt.show()
    
    
def plot_seg_result(segments, seg_pts, criterion = 'default'):
    plt.figure()
    for i in range (len(segments)):
        plt.plot(segments[i][0,:], segments[i][1,:], color=uniqueish_color())
        
    
    flatten_list = list(np.concatenate(segments, axis =1). flat )
    nb_elem = len(flatten_list)
    x_list = flatten_list[0:int(nb_elem/2)]
    y_list = flatten_list[int(nb_elem/2):int(nb_elem)]
    max_y = max(y_list)
    min_y = min(y_list)    
    for i in seg_pts:        
        plt.annotate('seg point', xy =(i, y_list[i]),
                 xytext =(i, y_list[i]),
                 arrowprops = dict(facecolor ='black',
                                   shrink = 4), )
    plt.ylim([min_y -5 , max_y + 5])
    plt.title(f"Segments obtained with {criterion} criterion")
    plt.show()    
    
    
def display_concrete_primitives(keypoints, kdx, new_keypoints, primitives_start_end_ind):
       
    nb_frames = len(keypoints[kdx])
    
    x_ref = []
    y_ref = []
    x_prim = []
    y_prim = []
    for i in range(nb_frames) :
       x_ref.append(keypoints[kdx][i][0])
       y_ref.append(keypoints[kdx][i][1])
       x_prim.append(new_keypoints[kdx][i][0])
       y_prim.append(new_keypoints[kdx][i][1])
    
    plt.figure()                
    plt.subplot(211)             
    plt.plot(x_ref,y_ref)
    plt.subplot(212)             
    for i in range(0,len(primitives_start_end_ind),2) :
        plt.plot(x_prim[primitives_start_end_ind[i]:primitives_start_end_ind[i+1]], 
                 y_prim[primitives_start_end_ind[i]:primitives_start_end_ind[i+1]], 
                 color=uniqueish_color())
  
    plt.show()   
        

def start_mid_end_display(abs_prim, title = '') :
   
    nb_prim = len(abs_prim)
    x = []
    y = []
    for j in range(nb_prim) :
        x.append(abs_prim[j]["start"][0])
        y.append(abs_prim[j]["start"][1])
        x.append(abs_prim[j]["mid"][0])
        y.append(abs_prim[j]["mid"][1])
        x.append(abs_prim[j]["end"][0])
        y.append(abs_prim[j]["end"][1])
   
    for i in range(0,len(x),3) :
        plt.scatter(x[i:i+3], y[i:i+3], color=uniqueish_color())
 
    plt.title(title)
    plt.show()


def matrix_display(mat):
    # Used to display matrices such as sim_mat and patterns
    plt.figure()        
    plt.imshow(mat, interpolation='nearest')
    plt.show()  

        
def curr_pattern_display(window_size, all_patterns_dict, pattern_index, concrete_primitives): 
# Displays all windows from the pattern
# The primitives of each window must be same color 
    pattern = all_patterns_dict[f'{window_size}'][pattern_index]
    true_window_size = window_size + 1
    x_plot = []
    y_plot = []    
    plt.figure()
    for window_start in pattern:
        x_temp = []
        y_temp = []
        for prim in range(window_start, window_start + true_window_size):
            x_temp = x_temp + (list(list(zip(*concrete_primitives[prim]))[0]))                      # Coordinates forming every primitive in current window
            y_temp = y_temp + (list(list(zip(*concrete_primitives[prim]))[1]))           
        x_plot.append(x_temp)
        y_plot.append(y_temp)   
    nb_rows = len(x_plot)        
    for i in range(nb_rows): 
        plt.plot(x_plot[i], y_plot[i], color=uniqueish_color())
        plt.title(f"Window size = {true_window_size} | Pattern = {pattern_index} " )           
    plt.show()
    

def repetition_display(all_patterns_dict):
# Displays all repetitions 
    nb_window_sizes = len(all_patterns_dict)
    for window_size in range (nb_window_sizes):
        nb_patterns = len(all_patterns_dict[f'{window_size}'])
        for pattern_index in range (nb_patterns):
            curr_pattern_display(window_size, all_patterns_dict, pattern_index)
            
        
                    
    