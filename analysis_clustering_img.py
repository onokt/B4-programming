import cv2
import time
import os
import numpy as np
import matplotlib.pyplot as plt

# os.makedirs('./Image/Measure')
# os.makedirs('./Image/Measure2')
file = open(f'./Data/Spark_coordinate.txt', 'a')
n = 0
startTime = time.time()
# for i in range(n):
while True:
    Center = []
    threshold = 70
    img = cv2.imread('./Image/Measure3/frame{}.jpg'.format(str(n)), 0)
    if img is None:
        file.close()
        break
    ret, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
# ノイズ除去
    ksize = 3
    img = cv2.medianBlur(img, ksize)

    Z1, X = img.shape
    x1 = []
    z1 = []
    for i in range(Z1):
        for j in range(X):
            if img[i, j] == 255:
                x1.append(j+0.5)
                z1.append(i+0.5)

    C1 = np.array(list(zip(x1, z1)))
    C1 = np.float32(C1)

    img_resize = cv2.resize(img, (int(Z1*0.4), int(X*0.4)))
    ret, img_resize = cv2.threshold(img_resize, threshold, 255, cv2.THRESH_BINARY)
    Z1_resize, X_resize = img_resize.shape


    img1 = cv2.imread('./Image/Measure4/frame{}.jpg'.format(str(n)), 0)
    if img1 is None:
        file.close()
        break
    ret, img1 = cv2.threshold(img1, threshold, 255, cv2.THRESH_BINARY)
# ノイズ除去
    img1 = cv2.medianBlur(img1, ksize)


    Z2, Y = img1.shape
    y1 = []
    z2 = []
    for i in range(Z2):
        for j in range(Y):
            if img1[i, j] == 255:
                y1.append(j+0.5)
                z2.append(i+0.5)

    C2 = np.array(list(zip(y1, z2)))
    C2 = np.float32(C2)

    img1_resize = cv2.resize(img1, (int(Z2*0.4), int(Y*0.4)))
    ret, img1_resize = cv2.threshold(img1_resize, threshold, 255, cv2.THRESH_BINARY)
    Z2_resize, Y_resize = img1_resize.shape


# 配列の定義
    case1 = np.array([[0, 0],
                      [0, 0]])

    case2_1 = np.array([[255, 0],
                        [0, 0]])
    case2_2 = np.array([[0, 255],
                        [0, 0]])
    case2_3 = np.array([[0, 0],
                        [255, 0]])
    case2_4 = np.array([[0, 0],
                        [0, 255]])
    case3_1 = np.array([[255, 255],
                        [0, 0]])
    case3_2 = np.array([[255, 0],
                        [255, 0]])
    case3_3 = np.array([[255, 0],
                        [0, 255]])
    case3_4 = np.array([[0, 255],
                        [255, 0]])
    case3_5 = np.array([[0, 255],
                        [0, 255]])
    case3_6 = np.array([[0, 0],
                        [255, 255]])

    case4_1 = np.array([[0, 255],
                        [255, 255]])
    case4_2 = np.array([[255, 0],
                        [255, 255]])
    case4_3 = np.array([[255, 255],
                        [0, 255]])
    case4_4 = np.array([[255, 255],
                        [255, 0]])

    case5 = np.array([[255, 255],
                      [255, 255]])


    case_number = 0
    for i in range(Z1_resize):
        for j in range(X_resize):
            k = img_resize[i:i+2, j:j+2]
            # m = img[Y-2-i:Y-i, j:j+2]
            if np.sum(k == case1) == 4:
                case_number += 0
                # print('1')
            elif np.sum(k == case2_1) == 4 or np.sum(k == case2_2) == 4 or np.sum(k == case2_3) == 4 or np.sum(k == case2_4) == 4:
                case_number += 1
                # print('2')
            elif np.sum(k == case3_1) == 4 or np.sum(k == case3_2) == 4 or np.sum(k == case3_3) == 4 or np.sum(k == case3_4) == 4 or np.sum(k == case3_5) == 4 or np.sum(k == case3_6) == 4:
                case_number += 0
                # print('3')
            elif np.sum(k == case4_1) == 4 or np.sum(k == case4_2) == 4 or np.sum(k == case4_3) == 4 or np.sum(k == case4_4) == 4:
                case_number -= 1
                # print('4')
            elif np.sum(k == case5):
                case_number += 0
                # print('5')

    cluster_num = case_number/4
    # print(cluster_num)


    case_number1 = 0
    for i in range(Z2_resize):
        for j in range(Y_resize):
            k = img1_resize[i:i+2, j:j+2]
            # m = img[Y-2-i:Y-i, j:j+2]
            if np.sum(k == case1) == 4:
                case_number1 += 0
                # print('1')
            elif np.sum(k == case2_1) == 4 or np.sum(k == case2_2) == 4 or np.sum(k == case2_3) == 4 or np.sum(k == case2_4) == 4:
                case_number1 += 1
                # print('2')
            elif np.sum(k == case3_1) == 4 or np.sum(k == case3_2) == 4 or np.sum(k == case3_3) == 4 or np.sum(k == case3_4) == 4 or np.sum(k == case3_5) == 4 or np.sum(k == case3_6) == 4:
                case_number1 += 0
                # print('3')
            elif np.sum(k == case4_1) == 4 or np.sum(k == case4_2) == 4 or np.sum(k == case4_3) == 4 or np.sum(k == case4_4) == 4:
                case_number1 -= 1
                # print('4')
            elif np.sum(k == case5):
                case_number1 += 0
                # print('5')

    cluster_num1 = case_number1/4
    # print(cluster_num1)



    if cluster_num == cluster_num1 ==3:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
        ret, label, center = cv2.kmeans(C1, 3, None, criteria, 100, cv2.KMEANS_RANDOM_CENTERS)

        A = C1[label.ravel() == 0]
        B = C1[label.ravel() == 1]
        C = C1[label.ravel() == 2]

        fig, ax = plt.subplots()
        ax.invert_yaxis()
        ax.scatter(A[:, 0], A[:, 1], s=5, c='b', label='coordinate of pixel')
        ax.scatter(B[:, 0], B[:, 1], s=5, c='g', label='coordinate of pixel')
        ax.scatter(C[:, 0], C[:, 1], s=5, c='r', label='coordinate of pixel')
        ax.scatter(center[:, 0], center[:, 1], s=8, c='y',  marker='s', label='center')
        plt.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=10)
        plt.xlabel('X'), plt.ylabel('Z')
        plt.title('Center of discharge')
        fig.show()
        # print(center)
        center = sorted(center, key=lambda x: x[1])
        for i in range(len(center)):
            Center.append(center[i][0])

        criteria1 = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
        ret, label1, center1 = cv2.kmeans(C2, 3, None, criteria1, 100, cv2.KMEANS_RANDOM_CENTERS)

        D = C2[label1.ravel() == 3]
        E = C2[label1.ravel() == 4]
        F = C2[label1.ravel() == 5]

        fig1, ay = plt.subplots()
        ay.invert_yaxis()
        ay.scatter(D[:, 0], D[:, 1], s=5, c='b', label='coordinate of pixel')
        ay.scatter(E[:, 0], E[:, 1], s=5, c='g', label='coordinate of pixel')
        ay.scatter(F[:, 0], F[:, 1], s=5, c='r', label='coordinate of pixel')
        ay.scatter(center1[:, 0], center1[:, 1], s=8, c='y',  marker='s', label='center')
        plt.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=10)
        plt.xlabel('Y'), plt.ylabel('Z')
        plt.title('Center of discharge2')
        fig1.show()
        # print(center1)
        center1 = sorted(center1, key=lambda x: x[1])
        for i in range(len(center1)):
            Center.append(center1[i][0])
    print(Center)
    if len(Center) == 6:
        for t in range(len(Center)):
            if t == len(Center) - 1:
                file.write(str(Center[t]) + '\n')
            else:
                file.write(str(Center[t]) + ' ')

    n += 1

endTime = time.time()
runTime = endTime - startTime
print(runTime)