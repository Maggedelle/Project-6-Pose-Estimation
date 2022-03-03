#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <opencv2/objdetect.hpp>
using namespace cv;
using namespace std;


int main() {
	VideoCapture cap(0);
	Mat img; 

	

	while (true) {
	    cap.read(img);
		rectangle(img,Point(200,200),Point(350,350), Scalar(255, 0, 255), 3);
		imshow("Image", img);
		Mat frame;
		
		waitKey(20);
	}
}