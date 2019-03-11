# gait-analysis-dataset
Raw dataset from "Signal Processing and Machine Learning for Diplegia Classification" and "Gait-Based Diplegia Classification Using LSMT Networks"

# Introduction
Diplegia is one of the most common forms of a broad family of motion
disorders named cerebral palsy (CP) affecting the voluntary
muscular system. In recent years, various
classification criteria have been proposed for CP, to assist in diagnosis, clinical decision-making and communication. 

# Data
Our dataset refers to 1139 trials acquired from 178 patients affected by different stages of diplegia using high frequency VICON
cameras in an Italian hospital.
WARNING: some trial may be invalid (e.g. invalid markers throughout the sequence).
## X
Each .npy file has a variable number of frames. 
For each frame, 19 markers are reported with 3D coordinates along with a validation flag.
If you're interested in other markers or other medical indicators, please write me an email.
## Y
The path to a .npy file can be seen as follow:
```
base_folder/class_label/subject_label/.npy 
```
# Utils
Along with the script employed to extract .npy file, the repo comes with a usefull visualizer based on [Open3D](http://www.open3d.org/).
Here there are some examples of the results:

<table style="width:100%">
    <tr>
        <th>
            <p align="center">
            <img src="./img/5_3.gif" alt="Example" width="75%" height="75%">
            <br>Class 0 example.
            </p>
        </th>
        <th>
            <p align="center">
            <img src="./img/34_1.gif" alt="Example" width="75%" height="75%">
            <br>Class 1 example.
            </p>
        </th>
     </tr>
 </table>
 

# How to cite
Please cite **both** the followings:
```
@inbook{inbook,
author = {Bergamini, Luca and Calderara, Simone and Bicocchi, Nicola and Ferrari, Alberto and Vitetta, Giorgio},
year = {2017},
month = {01},
pages = {97-108},
title = {Signal Processing and Machine Learning for Diplegia Classification},
isbn = {978-3-319-70741-9},
doi = {10.1007/978-3-319-70742-6_9}
}

Alberto Ferrari, Luca Bergamini, Giorgio Guerzoni, et al., “Gait-Based Diplegia Classification Using LSMT Networks,” Journal of Healthcare Engineering, vol. 2019, Article ID 3796898, 8 pages, 2019. https://doi.org/10.1155/2019/3796898.

```
