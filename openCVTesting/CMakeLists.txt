cmake_minimum_required(VERSION 3.10)
project(OpenCVTest)

find_package(OpenCV REQUIRED)

add_executable(openCVExec main.cpp)
target_link_libraries(openCVExec ${OpenCV_LIBS})
