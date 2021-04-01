import numpy as np
import os
import moviepy.editor as mp
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from app.configuration import Configuration 

class Animations:
    def __init__(self, angle_list: list, title: str):
        self.angle = angle_list
        self.point_to_show = 3
        self.title = title
    
    def update(self, i):
        new_data = self.angle[i : i + self.point_to_show]
        self.line.set_ydata(new_data)
        return self.line,
    
    def anime_plot(self, fps: int):
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
        
        self.ani = animation.FuncAnimation(fig, self.update, 
                                    frames = len(self.angle) - self.point_to_show, 
                                    interval = fps)
        
        plt.show()
    
    def save_as_gif(self):
        main_path = Configuration()._get_dir('main')
        self.ani.save(main_path + 'animations\\videos\\' + self.title + '.gif', 
                    writer = 'PillowWriter', fps = 30)
    
    def gif_to_mp4(self):
        main_path = Configuration()._get_dir('main')
        os.chdir(main_path + 'animations\\videos\\')
        clip = mp.VideoFileClip(self.title + '.gif')
        clip.write_videofile(self.title + '.mp4')