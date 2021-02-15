import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

startTime = time.time()
file = open(f'./Data/Spark_coordinate2.txt', 'a')
n = 0
threshold = 70
while True:
    img_x = cv2.imread('./Image/Measure3/frame{}.jpg'.format(str(n)), 0)
    img_y = cv2.imread('./Image/Measure4/frame{}.jpg'.format(str(n)), 0)
    img_x_y = [img_x, img_y]
    center = []
    if img_y is None:
        file.close()
        break

    for img in img_x_y:
        z = []
        x = []
        H, W = img.shape
        ret, img_binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        ksize = 3
        img_binary = cv2.medianBlur(img_binary, ksize)

        for a in range(H):
            for b in range(W):
                if img_binary[a, b] == 255:
                    z.append(a+0.5)
                    x.append(b+0.5)

        C = np.array(list(zip(z, x)))
        # C = []
        # for i in range(len(z1)):
        #     C.append((z1[i], x[i]))

#yのscanでクラスターの数を調べる
        cluster_num = 1
        for i in range(len(C)):
            if (C[i][0] > C[i-1][0]+1):
                cluster_num += 1

        # print(cluster_num_x)

        if cluster_num == 3:  #3点の場合は3、2点の場合は2
            j = 0
            k = 0
            C1 = []
            C2 = []
            C3 = []

            for i in range(len(C)):
                if (C[i][0] > C[i-1][0]+1) and j == 0:
                    C1 = C[:i]
                    k = i
                    j += 1

                elif (C[i][0] > C[i-1][0]+1) and j == 1:
                    C2 = C[k:i]
                    C3 = C[i:]
                    j += 1
                    break

        ###################################################################################################
            cluster = [C1, C2, C3]

        # 同じ層に複数なっているか確認
            B = []
            b = 0
            for k in cluster:
                for i in range(len(k)):
                    if (k[i][1] > k[i - 1][1] + 1):
                        b += 1
                B.append(b)
                b = 0
            # print(B)

        # calculation of center
            if B.count(0) == 3:
                ave = []
                Sum = 0
                for g in cluster:
                    for h in range(len(g)):
                        Sum += g[h][1]
                    ave.append(Sum/len(g))
                    Sum = 0
                center.append(ave)

    print(center)

    #ファイルに書き出し
    if len(center) == 2:
        for s in range(len(center[0])):
            file.write(str(center[0][s]) + ' ')
        for t in range(len(center[1])):
            if t == len(center[1])-1:
                file.write(str(center[1][t]) + '\n')
            else:
                file.write(str(center[1][t]) + ' ')

    # for s in range(len(ave)):
    #     if s == len(ave)-1:
    #         file.write(str(ave[s]) + '\n')
    #     else:
    #         file.write(str(ave[s]) + ' ')



    n += 1

endTime = time.time()
runTime = endTime - startTime

print(runTime)
