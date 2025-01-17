import os
import cv2


def CatchPICFromVideo(path_name, camera_idx=0, catch_pic_num=200):
    window_name = path_name + " - press q to quit"
    cv2.namedWindow(window_name)
    path_name = os.path.join('data', path_name)
    os.makedirs(path_name, exist_ok=False)

    # 视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)

    # 告诉OpenCV使用人脸识别分类器
    classfier = cv2.CascadeClassifier("./config/haarcascade_frontalface_default.xml")

    # 识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 191, 255)

    num = 0
    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将当前桢图像转换成灰度图像

        # 人脸检测
        faceRects = classfier.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:  # 大于0则检测到人脸
            for faceRect in faceRects:  # 单独框出每一张人脸
                x, y, w, h = faceRect

                # 将当前帧保存为图片
                img_name = '%s/%d.jpg ' % (path_name, num)
                image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                cv2.imwrite(img_name, image)

                num += 1
                if num > catch_pic_num:  # 如果超过指定最大保存数量退出循环
                    break

                # 画出矩形框
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

                # 显示当前捕捉到了多少人脸图片了
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '%d/%d' % (num, catch_pic_num), (x + 10, y - 30), font, 1, (255, 0, 255), 4)

                # 超过指定最大保存数量结束程序
        if num > catch_pic_num:
            break

        # 显示图像
        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break

            # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    CatchPICFromVideo('test')
