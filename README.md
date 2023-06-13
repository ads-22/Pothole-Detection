
# Detection of potholes on the roads

This repository contains a solution approach for the problem of detecting and locating potholes on roads and suggesting the best route to avoid them. The solution utilizes various APIs like Google Street View, OSRM, Overpass API, and geocoding API for data collection and implements different techniques for pothole detection.

## Problem Description

Potholes on roads can be hazardous for vehicles and drivers, leading to accidents and damages. Detecting and locating potholes in real-time can help drivers avoid these hazards and improve road safety. Additionally, providing an optimized route that minimizes the number of potholes can enhance the driving experience.
## Problem Description

Potholes on roads can be hazardous for vehicles and drivers, leading to accidents and damages. Detecting and locating potholes in real-time can help drivers avoid these hazards and improve road safety. Additionally, providing an optimized route that minimizes the number of potholes can enhance the driving experience.
## Solution Approach

The solution approach for detecting and locating potholes on roads and suggesting the best route to avoid them consists of the following steps:

#### 1. Data Collection: 

Data is collected from various APIs, including Google Street View, OSRM, Overpass API, and geocoding API. These APIs provide access to road images, fastest alternate paths between the source and destination, and information about road conditions.

#### 2. Image Extraction: 
The solution extracts images from the fastest alternate paths obtained from the OSRM API. These images serve as input for the pothole detection process.

#### 3. Pothole Detection Techniques: 
Two different techniques are employed for pothole detection: Convolutional Neural Network (CNN) and You Only Look Once (YOLO). The CNN technique focuses on checking the presence of potholes in the images, while YOLO is used for object detection by generating bounding boxes around potholes with specific coordinates.

#### 4. Model Selection: 
After evaluating the performance of both CNN and YOLO models, the model trained using the YOLO algorithm, which had the best results, is chosen for further use. This model is already trained on a relevant dataset.

#### 5. Pothole Calculation and Path Selection: 
The selected model is used to detect and count the number of potholes in each extracted image. The solution calculates the number of potholes for each path and selects the path with the minimum number of potholes as the best route.

#### 6. Optimization and Database Storage: 
To optimize the solution, the results of the pothole detection process are stored in a database for future use and reference.

#### 7. User Interface: 
A web application using Flask is created to provide a user-friendly interface. The application displays a map with the best possible route, which is determined by the YOLO model, to simplify the user experience.
