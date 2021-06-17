import os, argparse, pickle

from joints import JointsDataframe, JointsNumpys, JointsList
from utils.helpers import xyz_to_list, magnitude
from filters.moving_average import MovingAverage as MovingAverage
from biomechanics.biomechanics3D import Slope

# Starting point
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except:
    raise OSError

# Flag for analysis
parser = argparse.ArgumentParser(description = 'Provide flag or file.')
parser.add_argument('--flag', type = str,
                    help = '--cubemos or --cubemos_converter',
                    required = False)
parser.add_argument('--file', type = str,
                    help = 'Provide the directory of a 3D joints text file.',
                    required = False)
parser.add_argument('--wsize', type = int,
                    help = 'Provide moving average filter window size.',
                    default = 6,
                    required = False)
args = parser.parse_args()

# Get the path according to the flag
if args.file and args.flag:
    raise NotImplementedError

if args.flag:
    if args.flag == 'cubemos_converter':
        print('reading from cubemos_converter')
        jl = JointsList(f'{BASE_DIR}/cubemos_converter/logging/write_3d_joints_from_video.txt',
                    f'{BASE_DIR}/datatypes/logging/clean_3d.txt')
        jLs = jl.__return__()
    elif args.flag == 'cubemos':
        print('reading from cubemos')
        jl = JointsList(f'{BASE_DIR}/cubemos/logging/get_3d_joints.txt',
                f'{BASE_DIR}/datatypes/logging/clean_3d.txt')
        jLs = jl.__return__()

if args.file:
    print('reading from text file')
    jl = JointsList(args.file,
                f'{BASE_DIR}/datatypes/logging/clean_3d.txt')
    jLs = jl.__return__()

if not args.flag and not args.file:
    print('reading from after_filter')
    jl = JointsList(f'{BASE_DIR}/datatypes/logging/clean_3d.txt',
                f'{BASE_DIR}/datatypes/logging/set_joints_after_filter.txt')
    jLs = jl.__return__()


# Get all body joints
# Moving average filtering
mvg = MovingAverage()

# Right lower body side
mvg_rh_x = mvg.moving_average(jLs[24], args.wsize)
mvg_rh_y = mvg.moving_average(jLs[25], args.wsize)
mvg_rh_z = mvg.moving_average(jLs[26], args.wsize)

mvg_rk_x = mvg.moving_average(jLs[27], args.wsize)
mvg_rk_y = mvg.moving_average(jLs[28], args.wsize)
mvg_rk_z = mvg.moving_average(jLs[29], args.wsize)

mvg_ra_x = mvg.moving_average(jLs[30], args.wsize)
mvg_ra_y = mvg.moving_average(jLs[31], args.wsize)
mvg_ra_z = mvg.moving_average(jLs[32], args.wsize)

# Left lower body side
mvg_lh_x = mvg.moving_average(jLs[33], args.wsize)
mvg_lh_y = mvg.moving_average(jLs[34], args.wsize)
mvg_lh_z = mvg.moving_average(jLs[35], args.wsize)

mvg_lk_x = mvg.moving_average(jLs[36], args.wsize)
mvg_lk_y = mvg.moving_average(jLs[37], args.wsize)
mvg_lk_z = mvg.moving_average(jLs[38], args.wsize)

mvg_la_x = mvg.moving_average(jLs[39], args.wsize)
mvg_la_y = mvg.moving_average(jLs[40], args.wsize)
mvg_la_z = mvg.moving_average(jLs[41], args.wsize)

# Create list for moving average filtered data
mvg_right_knee = list(map(xyz_to_list, mvg_rk_x, mvg_rk_y, mvg_rk_z))
pos_right_knee = list(map(magnitude, mvg_rk_x, mvg_rk_y, mvg_rk_z))

mvg_left_knee = list(map(xyz_to_list, mvg_lk_x, mvg_lk_y, mvg_lk_z))
pos_left_knee = list(map(magnitude, mvg_lk_x, mvg_lk_y, mvg_lk_z))

mvg_right_ankle = list(map(xyz_to_list, mvg_ra_x, mvg_ra_y, mvg_ra_z))
pos_right_ankle = list(map(magnitude, mvg_ra_x, mvg_ra_y, mvg_ra_z))

mvg_left_ankle = list(map(xyz_to_list, mvg_la_x, mvg_la_y, mvg_la_z))
pos_left_ankle = list(map(magnitude, mvg_la_x, mvg_la_y, mvg_la_z))

# Slopes
sl = Slope()

ankle_length = list(map(sl.three_dim_slopes, mvg_right_ankle, mvg_left_ankle))
knee_length = list(map(sl.three_dim_slopes, mvg_right_knee, mvg_left_knee))

# Erase the content and write the new ones
# Knees distance
open('logging/knee_distances.txt', 'wb').close()
with open('logging/knee_distances.txt', 'wb') as F:
    pickle.dump(knee_length, F)

# Ankles distance
open('logging/ankle_distances.txt', 'wb').close()
with open('logging/ankle_distances.txt', 'wb') as F:
    pickle.dump(ankle_length, F)

# Knees magnitudes
open('logging/knee_right_mag.txt', 'wb').close()
with open('logging/knee_right_mag.txt', 'wb') as F:
    pickle.dump(pos_right_knee, F)

open('logging/knee_left_mag.txt', 'wb').close()
with open('logging/knee_left_mag.txt', 'wb') as F:
    pickle.dump(pos_left_knee, F)

# Ankles magnitudes
open('logging/ankle_right_mag.txt', 'wb').close()
with open('logging/ankle_right_mag.txt', 'wb') as F:
    pickle.dump(pos_right_ankle, F)

open('logging/ankle_left_mag.txt', 'wb').close()
with open('logging/ankle_left_mag.txt', 'wb') as F:
    pickle.dump(pos_left_ankle, F)