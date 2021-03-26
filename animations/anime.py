from matplotlib import pyplot as plt
import numpy as np
import matplotlib.animation as animation

class Animations:
    def __init__(self, angle_list: list):
        self.angle = angle_list
        self.point_to_show = 3
    
    def update(self, i):
        new_data = self.angle[i : i + self.point_to_show]
        self.line.set_ydata(new_data)
        return self.line,
    
    def anime_plot(self):
        my_list = self.angle
        
        fig, ax = plt.subplots()
        self.line, = ax.plot(range(self.point_to_show) ,np.zeros(self.point_to_show)*np.NaN, 'ro-')
        ax.set_ylim(min(self.angle) - 5, 180)
        ax.set_xlim(0, self.point_to_show - 1)
        ax.set_title('Animation')
        ax.set(xlabel = 'Frames', ylabel = 'Degrees')
        ax.set_facecolor('silver')
        plt.xticks([])
        plt.grid(True)
        
        ani = animation.FuncAnimation(fig, self.update, 
                                    frames = len(self.angle) - self.point_to_show, 
                                    interval = 30)
        
        plt.show()