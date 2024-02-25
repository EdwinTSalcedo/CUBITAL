from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import cv2
import time
from PIL import ImageQt
import os
import sys
import shutil

# Define path variables
HOME = os.getcwd()
PICTURES_PATH = os.path.join(HOME, "edgeai","pictures")

# Check if the folder exists
if os.path.exists(PICTURES_PATH):
    shutil.rmtree(PICTURES_PATH)
os.mkdir(PICTURES_PATH)

class UI_MainWindow():
    def setupUI(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(670, 370)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 480, 320))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(500, 263, 80, 70))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(582, 263, 80, 70))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(500, 3, 165, 124))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(500, 129, 165, 124))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 21))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.camera_on = False
        self.image_list = []
        self.pushButton.clicked.connect(self.start_video)
        self.pushButton_2.clicked.connect(self.save_picture)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton.setText(_translate("MainWindow", "START"))
        self.pushButton_2.setText(_translate("MainWindow", "CAPTURE"))

    def start_video(self):
        if not self.camera_on:
            self.Work = Work()
            self.Work.start()
            self.Work.Imageupd.connect(self.Imageupd_slot)
            self.camera_on = True
            self.pushButton.setText("STOP")
            self.pushButton_2.setEnabled(True)
        else:
            self.Work.stop()
            self.camera_on = False
            self.pushButton.setText("START")
            self.pushButton_2.setEnabled(False)

    def Imageupd_slot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def save_picture(self):
        # Obtain image from the camera (in Qpixmap format) and convert it to a Pillow image
        pixmap_image = self.label.pixmap()
        pillow_image = ImageQt.fromqpixmap(pixmap_image)
        
        # Save picture
        self.filename = 'picture' + str(time.strftime("%Y%m%d%H%M%S")) + '.png'
        pillow_image.save(os.path.join(PICTURES_PATH, self.filename))
        self.image_list.append(pixmap_image)

        # Display the latest image on a QPushButton
        self.pushButton_3.setIcon(QIcon(pixmap_image))
        self.pushButton_3.setIconSize(self.pushButton_3.size())
        self.pushButton_3.clicked.connect(self.toggleImageVisibility)

        if len(self.image_list) >=2:
            # Display the previous image on QPushButton_4
            previous_pixmap = self.image_list[-2]
            self.pushButton_4.setIcon(QIcon(previous_pixmap))
            self.pushButton_4.setIconSize(self.pushButton_4.size())
            self.pushButton_4.clicked.connect(self.toggleImageVisibility2)

    def toggleImageVisibility(self):
        # Toggle the visibility of the image in label_5
        if self.label.isVisible():
            self.label.clear()
            self.label.setVisible(False)
        else:
            pixmap = self.pushButton_3.icon().pixmap(self.pushButton_3.iconSize())
            scaled_pixmap = pixmap.scaled(self.label.width(), self.label.height())
            self.label.setPixmap(scaled_pixmap)
            self.label.setVisible(True)

    def toggleImageVisibility2(self):
        # Toggle the visibility of the image in label_5
        if self.label.isVisible():
            self.label.clear()
            self.label.setVisible(False)
        else:
            pixmap = self.pushButton_4.icon().pixmap(self.pushButton_4.iconSize())
            scaled_pixmap = pixmap.scaled(self.label.width(), self.label.height())
            self.label.setPixmap(scaled_pixmap)
            self.label.setVisible(True)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "START"))
        self.pushButton_2.setText(_translate("MainWindow", "CAPTURE"))


class Work(QThread):
    Imageupd = pyqtSignal(QImage)

    def run(self):
        self.hilo_corriendo = True
        cap = cv2.VideoCapture(0)
        while self.hilo_corriendo:
            ret, frame = cap.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flip = cv2.flip(Image, 1)
                convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format.Format_RGB888)
                # pic = convertir_QT.scaled(480, 320, Qt.KeepAspectRatio)
                pic = convertir_QT.scaled(480, 320)
                self.Imageupd.emit(pic)

    def stop(self):
        self.hilo_corriendo = False
        self.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUI(main_window)
    main_window.show()
    sys.exit(app.exec())
