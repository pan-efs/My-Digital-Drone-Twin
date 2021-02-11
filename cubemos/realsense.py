#!/usr/bin/env python3
from collections import namedtuple
import util as cm
import cv2
import time
import re
import pyrealsense2 as rs
import math
import numpy as np
from skeletontracker import skeletontracker


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
                    point_3d = np.round([float(i) for i in point_3d], 3)
                    point_str = [str(x) for x in point_3d]
                    cv2.putText(
                        render_image,
                        str(point_3d),
                        (int(joints_2D[joint_index].x), int(joints_2D[joint_index].y)),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.4,
                        text_color,
                        thickness,
                    )
"""
Description: [text]:
A function to get the joints of lower body.

Parameters: [list]: [list of skeletons]

Returns: [tuple]: [size 12] (right hip, right knee, right ankle, left hip, left knee, left ankle) for both x,y coords.
"""
def get_lower_body_joints(skeletons):
    for skeleton_index in range(len(skeletons)):
        skeleton = skeletons[skeleton_index]
        joints = skeleton.joints
        if skeleton.confidences[skeleton_index] > 0.3:
            return (joints[8].x, joints[8].y, joints[9].x, joints[9].y,
                    joints[10].x, joints[10].y, joints[11].x, joints[11].y,
                    joints[12].x, joints[12].y, joints[13].x, joints[13].y)

"""
Description: [text]:
A function to get the joints of upper body.

Parameters: [list]: [list of skeletons]

Returns: [tuple]: [size 12] (right shoulder, right elbow, right wrist, left shoulder, left elbow, left wrist) for both x,y coords.
"""
def get_upper_body_joints(skeletons):
    for skeleton_index in range(len(skeletons)):
        skeleton = skeletons[skeleton_index]
        joints = skeleton.joints
        if skeleton.confidences[skeleton_index] > 0.3:
            return (joints[2].x, joints[2].y, joints[3].x, joints[3].y,
                    joints[4].x, joints[4].y, joints[5].x, joints[5].y,
                    joints[6].x, joints[6].y, joints[7].x, joints[7].y)

"""
Description: [text]:
Helper function which converts current time to milliseconds.

Returns: [str]: [milliseconds]
"""
def get_time_milliseconds():
    milliseconds = int(round(time.time() * 1000))
    return str(milliseconds)

"""
Description: [text]:
Helper function which removes parenthesis.

Returns: [str]: [the string without parenthesis]
"""
def remove_parenthesis(log: str):
    log = log.replace('(', '')
    removed = log.replace(')', '')
    return removed

# Main content begins
if __name__ == "__main__":
    try:
        # Configure depth and color streams of the intel realsense
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
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
        
        # Erase the content of lower_body.txt file
        open('lower_body.txt', 'w').close()
        
        # Create window for initialisation
        window_name = "cubemos skeleton tracking with realsense D400 series"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL + cv2.WINDOW_KEEPRATIO)
        
        # Start timer
        start_time = time.time()
        
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
            
            # Get lower body joints and write them into a file
            log = get_lower_body_joints(skeletons)
            print(log)
            clean_log = remove_parenthesis(str(log))
            file = open('lower_body.txt', 'a')
            file.writelines(str(time.time() - start_time) + ', ' + clean_log + '\n')
            file.close()

            # render the skeletons on top of the acquired image and display it
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            cm.render_result(skeletons, color_image, joint_confidence)
            render_ids_3d(
                color_image, skeletons, depth, depth_intrinsic, joint_confidence
            )
            cv2.imshow(window_name, color_image)
            if cv2.waitKey(1) == 27:
                break
        
        pipeline.stop()
        cv2.destroyAllWindows()
        
    except Exception as ex:
        print('Exception occured: "{}"'.format(ex))