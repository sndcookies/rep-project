import matplotlib.pyplot as plt   
import numpy as np



plt.close('all')

def uniqueish_color():  
    """There're better ways to generate unique colors, but this isn't awful."""
    return plt.cm.gist_ncar(np.random.random())

def plot_traj(traj):
    
    plt.figure
    plt.plot(traj[0,:], traj[1,:])
    plt.show()
    
def scatter_traj(traj):
    
    plt.figure
    plt.scatter(traj[0,:], traj[1,:])
    plt.show()
    
def plot_seg_result(segments, criterion = 'default'):
    plt.figure()
    for i in range (len(segments)):
        plt.plot(segments[i][0,:], segments[i][1,:], color=uniqueish_color())
        
    plt.title(f"Segments obtained with {criterion} criterion") 
    plt.show()    
        
        
        
    