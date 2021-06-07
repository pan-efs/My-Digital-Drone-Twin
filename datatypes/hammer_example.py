import os, sys, argparse

from joints_list import JointsList
from filters.moving_average import MovingAverage as MovingAverage
from biomechanics.biomechanics3D import Slope

# Starting point
frozen = 'not'
if getattr(sys, 'frozen', False):
    frozen = 'even so'
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Flag for analysis
parser = argparse.ArgumentParser(description = 'Provide the flag.')
parser.add_argument('--flag', type = str,
                    help = '--cubemos or --cubemos_converter',
                    required = False)
parser.add_argument('--file', type = str,
                    help = 'Provide the directory of a 3D clean text file.',
                    required = False)
args = parser.parse_args()

# Get the path according to the flag
if args.file and args.flag:
    raise NotImplementedError

if args.flag:
    if args.flag == 'cubemos_converter':
        jl = JointsList(BASE_DIR + '/cubemos_converter/logging/get_3d_joints_from_video.txt',
                    BASE_DIR + '/datatypes/logging/clean_3d_from_video.txt')
        jLs = jl.__return__()
    elif args.flag == 'cubemos':
        jl = JointsList(BASE_DIR + '/cubemos/logging/get_3d_joints.txt',
                BASE_DIR + '/datatypes/logging/clean_3d.txt')
        jLs = jl.__return__()

if args.file:
    jl = JointsList(args.file,
                BASE_DIR + '/datatypes/logging/clean_3d.txt')
    jLs = jl.__return__()

################################################################
#--------------------------------------------------------------#
#--------------------------------------------------------------#
################################################################

# Get all body joints
joints = []

for i in range(0, len(jLs), 3):
    x = jl._converter_to_list(jLs[i], jLs[i+1], jLs[i+2])
    joints.append(x)

# Moving average filtering
mvg = MovingAverage()

# Right lower body side
mvg_rh_x = mvg.moving_average(jLs[24],6)
mvg_rh_y = mvg.moving_average(jLs[25],6)
mvg_rh_z = mvg.moving_average(jLs[26],6)

mvg_rk_x = mvg.moving_average(jLs[27],6)
mvg_rk_y = mvg.moving_average(jLs[28],6)
mvg_rk_z = mvg.moving_average(jLs[29],6)

mvg_ra_x = mvg.moving_average(jLs[30],6)
mvg_ra_y = mvg.moving_average(jLs[31],6)
mvg_ra_z = mvg.moving_average(jLs[32],6)

# Left lower body side
mvg_lh_x = mvg.moving_average(jLs[33],6)
mvg_lh_y = mvg.moving_average(jLs[34],6)
mvg_lh_z = mvg.moving_average(jLs[35],6)

mvg_lk_x = mvg.moving_average(jLs[36],6)
mvg_lk_y = mvg.moving_average(jLs[37],6)
mvg_lk_z = mvg.moving_average(jLs[38],6)

mvg_la_x = mvg.moving_average(jLs[39],6)
mvg_la_y = mvg.moving_average(jLs[40],6)
mvg_la_z = mvg.moving_average(jLs[41],6)

# Create list for moving average filtered data
mvg_right_knee, mvg_left_knee, mvg_right_ankle, mvg_left_ankle = ([] for i in range(4))

for i in range(0, len(mvg_rk_x)):
    mvg_a9 = [mvg_rk_x[i], mvg_rk_y[i], mvg_rk_z[i]]
    mvg_right_knee.append(mvg_a9)

for i in range(0, len(mvg_lk_x)):
    mvg_a12 = [mvg_lk_x[i], mvg_lk_y[i], mvg_lk_z[i]]
    mvg_left_knee.append(mvg_a12)

for i in range(0, len(mvg_ra_x)):
    mvg_a10 = [mvg_ra_x[i], mvg_ra_y[i], mvg_ra_z[i]]
    mvg_right_ankle.append(mvg_a10)

for i in range(0, len(mvg_la_x)):
    mvg_a13 = [mvg_la_x[i], mvg_la_y[i], mvg_la_z[i]]
    mvg_left_ankle.append(mvg_a13)

# Slopes
sl = Slope()

ankle_length, knee_length = ([] for i in range(2))
print(len(mvg_right_ankle), len(mvg_left_ankle))
print(len(mvg_right_knee), len(mvg_left_knee))

for i in range(0, len(mvg_right_ankle[:417])):
    xy, xz, yz, length = sl.three_dim_slopes(mvg_right_ankle[i], mvg_left_ankle[i])
    ankle_length.append(length)
    
    _xy, _xz, _yz, _length = sl.three_dim_slopes(mvg_right_knee[i], mvg_left_knee[i])
    knee_length.append(_length)

# Erase the content and write the new ones
# Knees
knee_dist_file = open('logging/knee_distances.txt', 'w').close()
knee_dist_file = open('logging/knee_distances.txt', 'w')

for i in knee_length:
    knee_dist_file.write(str(i) + '\n')
knee_dist_file.close()

# Ankles
ankle_dist_file = open('logging/ankle_distances.txt', 'w').close()
ankle_dist_file = open('logging/ankle_distances.txt', 'w')

for i in ankle_length:
    ankle_dist_file.write(str(i) + '\n')
ankle_dist_file.close()