find_program(DOT_EXECUTABLE "dot")

if(DOT_EXECUTABLE)
	message(STATUS "Dot found: ${DOT_EXECUTABLE}")
else()
	message(STATUS "Dot not found!")
endif()

if(DOT_EXECUTABLE)
	add_custom_command(OUTPUT ${CMAKE_SOURCE_DIR}/graphviz/${PROJECT_NAME}.dot
		COMMAND ${CMAKE_COMMAND} ${CMAKE_SOURCE_DIR} --graphviz=${CMAKE_SOURCE_DIR}/graphviz/${PROJECT_NAME}.dot
	)
	add_custom_command(OUTPUT ${CMAKE_SOURCE_DIR}/graphviz/${PROJECT_NAME}.png
		DEPENDS ${CMAKE_SOURCE_DIR}/graphviz/${PROJECT_NAME}.dot
		COMMAND ${DOT_EXECUTABLE} -Tpng ${CMAKE_SOURCE_DIR}/graphviz/${PROJECT_NAME}.dot -o ${CMAKE_SOURCE_DIR}/graphviz/${PROJECT_NAME}.png
		COMMAND ${CMAKE_COMMAND} -E remove -f ${CMAKE_SOURCE_DIR}/graphviz/${PROJECT_NAME}.dot
		COMMAND ${CMAKE_COMMAND} -E remove -f ${CMAKE_SOURCE_DIR}/graphviz/${PROJECT_NAME}.dot.*
	)
	add_custom_target(dependency-graph
		DEPENDS ${CMAKE_SOURCE_DIR}/graphviz/${PROJECT_NAME}.png
	)
endif()
