import cv2
import mediapipe as mp
import calculator as calc
import toJSON
import math
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip

LABELS_LENGHT = toJSON.labels_lenght()
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


mppose = mp.solutions.pose
pose = mppose.Pose()
arm_angle_list, back_deviation_list, shoulder_angle_list, back_angle_list = [], [], [], []
master_list = [arm_angle_list, back_deviation_list,
               shoulder_angle_list, back_angle_list]
totalAmountFound = 0

def calculateTimestampByFrame (frame):
    i = 0
    sec = 0
    while(i != frame):
        sec+=0.01
        i+=1
        if(i % 24 == 0):
            sec=math.ceil(sec)
    return sec

#LABELS_LENGHT
for i in range(LABELS_LENGHT):
    exerice = toJSON.find_exercise(i)
    cap = cv2.VideoCapture(f'C:/P6/Project-6-Pose-Estimation/dataset/{i}.wmv')
    frame = 0
    prevTime = 0
    hasBeenUp = False
    #30 frames persecond
    while True:
        frame +=1
        success, img = cap.read()
        
        try:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = pose.process(imgRGB)

            if result.pose_landmarks:
                p = list_coordinates(img, result.pose_landmarks.landmark)
                if exerice == 'armcurl':
                    arm_angle = calc.angle(p[WRIST_LEFT], p[ELBOW_LEFT], p[SHOULDER_LEFT])
                    arm_angle_list.append(arm_angle)
                    back_deviation_list.append(calc.devation(
                        p[SHOULDER_LEFT], p[HIP_LEFT]))

                    if hasBeenUp and arm_angle > 160:
                        sec = frame / 24;
                        input_video_path = "C:/P6/Project-6-Pose-Estimation/dataset/" + str(i) + ".wmv"
                        output_video_path = "C:/P6/Project-6-Pose-Estimation/dataset/singles/" + str(totalAmountFound) + ".mp4" 
                        
                        with VideoFileClip(input_video_path) as video:
                            new = video.subclip(round(float(prevTime),2), round(float(sec),2))
                            new.write_videofile(output_video_path, codec="libx264")
                        print("found an exercise ", sec, frame, prevTime)
                        totalAmountFound+=1
                        prevTime = sec
                        hasBeenUp = False
                        cv2.imshow("Image", img)
                        cv2.waitKey(100)
                        

                    if arm_angle < 60:
                        hasBeenUp = True
                       
                elif exerice == 'armraise':
                    arm_angle = calc.angle(p[HIP_LEFT], p[SHOULDER_LEFT], p[WRIST_LEFT])
                    arm_angle_list.append(arm_angle)
                    shoulder_angle_list.append(calc.angle(
                        p[ELBOW_LEFT], p[SHOULDER_LEFT], p[HIP_LEFT]))
                    back_deviation_list.append(calc.devation(
                        p[SHOULDER_LEFT], p[HIP_LEFT]))
                    if hasBeenUp and arm_angle < 10:
                        sec = frame / 24
                        input_video_path = "C:/P6/Project-6-Pose-Estimation/dataset/" + str(i) + ".wmv"
                        output_video_path = "C:/P6/Project-6-Pose-Estimation/dataset/singles/" + str(totalAmountFound) + ".mp4"
                        with VideoFileClip(input_video_path) as video:
                            new = video.subclip(round(float(prevTime),2), round(float(sec),2))
                            new.write_videofile(output_video_path, codec="libx264")
                        print("found an exercise ", sec, frame, prevTime)
                        totalAmountFound+=1
                        prevTime = sec
                        hasBeenUp = False
                        cv2.imshow("Image", img)
                        cv2.waitKey(100)
                    if arm_angle > 80:
                        hasBeenUp = True


                elif exerice == 'pushup':
                    shoulder_angle = calc.angle(
                       p[SHOULDER_LEFT],  p[ELBOW_LEFT], p[WRIST_LEFT])
                    arm_angle_list.append(calc.angle(
                        p[WRIST_LEFT], p[ELBOW_LEFT], p[SHOULDER_LEFT]))
                    shoulder_angle_list.append(shoulder_angle)
                    back_angle_list.append(calc.angle(
                        p[ANKLE_LEFT], p[HIP_LEFT], p[SHOULDER_LEFT]))
                    if hasBeenUp and shoulder_angle > 145:
                        sec = frame / 24
                        input_video_path = "C:/P6/Project-6-Pose-Estimation/dataset/" + str(i) + ".wmv"
                        output_video_path = "C:/P6/Project-6-Pose-Estimation/dataset/singles/" + str(totalAmountFound) + ".mp4"
                        with VideoFileClip(input_video_path) as video:
                            new = video.subclip(round(float(prevTime),2), round(float(sec),2))
                            new.write_videofile(output_video_path, codec="libx264")
                        print("found an exercise ", sec, frame, prevTime)
                        totalAmountFound+=1
                        prevTime = sec
                        hasBeenUp = False
                        cv2.imshow("Image", img)
                        cv2.waitKey(100)
                    if shoulder_angle < 80:
                        hasBeenUp = True

        except Exception as e:
            print(e)
            if exerice == 'armcurl':
                toJSON.add_data(arm_angle_list, i, 'arm_angle')
                toJSON.add_data(back_deviation_list, i, 'upperback_deviation')

            elif exerice == 'armraise':
                toJSON.add_data(arm_angle_list, i, 'arm_angle')
                toJSON.add_data(shoulder_angle_list, i, 'shoulder_angle')
                toJSON.add_data(back_deviation_list, i, 'upperback_deviation')

            elif exerice == 'pushup':
                toJSON.add_data(arm_angle_list, i, 'arm_angle')
                toJSON.add_data(shoulder_angle_list, i, 'shoulder_angle')
                toJSON.add_data(back_angle_list, i, 'upperback_angle')

            for lists in master_list:
                lists.clear()

            print(f"Processing [{i+1}/{LABELS_LENGHT}]")
            if i+1 == LABELS_LENGHT:
                print("Done! :)")
            break
    
