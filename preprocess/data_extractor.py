import cv2
import mediapipe as mp
import calculator as calc
import normalization
import json
import os

WRIST_LEFT = 15
WRIST_RIGHT = 16
ELBOW_LEFT = 13
ELBOW_RIGHT = 14
SHOULDER_LEFT = 11
SHOULDER_RIGHT = 12
HIP_LEFT = 23
HIP_RIGHT = 24
KNEE_LEFT = 25
KNEE_RIGHT = 26
ANKLE_LEFT = 27
ANKLE_RIGHT = 28


def list_coordinates(img, landmarks):
    poselist = []
    for index, landmark in enumerate(landmarks):
        height, width, not_used = img.shape
        x, y = int(width * landmark.x), int(height * landmark.y)
        poselist.append([index, x, y])

    return poselist


def find_correctness(correctness):
    if correctness == 'correct':
        return 1
    else:
        return 0


mppose = mp.solutions.pose
pose = mppose.Pose()

arm_angle_list, back_deviation_list, shoulder_angle_list, hip_angle_list, leg_angle_list = [], [], [], [], []
master_list = [arm_angle_list, back_deviation_list,
               shoulder_angle_list, hip_angle_list, leg_angle_list]

data = []
id_ = 0
folder = os.listdir('dataset')

with open('preprocess/labels.json', 'w', encoding='utf-8') as f:
    for exercise_folder in folder:
        correct_folder = os.listdir(f'dataset/{exercise_folder}')

        for correctness in correct_folder:
            clips = os.listdir(f'dataset/{exercise_folder}/{correctness}')

            for i in range(len(clips)):
                cap = cv2.VideoCapture(
                    f'dataset/{exercise_folder}/{correctness}/{i}.mp4')

                while True:
                    success, img = cap.read()

                    try:
                        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        result = pose.process(imgRGB)

                        if result.pose_landmarks:
                            p = list_coordinates(
                                img, result.pose_landmarks.landmark)

                            if exercise_folder == 'armcurl':
                                arm_angle_list.append(calc.angle(
                                    p[WRIST_LEFT], p[ELBOW_LEFT], p[SHOULDER_LEFT]))
                                shoulder_angle_list.append(calc.angle(
                                    p[ELBOW_LEFT], p[SHOULDER_LEFT], p[HIP_LEFT]))
                                back_deviation_list.append(calc.devation(
                                    p[SHOULDER_LEFT], p[HIP_LEFT]))

                            elif exercise_folder == 'armraise':
                                arm_angle_list.append(calc.angle(
                                    p[WRIST_LEFT], p[ELBOW_LEFT], p[SHOULDER_LEFT]))
                                shoulder_angle_list.append(calc.angle(
                                    p[HIP_LEFT], p[SHOULDER_LEFT], p[WRIST_LEFT]))
                                back_deviation_list.append(calc.devation(
                                    p[SHOULDER_LEFT], p[HIP_LEFT]))

                            elif exercise_folder == 'pushup':
                                arm_angle_list.append(calc.angle(
                                    p[SHOULDER_RIGHT], p[ELBOW_RIGHT], p[WRIST_RIGHT]))
                                leg_angle_list.append(calc.angle(
                                    p[ANKLE_RIGHT], p[KNEE_RIGHT], p[HIP_RIGHT]))
                                hip_angle_list.append(calc.angle(
                                    p[KNEE_RIGHT], p[HIP_RIGHT], p[SHOULDER_RIGHT]))

                    except Exception as e:
                        # print(e)
                        if exercise_folder == 'armcurl':
                            f1w, f1n, f1c = 0, 0, 0
                            f2c, f2_bend = 0, 0
                            f3w, f3n, f3c = 0, 0, 0
                            if sum(arm_angle_list.copy()) > 6000:
                                f1w = 1
                            elif sum(arm_angle_list.copy()) < 4000:
                                f1n = 1
                            else:
                                f1c = 1
                            if 200 < sum(back_deviation_list.copy()) and sum(back_deviation_list.copy()) > 600:
                                f2c = 1
                            else:
                                f2_bend = 1

                            if sum(shoulder_angle_list.copy()) > 16000:
                                f3w = 1
                            elif sum(shoulder_angle_list.copy()) < 8000:
                                f3n = 1
                            else:
                                f3c = 1
                            data.append(
                                {'id': id_,
                                    'exercise': exercise_folder,
                                    'correct': find_correctness(correctness),
                                    'feature_1_angle_correct': f1c,
                                    'feature_1_angle_wide': f1w,
                                    'feature_1_angle_narrow': f1n,
                                    'feature_2_back_correct': f2c,
                                    'feature_2_back_bend': f2_bend,
                                    'feature_3_angle_correct': f3c,
                                    'feature_3_angle_wide': f3w,
                                    'feature_3_angle_narrow': f3n,
                                    'feature_armcurl': 1,
                                    'feature_armraise': 0,
                                    'feature_pushup': 0,
                                    'feature_1': sum(arm_angle_list.copy()),
                                    'feature_2': sum(back_deviation_list.copy()),
                                    'feature_3': sum(shoulder_angle_list.copy()),
                                    'feature_4': 0,
                                    'feature_5': 0
                                 })
                        elif exercise_folder == 'armraise':
                            f1w, f1n, f1c = 0, 0, 0
                            f2_bend, f2c = 0, 0
                            f3w, f3n, f3c = 0, 0, 0

                            if sum(arm_angle_list.copy()) > 11000:
                                f1w = 1
                            elif sum(arm_angle_list.copy()) < 7500:
                                f1n = 1
                            else:
                                f1c = 1

                            if 700 < sum(back_deviation_list.copy()) and sum(back_deviation_list.copy()) > 1300:
                                f2c = 1
                            else:
                                f2_bend = 1

                            if sum(shoulder_angle_list.copy()) > 3200:
                                f3w = 1
                            elif sum(shoulder_angle_list.copy()) < 2500:
                                f3n = 1
                            else:
                                f3c = 1

                            data.append(
                                {'id': id_,
                                    'exercise': exercise_folder,
                                    'correct': find_correctness(correctness),
                                    'feature_1_angle_correct': f1c,
                                    'feature_1_angle_wide': f1w,
                                    'feature_1_angle_narrow': f1n,
                                    'feature_2_back_correct': f2c,
                                    'feature_2_back_bend': f2_bend,
                                    'feature_3_angle_correct': f3c,
                                    'feature_3_angle_wide': f3w,
                                    'feature_3_angle_narrow': f3n,
                                    'feature_armcurl': 0,
                                    'feature_armraise': 1,
                                    'feature_pushup': 0,
                                    'feature_1': sum(arm_angle_list.copy()),
                                    'feature_2': sum(back_deviation_list.copy()),
                                    'feature_3': sum(shoulder_angle_list.copy()),
                                    'feature_4': 0,
                                    'feature_5': 0
                                 })
                        elif exercise_folder == 'pushup':
                            f1_high, f1_low, f1c = 0, 0, 0
                            f4_bend, f4c = 0, 0
                            # Used to check indicate how the hips are bending
                            f5_high_bend, f5_low_bend, f5c = 0, 0, 0

                            if sum(arm_angle_list.copy()) > 5000:
                                f1_high = 1
                            elif sum(arm_angle_list.copy()) < 4000:
                                f1_low = 1
                            else:
                                f1c = 1

                            if 6400 < sum(leg_angle_list.copy()) and sum(leg_angle_list.copy()) < 7400:
                                f4_bend = 1
                            else:
                                f4c = 1

                            if sum(hip_angle_list.copy()) > 8200:
                                f5_high_bend = 1
                            elif sum(hip_angle_list.copy()) < 7100:
                                f5_low_bend = 1
                            else:
                                f5c = 1

                            data.append(
                                {'id': id_,
                                    'exercise': exercise_folder,
                                    'correct': find_correctness(correctness),
                                    'feature_1_angle_correct': f1c,
                                    'feature_1_angle_wide': f1w,
                                    'feature_1_angle_narrow': f1n,
                                    'feature_2_back_correct': f4c,
                                    'feature_2_back_bend': f4_bend,
                                    'feature_3_angle_correct': f5c,
                                    'feature_3_angle_wide': f5_high_bend,
                                    'feature_3_angle_narrow': f5_low_bend,
                                    'feature_armcurl': 0,
                                    'feature_armraise': 0,
                                    'feature_pushup': 1,
                                    'feature_1': sum(arm_angle_list.copy()),
                                    'feature_2': 0,
                                    'feature_3': 0,
                                    'feature_4': sum(leg_angle_list.copy()),
                                    'feature_5': sum(hip_angle_list.copy())
                                 })

                        for lists in master_list:
                            lists.clear()

                        print(f'Processing [{id_}]')
                        break
                id_ += 1
    json.dump(data, f)
print("Data extracted")
normalization.normalizer()
