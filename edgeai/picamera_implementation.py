import numpy as np
import tflite_runtime.interpreter as tflite
import cv2
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

CAPTURE_DIMENSION = 272
INPUT_MODEL_DIMENSION = 512  #Options: 512, 256, 128, 64

# Load the TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path=f"models/unet{INPUT_MODEL_DIMENSION}x{INPUT_MODEL_DIMENSION}.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (CAPTURE_DIMENSION, CAPTURE_DIMENSION)
camera.framerate = 1
camera.rotation = 90
rawCapture = PiRGBArray(camera, size=(CAPTURE_DIMENSION, CAPTURE_DIMENSION))

# allow the camera to warmup
time.sleep(0.1)

def segment_regions(image):
    image = cv2.resize(image, (INPUT_MODEL_DIMENSION, INPUT_MODEL_DIMENSION), interpolation = cv2.INTER_AREA)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    image = clahe.apply(image)
    image = image.astype(dtype=np.float32) / 127.5 - 1

    image = np.expand_dims(np.expand_dims((image), axis=0), axis=3)

    interpreter.set_tensor(input_details[0]['index'], image)

    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predictions = np.squeeze(output_data)
    predictions = np.argmax(predictions, axis=2)
    prediction_mask = predictions.astype(np.uint8)

    output = cv2.cvtColor(prediction_mask, cv2.COLOR_GRAY2RGB)
    output[prediction_mask == 2] = [0, 0, 255]
    output[prediction_mask == 1] = [0, 255, 0]
    output = cv2.resize(output, (CAPTURE_DIMENSION, CAPTURE_DIMENSION), interpolation = cv2.INTER_AREA)
    return output

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    image = frame.array
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_copy = image.copy().astype(np.uint8)
    output = segment_regions(image)
    combined = cv2.addWeighted(image_copy, 1, output, 0.9, 0)

    # show the frame
    cv2.imshow("Frame", combined)
    #cv2.resizeWindow("output", 256, 256)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

