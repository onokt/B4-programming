import cv2
import numpy as np
import matplotlib.pyplot as plt

bg = cv2.imread('./Image/background.jpg')
cap = cv2.VideoCapture('./image/chamber.mp4')
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
    if cnt > 1500 and cnt < 1600:  #threshold(1)　ここでthresholdをきつくすれば1層しかならないときのものをきれるはず
        cv2.imwrite('./Image/Measure/frame{}.jpg'.format(str(n)), frame)  #異常のあるフレーム(光っている)を保存
    # cv2.imwrite('/Image/Measure2/mask_image{}.jpg'.format(str(n)), output)
        img = cv2.imread('./Image/Measure/frame{}.jpg'.format(str(n)))
        model2 = cv2.bgsegm.createBackgroundSubtractorMOG()
        mask2 = model.apply(bg)
        mask2 = model.apply(img)
        cv2.imwrite('./Image/Measure2/mask_image{}.jpg'.format(str(n)), mask2)  #maskを保存(はじめのほうで保存できないのはなぜ？)

        Y, X = mask2.shape

        R = []  # 画素値がゼロでないエリアのｙ座標
        for j in range(Y):
            x = []  # x座標
            s = []  # 明るさ
            for i in range(X):
                x.append(i)
                s.append(int(mask2[j, i]))
            print(s)
            if s.count(255) > 20:  # threshold(2) (ここのthresholdはさじ加減大事)
                R.append(j)

        # print(R)
        # print(len(R))
        y_max = []  #光っているy座標
        x_max = []  #光っている位置xのうち画素値が最大のx座標
        for y2 in R:
            x1 = []
            s1 = []
            for m in range(X):
                x1.append(m)
                s1.append(int(mask2[y2, m]))
            y_max.append(y2)
            x_max.append((s1.index(max(s1))))
            # plt.plot(x1, y1)
            # plt.show()

        # print(str(x_max)+' '+str(y_max))

        file = open(f'./Data/list{str(n)}.txt', 'w')
        for i in range(int(len(x_max))):
            file.write(str(x_max[i])+' '+str(-y_max[i])+'\n')
            # print(len(x_max))
        file.close()
        n += 1

