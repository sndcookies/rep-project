import numpy as np
import random



def add_noise(x, y, l):
    
    nb_pts = len(x)
    x = np.array(x)
    y = np.array(y)
    x_noise = x + np.random.randint(-l/2, l/2, nb_pts) 
    y_noise = y + np.random.randint(-l/2, l/2, nb_pts) 
    
    return x_noise, y_noise

# %%
def sinusoid(freq = 2, amp = 2, start = 0, stop = 5, nb_samples = 1000):
    time = np.linspace(0, 5, 1000)    
    return amp*np.sin(2*np.pi*freq*time), time


# %%
def stationary(x0, y0, nb_pts = 20):
    x = [x0] * nb_pts
    y = [y0] * nb_pts
    return np.array(x), np.array(y)

# %% Line block

def line_block(start, stop, nb_samples, a, b): 
    
    time = np.linspace(start, stop, nb_samples, True)  
    line_block = a * time + b
     
    return time, line_block


# %% Funky line

def funky_line(nb_samples = 1, t_start = 0, t_end = 0, s_start = 0, s_end = 0):
    
    time = np.linspace(t_start, t_end, nb_samples)
    signal = np.linspace(s_start, s_end, nb_samples) 
        
    return time, signal


# %% Round block

def round_block(amp, freq = 2/9, initial_nb_pts = 50, end = 5, offset1 = 0, offset2 = 0):
    
    time = np.linspace(0, end, initial_nb_pts)         
    sinusoid = amp*np.sin(2*np.pi*freq*time) + offset1              # sinusoïde de base
    
    index = np.where(sinusoid[1:-1] < offset2)                      # tronquer le signal au premier offset    
    nb_pts = index[0][0] + 1
    round_block = np.append(sinusoid[0:nb_pts - 1], offset2)    
    
    return round_block


# %% Build signal blocks

# args = [[round_block, 100] , [line_block, 200]]
def build_signal_blocks(args, nb_blocks):
    
    signal = np.empty(0)
    time = np.empty(0)
    for i in range(nb_blocks):
        for block in args :
            signal = np.append(signal,block[0])
            print(block)
            nb_pts = len(block[0])  
            
            start = 0
            if len(time) != 0 :
                start = time[-1]
                
            time = np.append(time, np.linspace(start, start + block[1], nb_pts))  # step should be interchangeable 
    
    return time, signal 


# %% Let's handcraft 

def generate_signal_manually():
    
    block1 = round_block(60, offset1 = -10, offset2 = -5, end = 5)
    block2 = - round_block(20, offset1 = 5, offset2 = 2, end = 10)    
    block3 = round_block(15, offset1 = 5, offset2 = 2, initial_nb_pts = 100, end = 50)
    time, block4 = line_block(0, 2, 50, 20)
    block5 = round_block(10, offset1 = 2, offset2 =5 , initial_nb_pts = 100, end = 50)
    block6 = round_block(55, offset1 = 5, offset2 = 0, end = 4)
    time, block7 = line_block(0.5, 0, 50, 10)
    block8 =  round_block(20, offset1 = 5, offset2 = -10)
    
    synthetic_signal = np.concatenate([block1, block2, block3, block4, block5, block6, block7, block8])    
    for i in range(2):
        synthetic_signal = np.concatenate([synthetic_signal,synthetic_signal])
        nb_pts = len(synthetic_signal)
        time_vector = np.linspace(0, nb_pts-1, nb_pts)
        
        return time_vector, synthetic_signal
    
# %% Triangle synthetic traj for segmentation testing
    
def triangle(traj_size):

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

# %%
def build_signal_blocks(args, noise_mag = 0):
    
    y = []
    x = []
    
    
    for block_info in args:
    
        param = block_info[1]
        if block_info[0] == 'stationary':    
            curr_x, curr_y = stationary(param[0], param[1], param[2])            
        elif block_info[0] == 'funky_line':
            curr_x, curr_y = funky_line(param[0], param[1], param[2], param[3], param[4])    
        x = x + list(curr_x)   
        y = y + list(curr_y)
    
    if not args :
        nb_blocks = random.randint(5, 10)
        stat = False
        x_prev = random.randint(-50, 50)
        y_prev = random.randint(-50, 50)
        for i in range(nb_blocks):
            block_type = random.randint(0, 10)
            if not stat and block_type > 8 :
                stat = True
                curr_x, curr_y = stationary(x_prev, y_prev, random.randint(5, 10))
            else:
                stat = False
                x_last = random.randint(-50, 50)
                y_last = random.randint(-50, 50)
                curr_x, curr_y = funky_line(random.randint(8, 15), x_prev, x_last, y_prev, y_last)
                x_prev = x_last
                y_prev = y_last
                
            x = x + list(curr_x)   
            y = y + list(curr_y)
    
    if noise_mag :    
        x, y = add_noise(x, y, noise_mag)
        
    return x, y