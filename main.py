import cv2
import time
import glob
from emailing import send_email
import os
from threading import Thread

video = cv2.VideoCapture(0)

def clean_images():
    images = glob.glob('images/*.png')
    for img in images:
        os.remove(img)

time.sleep(1)
first_frame = None
status_list = []
count=0
clean_images()
while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21,21),0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame,gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame,63,255,cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dil_frame = cv2.dilate(thresh_frame, kernel, iterations=2)
    #cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for con in contours:
        if cv2.contourArea(con) <10000:
            continue
        x, y, w, h = cv2.boundingRect(con)
        rectangle = cv2.rectangle(frame,(x,y),(x+w,h+y),(0,255,0),3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        all_images = glob.glob('images/*.png')
        index = int(len(all_images) / 2)
        email_thread = Thread(target=send_email, args=(all_images[index],))
        email_thread.start()


    cv2.imshow('Video',frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
