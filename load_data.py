import json
import os
import cv2
import numpy as np

IMAGE_SIZE = 64


# 按照指定图像大小调整尺寸
def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
    top, bottom, left, right = (0, 0, 0, 0)

    # 获取图像尺寸
    h, w, _ = image.shape  # (237, 237, 3)

    # 对于长宽不相等的图片，找到最长的一边
    longest_edge = max(h, w)

    # 计算短边需要增加多上像素宽度使其与长边等长
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass

        # RGB颜色
    BLACK = [0, 0, 0]

    # 边缘填充 0 给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)

    # 调整图像大小并返回
    return cv2.resize(constant, (height, width))


images = []
labels = []

# 读取训练数据
def read_path(path_name):
    for dir_item in os.listdir(path_name):

        # 从初始路径开始叠加，合并成可识别的操作路径
        full_path = os.path.join(path_name, dir_item)

        if os.path.isdir(full_path):  # 如果是文件夹，继续递归调用
            read_path(full_path)
        else:  # 文件
            if dir_item.endswith('.jpg'):
                image = cv2.imread(full_path)
                if image is None:
                    return
                image = resize_image(image, IMAGE_SIZE, IMAGE_SIZE)

                # 放开这个代码，可以看到resize_image()函数的实际调用效果
                # cv2.imwrite('1.jpg', image)

                images.append(image)
                labels.append(path_name.split('\\')[-1])

    return images, labels

# 捏麻麻的,这个递归是真烦,害老子debug找了好久
# 不太好的实现,但是懒得优化了,为了这个递归妥协下
def read_path_with_clear(path_name):
    global images
    global labels
    images_, labels_ = read_path(path_name)
    images = []
    labels = []
    return images_, labels_

def read_saved_name_for_ui(path_name='./data/'):
    labels_ = []
    dir_item = os.listdir(path_name)
    for i in dir_item:
        i = str(i)
        i = i.replace('./data/', '')
        labels_.append(i)
    return labels_


# 从指定路径读取训练数据
def load_dataset(path_name):
    temp_images, temp_labels = read_path_with_clear(path_name)
    print('labels:', temp_labels)

    # 将输入的所有图片转成四维数组，尺寸为(图片数量*IMAGE_SIZE*IMAGE_SIZE*3)
    # 图片为64 * 64像素,一个像素3个颜色值(RGB)
    temp_images = np.array(temp_images)
    print(temp_images.shape)

    labels1 = list(set(temp_labels))
    face_num = len(labels1)
    print('face_num:', face_num)
    num = [i for i in range(face_num)]
    contrast_table = dict(zip(num, labels1))
    # 这里不再更新contrast_table, 防止训练一半退出导致错乱, 应在update_contrast_table()更新
    # with open('./config/contrast_table', 'w') as f:
    #    f.write(json.dumps(contrast_table))
    # print('contrast_table:', contrast_table)
    for index, name in contrast_table.items():
        for i in range(len(temp_labels)):
            if temp_labels[i] == name:
                temp_labels[i] = index
    # print(labels)
    temp_labels = np.array(temp_labels)

    return temp_images, temp_labels, face_num


def update_contrast_table(path_name):
    temp_images, temp_labels = read_path_with_clear(path_name)

    labels1 = list(set(temp_labels))
    face_num = len(labels1)
    print('generating contrast table')
    print('temp_labels=', temp_labels)
    print('labels1=', labels1)
    print('face_num=', face_num)
    num = [i for i in range(face_num)]
    contrast_table = dict(zip(num, labels1))
    with open('./config/contrast_table', 'w') as f:
        f.write(json.dumps(contrast_table))


if __name__ == '__main__':
    update_contrast_table('./data/')
