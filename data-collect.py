import time
import pyautogui
import random 
import face_recognition
import cv2
import numpy as np
import os


screen_w, screen_h = pyautogui.size()
video_capture = cv2.VideoCapture(0)
l,r = 0,0
directory = "data"
x_buffer = 20
y_buffer = 20

def bounding_box(points):
	x_coordinates, y_coordinates = zip(*points)
	return [(min(x_coordinates) - x_buffer, min(y_coordinates) - y_buffer), (max(x_coordinates) + x_buffer, max(y_coordinates) + y_buffer)]


if not os.path.exists(directory+"/left"):
    os.makedirs(directory+"/left")
if not os.path.exists(directory+"/right"):
    os.makedirs(directory+"/right")
while True:
	# Move the cursor to a random location on the screen
	cursor_x,cursor_y = random.randrange(screen_w-5),random.randrange(screen_h-5)
	pyautogui.moveTo(cursor_x, cursor_y, duration=0.25)
	

	# Give the eye time to move
	time.sleep(0.5)		
	
	# Grab a single frame of video
	ret, frame = video_capture.read()

	# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	face_landmarks_list = face_recognition.face_landmarks(frame[:, :, ::-1])
	# Check if there are any face landmarks 
	if len(face_landmarks_list) > 0:
		face_landmarks = face_landmarks_list[0]
		if face_landmarks['left_eye']:
			points = bounding_box(face_landmarks['left_eye'])
			left = frame[points[0][1]:points[1][1], points[0][0]: points[1][0]]
			cv2.imwrite(directory+"/left/{}_{}_{}.jpg".format(l, cursor_x, cursor_y), left)
			l += 1
		if face_landmarks['right_eye']:
			points = bounding_box(face_landmarks['right_eye'])
			right = frame[points[0][1]:points[1][1], points[0][0]: points[1][0]]
			cv2.imwrite(directory+"/right/{}_{}_{}.jpg".format(r, cursor_x, cursor_y), right)
			r += 1
	#pauses for 50 miliseconds before fetching next image
	key = cv2.waitKey(1) 
	#if ESC is pressed, exit loop
	if key == 27:
		break
	
# Release handle to the webcam
video_capture.release()