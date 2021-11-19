# Install script for directory: /home/hung/Desktop/Self-driving-car/catkin_ws/src/vehicle_sim/launcher/vehicle_sim_launcher

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/hung/Desktop/Self-driving-car/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/hung/Desktop/Self-driving-car/catkin_ws/build/vehicle_sim/launcher/vehicle_sim_launcher/catkin_generated/installspace/vehicle_sim_launcher.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/vehicle_sim_launcher/cmake" TYPE FILE FILES
    "/home/hung/Desktop/Self-driving-car/catkin_ws/build/vehicle_sim/launcher/vehicle_sim_launcher/catkin_generated/installspace/vehicle_sim_launcherConfig.cmake"
    "/home/hung/Desktop/Self-driving-car/catkin_ws/build/vehicle_sim/launcher/vehicle_sim_launcher/catkin_generated/installspace/vehicle_sim_launcherConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/vehicle_sim_launcher" TYPE FILE FILES "/home/hung/Desktop/Self-driving-car/catkin_ws/src/vehicle_sim/launcher/vehicle_sim_launcher/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/vehicle_sim_launcher" TYPE DIRECTORY FILES "/home/hung/Desktop/Self-driving-car/catkin_ws/src/vehicle_sim/launcher/vehicle_sim_launcher/launch")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/vehicle_sim_launcher" TYPE DIRECTORY FILES "/home/hung/Desktop/Self-driving-car/catkin_ws/src/vehicle_sim/launcher/vehicle_sim_launcher/scripts")
endif()

