
#阴影去除算法
#先寻找阴影，然后再去除阴影
import cv2
import numpy as np
#读取图像数据到矩阵
def readImg(filepath):

    if filepath =="":
        return None

    img = cv2.imread(filepath)
    return img

#将图像转换为LAB空间
def imgToLAB(img):
    # if img==None:
    #     return None
    lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB) #参数选择cv2.COLOR_BGR2Lab,cv2.COLOR_BGR2LAB

    return lab
#将图像转换为HSV空间


#将LAB空间分割
def imgSplitLAB(img):

    l,a,b =  cv2.split(img)
    return l,a,b

#计算矩阵的平均值
def calMatAvg(img_single):
    print(img_single.shape)
    w,h = img_single.shape
    sum = 0

    for i in range(w):
        for j in range(h):
            sum = sum+img_single[i][j]

    avg = sum/(w*h)

    return avg

#计算矩阵标准差
def calMatSD(mat):

    mat = np.array(mat)
    sd = np.std(mat)

    return sd

#获取阴影像素所在位置的集合列表
def getPointSetByL(img_lab,l,b):

    L, A, B = imgSplitLAB(img_lab)
    avg_l = calMatAvg(L)
    avg_a = calMatAvg(A)
    avg_b = calMatAvg(B)
    sd = calMatSD(L)
    points = []
    w,h = L.shape
    thre = avg_l-(sd/3)
    print(avg_a+avg_b)

    for i in range(w):
        for j in range(h):
            print(B[i][j],end=" ")
            if (avg_a+avg_b)<256:
                if L[i][j]<thre:
                    points.append((i,j))
            elif (L[i][j]>l[0] and L[i][j]<l[1]) and B[i][j]>b[0] and B[i][j]<b[1]:
                points.append((i,j))
        print("")
    return points

#LAB颜色空间拾取器
def onmouse(event, x, y, flags, param):
    img_lab = imgToLAB(img)
    L, A, B = imgSplitLAB(img_lab)

    if event == cv2.EVENT_MOUSEMOVE:
        show = []
        show.append(L[y][x])
        show.append(A[y][x])
        show.append(B[y][x])
        print(show)

def getLAB(img):
    cv2.namedWindow("img")  # 构建窗口
    cv2.setMouseCallback("img", onmouse)  # 回调绑定窗口
    while True:  # 无限循环
        cv2.imshow("img", img)  # 显示图像
        if cv2.waitKey() == ord('q'): break  # 按下‘q'键，退出
    cv2.destroyAllWindows()

if __name__ =="__main__":
   img = readImg("./image/one.jpg")
   l = [120,160]
   b = [125,130]
   #getLAB(img)
   img_lab = imgToLAB(img)
   res = getPointSetByL(img_lab,l,b)
   print(res)

   for p in res:
       x,y = p
       cv2.circle(img,(y,x),1,(0,0,255),-1)

   cv2.imshow("img",img)

   cv2.waitKey(0)
   cv2.destroyWindow()
