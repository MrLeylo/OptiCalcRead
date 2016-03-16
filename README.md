# OptiCalcRead

 January, 2016 version

##Overview

This project has born during my TFG. The idea is to develop from the scratch a system able to recognize a mathematical expression from the digital ink data captured by a tactile input device, what is called an Online Handwritten OCR (Optical Character Reader) for mathematical expressions.

##Note

This project is under development, it is NOT a final version! It's being tested under Linux, if you want to try it under Windows, there must be added a modification of the code.               
 

##Requirements

- Install python interpreter on your Linux OS
- Download the following database:

http://www.isical.ac.in/~crohme/ICFHR_package.zip

- Uncompress the .zip on a folder called ICFHR_package
- Uncompress the ICFHR_package/CROHME2012_data/trainData/trainData.zip on a folder called trainData on the same path
- Uncompress the ICFHR_package/CROHME2012_data/testData/testData.zip on a folder called testData on the same path
- Create a folder called trainData
- Create a folder called testData
- Copy the folder from the path ICFHR_package/CROHME2011_data/CROHME_training to trainData (so its new path is trainData/CROHME_training)
- Copy the folder from the path ICFHR_package/CROHME2012_data/trainData/trainData to trainData and rename it as trainData_v2 (so its new path is trainData/trainData_v2)
- Create a folder on trainData called TrainINKML (so its path is trainData/TrainINKML)
- Copy the folder from the path ICFHR_package/CROHME2011_data/CROHME_test to testData (so its new path is testData/CROHME_test)
- Copy the folder from the path ICFHR_package/CROHME2012_data/testData/testData to testData (so its new path is testData/testData)

##Commands

- To update the templates/database type:

./pyUpdate

- To update feature ponderations once we have templates type:

./storeDataConc

- To compute over an .inkml file once we have templates and we have the features ponderated type:

./overAll <filename>

- To create a list of testing files type:

./pyLook

- To compute over the database  once we have templates, we have the features ponderated and we have a list of testing files type:

./seeAll
