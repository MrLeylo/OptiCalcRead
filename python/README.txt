               ------------
               OPTICALCREAD
               ------------
               January, 2016 version
               
               
This project is under development, it is NOT a final version! It's being tested under linux, if you want to try it under Windows, there must be added a modification of the code.               
 
------------
Requirements
------------
1)Install python interpreter on your Linux OS
2)Download the following database:

http://www.isical.ac.in/~crohme/ICFHR_package.zip

3)Uncompress the .zip on a folder called ICFHR_package
4)Uncompress the ICFHR_package/CROHME2012_data/trainData/trainData.zip on a folder called trainData on the same path
5)Uncompress the ICFHR_package/CROHME2012_data/testData/testData.zip on a folder called testData on the same path
6)Create a folder called trainData
7)Create a folder called testData
8)Copy the folder from the path ICFHR_package/CROHME2011_data/CROHME_training to trainData (so its new path is trainData/CROHME_training)
9)Copy the folder from the path ICFHR_package/CROHME2012_data/trainData/trainData to trainData and rename it as trainData_v2 (so its new path is trainData/trainData_v2)
10)Create a folder on trainData called TrainINKML (so its path is trainData/TrainINKML)
11)Copy the folder from the path ICFHR_package/CROHME2011_data/CROHME_test to testData (so its new path is testData/CROHME_test)
12)Copy the folder from the path ICFHR_package/CROHME2012_data/testData/testData to testData (so its new path is testData/testData)

------------
Commands
------------
1)To update the templates/database type:

./pyUpdate

2)To update feature ponderations once we have templates type:

./storeDataConc

3)To compute over an .inkml file once we have templates and we have the features ponderated type:

./overAll <filename>

4)To create a list of testing files type:

./pyLook

5)To compute over the database  once we have templates, we have the features ponderated and we have a list of testing files type:

./seeAll
