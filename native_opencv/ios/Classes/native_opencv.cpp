#include <stdint.h>
#include <opencv2/core/version.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <opencv2/objdetect.hpp>
using namespace std;
using namespace cv;
extern "C" {
__attribute__((visibility("default"))) __attribute__((used))
int32_t native_add(int32_t x, int32_t y) {
    return x + y;
}
const char* version() {
    return CV_VERSION;
}

const float* rect(int width, int height, int rotation, uint8_t* bytes, bool isYUV, int32_t* outCount) {
    Mat frame;
    if (isYUV) {
        Mat myyuv(height + height / 2, width, CV_8UC1, bytes);
        cvtColor(myyuv, frame, COLOR_YUV2BGRA_NV21);
    } else {
        frame = Mat(height, width, CV_8UC4, bytes);
    }

    vector<float> output;

    output.push_back(10.0);
    output.push_back(20.0);
    output.push_back(400.0);
    output.push_back(500.0);

    unsigned int total = sizeof(float) * output.size();
    float* jres = (float*)malloc(total);
    memcpy(jres, output.data(), total);

    *outCount = output.size();
    return jres;



}
}


