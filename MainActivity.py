import json
import os
import sys

import PyQt5
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QAbstractItemView

from encrypt import read_with_decrypt, write_with_encrypt
from face_recognition import start_face_recognition_test, start_face_recognition
from face_train import do_train
from get_face import CatchPICFromVideo
from load_data import read_saved_name_for_ui
from ui_diary import Ui_Diary
from ui_main import Ui_MainWindow
from ui_settings import Ui_Settings


def add_tmp_env_var():
    """
    下面这三句是在使用临时环境变量
    正常来说应该添加到系统环境变量, 但这里用的venv, 就暂时用这个临时的吧
    """
    dir_name = os.path.dirname(PyQt5.__file__)
    plugin_path = os.path.join(dir_name, 'Qt5', 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


def pushButton_start_face_recognition():
    try:
        open('./config/contrast_table', 'r')
    except OSError:
        show_hint('请先进行训练')
        return
    start_face_recognition_test()
def pushButton_get_pic():
    name_ = settings_ui.plainTextEdit_human_name.toPlainText()
    if name_ is None or '':
        show_hint('输入无效')
        return
    CatchPICFromVideo(name_)
    show_hint('采集完成')
    refresh_ListView()
def pushButton_start_train():
    do_train()
    show_hint('训练完成')
    refresh_ListView()
    '''
    thread = z_thread()
    thread.breakSignal.connect(print_done)
    thread.start()
    '''
def commandLinkButton_start_write_diary():
    global curr_user_name
    name = start_face_recognition()
    print(name)
    if name is not None:
        curr_user_name = name
        show_hint('欢迎回来,' + curr_user_name)
    else:
        show_hint('获取用户信息失败')
        return

    # main_window.close()
    text = '在这里记录你的每一天'
    try:
        text = read_with_decrypt('./diary/'+curr_user_name+'/', 'diary')
        # diary = open(, 'r')
        # text = diary.read()
    except OSError:
        pass

    diary_ui.plainTextEdit_diary.setPlainText(text)
    diary_window.setWindowTitle(curr_user_name + '的日记')
    diary_window.show()


def save_diary():
    # return的是是否保存成功
    if curr_user_name is None:
        show_hint('当前用户无效')
        return False
    try:
        write_with_encrypt('./diary/'+curr_user_name+'/', 'diary', diary_ui.plainTextEdit_diary.toPlainText())
        # diary = open('diary/'+curr_user_name, 'w')
        # diary.write(diary_ui.plainTextEdit_diary.toPlainText())
    except OSError:
        show_hint('保存失败')
        return False

    show_hint('保存完成')
    return True
def save_diary_and_exit():
    if not save_diary():
        return
    sys.exit(0)


def show_hint(text):
    msg_box = QMessageBox(QMessageBox.Warning, '提示', text)
    msg_box.exec_()


def init_ListView(list_, view):
    string_list_model = QStringListModel()  # 创建mode
    string_list_model.removeRows(1, 2)
    string_list_model.setStringList(list_)
    view.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不允许编辑

    view.setModel(string_list_model)
def refresh_ListView():
    init_ListView(read_saved_name_for_ui(), settings_ui.listView_human_list)
    try:
        f = open('./config/contrast_table', 'r')
        contrast_table = json.loads(f.read())
        name_list = []
        for i in contrast_table:
            name = str(contrast_table[str(i)])
            name = name.replace('./data/', '')
            name_list.append(name)
    except OSError:
        name_list=[]

    init_ListView(name_list, settings_ui.listView_human_list_trained)


# 程序入口点
if __name__ == '__main__':
    add_tmp_env_var()

    myapp = QApplication(sys.argv)

    main_window = QMainWindow()
    main_ui = Ui_MainWindow()
    main_ui.setupUi(main_window)

    settings_window = QWidget()
    settings_ui = Ui_Settings()
    settings_ui.setupUi(settings_window)

    diary_window = QWidget()
    diary_ui = Ui_Diary()
    diary_ui.setupUi(diary_window)

    # 连接各个按钮的onclick事件
    settings_ui.pushButton_start_face_recognition.clicked.connect(pushButton_start_face_recognition)
    settings_ui.pushButton_get_pic.clicked.connect(pushButton_get_pic)
    settings_ui.pushButton_start_train.clicked.connect(pushButton_start_train)    # todo qthread
    main_ui.commandLinkButton_settings.clicked.connect(settings_window.show)
    main_ui.commandLinkButton_start_write_diary.clicked.connect(commandLinkButton_start_write_diary)
    diary_ui.commandLinkButton_save.clicked.connect(save_diary)
    diary_ui.commandLinkButton_save_and_exit.clicked.connect(save_diary_and_exit)
    curr_user_name = 'null'

    refresh_ListView()

    main_window.show()
    sys.exit(myapp.exec_())
