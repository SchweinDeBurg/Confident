list(APPEND ${PROJECT_NAME}_HEADERS
	common-defs.h
)

list(APPEND ${PROJECT_NAME}_SOURCES
	entry-point.cpp
	filesystem-tasks.cpp
	program-options.cpp
)

find_package(Boost 1.63.0 COMPONENTS filesystem program_options regex REQUIRED)

add_executable(${PROJECT_NAME} ${${PROJECT_NAME}_SOURCES})
#add_dependencies(${PROJECT_NAME} dependency-graph)

target_include_directories(${PROJECT_NAME} PRIVATE ${Boost_INCLUDE_DIR})
target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})

install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION ${BIN_INSTALL_PATH})
