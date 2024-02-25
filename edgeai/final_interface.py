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
        self.camera_on = False
        self.picture_pixmaps = {}

        # Set main window
        main_window.setObjectName("main_window")
        main_window.resize(670, 370)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        # Set video pane
        self.label = QtWidgets.QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(10, 10, 480, 320))
        self.label.setObjectName("label")

        # Set buttons for start/stop capturing video stream 
        self.start_stream_button = QtWidgets.QPushButton(self.central_widget)
        self.start_stream_button.setGeometry(QtCore.QRect(500, 263, 80, 70))
        self.start_stream_button.setObjectName("start_stream_button")
        # Set buttons for capturing pictures
        self.take_picture_button = QtWidgets.QPushButton(self.central_widget)
        self.take_picture_button.setGeometry(QtCore.QRect(582, 263, 80, 70))
        self.take_picture_button.setObjectName("take_picture_button")
        # Set buttons for selecting pictures on the right
        self.picture1_button = QtWidgets.QPushButton(self.central_widget)
        self.picture1_button.setGeometry(QtCore.QRect(500, 3, 165, 124))
        self.picture1_button.setText("")
        self.picture1_button.setObjectName("picture1_button")
        self.picture1_button.clicked.connect(self.visualize_picture1)
        self.picture2_button = QtWidgets.QPushButton(self.central_widget)
        self.picture2_button.setGeometry(QtCore.QRect(500, 129, 165, 124))
        self.picture2_button.setText("")
        self.picture2_button.setObjectName("picture2_button")
        self.picture2_button.clicked.connect(self.visualize_picture2)

        # Finish configuring the main window 
        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 21))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        # Add events to the buttons
        self.start_stream_button.clicked.connect(self.start_video)
        self.take_picture_button.clicked.connect(self.save_picture)

        self.retranslate_UI(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_UI(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "CUBITAL"))
        self.start_stream_button.setText(_translate("MainWindow", "START"))
        self.take_picture_button.setText(_translate("MainWindow", "CAPTURE"))

    def start_video(self):
        if self.camera_on:
            self.Work.stop()
            self.camera_on = False
            self.start_stream_button.setText("START")
            self.take_picture_button.setEnabled(False)
        else:
            if not self.label.isVisible():
                self.label.setVisible(True)
            self.Work = Work()
            self.Work.start()
            self.Work.Imageupd.connect(self.set_video_stream)
            self.camera_on = True
            self.start_stream_button.setText("STOP")
            self.take_picture_button.setEnabled(True)

    def set_video_stream(self, stream):
        self.label.setPixmap(QPixmap.fromImage(stream))

    def save_picture(self):
        # Obtain image from the camera (in Qpixmap format) and convert it to a Pillow image
        pixmap_image = self.label.pixmap()
        pillow_image = ImageQt.fromqpixmap(pixmap_image)
        
        # Save picture
        self.filename = 'picture' + str(time.strftime("%Y%m%d%H%M%S")) + '.png'
        pillow_image.save(os.path.join(PICTURES_PATH, self.filename))
        
        if "first" in self.picture_pixmaps: 
            self.picture_pixmaps["second"] = self.picture_pixmaps["first"]
            previous_pixmap = self.picture_pixmaps["first"]
            self.picture2_button.setIcon(QIcon(previous_pixmap))
            self.picture2_button.setIconSize(self.picture2_button.size())

        # Display the latest image on the first button
        self.picture_pixmaps["first"] = pixmap_image
        self.picture1_button.setIcon(QIcon(pixmap_image))
        self.picture1_button.setIconSize(self.picture1_button.size())
          
    def visualize_picture1(self):
        if self.camera_on:
            self.Work.stop()
            self.label.clear()
            self.camera_on = False
            self.start_stream_button.setText("START")
            self.take_picture_button.setEnabled(False)
            self.label.setVisible(False)
        else: 
            self.label.setPixmap(self.picture_pixmaps["first"])
            self.label.setVisible(True)

    def visualize_picture2(self):
        if self.camera_on:
            self.Work.stop()
            self.label.clear()
            self.camera_on = False
            self.start_stream_button.setText("START")
            self.take_picture_button.setEnabled(False)
            self.label.setVisible(False)
        else:
            self.label.setPixmap(self.picture_pixmaps["second"])
            self.label.setVisible(True)

class Work(QThread):
    Imageupd = pyqtSignal(QImage)

    def run(self):
        self.running_thread = True
        cap = cv2.VideoCapture(0)
        while self.running_thread:
            ret, frame = cap.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flip = cv2.flip(Image, 1)
                convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format.Format_RGB888)
                # pic = convertir_QT.scaled(480, 320, Qt.KeepAspectRatio)
                pic = convertir_QT.scaled(480, 320)
                self.Imageupd.emit(pic)

    def stop(self):
        self.running_thread = False
        self.quit()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUI(main_window)
    main_window.show()
    sys.exit(app.exec())
