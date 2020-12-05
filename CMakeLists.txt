cmake_minimum_required(VERSION 3.14.0)

project(Confident)

include(FindPkgConfig)
include(GNUInstallDirs)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)
set(BIN_INSTALL_PATH ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR} CACHE PATH "Install path for binaries")

add_subdirectory(src)

message(STATUS "Configuration summary:")
message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C compiler options: ${CMAKE_C_FLAGS}")
message(STATUS "  C++ compiler options: ${CMAKE_CXX_FLAGS}")
