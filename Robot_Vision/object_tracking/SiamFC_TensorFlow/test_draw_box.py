# -*- coding: utf-8 -*-

import cv2
import pdb

def draw_box(event,x,y,flags,param):
    ix,iy,drawFlag,tempFlag,bbox = param

    if event == cv2.EVENT_LBUTTONDOWN:
        print("Click on {},{} .".format(x,y))
        param[2],param[3] = True,True
        param[0],param[1] = x,y

    elif event == cv2.EVENT_LBUTTONUP:
        if drawFlag == True:
            param[2] = False
            param[-1] = (ix,iy,x,y)
            print("Draw box on {},{},{},{}".format(ix,iy,x,y))

def main():
    # ix,iy,drawFlag,tempFlag,bbox = draw_box_params
    draw_box_params = [-1,-1,False,False,(-1,-1,-1,-1)]

    cap = cv2.VideoCapture(-1)

    f_count = 0
    cv2.namedWindow("temp")
    cv2.setMouseCallback("temp",draw_box,draw_box_params)

    while True:
        ret,frame = cap.read()
        ix,iy,drawFlag,tempFlag,bbox = draw_box_params

        if f_count == 0: # wait for drawing box
            while True:
                init_frame = frame
                cv2.imshow("temp",init_frame)
                k = cv2.waitKey(0)
                if k == 32:
                    ix,iy,drawFlag,tempFlag,bbox = draw_box_params
                    cv2.rectangle(init_frame,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,255,0),1)
                    break

        cv2.rectangle(frame,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,255,0),1)
        cv2.imshow("video",frame)
        cv2.imshow("temp",init_frame)
        f_count += 1
        k = cv2.waitKey(33)
        if k == 32: # press `Space`
            break


if __name__ == '__main__':
    main()

