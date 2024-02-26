# CUBITAL Deployment

## Installation on Raspberry Pi OS

1. Install Raspbian OS Bullseye 64 Bits using the Raspberry Pi Imager: https://www.raspberrypi.com/software/

2. Install the 3.5 inch RPI Display

```bash
$ sudo rm -rf LCD-show
$ git clone https://github.com/goodtft/LCD-show.git
$ chmod -R 755 LCD-show
$ cd LCD-show/
$ sudo ./LCD35-show
```

3. After reboot, change the resolution of the device and activate VNC. 

```bash
$ sudo raspi-config
```

Activate the options: 
- Interface Options -> VNC 
- Display -> Resolution -> 800x600 60Hz 4:3

4. Check the Raspberry OS characteristics

For the OS version:
```bash
$ cat /etc/os-release 
```

This should show: 

```console
PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
NAME="Debian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```

For the OS architecture:
```bash
$ uname -a
```

```console
aarch64 GNU/Linux
```

For the Python version:
```bash
$ python -V
```

This should show: 

```
Python 3.9.2
```

5. Update package lists for apt-get

```bash
$ sudo apt-get update
$ sudo apt-get dist-upgrade
```

6. Install some packages

```bash
$ sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev cython3 libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5
```

7. Clone project and create environment 

```bash
$ git clone git@github.com:EdwinTSalcedo/CUBITAL.git cubital
$ cd cubital
$ sudo pip3 install virtualenv
$ python3 -m venv env
$ source env/bin/activate
```

8. Install the dependencies
```bash
$ pip3 install -R requirements.txt 
```

9. Install TensorFlow Lite Runtime. This is a lighter version of the TF Lite that comes with TensorFlow. Otherwise, we'd need to install the entire framework. See more details [here](https://www.tensorflow.org/lite/guide/python#install_tensorflow_lite_for_python). 

```bash
$ python3 -m pip install tflite-runtime
```

10. Install OpenCV 
```bash
$ pip3 install opencv-python
```

11. Execute the interface
```bash
$ python pyqt_interface.py
```

Alternatively, you can try running the file `picamera_implementation.py`. This contains a similar interface and uses `picamera` to access the camera.  


## Installation on Linux, Windows, MACOS

1. Clone project and create environment 

```bash
$ git clone git@github.com:EdwinTSalcedo/CUBITAL.git cubital
$ cd cubital
$ sudo pip3 install virtualenv
$ python3 -m venv env
$ source env/bin/activate
$ cd edgeai
```

2. Install the dependencies
```bash
$ pip3 install -r requirements.txt 
```

3. Execute the interface
```bash
$ python pyqt_interface.py
```