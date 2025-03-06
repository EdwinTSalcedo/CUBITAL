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
HOME = os.getcwd()

unet = tf.saved_model.load(os.path.join(HOME,"edgeai/models/unet_multi"))

# Access the 'serving_default' signature
infer = unet.signatures["serving_default"]

# Define path variables

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
            self.Work.imageupd.connect(self.set_video_stream)
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
    '''
        This class lets process each input frame in a different thread. Then, it applies a model 
        to obtain the segments representing the vein in the antecubital fossa. 
    '''
    imageupd = pyqtSignal(QImage)

    def run(self):
        self.running_thread = True
        cap = cv2.VideoCapture(0)

        # Dimensions of the image to be displayed in the interface, considering the 16:9 aspect ratio. 
        IMAGE_WIDTH_TO_SHOW = 568
        IMAGE_HEIGHT_TO_SHOW = 320
        
        # Piles to average the x and y coordinates of the antecubital fossa localised by the model.
        x_buffer = []
        y_buffer = []
        buffer_size = 30

        masks_buffer = []
        masks_buffer_size = 10

        while self.running_thread:
            ret, frame = cap.read()

            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)
                image = cv2.resize(image, (IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW), interpolation = cv2.INTER_AREA)
                
                # Obtain the predicted mask
                left_limit = int(IMAGE_HEIGHT_TO_SHOW//2)
                right_limit = left_limit + IMAGE_HEIGHT_TO_SHOW
                new_image_to_segment = image[:,left_limit:right_limit,:]
                new_image_to_segment = cv2.resize(new_image_to_segment, (INPUT_MODEL_DIMENSION, INPUT_MODEL_DIMENSION), interpolation = cv2.INTER_AREA)
                mask, values = self.segment_and_predict(new_image_to_segment)

                mask[mask == 1] = 0
                mask[mask == 2] = 255

                # Average the present and previous masks in a weighted manner
                if len(masks_buffer) >= masks_buffer_size: 
                    masks_buffer.pop(0)
                masks_buffer.append(mask)
                new_mask = (np.where(self.average(masks_buffer)>0.5, 255, 0)).astype(np.uint8)

                resized_mask = cv2.resize(new_mask, (IMAGE_HEIGHT_TO_SHOW, IMAGE_HEIGHT_TO_SHOW), interpolation = cv2.INTER_AREA)
                _, binary_mask = cv2.threshold(resized_mask, 127, 255, cv2.THRESH_BINARY)

                masked_mask = np.zeros((image.shape[0],image.shape[1]), dtype=np.uint8)
                masked_mask[:,left_limit:right_limit] = binary_mask

                # Include a bounding box by using the x and y coordinates of the antecubital fossa obtained by the model.
                x = int(values[0][0] * IMAGE_HEIGHT_TO_SHOW) + (left_limit)
                y = int(values[0][1] * IMAGE_HEIGHT_TO_SHOW)
                angle = values[0][2] * 180

                if len(x_buffer) >= buffer_size:
                    x_buffer.pop(0)
                x_buffer.append(x)

                if len(y_buffer) > buffer_size:
                    y_buffer.pop(0)
                y_buffer.append(y)

                # Average the x and y coordinates to avoid inconstant coordinates
                new_x = int(sum(x_buffer) / len(x_buffer) if x_buffer else 0)
                new_y = int(sum(y_buffer) / len(y_buffer) if y_buffer else 0)

                # Remove segments out of the antecubital fossa's window 
                window_size = 100
                window_size = window_size // 2

                bbox_x1 = new_x-window_size
                bbox_x2 = new_x+window_size
                bbox_y1 = new_y-window_size
                bbox_y2 = new_y+window_size
                
                masked_mask[:bbox_y1,:masked_mask.shape[1]] = 0
                masked_mask[bbox_y1:bbox_y2,:bbox_x1] = 0
                masked_mask[bbox_y1:bbox_y2,bbox_x2:] = 0
                masked_mask[bbox_y2:,:masked_mask.shape[1]] = 0

                # Change the color of all vein segments to green
                output = cv2.cvtColor(masked_mask, cv2.COLOR_GRAY2RGB)
                output[masked_mask==255] = [0,255,0]                
                combined = cv2.addWeighted(output, 1, image, 0.8, 0)

                # Draw the bounding box representing the antecubital fossa
                cv2.rectangle(combined,(bbox_x1,bbox_y1),(bbox_x2,bbox_y2),(31,255,255),1)

                qimage = QImage(combined.data, combined.shape[1], combined.shape[0], QImage.Format.Format_RGB888)
                self.imageupd.emit(qimage)

        cap.release()

    def stop(self):
        self.running_thread = False
        self.quit()

    def average(self, arrays):
        assert len(arrays) > 0, "Input list must not be empty"
        assert all(arr.shape == arrays[0].shape for arr in arrays), "All arrays must have the same shape"

        avg = np.mean(arrays, axis=0)
        return avg

    def segment_and_predict(self, image):
       image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  

       # Implement CLAHE and normalise the image
       clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
       image = clahe.apply(image)
       image = image.astype(dtype=np.float32) / 127.5 - 1

       # Convert image to TensorFlow tensor
       image = np.expand_dims(np.expand_dims((image), axis=0), axis=3)
       image_tensor = tf.convert_to_tensor(image, dtype=tf.float32)

       # Obtain inference results with the model
       results = infer(image_tensor)
       values = results['output_1']
       mask = results['output_0']
       mask = np.squeeze(mask)
       prediction_mask = np.argmax(mask, axis=2).astype(np.uint8)

       return prediction_mask, values
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUI(main_window)
    main_window.show()
    sys.exit(app.exec())
