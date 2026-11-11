/*
    Desc: This is a test file in a test folder to play 
        with the functionalities of openCV

    Author: Vishnu Channagiri
*/

#include <opencv2/opencv.hpp>
#include <iostream>

//using namespace std;
//using namespace cv;
int main(){
    std::cout << "OpenCV version: " << CV_VERSION << std::endl;

    //second arg: if 0, greyscale; if 1 or no inp then color 
    cv::Mat img = cv::imread("../inpImage.jpg");

    if (img.empty()) {
        std::cerr << "Error: Could not find or open image" << std::endl;
        return -1;
    }

    cv::imshow("Original image", img);
    cv::waitKey(0); //disp image until a key is pressed

    return 0;
}