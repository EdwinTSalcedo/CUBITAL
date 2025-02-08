<h1 align="center">Edge AI-Based Vein Detector for Efficient Venipuncture in the Antecubital Fossa (CUBITAL)</h1> 

This repository contains supplementary material for the conference paper [*"Edge AI-Based Vein Detector for Efficient Venipuncture in the Antecubital Fossa"*](https://link.springer.com/chapter/10.1007/978-3-031-47640-2_24) (MICAI 2023 Oral session). **Authors:** [Edwin Salcedo](https://www.linkedin.com/in/edwinsalcedo) and [Patricia Peñaloza](https://www.linkedin.com/in/patricia-jael-pe%C3%B1aloza-sola-6b9b65131)

[[Project page]](https://edwinsalcedo.com/publication/cubital) [[Dataset]](https://drive.google.com/file/d/191uA9ErYRSXculIa3AXHqfBhXjd7O3St/view?usp=sharing) [[arXiv]](https://arxiv.org/pdf/2310.18234) 


## Contents
[1. Overview](#overview) </br>
[2. Dataset](#dataset) </br>
[3. Getting Started](#gettingstarted) </br>
[4. Citation](#citation) </br>
<br>

# 1. Overview
<a id="overview"></a>

## Motivation
Assessing vein condition and visibility is crucial before obtaining intravenous access in the antecubital fossa, a common site for blood draws and intravenous therapy. However, medical practitioners often struggle with patients who have less visible veins due to factors such as fluid retention, age, obesity, dark skin tone, or diabetes. Current research explores the use of near-infrared (NIR) imaging and deep learning (DL) for forearm vein segmentation, achieving high precision. However, a research gap remains in recognising veins specifically in the antecubital fossa. Additionally, most studies rely on stationary computers, limiting portability for medical personnel during venipuncture procedures. To address these challenges, we propose a portable vein finder for the antecubital fossa based on the Raspberry Pi 4B.

## CV pipeline and DL architecture
The CV pipeline for vein recognition in the antecubital region involves the following steps: 

<p align="center">
<img src="images/pipeline.png" width="700">
</p>

<p align="center">
<img src="images/final-unet.png" width="700">
</p>

We implemented different vein semantic segmentation models, and modified the best one, a U-Net model, including an additional head to identify coordinates of the antecubital fossa, and an angle. 

## Hardware Prototype

<p align="center">
  <img src="images/isometric.png" height="240">
  <img src="images/posterior.png" height="240">
</p>

| Component | CAD Design |
| --- | --- | 
| Case | [`Base`](cad/base.SLDPRT) [`Cover`](cad/cover.SLDPRT) [`Charger`](cad/charger.SLDPRT) |
| Battery | [`Case`](cad/battery_cover.SLDPRT) [`Holder`](cad/battery_holder.SLDPRT) [`Battery`](cad/battery.SLDPRT) |  
| Camera | [`Holder`](cad/cam_holder.SLDPRT) [`Picam Noir`](cad/pi_cam.SLDPRT) [`Leds Matrix`](cad/leds_matrix.SLDPRT) |  
| LCD Screen | [`Screen`](cad/lcd_screen.SLDPRT) [`LCD Assembly`](cad/rpi_lcd.SLDPRT) | 
| Additional Parts | [`Power bank`](cad/powerbank.SLDPRT) [`Relay`](cad/relay_module.SLDPRT) [`Raspberry Pi 4B`](cad/raspberryPi4B.SLDPRT) |  

The complete device can be assembled by opening the file [`Ensamblaje.SLDASM`](cad/Ensamblaje.SLDASM).

# 2. Dataset
<a id="dataset"></a>

To collect the dataset, 1,008 subjects with low-visible veins placed one arm at a time on a table. Then, we captured an NIR image with the preliminary version of the vein finder. Below, you can see the original NIR samples, their preprocessed version (). The final version of the dataset can be found here: [Dataset](https://drive.google.com/file/d/191uA9ErYRSXculIa3AXHqfBhXjd7O3St/view?usp=sharing). We created an additional [Dataset](https://drive.google.com/file/d/1-6hCFfxxFFCx1fuBaQODVqDVOiWPl42U/view?usp=sharing) version with normalized samples with dimensions of 512x512 pixels for training with the proposed architecture. 

|  NIR Images |  Preprocessing |  Annotations |  
|---|---|---|
|<img src="images/samples/nir1.jpg" width="250px"/> | <img src=images/samples/preprocessed_image1.jpg  width="250px"/> | <img src=images/samples/annotation1.jpg width="250px"/> |
|<img src="images/samples/nir2.jpg" width="250px"/> | <img src=images/samples/preprocessed_image2.jpg  width="250px"/> | <img src=images/samples/annotation2.jpg width="250px"/> |
|<img src="images/samples/nir3.jpg" width="250px"/> | <img src=images/samples/preprocessed_image3.jpg  width="250px"/> | <img src=images/samples/annotation3.jpg width="250px"/> |

<!-- # Experimental Results

## Validation
<p align="center">
  <img src="images/inference2.png" width="65%">
</p>

## Interface

-->

# 3. Getting Started
<a id="gettingstarted"></a>

With the project, we provide you with one pretrained multi-task unet model, which is embedded inside a complete pipeline to generate inference given a NIR image. You can execute the latter by following the next steps: 

```bash
# Clone the repository
git clone git@github.com:EdwinTSalcedo/CUBITAL.git cubital

# Create and activate a new conda environment
conda create -n new_env python=3.10.12
conda activate new_env

# Install the dependencies 
pip install -r requirements.txt

# Execute inference script
python inference.py
```

The pretrained serialized models for this pipeline are placed in `edge/models`, while their detailed implementations are located in `notebooks`.


# 4. Citation
<a id="citation"></a>
If you find *CUBITAL* useful in your project, please consider to cite the following paper:

```
@inproceedings{salcedo2023,
  title={Edge AI-Based Vein Detector for Efficient Venipuncture in the Antecubital Fossa},
  author={Salcedo, Edwin and Pe{\~n}aloza, Patricia},
  booktitle={Mexican International Conference on Artificial Intelligence},
  pages={297--314},
  year={2023},
  organization={Springer}
}
```
