<p align="center">Computer Vision and Image Processing</br>CSE573 - Fall 2018</br>Keypoint detection in Images using SIFT</p>

--------------------------

<p align="center">
  <img width="640" height="400" src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/task2.jpg"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Keypoint%20Image_2.png">
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Output%20Image.png">
</p>

-------

Goal
-------
To detect keypoints in any given image using Scale Invariant Feature Transform (SIFT) algorithm. SIFT is used to identify features in the objects in the given image, these features are resilient to any change in scale, rotation, illuminations and viewpoint of the object. Although this repository does not implement the entire algorithm (which by the way is patented), it goes as far as detecting the keypoints in images by computing different scale spaces (octaves), application of Laplacian of Gaussian, identifing the maxima/minima in the keypoints

Scale Spaces
-------
Original/Input image is progressively blurred using a Guassian filter to create 5 more images, then the input image is halved in sized and the process is repeated. Each level is called an octave consisting of 5 images. The amount of blur is given by sigma, and at each level sigma differs by a factor sqrt(2) to the previous level

The output of the 2nd octave is shown below

<p align="center">
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Gaussian%20Image_1.png"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Gaussian%20Image_2.png"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Gaussian%20Image_3.png"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Gaussian%20Image_4.png"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Gaussian%20Image_5.png"></br>
</p>

Laplacian of Gaussian
-------

Laplacian of Gaussian is good at detecting corners and edges which are good key points. We find the difference of Gaussian of the consecutive images in each octave to produce 4 difference of Gaussian images which is a very good approximation of Laplacian of Gaussian

The DoG of the 2nd octave is shown below

<p align="center">
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_DifferenceOfGaussian_1.png"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_DifferenceOfGaussian_2.png"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_DifferenceOfGaussian_3.png"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_DifferenceOfGaussian_4.png"></br>
</p>

Detecting Keypoints
-------

Keypoints are identified using the maxima/minima i.e. take first 3 DoG images together and for every pixel, compare 26 neigbouring pixels (like a sandwich). I took all the neighbouring cells, appended to a list and sorted them. If the pixel in question is less than or equal to the first element in the list or greater than or equal to the last element in the list, we set them as minima and maxima respectively. These pixels are the keypoints that are placed in the images for every octave. Although the implementation ends here, we can further reject low contrast keypoints and detect features in the images.

The minima/maxima keypoints detected in 2nd octave are shown below

<p align="center">
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Keypoint%20Image_1.png"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Keypoint%20Image_2.png"></br>
  <img src="https://github.com/sudonav/ImageKeypointRecognition/blob/master/Output/Octave_2_Output%20Image.png"></br>
</p>


Credits
-------
I thank [**Professor Junsong Yuan**](https://cse.buffalo.edu/~jsyuan/index.html) for delivering the Course [**CSE 573**] that helped me learn the skills of Computer Vision and Image Processing to create this **Keypoint Detection** in images using Scale Invariant Feature Tranform - SIFT implementation.

Developer
---------
Navaneethakrishnan Ramanathan nramanat@buffalo.edu</br>
[LinkedIn](https://www.linkedin.com/in/nramanat/)

SIFT - A great read!
---------
Check out this amazing article that has covers the entire SIFT algorithm [**SIFT**](http://aishack.in/tutorials/sift-scale-invariant-feature-transform-keypoints/)

License
----------
Copyright {2019} 
{Navaneethakrishnan Ramanathan nramanat@buffalo.edu} 

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
