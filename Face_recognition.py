import json
import os.path
import cv2
from face_train import Model


class face_recognition:
    def __init__(self):
        with open('./config/contrast_table', 'r') as f:
            self.contrast_table = json.loads(f.read())
        self.model = Model()
        self.model.load_model(file_path=os.path.abspath('./model/face.model'))
        # 框住人脸的矩形边框颜色
        self.color = (0, 255, 0)

        # 捕获指定摄像头的实时视频流
        self.cap = cv2.VideoCapture(0)

        # 人脸识别分类器本地存储路径
        self.cascade_path = "./config/haarcascade_frontalface_default.xml"

    def recognition_test(self):
        while True:
            ret, frame = self.cap.read()  # 读取一帧视频

            if ret is True:
                # 图像灰化，降低计算复杂度
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                continue
            # 使用人脸识别分类器，读入分类器
            cascade = cv2.CascadeClassifier(self.cascade_path)

            # 利用分类器识别出哪个区域为人脸
            faceRects = cascade.detectMultiScale(frame_gray, scaleFactor=1.3, minNeighbors=3, minSize=(32, 32))
            if len(faceRects) > 0:
                for faceRect in faceRects:
                    x, y, w, h = faceRect

                    # 截取脸部图像提交给模型识别这是谁
                    image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                    probability, name_number = self.model.face_predict(image)
                    print(name_number)
                    name = str(self.contrast_table[str(name_number)])

                    name = name.replace('./data/', '')

                    # print('name_number:', name_number)
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), self.color, thickness=2)

                    if probability > 0.7:
                        cv2.putText(frame, name, (x + 10, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                    else:
                        cv2.putText(frame, 'unknown_human', (x + 10, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 255), 2)

            cv2.imshow("face_recognition | press q to exit", frame)

            # 等待10毫秒看是否有按键输入
            k = cv2.waitKey(10)
            # 如果输入q则退出循环
            if k & 0xFF == ord('q'):
                break

        # 释放摄像头并销毁所有窗口
        self.cap.release()
        cv2.destroyAllWindows()

    def recognition(self):
        believe_num = 30
        name = None
        believe = 0
        temp_name = None
        while True:
            ret, frame = self.cap.read()  # 读取一帧视频

            if ret is True:
                # 图像灰化，降低计算复杂度
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                continue
            # 使用人脸识别分类器，读入分类器
            cascade = cv2.CascadeClassifier(self.cascade_path)

            # 利用分类器识别出哪个区域为人脸
            faceRects = cascade.detectMultiScale(frame_gray, scaleFactor=1.3, minNeighbors=3, minSize=(32, 32))
            if len(faceRects) > 0:
                for faceRect in faceRects:
                    x, y, w, h = faceRect

                    # 截取脸部图像提交给模型识别这是谁
                    image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                    probability, name_number = self.model.face_predict(image)
                    name = str(self.contrast_table[str(name_number)])
                    name = name.replace('./data/', '')


                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), self.color, thickness=2)

                    if probability > 0.7:
                        cv2.putText(frame, 'analyzing('+str(100*believe//believe_num)+')%', (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                    else:
                        cv2.putText(frame, 'unknown', (x + 10, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 255), 2)
                        believe = 0

                    print(name,temp_name)
                    if name != temp_name:
                        temp_name = name
                        believe = 0
                    else:
                        believe += 1


            cv2.imshow("verifying | press q to exit", frame)

            # 等待10毫秒看是否有按键输入
            k = cv2.waitKey(10)
            # 如果输入q则退出循环
            if k & 0xFF == ord('q'):
                break
            if believe > believe_num:
                break

        # 释放摄像头并销毁所有窗口
        self.cap.release()
        cv2.destroyAllWindows()
        if believe > believe_num:
            return name
        else:
            return None


def start_face_recognition_test():
    fr = face_recognition()
    fr.recognition_test()

def start_face_recognition():
    fr = face_recognition()
    return fr.recognition()


if __name__ == '__main__':
    start_face_recognition_test()
