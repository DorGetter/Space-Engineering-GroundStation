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

![ezgif-2-3daec10f894d](https://user-images.githubusercontent.com/57401083/120172646-8d862000-c203-11eb-9412-6fd2db1137b8.gif)


#### Running The On Live Photage Using Camera And The Telescope Tripod: 

##### PC frame: 

In the video, the algorithm detects an object (probably a satellite or a plane at high altitude) and after a "follow" command the algorithm tracks the object while using the telescopic tripod motors to keep it in the center of the frame. <br />
We can see the object data in the frame as well as the motion data for the motors on the X and Y axes as well as the speed of movement in each of the axes.

![Hnet com-image](https://user-images.githubusercontent.com/57187365/121262624-203a5500-c8bd-11eb-8afd-840619c753f7.gif)


  ##### For the full video visit https://youtu.be/62CU6IS1yPU <br />

  


##### Video of the setting: 

![Hnet-image (3)](https://user-images.githubusercontent.com/57187365/121263150-e1f16580-c8bd-11eb-9809-58de113640a3.gif)





# Experiement Documantations: 
https://docs.google.com/document/d/1wRMaSamaBNzidF_HhinaGVvgcgpyVfukSng88PlZtuM/edit
