# -*- coding:utf-8 -*-
import cv2
import numpy as np
import sys

def videoBlueColorCapture():

    cap = cv2.VideoCapture(0)

    while (1):

        # 读取视频的每一帧
        _, frame = cap.read()

        # 将图片从 BGR 空间转换到 HSV 空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 定义在HSV空间中蓝色的范围
        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # 根据以上定义的蓝色的阈值得到蓝色的部分
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

def videoCapture():
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('test.avi') #use local file to create capture
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame, 0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)

    # 视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)

    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break

            # 显示图像并等待10毫秒按键输入，输入‘q’退出程序
        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break

            # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        CatchUsbVideo("截取视频流", int(0))
        #print("Usage:%s camera_id\r\n" % (sys.argv[0]))
    else:
        CatchUsbVideo("截取视频流", int(sys.argv[1]))