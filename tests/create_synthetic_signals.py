import numpy as np


# %% Round block

def create_round_block(amp, freq = 2/9, initial_nb_pts = 50, end = 5, offset1 = 0, offset2 = 0):
    
    time = np.linspace(0, end, initial_nb_pts)         
    sinusoid = amp*np.sin(2*np.pi*freq*time) + offset1              # sinusoïde de base
    
    index = np.where(sinusoid[1:-1] < offset2)                      # tronquer le signal au premier offset    
    nb_pts = index[0][0] + 1
    round_block = np.append(sinusoid[0:nb_pts - 1], offset2)    
    
    return round_block


# %% Line block

def create_line_block(a, b, initial_nb_pts = 50, end = 5): 
    
    time = time = np.linspace(0, end-1, end)  
    line_block = a * time + b
     
    return line_block


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
    
    return signal, time


# %% Let's handcraft 

def generate_signal_manually():
    
    block1 = create_round_block(60, offset1 = -10, offset2 = -5, end = 5)
    block2 = - create_round_block(20, offset1 = 5, offset2 = 2, end = 10)    
    block3 = create_round_block(15, offset1 = 5, offset2 = 2, initial_nb_pts = 100, end = 50)
    block4 = create_line_block(0, 2, 50, 20)
    block5 = create_round_block(10, offset1 = 2, offset2 =5 , initial_nb_pts = 100, end = 50)
    block6 = create_round_block(55, offset1 = 5, offset2 = 0, end = 4)
    block7 = create_line_block(0.5, 0, 50, 10)
    block8 =  create_round_block(20, offset1 = 5, offset2 = -10)
    
    synthetic_signal = np.concatenate([block1, block2, block3, block4, block5, block6, block7, block8])    
    for i in range(2):
        synthetic_signal = np.concatenate([synthetic_signal,synthetic_signal])
        
        return synthetic_signal
    
