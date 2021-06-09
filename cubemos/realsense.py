#!/usr/bin/env python3
from collections import namedtuple
from datetime import datetime
import sys, os, cv2, math, shutil
import numpy as np

import pyrealsense2 as rs

from cubemos import util as cm
from cubemos.skeletontracker import skeletontracker

def _get_base_dir():
    frozen = 'not'
    if getattr(sys, 'frozen', False):
        frozen = 'ever so'
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return BASE_DIR

def render_ids_3d(
    render_image, skeletons_2d, depth_map, depth_intrinsic, joint_confidence
):
    thickness = 1
    text_color = (255, 255, 255)
    rows, cols, channel = render_image.shape[:3]
    distance_kernel_size = 5
    
    # calculate 3D keypoints and display them
    for skeleton_index in range(len(skeletons_2d)):
        skeleton_2D = skeletons_2d[skeleton_index]
        joints_2D = skeleton_2D.joints
        did_once = False
        
        for joint_index in range(len(joints_2D)):
            if did_once == False:
                cv2.putText(
                    render_image,
                    "id: " + str(skeleton_2D.id),
                    (int(joints_2D[joint_index].x), int(joints_2D[joint_index].y - 30)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    text_color,
                    thickness,
                )
                did_once = True
            # check if the joint was detected and has valid coordinate
            if skeleton_2D.confidences[joint_index] > joint_confidence:
                distance_in_kernel = []
                low_bound_x = max(
                    0,
                    int(
                        joints_2D[joint_index].x - math.floor(distance_kernel_size / 2)
                    ),
                )
                upper_bound_x = min(
                    cols - 1,
                    int(joints_2D[joint_index].x + math.ceil(distance_kernel_size / 2)),
                )
                low_bound_y = max(
                    0,
                    int(
                        joints_2D[joint_index].y - math.floor(distance_kernel_size / 2)
                    ),
                )
                upper_bound_y = min(
                    rows - 1,
                    int(joints_2D[joint_index].y + math.ceil(distance_kernel_size / 2)),
                )
                for x in range(low_bound_x, upper_bound_x):
                    for y in range(low_bound_y, upper_bound_y):
                        distance_in_kernel.append(depth_map.get_distance(x, y))
                median_distance = np.percentile(np.array(distance_in_kernel), 50)
                depth_pixel = [
                    int(joints_2D[joint_index].x),
                    int(joints_2D[joint_index].y),
                ]
                if median_distance >= 0.3:
                    point_3d = rs.rs2_deproject_pixel_to_point(
                        depth_intrinsic, depth_pixel, median_distance
                    )
                    file = open('logging/get_3d_joints.txt', 'a')
                    file.writelines(str(joint_index) + ', ' + str(point_3d) + '\n')
                    file.close()
                    point_3d = np.round([float(i) for i in point_3d], 3)
                    cv2.putText(
                        render_image,
                        str(point_3d),
                        (int(joints_2D[joint_index].x), int(joints_2D[joint_index].y)),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.4,
                        text_color,
                        thickness,
                    )
                else:
                    file = open('logging/get_3d_joints.txt', 'a')
                    file.writelines(str(joint_index) + ', ' + '[NaN, NaN, NaN]' + '\n')
                    file.close()
            else:
                file = open('logging/get_3d_joints.txt', 'a')
                file.writelines(str(joint_index) + ', ' + '[NaN, NaN, NaN]' + '\n')
                file.close()

# Main content begins
if __name__ == "__main__":
    try:
        # Configure depth and color streams of the intel realsense
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

        # Start the realsense pipeline
        pipeline = rs.pipeline()
        pipeline.start()

        # Create align object to align depth frames to color frames
        align = rs.align(rs.stream.color)

        # Get the intrinsics information for calculation of 3D point
        unaligned_frames = pipeline.wait_for_frames()
        frames = align.process(unaligned_frames)
        depth = frames.get_depth_frame()
        depth_intrinsic = depth.profile.as_video_stream_profile().intrinsics

        # Initialize the cubemos api with a valid license key in default_license_dir()
        skeletrack = skeletontracker(cloud_tracking_api_key="")
        joint_confidence = 0.2
        
        # Save video
        dt = datetime.now().strftime('%m-%d-%Y %H-%M-%S')
        output_skeleton = dt + '.avi'
        videoout = cv2.VideoWriter(output_skeleton, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (1280, 720))
        
        # Erase the content of .txt files
        open('logging/get_3d_joints.txt', 'w').close()
        
        # Create window for initialisation
        window_name = "Skeleton tracking with Intel RealSense camera. Press Esc button for exit."
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL + cv2.WINDOW_KEEPRATIO)
        
        while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
            unaligned_frames = pipeline.wait_for_frames()
            frames = align.process(unaligned_frames)
            depth = frames.get_depth_frame()
            color = frames.get_color_frame()
            if not depth or not color:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth.get_data())
            color_image = np.asanyarray(color.get_data())

            # perform inference and update the tracking id
            skeletons = skeletrack.track_skeletons(color_image)

            # render the skeletons on top of the acquired image and display it
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            
            cm.render_result(skeletons, color_image, joint_confidence)
            render_ids_3d(color_image, skeletons, depth, depth_intrinsic, joint_confidence)
            videoout.write(color_image)
            
            cv2.imshow(window_name, color_image)
            if cv2.waitKey(1) == 27:
                # Press Esc button for exit and save on user's desktop
                source = _get_base_dir() + '/cubemos/' + output_skeleton
                dest = os.path.expanduser("~/Desktop") # works both on windows and linux
                shutil.copy2(source, dest)
                break
        
        pipeline.stop()
        videoout.release()
        cv2.destroyAllWindows()
        #os.remove(source)
        
    except Exception as ex:
        print('Exception occured: "{}"'.format(ex))
        raise ex