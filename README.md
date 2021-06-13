# Space-Engineering-GroundStation


## Background: 

This repository shows an experiment conducted as part of a space engineering course. <br />
The goal is to build a ground station capable of detecting and tracking objects moving in the sky (mostly satellites).<br />
The system is based on the use of the "NexStar 8SE Computerized Telescope". <br />
The telescope is connected to a laptop that processes the image and directs the tripod motors so that the selected object remains in the center of the frame.
This video shows the last experiment performed on 08/06/2021 on the roof of Building 21 (Communication Building) at Ariel University.<br />


### Image of the telescope: 

![050234110693-_NexStar_8SE_11069_1_570x380@2x](https://user-images.githubusercontent.com/57401083/120164921-5ad82980-c1fb-11eb-9b6a-66e0d66d3fdf.jpg)


### about the telescope: 

The NextStar 8SE is a computerized telescope that has 2032mm of Focal Length and can magnify up to x480. <br />
In this project we will design and implement a software that will give the telescope the ability the detect objects and track them. <br />

The video camera mounted on the side of a telescope sends frame to a PC, the PC detects objects and let the operator of the telescope to choose one objects to track,
based on the selection of the operator, the PC calculates the movement that the telescope has to make in order the keep the object
in the center of its frame, the PC sends the instructions to a DC Motor that controll the telescope thorugh a microprocessor. <br />


#### Running The Code On Video: 
In the initial phase the testing of the algorithms was done using a video of the ISS station moving at an altitude of about 870 miles.
It can be seen that the algorithm is able to identify and track the space station despite the great difficulty of the distance.<br />

![ezgif-2-3daec10f894d](https://user-images.githubusercontent.com/57401083/120172646-8d862000-c203-11eb-9412-6fd2db1137b8.gif)


#### Running The On Live Photage Using Camera And The Telescope Tripod: 

##### PC frame: 
In the second stage we went from testing the algorithms by video to testing it in the real world.
To do this, we built an interface for working with the tripod motors of a telescope and integrating the algorithms.
In the video, the algorithm detects an object (probably a satellite or a plane at high altitude) and after a "follow" command the algorithm tracks the object while using the telescopic tripod motors to keep it in the center of the frame. <br />
We can see the object data in the frame as well as the motion data for the motors on the X and Y axes as well as the speed of movement in each of the axes.

![Hnet com-image](https://user-images.githubusercontent.com/57187365/121262624-203a5500-c8bd-11eb-8afd-840619c753f7.gif)


  ##### For the full video visit https://youtu.be/62CU6IS1yPU <br />

  
   <br /> 
   <br />
  
  ## How to use our code 
  1. Clone this repository  <br />
  
  2. Run the movement/tracking algorithm: <br />
  Run the main_tracking_api.py script (make sure to check which port is serial for the telescope).  <br />
  
  3. Explore the telescope API for self implementation:<br /> 
  Run quickstart.py, everything you want to know for basic controls can be found there. <br />
  You can also check the Telecontrol.py file for documentation. <br />




  
   <br /> 
   <br />
   
##### Video of the setting: 

![Hnet-image (3)](https://user-images.githubusercontent.com/57187365/121263150-e1f16580-c8bd-11eb-9809-58de113640a3.gif)

<br />
   
#### Picture of the setting: 

![image](https://user-images.githubusercontent.com/57187365/121382378-37298780-c94f-11eb-9079-78ca48ec7b63.png)

<br />
   
#### Video operating the telescope using code:

![Hnet-image (6)](https://user-images.githubusercontent.com/57187365/121384245-c1262000-c950-11eb-8181-4a82d7a307df.gif)

<br />
   



# Experiement Documantations: 
### ballon Experiement
https://docs.google.com/document/d/1wRMaSamaBNzidF_HhinaGVvgcgpyVfukSng88PlZtuM/edit <br />
### Project proposal 
https://docs.google.com/document/d/1wRMaSamaBNzidF_HhinaGVvgcgpyVfukSng88PlZtuM/edit <br />
### Check out the GroundStationDocument for further information
https://github.com/DorGetter/Space-Engineering-GroundStation/blob/master/GroundStationDocument.pdf <br />
