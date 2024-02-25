# CUBITAL Deployment

## Installation on Raspberry Pi OS

1. Install Raspbian OS Bullseye 64 Bits using the Raspberry Pi Imager: https://www.raspberrypi.com/software/

2. Check the Raspberry OS characteristics

For the OS version and architecture:
```console
$ cat /etc/os-release 
$ uname -a
```

This should show: 

```
NAME="Raspberry OS"
ID=alpine
VERSION_ID=3.12.1
PRETTY_NAME="Alpine Linux v3.12"
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://bugs.alpinelinux.org/"

aarch64 GNU/Linux
```

For the Python version:
```console
$ python -V
```

This should show: 

```
3.9.2
```

3. Update package lists for apt-get

```console
$ sudo apt-get update
$ sudo apt-get dist-upgrade
```

4. Install some packages

```console
$ sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev cython3 libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5
```

5. Clone project and create environment 

```console
$ git clone git@github.com:EdwinTSalcedo/CUBITAL.git cubital
$ cd cubital
$ sudo pip3 install virtualenv
$ python3 -m venv env
$ source env/bin/activate
```

6. Install the dependencies
```console
pip3 install -R requirements.txt 
```

7. Install TensorFlow Lite Runtime. This is a lighter version of the TF Lite that comes with TensorFlow. Otherwise, we'd need to install the entire framework. See more details [here](https://www.tensorflow.org/lite/guide/python#install_tensorflow_lite_for_python). 

```console
$ python3 -m pip install tflite-runtime
```

8. Install OpenCV 
```console
$ pip3 install opencv-python
```

9. Execute the interface
```console
$ python pyqt_interface.py
```


## Installation on Linux, Windows, MACOS

1. Clone project and create environment 

```console
$ git clone git@github.com:EdwinTSalcedo/CUBITAL.git cubital
$ cd cubital
$ sudo pip3 install virtualenv
$ python3 -m venv env
$ source env/bin/activate
$ cd edgeai
```

2. Install the dependencies
```console
pip3 install -r requirements.txt 
```

3. Execute the interface
```console
$ python pyqt_interface.py
```