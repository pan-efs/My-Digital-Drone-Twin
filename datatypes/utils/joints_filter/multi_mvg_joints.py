import time

from datatypes.joints import JointsList
from filters.moving_average import MovingAverage as MovingAverage

def __return_jLs(joints_file):
    if joints_file.endswith('.txt'):
        jl = JointsList(
                    joints_file,
                    'mvg_filtered_joints.txt')
        jLs = jl.__return__()
    
    return jLs

def mvg_all_joints(jLs, face_keypoints=True, upper_sternum=True, upper_body=True, lower_body=True, wsize=6):
    """
    
    :param jLs: list of lists with length 54 derived from text file 
                including x,y,z coordinates for each joint as separately list.
    :type jLs: list
    
    :param face_keypoints: 15 face keypoints in total, defaults to True
    :type face_keypoints: bool, optional
    
    :param upper_sternum: 3 upper sternum keypoints in total, defaults to True
    :type upper_sternum: bool, optional
    
    :param upper_body: 18 upper body keypoints in total, defaults to True
    :type upper_body: bool, optional
    
    :param lower_body: 18 lower body keypoints in total, defaults to True
    :type lower_body: bool, optional
    
    :param wsize: windows size of moving average filter, defaults to 6
    :type wsize: int, optional
    
    :return: maximum 54 arrays for all body joints 
    :rtype: list of arrays
    """
    if wsize <= 2:
        raise ValueError('Windows size is recommended to be at least 3.')
    
    if face_keypoints == False and upper_sternum == False and lower_body == False and upper_body == False:
        raise NotImplementedError('There are no keypoints to filter.')
    
    mvg_joints = []
    mvg = MovingAverage()
    
    if face_keypoints:
        # Nose
        mvg_nose_x = mvg.moving_average(jLs[0], wsize)
        mvg_nose_y = mvg.moving_average(jLs[1], wsize)
        mvg_nose_z = mvg.moving_average(jLs[2], wsize)
        
        # Eyes
        mvg_reye_x = mvg.moving_average(jLs[42], wsize)
        mvg_reye_y = mvg.moving_average(jLs[43], wsize)
        mvg_reye_z = mvg.moving_average(jLs[44], wsize)
        
        mvg_leye_x = mvg.moving_average(jLs[45], wsize)
        mvg_leye_y = mvg.moving_average(jLs[46], wsize)
        mvg_leye_z = mvg.moving_average(jLs[47], wsize)
        
        # Ears
        mvg_rear_x = mvg.moving_average(jLs[48], wsize)
        mvg_rear_y = mvg.moving_average(jLs[49], wsize)
        mvg_rear_z = mvg.moving_average(jLs[50], wsize)
        
        mvg_lear_x = mvg.moving_average(jLs[51], wsize)
        mvg_lear_y = mvg.moving_average(jLs[52], wsize)
        mvg_lear_z = mvg.moving_average(jLs[53], wsize)
        
        mvg_joints.extend(
            [mvg_nose_x, mvg_nose_y, mvg_nose_z,
            mvg_reye_x, mvg_reye_y, mvg_reye_z,
            mvg_leye_x, mvg_leye_y, mvg_leye_z,
            mvg_rear_x, mvg_rear_y, mvg_rear_z,
            mvg_lear_x, mvg_lear_y, mvg_lear_z]
        )
    
    if upper_sternum:
        # Upper sternum
        mvg_upster_x = mvg.moving_average(jLs[3], wsize)
        mvg_upster_y = mvg.moving_average(jLs[4], wsize)
        mvg_upster_z = mvg.moving_average(jLs[5], wsize)
        
        mvg_joints.extend(
            [mvg_upster_x, mvg_upster_y, mvg_upster_z]
        )
    
    if upper_body:
        # Right upper body side
        mvg_rs_x = mvg.moving_average(jLs[6], wsize)
        mvg_rs_y = mvg.moving_average(jLs[7], wsize)
        mvg_rs_z = mvg.moving_average(jLs[8], wsize)
        
        mvg_rel_x = mvg.moving_average(jLs[9], wsize)
        mvg_rel_y = mvg.moving_average(jLs[10], wsize)
        mvg_rel_z = mvg.moving_average(jLs[11], wsize)
        
        mvg_rw_x = mvg.moving_average(jLs[12], wsize)
        mvg_rw_y = mvg.moving_average(jLs[13], wsize)
        mvg_rw_z = mvg.moving_average(jLs[14], wsize)
        
        mvg_ls_x = mvg.moving_average(jLs[15], wsize)
        mvg_ls_y = mvg.moving_average(jLs[16], wsize)
        mvg_ls_z = mvg.moving_average(jLs[17], wsize)
        
        mvg_lel_x = mvg.moving_average(jLs[18], wsize)
        mvg_lel_y = mvg.moving_average(jLs[19], wsize)
        mvg_lel_z = mvg.moving_average(jLs[20], wsize)
        
        mvg_lw_x = mvg.moving_average(jLs[21], wsize)
        mvg_lw_y = mvg.moving_average(jLs[22], wsize)
        mvg_lw_z = mvg.moving_average(jLs[23], wsize)
        
        mvg_joints.extend(
            [mvg_rs_x, mvg_rs_y, mvg_rs_z,
            mvg_rel_x, mvg_rel_y, mvg_rel_z,
            mvg_rw_x, mvg_rw_y, mvg_rw_z,
            mvg_ls_x, mvg_ls_y, mvg_ls_z,
            mvg_lel_x, mvg_lel_y, mvg_lel_z,
            mvg_lw_x, mvg_lw_y, mvg_lw_z]
        )
    
    if lower_body:
        # Right lower body side
        mvg_rh_x = mvg.moving_average(jLs[24], wsize)
        mvg_rh_y = mvg.moving_average(jLs[25], wsize)
        mvg_rh_z = mvg.moving_average(jLs[26], wsize)

        mvg_rk_x = mvg.moving_average(jLs[27], wsize)
        mvg_rk_y = mvg.moving_average(jLs[28], wsize)
        mvg_rk_z = mvg.moving_average(jLs[29], wsize)

        mvg_ra_x = mvg.moving_average(jLs[30], wsize)
        mvg_ra_y = mvg.moving_average(jLs[31], wsize)
        mvg_ra_z = mvg.moving_average(jLs[32], wsize)

        # Left lower body side
        mvg_lh_x = mvg.moving_average(jLs[33], wsize)
        mvg_lh_y = mvg.moving_average(jLs[34], wsize)
        mvg_lh_z = mvg.moving_average(jLs[35], wsize)

        mvg_lk_x = mvg.moving_average(jLs[36], wsize)
        mvg_lk_y = mvg.moving_average(jLs[37], wsize)
        mvg_lk_z = mvg.moving_average(jLs[38], wsize)

        mvg_la_x = mvg.moving_average(jLs[39], wsize)
        mvg_la_y = mvg.moving_average(jLs[40], wsize)
        mvg_la_z = mvg.moving_average(jLs[41], wsize)
        
        mvg_joints.extend(
            [mvg_rh_x, mvg_rh_y, mvg_rh_z,
            mvg_rk_x, mvg_rk_y, mvg_rk_z,
            mvg_ra_x, mvg_ra_y, mvg_ra_z,
            mvg_lh_x, mvg_lh_y, mvg_lh_z,
            mvg_lk_x, mvg_lk_y, mvg_lk_z,
            mvg_la_x, mvg_la_y, mvg_la_z]
        )
    
    return mvg_joints

# Run example
# For 202716 lines of text, we need 10 seconds approximately. 
""" if __name__ == "__main__":
    start_time = time.time()
    
    jLs = __return_jLs('long.txt') # provide here your file
    mvg_joints = mvg_all_joints(jLs)
    
    duration = time.time() - start_time
    print(f"Duration {duration} seconds") """