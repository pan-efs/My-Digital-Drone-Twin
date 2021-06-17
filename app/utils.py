import os, pickle, subprocess
import pyqtgraph as pg

def _get_base_dir():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return BASE_DIR

def add_line(graphWidget, position):
    new_line = graphWidget.addLine(
                                x = position, 
                                pen = pg.mkPen(color= 'g', width = 2), 
                                angle = 90, 
                                movable = False
                            )
    return new_line

def graph_length(base_dir:str, screen: str):
    if screen == 'Yes':
        folder = 'cubemos'
        txt = 'get_3d_joints.txt'
    else:
        folder = 'cubemos_converter'
        txt = 'write_3d_joints_from_video.txt'
    
    _dir = f'{base_dir}/{folder}/logging/{txt}'
    graph = open(_dir, 'r').readlines()
    
    graph_len = len(graph)/18
    
    print(graph_len)
    
    return graph_len

def radiobutton_toggled(base_dir: str, radiobutton1, radiobutton2, radiobutton3, combobox):
    if radiobutton1.isDown():
        windows_size_changed(base_dir, 3)
        combobox.setCurrentText('None')
        return 3
    elif radiobutton2.isDown():
        windows_size_changed(base_dir, 6)
        combobox.setCurrentText('None')
        return 6
    elif radiobutton3.isDown():
        windows_size_changed(base_dir, 9)
        combobox.setCurrentText('None')
        return 9
    else:
        windows_size_changed(base_dir, 12)
        combobox.setCurrentText('None')
        return 12

def plot_cases(base_dir:str, graphWidget, combobox):
        txt = combobox.currentText()
        
        if txt == 'Distances':
            graphWidget.clear()
            
            knees_dir = f'{base_dir}/datatypes/logging/knee_distances.txt'
            with open(knees_dir, 'rb') as knees:
                kn_lines = pickle.load(knees)
            
            ankles_dir = f'{base_dir}/datatypes/logging/ankle_distances.txt'
            with open(ankles_dir, 'rb') as ankles:
                an_lines = pickle.load(ankles)
            
            pen_kn = pg.mkPen(color= 'r', width = 4)
            pen_an = pg.mkPen(color= 'b', width = 4)
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            graphWidget.setLabel('left', 'meters', **styles)
            graphWidget.setLabel('bottom', 'frames', **styles)
            graphWidget.addLegend()
            graphWidget.setRange(xRange = (0, max(len(an_lines), len(an_lines))), yRange = (0, max(max(kn_lines), max(an_lines))))
            graphWidget.plot(kn_lines, name = 'Knees', pen = pen_kn)
            graphWidget.plot(an_lines, name = 'Ankles', pen = pen_an)
            
        
        elif txt == 'Knees Magnitude':
            graphWidget.clear()
            
            knee_dir_R = f'{base_dir}/datatypes/logging/knee_right_mag.txt'
            with open(knee_dir_R, 'rb') as knee_R:
                kn_lines_R = pickle.load(knee_R)
            
            knee_dir_L = f'{base_dir}/datatypes/logging/knee_left_mag.txt'
            with open(knee_dir_L, 'rb') as knee_L:
                kn_lines_L = pickle.load(knee_L)
            
            pen_kn_r = pg.mkPen(color= 'r', width = 4)
            pen_kn_l = pg.mkPen(color= 'b', width = 4)
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            graphWidget.setLabel('left', 'magnitude', **styles)
            graphWidget.setLabel('bottom', 'frames', **styles)
            graphWidget.addLegend()
            graphWidget.setRange(xRange = (0, len(kn_lines_R)), yRange = (0, max(max(kn_lines_R), max(kn_lines_L))))
            graphWidget.plot(kn_lines_R, name = 'Knee right', pen = pen_kn_r)
            graphWidget.plot(kn_lines_L, name = 'Knee left', pen = pen_kn_l)
        
        elif txt == 'Ankles Magnitude':
            graphWidget.clear()
            
            ankle_dir_R = f'{base_dir}/datatypes/logging/ankle_right_mag.txt'
            with open(ankle_dir_R, 'rb') as ankle_R:
                an_lines_R = pickle.load(ankle_R)
            
            ankle_dir_L = f'{base_dir}/datatypes/logging/ankle_left_mag.txt'
            with open(ankle_dir_L, 'rb') as ankle_L:
                an_lines_L = pickle.load(ankle_L)
            
            pen_an_r = pg.mkPen(color= 'r', width = 4)
            pen_an_l = pg.mkPen(color= 'b', width = 4)
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            graphWidget.setLabel('left', 'magnitude', **styles)
            graphWidget.setLabel('bottom', 'frames', **styles)
            graphWidget.addLegend()
            graphWidget.setRange(xRange = (0, len(an_lines_R)), yRange = (0, max(max(an_lines_R), max(an_lines_L))))
            graphWidget.plot(an_lines_R, name = 'Ankle right', pen = pen_an_r)
            graphWidget.plot(an_lines_L, name = 'Ankle left', pen = pen_an_l)
        
        elif txt == 'None':
            graphWidget.clear()

def windows_size_changed(base_dir: str, wsize: int):
    os.chdir(f'{base_dir}/datatypes')
    retcode = subprocess.call(f'python processing.py --wsize {wsize}', shell = True)
    
    if retcode == 0:
        print('Windows size changed to', wsize)
    else:
        raise NotImplementedError