# Motion Detector

It detects any motion in camera, and stores the time of motion in an excel file. It is based on OpenCV, basically it works on a simple princple.

All work should be done in grayscale.

1. As soon as camera triggers first frame will be static background for further comparison.
2. Then calculate the difference between current frame and static background frame.
3. Then apply threshold to find if changes are found or not.
4. Then find contours of the current frame and check if the area of the contours is greater than a threshold then we'll consider it as a moving object else not. This will help in generating good result.
5. Then apply rectangle on the moving object.
