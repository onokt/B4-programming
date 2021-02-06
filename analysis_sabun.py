import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('./Image/Measure')
os.makedirs('./Image/Measure2')
# os.makedirs('./Data/Scan')  #改善したい

bg = cv2.imread('./Image/background.jpg')
cap = cv2.VideoCapture('./Image/discharge.MOV')
# number = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
# model = cv2.bgsegm.createBackgroundSubtractorMOG()

n = 0  #ファイルの読み込みのためのindex

while True:
    ret, frame = cap.read()
    if not ret:
        break
    model = cv2.bgsegm.createBackgroundSubtractorMOG()

    mask = model.apply(bg)
    mask = model.apply(frame)

    cnt = cv2.countNonZero(mask)
    if cnt > 200 and cnt < 1600:  #threshold(1)　ここでthresholdをきつくすれば1層しかならないときのものをきれるはず
        cv2.imwrite('./Image/Measure/frame{}.jpg'.format(str(n)), frame)  #異常のあるフレーム(光っている)を保存
    # cv2.imwrite('/Image/Measure2/mask_image{}.jpg'.format(str(n)), output)

        img = cv2.imread('./Image/Measure/frame{}.jpg'.format(str(n)))
        model2 = cv2.bgsegm.createBackgroundSubtractorMOG()
        mask2 = model.apply(bg)
        mask2 = model.apply(img)
        cv2.imwrite('./Image/Measure2/mask_image{}.jpg'.format(str(n)), mask2)  #maskを保存(はじめのほうで保存できないのはなぜ？)

#######################################################################################################################

        #x_max y_max の取得
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        Y, X = gray.shape

        y_max = []  # 画素値がゼロでないエリアのｙ座標
        for j in range(Y):
            x = []  # x座標
            s = []  # 明るさ
            for i in range(X):
                x.append(i)
                s.append(int(gray[j, i]))
            print(s)
            if max(s) > 100:  # threshold(2) (ここのthresholdはさじ加減大事)
                # fig = plt.figure()
                # plt.plot(x, s)
                # fig.savefig("./Data/Scan/img{}.png".format(str(j)))  # j = y座標
                y_max.append(j)

        # print(R)
        # print(len(R))
        x_max = []  #光っている位置xのうち画素値が最大のx座標
        for y2 in y_max:
            s1 = []
            for m in range(X):
                s1.append(int(gray[y2, m]))
            x_max.append((s1.index(max(s1))))
            # plt.plot(x1, y1)
            # plt.show()

#####################################################################################################################
        # 各座標の平均を求める
        ave_x1_x2_x3 = []  #平均:　放電の数だけx座標が入る
        ave_y1_y2_y3 = []
        r = 0  #連続部の数　（一か所平均が求まるとリセットされる）
        j = 0  #while文を回すためのindex
        Sum_x = 0
        Sum_y = 0
        while True:
            if j == len(y_max) - 1:
                Sum_x += x_max[j]
                Sum_y += y_max[j]
                ave_x1_x2_x3.append(round((Sum_x / (r + 1)), 1))
                ave_y1_y2_y3.append(round((Sum_y / (r + 1)), 1))
                break
            if y_max[j + 1] == y_max[j] + 1:
                Sum_x += x_max[j]
                Sum_y += y_max[j]
                r += 1
            elif y_max[j + 1] > y_max[j] + 1:
                Sum_x += x_max[j]
                Sum_y += y_max[j]
                ave_x1_x2_x3.append(round((Sum_x / (r + 1)), 1))
                ave_y1_y2_y3.append(round((Sum_y / (r + 1)), 1))
                Sum_x = 0
                Sum_y = 0
                r = 0

            j += 1

        # print(ave_x1_x2_x3)
        # print(ave_y1_y2_y3)
##################################################################################################################

        file = open(f'./Data/Spark_coordinate.txt', 'a')
        file.write(str(ave_x1_x2_x3)+'\n')
            # print(len(x_max))
        file.close()






        # file = open(f'./Data/list{str(n)}.txt', 'w')
        # for i in range(int(len(x_max))):
        #     file.write(str(x_max[i])+' '+str(-y_max[i])+'\n')
        #     # print(len(x_max))
        # file.close()
        n += 1

