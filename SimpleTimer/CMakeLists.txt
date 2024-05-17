cmake_minimum_required(VERSION 3.12)

set(PICO_BOARD pico_w)

# Pull in SDK (must be before project)
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(SimpleTimer C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the SDK
pico_sdk_init()


# Lists all local c files needed for the program #
add_executable(SimpleTimer
        timer.c
        PicoType.c
        )

# Pulls in common dependencies #
target_link_libraries(SimpleTimer pico_stdlib hardware_pwm hardware_adc)

# Creates the map/bin/hex file etc #
pico_add_extra_outputs(SimpleTimer)