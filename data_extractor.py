import cv2
import mediapipe as mp
import time
import calculator as calc
import toJSON


def list_coordinates(img, landmarks):
    poselist = []
    for index, landmark in enumerate(landmarks):
        height, width, not_used = img.shape
        x, y = int(width * landmark.x), int(height * landmark.y)
        poselist.append([index, x, y])

    return poselist


list_data_type = ['arm_angle', 'upperback_angle']
mp_draw = mp.solutions.drawing_utils
mppose = mp.solutions.pose
pose = mppose.Pose()
angle_list = []
deviation_list = []
time_b = 0

for i in range(6):
    cap = cv2.VideoCapture(f'dataset/{i}.wmv')
    while True:
        success, img = cap.read()
        try:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = pose.process(imgRGB)

            if result.pose_landmarks:
                mp_draw.draw_landmarks(img, result.pose_landmarks,
                                       mppose.POSE_CONNECTIONS)
                plist = list_coordinates(img, result.pose_landmarks.landmark)

                cv2.putText(img, str(int(calc.angle(plist[15], plist[13], plist[11]))), (plist[13][1] - 50, plist[13][2] + 30),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))
                # cv2.putText(img, str(int(calc_angle(plist[23], plist[25], plist[27]))), (plist[25][1] - 50, plist[25][2] + 30),
                # cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))
                # cv2.putText(img, str(int(calc_angle(plist[24], plist[12], plist[14]))), (plist[12][1] - 50, plist[12][2] + 30),
                # cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))
                # cv2.putText(img, str(int(calc_angle(plist[12], plist[14], plist[16]))), (plist[14][1] - 50, plist[14][2] + 30),
                # cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255))

                deviation_list.append(calc.devation(plist[11], plist[23]))
                angle_list.append(calc.angle(plist[15], plist[13], plist[11]))

            time_a = time.time()
            fps = 1/(time_a-time_b)
            time_b = time_a

            cv2.putText(img, "fps: " + str(int(fps)), (70, 50),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
            #cv2.imshow("Image", img)
            # cv2.waitKey(10)

        except Exception as e:
            print(e)
            toJSON.add_data(angle_list, i, list_data_type[0])
            toJSON.add_data(deviation_list, i, list_data_type[1])
            print(f"Done! {i}")
            break
