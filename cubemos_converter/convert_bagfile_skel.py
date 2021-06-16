from collections import namedtuple 
import pyrealsense2 as rs
import numpy as np
import cv2, math, argparse

from cubemos_converter import util as cm
from cubemos_converter.skeletontracker import skeletontracker

# Starting point
parser = argparse.ArgumentParser(description = 'Provide directory of .bag file.')
parser.add_argument('--file', type = str,
                    help = 'Provide the directory of a .bag file.',
                    required = True)
args = parser.parse_args()

if not args.file:
    raise NotImplementedError

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
        for joint_index in range(len(joints_2D)): # all joints, *use e.g. -x in order to remove not desired joints
            if did_once == False:
                cv2.putText(
                    render_image,
                    "id: " + str(skeleton_2D.id),
                    (int(joints_2D[joint_index].x), int(joints_2D[joint_index].y - 30)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    text_color,
                    2,
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
                    file = open('logging/write_3d_joints_from_video.txt', 'a')
                    file.writelines(str(joint_index) + ', ' + str(point_3d) + '\n')
                    file.close()
                    point_3d = np.array([int(i*100) for i in point_3d])
                    cv2.putText(
                        render_image,
                        str(point_3d),
                        (int(joints_2D[joint_index].x), int(joints_2D[joint_index].y)),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.3,
                        text_color,
                        thickness,
                    )
                else:
                    file = open('logging/write_3d_joints_from_video.txt', 'a')
                    file.writelines(str(joint_index) + ', ' + '[NaN, NaN, NaN]' + '\n')
                    file.close()
            else:
                file = open('logging/write_3d_joints_from_video.txt', 'a')
                file.writelines(str(joint_index) + ', ' + '[NaN, NaN, NaN]' + '\n')
                file.close()

# Main content begins
if __name__ == "__main__":
    try:
        # Configure depth and color streams of the intel realsense
        config = rs.config()
        config.enable_device_from_file(args.file, False)
        config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

        # Start the realsense pipeline
        pipeline = rs.pipeline()
        pipeline.start(config)

        # Set non-realtime
        device = pipeline.get_active_profile().get_device().as_playback()
        device.set_real_time(False)

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
        videoout = cv2.VideoWriter('output-skeleton.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.0, (1280, 720))
        
        # Erase the content of .txt file
        open('logging/write_3d_joints_from_video.txt', 'w').close()
        
        while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
            unaligned_frames = pipeline.wait_for_frames(100) 
            frames = align.process(unaligned_frames)
            depth = frames.get_depth_frame()
            color = frames.get_color_frame()
            if not depth or not color:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth.get_data())
            color_image = np.asanyarray(color.get_data())

            # Convert color in image if necessary
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            
            # perform inference and update the tracking id
            skeletons = skeletrack.track_skeletons(color_image)

            # render the skeletons on top of the acquired image and display it
            cm.render_result(skeletons, color_image, joint_confidence)
            render_ids_3d(color_image, skeletons, depth, depth_intrinsic, joint_confidence)
            videoout.write(color_image)

        pipeline.stop()
        videoout.release()

    except Exception as ex:
        print('Exception occured: "{}"'.format(ex))
        # Should be included licence error as well, but cannot be checked now.
        if 'Exception occured: "{}"'.format(ex) == 'Exception occured: "Couldn\'t resolve requests"':
            raise ex