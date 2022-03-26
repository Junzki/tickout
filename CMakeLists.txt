# CMakeList.txt : CMake project for tickout, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)

project ("tickout" CXX)
set(CMAKE_CXX_STANDARD 14)

include_directories("${PROJECT_SOURCE_DIR}/include")


set(${PROJECT_NAME}_SOURCE "${PROJECT_SOURCE_DIR}/src")
file(GLOB_RECURSE ${PROJECT_NAME}_FILES "${${PROJECT_NAME}_SOURCE}/*.*")

find_package(unofficial-curlpp CONFIG REQUIRED)


set(TARGET_LIBRARIES unofficial::curlpp::curlpp)
if(WIN32)
list(APPEND TARGET_LIBRARIES shlwapi)
endif()

# Targets
set(TARGET_BINARY "tickout")

# Add source to this project's executable.
add_executable (${TARGET_BINARY} ${${PROJECT_NAME}_FILES})

target_link_libraries(${TARGET_BINARY} PRIVATE ${TARGET_LIBRARIES})
# TODO: Add tests and install targets if needed.
