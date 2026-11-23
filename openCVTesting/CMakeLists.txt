cmake_minimum_required(VERSION 3.10)
project(OpenCVTest)

# OpenCV
find_package(OpenCV REQUIRED)

# RapidOCRLite
find_package(RapidOCRLite CONFIG REQUIRED)

add_executable(openCVExec main.cpp)

# Link both libraries
target_link_libraries(openCVExec PRIVATE
    ${OpenCV_LIBS}
    RapidOCRLite::rapidocrlite
)