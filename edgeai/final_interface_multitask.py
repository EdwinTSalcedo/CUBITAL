from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
import cv2
import time
from PIL import ImageQt
import os
import sys
import shutil  
import numpy as np
import tensorflow as tf

INPUT_MODEL_DIMENSION = 512  #Options: 512, 256, 128, 64

unet = tf.saved_model.load(f"models/unet_multi")

# Access the 'serving_default' signature
infer = unet.signatures["serving_default"]

# Define path variables
HOME = os.getcwd()
PICTURES_PATH = os.path.join(HOME, "pictures")

# Check if the folder exists
if os.path.exists(PICTURES_PATH):
    shutil.rmtree(PICTURES_PATH)
os.mkdir(PICTURES_PATH)

class UI_MainWindow():
    def setupUI(self, main_window):
        self.camera_on = False
        self.picture_pixmaps = {}

        # Set main window
        main_window.setWindowTitle("CUBITAL")
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
        self.start_stream_button.clicked.connect(self.start_video)
        self.start_stream_button.setText("START")
        # Set buttons for capturing pictures
        self.take_picture_button = QtWidgets.QPushButton(self.central_widget)
        self.take_picture_button.setGeometry(QtCore.QRect(582, 263, 80, 70))
        self.take_picture_button.setObjectName("take_picture_button")
        self.take_picture_button.clicked.connect(self.save_picture)
        self.take_picture_button.setText("CAPTURE")
        
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

        # Set labels to ask to press the buttons again
        self.label_first_picture = QtWidgets.QLabel(self.central_widget)
        self.label_first_picture.setGeometry(QtCore.QRect(500, 97, 165, 25))
        self.label_first_picture.setObjectName("label_first_picture")
        self.label_first_picture.setText("Press again")
        self.label_first_picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_first_picture.setVisible(False)
        self.label_first_picture.setStyleSheet("background-color: black;color:white;opacity: 0.7;") 
        self.label_second_picture = QtWidgets.QLabel(self.central_widget)
        self.label_second_picture.setGeometry(QtCore.QRect(500, 225, 165, 25))
        self.label_second_picture.setObjectName("label_second_picture")
        self.label_second_picture.setText("Press again")
        self.label_second_picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_second_picture.setVisible(False)
        self.label_second_picture.setStyleSheet("background-color: black;color:white;opacity: 0.7;") 

        # Finish configuring the main window 
        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 21))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(main_window)

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
            self.label_first_picture.setVisible(True)
        else: 
            self.label.setPixmap(self.picture_pixmaps["first"])
            self.label.setVisible(True)
            self.label_first_picture.setVisible(False)

    def visualize_picture2(self):
        if self.camera_on:
            self.Work.stop()
            self.label.clear()
            self.camera_on = False
            self.start_stream_button.setText("START")
            self.take_picture_button.setEnabled(False)
            self.label.setVisible(False)
            self.label_second_picture.setVisible(True)
        else:
            self.label.setPixmap(self.picture_pixmaps["second"])
            self.label.setVisible(True)
            self.label_second_picture.setVisible(False)

class Work(QThread):
    Imageupd = pyqtSignal(QImage)

    def run(self):
        self.running_thread = True
        cap = cv2.VideoCapture(0)
        while self.running_thread:
            ret, frame = cap.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)

                new_image_to_segment = image[:,420:1500,:]
                new_image_to_segment = cv2.resize(new_image_to_segment, (512, 512), interpolation = cv2.INTER_AREA)
                mask, values = self.segment_and_predict(new_image_to_segment)
                resized_mask = cv2.resize(mask, (320, 320), interpolation = cv2.INTER_AREA)

                scaled_image_to_display = cv2.resize(image, (569, 320), interpolation = cv2.INTER_AREA)
                scaled_image_to_display = scaled_image_to_display[:,45:525,:]
                masked_image = np.zeros(scaled_image_to_display.shape, dtype=np.uint8)

                masked_image[:,80:400,:] = resized_mask

                # Add regression values
                x = int(values[0][0] * INPUT_MODEL_DIMENSION)
                y = int(values[0][1] * INPUT_MODEL_DIMENSION)
                angle = values[0][2] * 180

                # Window size 
                window_size = 100
                window_size = window_size // 2
                
                masked_image[:y-window_size,:masked_image.shape[1],:] = [0, 0, 0]
                masked_image[y-window_size:y+window_size,:x-window_size,:] = [0, 0, 0]
                masked_image[y-window_size:y+window_size,x+window_size:,:] = [0, 0, 0]
                masked_image[y+window_size:,:masked_image.shape[1],:] = [0, 0, 0]
                
                combined = cv2.addWeighted(scaled_image_to_display, 1, masked_image, 0.8, 0)

                # cv2.circle(combined, (x, y), radius=5, color=(0,255,0), thickness=-1)
                # cv2.putText(combined, f"{angle:.2f}", (x+10, y+5), 1, 1, (0,0,255))

                qimage = QImage(combined.data, combined.shape[1], combined.shape[0], QImage.Format.Format_RGB888)
                self.Imageupd.emit(qimage)

    def stop(self):
        self.running_thread = False
        self.quit()

    def segment_and_predict(self, image):
       image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  
       clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
       image = clahe.apply(image)
       image = image.astype(dtype=np.float32) / 127.5 - 1

       image = np.expand_dims(np.expand_dims((image), axis=0), axis=3)
       image_tensor = tf.convert_to_tensor(image, dtype=tf.float32)

       results = infer(image_tensor)
       values = results['output_1']
       mask = results['output_0']
       mask = np.squeeze(mask)
       prediction_mask = np.argmax(mask, axis=2).astype(np.uint8)

       output = cv2.cvtColor(prediction_mask, cv2.COLOR_GRAY2RGB)
       output[prediction_mask == 2] = [0, 255, 0]
       output[prediction_mask == 1] = [0, 0, 0]

       return output, values
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUI(main_window)
    main_window.show()
    sys.exit(app.exec())
