import cv2

keypoint_ids = [
    (1, 2),
    (1, 5),
    (2, 3),
    (3, 4),
    (5, 6),
    (6, 7),
    (1, 8),
    (8, 9),
    (9, 10),
    (1, 11),
    (11, 12),
    (12, 13),
    (1, 0),
    (0, 14),
    (14, 16),
    (0, 15),
    (15, 17)
]

def get_valid_keypoints(keypoint_ids, skeleton, confidence_threshold):
    keypoints = [
        (tuple(map(int, skeleton.joints[i])), tuple(map(int, skeleton.joints[v])))
        for (i, v) in keypoint_ids
        if skeleton.confidences[i] >= confidence_threshold
        and skeleton.confidences[v] >= confidence_threshold
    ]
    valid_keypoints = [
        keypoint
        for keypoint in keypoints
        if keypoint[0][0] >= 0 and keypoint[0][1] >= 0 and keypoint[1][0] >= 0 and keypoint[1][1] >= 0
    ]
    return valid_keypoints


def render_result(skeletons, img, confidence_threshold):
    skeleton_color = (100, 254, 213)
    for index, skeleton in enumerate(skeletons):
        keypoints = get_valid_keypoints(keypoint_ids, skeleton, confidence_threshold)
        for keypoint in keypoints:
            cv2.line(
                img, keypoint[0], keypoint[1], skeleton_color, thickness=2, lineType=cv2.LINE_AA
            )


def render_ids(skeletons, img, thickness=5):
    id_text_color_offline_tracking = (51, 153, 255)
    id_text_color_cloud_tracking = (57, 201, 100)
    text_color = id_text_color_offline_tracking
    for skeleton in skeletons:
        if skeleton.id_confirmed_on_cloud == True:
            text_color = id_text_color_cloud_tracking
        for joint in skeleton.joints:
            x, y = tuple(map(int, joint))
            if x < 0 or y < 0:
                continue
            cv2.putText(img, f'{skeleton.id}', (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 5, text_color, thickness)
            break


def get_cloud_tracking_api_key():
    print("---------------------------------------------------------------------")
    print("Initialising the cubemos skeleton tracking SDK ")
    print("The available tracking styles are: ")
    print("             1. EDGE tracking on the Host PC")
    print("             2. CLOUD tracking with enhanced fullbody based ReIdentification requiring Internet Connection")
    print("---------------------------------------------------------------------")
    print("If you would like to use tracking on the CLOUD, please enter the API Key")
    print("provided by cubemos and hit ENTER key")
    print("             [OR]                  ")
    print("Simply press ENTER key without typing anything")
    print("---------------------------------------------------------------------")
    cloud_tracking_api_key = input("Cloud tracking API Key: ")
    print("Cloud Tracking API Key entered: " + cloud_tracking_api_key)
    print("---------------------------------------------------------------------")
    return cloud_tracking_api_key