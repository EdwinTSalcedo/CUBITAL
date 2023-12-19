# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import time
from PIL import ImageQt, Image, ImageTk
import sys
import tflite_runtime.interpreter as tflite
import numpy as np

INPUT_MODEL_DIMENSION = 128  #Options: 512, 256, 128, 64

# Load the TFLite model and allocate tensors. Note this load the corresponding model given the input dimensions. 
interpreter = tflite.Interpreter(model_path=f"models/unet{INPUT_MODEL_DIMENSION}x{INPUT_MODEL_DIMENSION}.tflite")
# Assign memory addresses to save new data in tensor format
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("CUBITAL")
        MainWindow.resize(480, 275)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(2, 9, 475, 250))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(480, 320))
        self.label.setMaximumSize(QtCore.QSize(480, 320))
        self.label.setStyleSheet("background-color:rgb(255, 255, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setMinimumSize(QtCore.QSize(165, 124))
        self.label_2.setMaximumSize(QtCore.QSize(165, 124))
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setMinimumSize(QtCore.QSize(165, 124))
        self.label_3.setMaximumSize(QtCore.QSize(165, 124))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setMinimumSize(QtCore.QSize(80, 70))
        self.pushButton.setMaximumSize(QtCore.QSize(80, 70))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.camera_on = False
        self.image_list = []
        self.pushButton.clicked.connect(self.start_video)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def start_video(self):
        if not self.camera_on:
            self.Work = Work()
            self.Work.start()
            self.Work.Imageupd.connect(self.Imageupd_slot)
            self.camera_on = True
            self.pushButton.setText("STOP")

        else:
            self.Work.stop()
            self.camera_on = False
            self.pushButton.setText("START")

    def Imageupd_slot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def savePhoto(self):
        gallery = ImageQt.fromqpixmap(self.label.pixmap())
        self.filename = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        gallery.save(self.filename)

        pixmap = QPixmap(self.filename)
        self.image_list.append(pixmap)
        scaled_pixmap = pixmap.scaled(self.label_2.width(), self.label_2.height())
        self.label_2.setPixmap(scaled_pixmap)

        if len(self.image_list)>=2:
            scaled_pixmap = self.image_list[-2].scaled(self.label_3.width(), self.label_3.height())
            self.label_3.setPixmap((scaled_pixmap))

    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("CUBITAL", "CUBITAL"))
        self.pushButton.setText(_translate("START", "START"))

class Work(QThread):
    Imageupd = pyqtSignal(QImage)

    def segment_regions(self, image):
       BASE_DIMENSION = image.shape[0]
       image = cv2.resize(image, (INPUT_MODEL_DIMENSION, INPUT_MODEL_DIMENSION), interpolation = cv2.INTER_AREA)
       image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
       clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
       image = clahe.apply(image)
       image = image.astype(dtype=np.float32) / 127.5 - 1

       image = np.expand_dims(np.expand_dims((image), axis=0), axis=3)

       interpreter.set_tensor(input_details[0]['index'], image)

       interpreter.invoke()

       # The function `get_tensor()` returns a copy of the tensor data.
       output_data = interpreter.get_tensor(output_details[0]['index'])
       predictions = np.squeeze(output_data)
       predictions = np.argmax(predictions, axis=2)
       prediction_mask = predictions.astype(np.uint8)

       output = cv2.cvtColor(prediction_mask, cv2.COLOR_GRAY2RGB)
       output[prediction_mask == 2] = [0, 0, 255]
       output[prediction_mask == 1] = [0, 255, 0]
       output = cv2.resize(output, (BASE_DIMENSION, BASE_DIMENSION), interpolation = cv2.INTER_AREA)
       return output

    def run(self):
        self.camera_capturing = True
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Available options for Picam NOIR: 1280x720, 640x480, 640x360
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # Default: 640x480
        self.cap.set(cv2.CAP_PROP_FPS, 1)

        # Allow the camera to warmup
        time.sleep(0.2)

        while self.camera_capturing:

            ret, frame = self.cap.read()
            if ret:
                # Transform image to pass it to the model
                new_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                new_frame = new_frame[370:910,:,:]
                new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
                image = new_frame[:,90:630,:]
                output = self.segment_regions(image)
                # Combine the output mask with the frame
                combined = cv2.addWeighted(image, 1, output, 0.9, 0)
                new_frame[:,90:630,:] = combined
                # Show the segmented image inside the GUI element
                qimage = QImage(new_frame.data, new_frame.shape[1], new_frame.shape[0], QImage.Format_RGB888)
                qimage = qimage.scaled(470, 350)
                self.Imageupd.emit(qimage)

    def stop(self):
        self.cap.release()
        self.camera_capturing = False
        self.quit()

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
