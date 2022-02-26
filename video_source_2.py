from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
import sys
import numpy as np
import cv2
from time import sleep


# start ui class
class UI(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(589, 300)
        self.video_sources = QtWidgets.QComboBox(Dialog)
        self.video_sources.setGeometry(QtCore.QRect(70, 70, 401, 31))
        self.video_sources.setCurrentText("")
        self.video_sources.setObjectName("video_sources")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(70, 160, 351, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.file_btn = QtWidgets.QPushButton(Dialog)
        self.file_btn.setGeometry(QtCore.QRect(440, 160, 41, 31))
        self.file_btn.setObjectName("file_btn")
        self.start_btn = QtWidgets.QPushButton(Dialog)
        self.start_btn.setGeometry(QtCore.QRect(460, 240, 111, 41))
        self.start_btn.setObjectName("start_btn")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 30, 251, 41))
        self.label.setObjectName("label")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QtCore.QRect(70, 130, 161, 31))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Choose  video source"))
        self.file_btn.setText(_translate("Dialog", "..."))
        self.start_btn.setText(_translate("Dialog", "start"))
        self.label.setText(_translate("Dialog", "Choose video source"))
        self.checkBox.setText(_translate("Dialog", "Or choose video file"))

# end ui class


class VideoSources(QtWidgets.QDialog, UI):
    def __init__(self, parent=None):
        super(VideoSources, self).__init__(parent)
        QtWidgets.QDialog.__init__(self)
        self.selected_source = None
        self.setupUi(self)

        self.sources_dict = {}
        self.sources = self.video_sources

        self.append_sources()
        self.buttons()

    def buttons(self):
        self.start_btn.clicked.connect(self.get_selected_source)
        self.file_btn.clicked.connect(self.get_file)
        self.start_btn.clicked.connect(self.start_opencv)

    def get_sources(self):
        for i in range(0, 10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cap.release()
                self.sources_dict[f'source {i + 1}'] = i
            else:
                continue

        return self.sources_dict

    def append_sources(self):
        self.get_sources()
        self.sources.addItems(self.sources_dict.keys())

    def get_selected_source(self):
        if self.checkBox.isChecked():
            self.selected_source = self.lineEdit.text()

        else:
            self.selected_source = int(self.sources_dict[self.sources.currentText()])

    def get_file(self):
        text = QFileDialog.getOpenFileName(self, "select the video")
        self.lineEdit.setText(str(text[0]))

    def draw_rect_and_take_photo(self, e, x, y, flags, params):
        window = params['window']
        image = params['img']
        spare_img = params['img'].copy()
        p_w = 100
        p_h = 100

        if e == cv2.EVENT_MOUSEMOVE:
            cv2.rectangle(image, (x - p_w, y - p_h), (x + p_w, y + p_h), (0, 255, 0), 2)
            cv2.imshow(window, image)

        elif e == cv2.EVENT_LBUTTONDOWN:
            if x - p_w <= 0:
                x_start = 0
            else:
                x_start = x - p_w

            if x + p_w >= image.shape[1]:
                x_end = x + (image.shape[1] - x)
            else:
                x_end = x + p_w

            if y - p_h <= 0:
                y_start = 0
            else:
                y_start = y - p_h

            if y + p_h >= image.shape[0]:
                y_end = y + (image.shape[0] - y)
            else:
                y_end = y + p_h

            photo = image[y_start: y_end, x_start: x_end]
            cv2.imshow('photo', photo)

        cv2.imshow(window, spare_img)

    def start_opencv(self):
        self.window().hide()
        cap = cv2.VideoCapture(self.selected_source)
        while cap.isOpened():
            _, img = cap.read()

            if _:
                height, width, channels = img.shape
                part1 = img[0:height, 0: int(width/2)].copy()
                part2 = img[0:height, int(width/2): int(width)].copy()

                # cv2.imshow('original', img)
                cv2.imshow('part1', part1)
                cv2.imshow('part2', part2)

                # cv2.setMouseCallback('original', draw_rect_and_take_photo, {'window': 'original', 'img': img})
                cv2.setMouseCallback('part1', self.draw_rect_and_take_photo, {'window': 'part1', 'img': part1})
                cv2.setMouseCallback('part2', self.draw_rect_and_take_photo, {'window': 'part2', 'img': part2})

            k = cv2.waitKey(1)
            if k == 27:
                break

            sleep(.05)

        cap.release()
        cv2.destroyAllWindows()
        sys.exit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = VideoSources()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
