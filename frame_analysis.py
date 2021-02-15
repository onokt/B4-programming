import cv2
import os
import time

startTime = time.time()
os.makedirs('./Image/Measure')
os.makedirs('./Image/Measure2')


# x方向の動画
bg_x = cv2.imread('./Image/background.jpg')
cap_x = cv2.VideoCapture('./Image/discharge.MOV')
W_x = cap_x.get(cv2.CAP_PROP_FRAME_WIDTH)
H_x = cap_x.get(cv2.CAP_PROP_FRAME_HEIGHT)

# y方向の動画
bg_y = cv2.imread('./Image/background_3.jpg')
cap_y = cv2.VideoCapture('./Image/sample.mp4')
W_y = cap_y.get(cv2.CAP_PROP_FRAME_WIDTH)
H_y = cap_y.get(cv2.CAP_PROP_FRAME_HEIGHT)

j = 0  #ファイル保存のindex
count = 0
threshold = 0

while True:
    ret, frame_x = cap_x.read()
    ret, frame_y = cap_y.read()
    if not ret:
        break

    model_x = cv2.bgsegm.createBackgroundSubtractorMOG()
    model_y = cv2.bgsegm.createBackgroundSubtractorMOG()

    mask_x = model_x.apply(bg_x)
    mask_x = model_x.apply(frame_x)

    mask_y = model_y.apply(bg_y)
    mask_y = model_y.apply(frame_y)

    Size_x = W_x * H_x
    white_cnt_x = cv2.countNonZero(mask_x)
    # black_cnt_x = Size_x - white_cnt_x
    ratio_x = white_cnt_x/Size_x

    Size_y = W_y * H_y
    white_cnt_y = cv2.countNonZero(mask_y)
    # black_cnt_y = Size_y - white_cnt_y
    ratio_y = white_cnt_y / Size_y
    # print(str(ratio_x) + ' ' + str(ratio_y))
    # print(ratio_y)
    if (ratio_x < 0.1 and ratio_y < 0.1 ):
        if(ratio_x != 0 and ratio_y != 0 and count != k+1):
            # print(count)
            # print(str(ratio_x)+' '+str(ratio_y))
            cv2.imwrite('./Image/Measure/frame{}.jpg'.format(str(j)), frame_x)
            cv2.imwrite('./Image/Measure2/frame{}.jpg'.format(str(j)), frame_y)
            j += 1
            k = count

    count += 1

endTime = time.time()
runTime = endTime - startTime

print(runTime)

