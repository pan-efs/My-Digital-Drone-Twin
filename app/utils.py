import os, pickle, subprocess, shutil
import pyqtgraph as pg

from datatypes.joints import JointsList
from datatypes.utils.helpers import magnitude

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

def add_plot(graphWidget, data, joint_number):
    new_plot = graphWidget.plot(
                                data,
                                name = f'joint_{joint_number}',
                                pen = pg.mkPen(width = 2),
    )
    
    return new_plot

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

def windows_size_changed(base_dir: str, wsize: int):
    os.chdir(f'{base_dir}/datatypes')
    retcode = subprocess.call(f'python processing.py --wsize {wsize}', shell = True)
    
    if retcode == 0:
        print('Windows size changed to', wsize)
    else:
        raise NotImplementedError

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

def copy_text_file(base_dir: str):
    source = f'{base_dir}/datatypes/logging/all_joints_clean_3d.txt'
    dest = os.path.expanduser("~/Desktop")
    shutil.copy2(source, dest)

def magnitude_all_joints(base_dir: str, event: str):
    if event == 'Yes':
        print('all joints cubemos')
        jl = JointsList(f'{base_dir}/cubemos/logging/get_3d_joints.txt',
                    f'{base_dir}/datatypes/logging/all_joints_clean_3d.txt')
        jLs = jl.__return__()
        copy_text_file(base_dir)
        
    elif event == 'No':
        print('all joints cubemos_converter')
        jl = JointsList(f'{base_dir}/cubemos_converter/logging/write_3d_joints_from_video.txt',
                    f'{base_dir}/datatypes/logging/all_joints_clean_3d.txt')
        jLs = jl.__return__()
        copy_text_file(base_dir)
        
    elif event.endswith('.txt'):
        print('all joints text')
        jl = JointsList(event,
                    f'{base_dir}/datatypes/logging/all_joints_clean_3d.txt')
        jLs = jl.__return__()
    
    magnitude_jLs = []
    
    for i in range(0, 54, 3):
        magnitude_jLs.append(list(map(magnitude, jLs[i], jLs[i + 1], jLs[i + 2])))
    
    return magnitude_jLs

def plot_all_joints(base_dir: str, graphWidget, event: str):
    _joints = magnitude_all_joints(base_dir, event)
    
    styles = {
            'color': '#000000', 
            'font-size': '20px',
            }
    
    graphWidget.setLabel('left', 'non filter-magnitude', **styles)
    graphWidget.setLabel('bottom', 'frames', **styles)
    legend = graphWidget.addLegend()
    
    # Face, chest
    nose = graphWidget.plot(_joints[0], name = 'nose', pen = pg.mkPen(color = (255,102,102), width = 2))
    sternum = graphWidget.plot(_joints[1], name = 'sternum', pen = pg.mkPen(color = (255,178,102), width = 2))
    
    # Upper body
    shoulder_r = graphWidget.plot(_joints[2], name = 'shoulder_r', pen = pg.mkPen(color = (255,255,102), width = 2))
    elbow_r = graphWidget.plot(_joints[3], name = 'elbow_r', pen = pg.mkPen(color = (178,255,102), width = 2))
    wrist_r = graphWidget.plot(_joints[4], name = 'wrist_r', pen = pg.mkPen(color = (102,178,102), width = 2))
    
    shoulder_l = graphWidget.plot(_joints[5], name = 'shoulder_l', pen = pg.mkPen(color = (102,255,178), width = 2))
    elbow_l = graphWidget.plot(_joints[6], name = 'elbow_l', pen = pg.mkPen(color = (102,255,178), width = 2))
    wrist_l = graphWidget.plot(_joints[7], name = 'wrist_l', pen = pg.mkPen(color = (102,255,255), width = 2))
    
    # Lower body
    hip_r = graphWidget.plot(_joints[8], name = 'hip_r', pen = pg.mkPen(color = (102,178,255), width = 2))
    knee_r = graphWidget.plot(_joints[9], name = 'knee_r', pen = pg.mkPen(color = (102,102,255), width = 2))
    ankle_r = graphWidget.plot(_joints[10], name = 'ankle_r', pen = pg.mkPen(color = (178,102,255), width = 2))
    
    hip_l = graphWidget.plot(_joints[11], name = 'hip_l', pen = pg.mkPen(color = (255,102,255), width = 2))
    knee_l = graphWidget.plot(_joints[12], name = 'knee_l', pen = pg.mkPen(color = (255,102,178), width = 2))
    ankle_l = graphWidget.plot(_joints[13], name = 'ankle_l', pen = pg.mkPen(color = (192,192,192), width = 2))
    
    # No eyes and ears
    
    return legend, nose, sternum, shoulder_r, elbow_r, wrist_r, shoulder_l, elbow_l, wrist_l, hip_r, knee_r, ankle_r, hip_l, knee_l, ankle_l

def hide_joint(graphWidget, legend, joint):
    graphWidget.removeItem(joint)
    legend.removeItem(joint)

def show_joint(graphwidget, joint):
    graphwidget.addItem(joint)

def hide_joints_from_plot_cases(graphWidget_all, legend_all, checkboxes: list):
    if checkboxes[0].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[1])
    else:
        show_joint(graphWidget_all, legend_all[1])
                
    if checkboxes[1].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[2])
    else:
        show_joint(graphWidget_all, legend_all[2])
        
    if checkboxes[2].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[3])
    else:
        show_joint(graphWidget_all, legend_all[3])
    
    if checkboxes[3].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[4])
    else:
        show_joint(graphWidget_all, legend_all[4])
    
    if checkboxes[4].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[5])
    else:
        show_joint(graphWidget_all, legend_all[5])
    
    if checkboxes[5].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[6])
    else:
        show_joint(graphWidget_all, legend_all[6])
    
    if checkboxes[6].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[7])
    else:
        show_joint(graphWidget_all, legend_all[7])
    
    if checkboxes[7].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[8])
    else:
        show_joint(graphWidget_all, legend_all[8])
    
    if checkboxes[8].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[9])
    else:
        show_joint(graphWidget_all, legend_all[9])
    
    if checkboxes[9].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[10])
    else:
        show_joint(graphWidget_all, legend_all[10])
    
    if checkboxes[10].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[11])
    else:
        show_joint(graphWidget_all, legend_all[11])
    
    if checkboxes[11].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[12])
    else:
        show_joint(graphWidget_all, legend_all[12])
    
    if checkboxes[12].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[13])
    else:
        show_joint(graphWidget_all, legend_all[13])
    
    if checkboxes[13].isChecked():
        hide_joint(graphWidget_all, legend_all[0], legend_all[14])
    else:
        show_joint(graphWidget_all, legend_all[14])
