import pygame
import cv2
from gaze_tracking import GazeTracking
from threading import Thread
import numpy as np
import pyautogui
import time

def gazetracking():
    global left_pupil, tracking_active
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    webcam.set(cv2.CAP_PROP_FPS, 50)  # Set FPS

    fixed_size = (500, 800)

    while True:
        ret, frame = webcam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(200, 200))

        if len(faces) == 0:
            print("No faces detected")
            face = None
        else:
            # Take the first detected face
            (x, y, w, h) = faces[0]
            face = frame[y-100 : y+h+100, x-10 : x+w+10]

            if face.size == 0:  # Check if the face region is valid
                face = None

        if face is not None:
            print("face detected")
            face = cv2.resize(face, fixed_size)
            frame[0:fixed_size[1], 0:fixed_size[0]] = face

            gaze.refresh(face)
            face = gaze.annotated_frame()

            left_pupil = gaze.pupil_left_coords()
            print(left_pupil)

            if left_pupil is not None:
                left_pupil = (left_pupil[0] * -1 + 1920, left_pupil[1])

            cv2.putText(face, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.imshow("Demo", face)

        cv2.imshow('Face Detection and Zoom', frame)

        if tracking_active or cv2.waitKey(1) & 0xFF == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()

def Calibration():

    time.sleep(3)

    global left_pupil, right_pupil, eye_coordinate, tracking_active

    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    bg_color = 40, 40, 40

    pygame.mouse.set_visible(True)
    click_n = [0 for _ in range(9)]
    COLOR_CHANGE = [(200, 200, 255), (150, 150, 255), (100, 100, 255)]
    colors = [(255, 255, 255) for _ in range(9)]
    pos = [[40, 40], [width / 2, 40], [width - 40, 40], [40, height / 2], [width / 2, height / 2],
           [width - 40, height / 2], [40, height - 40], [width / 2, height - 40], [width - 40, height - 40]]

    visible_index = 0
    click_num = 0
    eye_coord1, eye_coord2 = [], []

    while True:
        screen.fill(bg_color)
        for i in range(visible_index + 1):
            pygame.draw.circle(screen, colors[i], pos[i], 15)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if left_pupil is not None:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if click_num < 9:
                        eye_coord1.append(left_pupil)
                    elif click_num >= 9:
                        eye_coord2.append(left_pupil)
                else:
                    font = pygame.font.Font(None, 74)
                    text = font.render("Pupil not detected", True, (255, 0, 0))
                    pupil_not_detected = text.get_rect(center=(width / 2, height / 2))

                    screen.blit(text, pupil_not_detected)
                    pygame.display.flip()
                    click_num -= 1
                    time.sleep(2)
                R = visible_index + 1
                for i in range(R):
                    if (mouse_x - pos[i][0]) ** 2 + (mouse_y - pos[i][1]) ** 2 <= 225:
                        if click_n[i] <= 1:
                            click_n[i] += 1
                            clicked = pos[i]
                        colors[i] = COLOR_CHANGE[click_n[i]]
                        if click_n[i] == 1 and visible_index < 8:
                            visible_index += 1

                click_num += 1
                print(f'click_num = {click_num}')

                if click_num == 18:
                    visible_index = 0
                    click_n = [0 for _ in range(9)]

                    if len(eye_coord1) > 0 and len(eye_coord2) > 0:
                        print(eye_coord1)
                        print(eye_coord2)
                        eye_coordinate = (np.array(eye_coord1) + np.array(eye_coord2))/2
                        print(eye_coordinate)
                        print(eye_coordinate[0])
                        return culculate_eye_coordinates(eye_coordinate)
                    else:
                        print("eye coord not activated")

        if cv2.waitKey(1) == 27:
            break

        if left_pupil:
            font = pygame.font.Font(None, 20)
            text = font.render("Pupil detected", True, (0, 100, 200))
            pupil_detected = text.get_rect(center=(width-10, 0))

            screen.blit(text, pupil_detected)
            pygame.display.flip()

def culculate_eye_coordinates(eye_coordinate):
    r = 0

    a = (eye_coordinate[0][0] - r + eye_coordinate[3][0] - r + eye_coordinate[6][0] - r) / 3
    b = (eye_coordinate[0][1] - r + eye_coordinate[1][1] - r + eye_coordinate[3][1] - r) / 3
    c = (eye_coordinate[2][0] + r + eye_coordinate[5][0] + r + eye_coordinate[8][0] + r) / 3
    d = (eye_coordinate[6][1] + r + eye_coordinate[7][1] + r + eye_coordinate[8][1] + r) / 3

    print(f'a={a}  b={b}  c={c}  d={d}')

    new_w = c - a
    new_h = d - b

    tracking_active = True
    return tracking(new_w, new_h, a, b)

import pygame
import cv2
from gaze_tracking import GazeTracking
from threading import Thread
import numpy as np
import pyautogui
import time

def gazetracking():
    global left_pupil, tracking_active
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    webcam.set(cv2.CAP_PROP_FPS, 50)  # Set FPS

    fixed_size = (500, 800)

    while True:
        ret, frame = webcam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(200, 200))

        if len(faces) == 0:
            print("No faces detected")
            face = None
        else:
            # Take the first detected face
            (x, y, w, h) = faces[0]
            face = frame[y-100 : y+h+100, x-10 : x+w+10]

            if face.size == 0:  # Check if the face region is valid
                face = None

        if face is not None:
            print("face detected")
            face = cv2.resize(face, fixed_size)
            frame[0:fixed_size[1], 0:fixed_size[0]] = face

            gaze.refresh(face)
            face = gaze.annotated_frame()

            left_pupil = gaze.pupil_left_coords()
            print(left_pupil)

            if left_pupil is not None:
                left_pupil = (left_pupil[0] * -1 + 1920, left_pupil[1])

            cv2.putText(face, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.imshow("Demo", face)

        cv2.imshow('Face Detection and Zoom', frame)

        if tracking_active or cv2.waitKey(1) & 0xFF == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()

def Calibration():

    time.sleep(3)

    global left_pupil, right_pupil, eye_coordinate, tracking_active

    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    bg_color = 40, 40, 40

    pygame.mouse.set_visible(True)
    click_n = [0 for _ in range(9)]
    COLOR_CHANGE = [(200, 200, 255), (150, 150, 255), (100, 100, 255)]
    colors = [(255, 255, 255) for _ in range(9)]
    pos = [[40, 40], [width / 2, 40], [width - 40, 40], [40, height / 2], [width / 2, height / 2],
           [width - 40, height / 2], [40, height - 40], [width / 2, height - 40], [width - 40, height - 40]]

    visible_index = 0
    click_num = 0
    eye_coord1, eye_coord2 = [], []

    while True:
        screen.fill(bg_color)
        for i in range(visible_index + 1):
            pygame.draw.circle(screen, colors[i], pos[i], 15)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if left_pupil is not None:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if click_num < 9:
                        eye_coord1.append(left_pupil)
                    elif click_num >= 9:
                        eye_coord2.append(left_pupil)
                else:
                    font = pygame.font.Font(None, 74)
                    text = font.render("Pupil not detected", True, (255, 0, 0))
                    pupil_not_detected = text.get_rect(center=(width / 2, height / 2))

                    screen.blit(text, pupil_not_detected)
                    pygame.display.flip()
                    click_num -= 1
                    time.sleep(2)
                R = visible_index + 1
                for i in range(R):
                    if (mouse_x - pos[i][0]) ** 2 + (mouse_y - pos[i][1]) ** 2 <= 225:
                        if click_n[i] <= 1:
                            click_n[i] += 1
                            clicked = pos[i]
                        colors[i] = COLOR_CHANGE[click_n[i]]
                        if click_n[i] == 1 and visible_index < 8:
                            visible_index += 1

                click_num += 1
                print(f'click_num = {click_num}')

                if click_num == 18:
                    visible_index = 0
                    click_n = [0 for _ in range(9)]

                    if len(eye_coord1) > 0 and len(eye_coord2) > 0:
                        print(eye_coord1)
                        print(eye_coord2)
                        eye_coordinate = (np.array(eye_coord1) + np.array(eye_coord2))/2
                        print(eye_coordinate)
                        print(eye_coordinate[0])
                        return culculate_eye_coordinates(eye_coordinate)
                    else:
                        print("eye coord not activated")

        if cv2.waitKey(1) == 27:
            break

        if left_pupil:
            font = pygame.font.Font(None, 20)
            text = font.render("Pupil detected", True, (0, 100, 200))
            pupil_detected = text.get_rect(center=(width-10, 0))

            screen.blit(text, pupil_detected)
            pygame.display.flip()

def culculate_eye_coordinates(eye_coordinate):
    r = 0

    a = (eye_coordinate[0][0] - r + eye_coordinate[3][0] - r + eye_coordinate[6][0] - r) / 3
    b = (eye_coordinate[0][1] - r + eye_coordinate[1][1] - r + eye_coordinate[3][1] - r) / 3
    c = (eye_coordinate[2][0] + r + eye_coordinate[5][0] + r + eye_coordinate[8][0] + r) / 3
    d = (eye_coordinate[6][1] + r + eye_coordinate[7][1] + r + eye_coordinate[8][1] + r) / 3

    print(f'a={a}  b={b}  c={c}  d={d}')

    new_w = c - a
    new_h = d - b

    tracking_active = True
    return tracking(new_w, new_h, a, b)

def tracking(w, h, a, b):
    print("eye_tracking_activated")

    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    bg_color = 0, 0, 0

    clock = pygame.time.Clock()
    pyautogui.FAILSAFE = False

    while True:
        screen.fill(bg_color)

        if left_pupil:
            new_x = (left_pupil[0] - a) / w * width
            new_y = (left_pupil[1] - b) / h * heighte
            print(f'{left_pupil[0]}  ,  {left_pupil[1]}   --> {new_x} , {new_y}')

            if new_x > width:
                new_x = width
            elif new_x < 0:
                new_x = 0
            elif new_y > height:
                new_y = height
            elif new_y < 0:
                new_y = 0

            pygame.draw.circle(screen, (255, 0, 0), (int(new_x), int(new_y)), 30)
            pyautogui.moveTo(int(new_x), int(new_y), 0.1)

        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                pygame.quit()
                return

        #clock.tick(60)  # Limit to 60 FPS

tracking_active = False

eye = Thread(target=gazetracking)
calibrate = Thread(target=Calibration)

eye.start()
calibrate.start()

eye.join()
calibrate.join()
