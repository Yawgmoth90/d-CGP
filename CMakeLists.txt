cmake_minimum_required(VERSION 3.2.0)

project(dCGP VERSION 1.0.1)

enable_testing()

# Here we augment the cmake modules path
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake" "${CMAKE_CURRENT_SOURCE_DIR}/cmake/yacma")

# Set default build type to "Release".
if(NOT CMAKE_BUILD_TYPE)
	set(CMAKE_BUILD_TYPE Release CACHE STRING
		"Choose the type of build, options are: None Debug Release RelWithDebInfo MinSizeRel."
	FORCE)
endif(NOT CMAKE_BUILD_TYPE)

include(YACMACompilerLinkerSettings)

# Setup the CXX flags from YACMA and show final result
YACMA_SETUP_CXX_FLAGS()

# Provides build options to CMake
# Build Option: when active the file main.cpp is built and linked to the PaGMO static library
option(BUILD_MAIN "Build 'main.cpp'." ON)
option(BUILD_TESTS "Build test set." OFF)
option(BUILD_EXAMPLES "Build examples." OFF)
option(BUILD_DCGPY "Build the Python bindings." OFF)

set(MANDATORY_LIBRARIES "")

# -----------------------------------------------------------------------------------
# We start finding third party dependencies

# 0 - Initial thread setup.
include(YACMAThreadingSetup)
set(MANDATORY_LIBRARIES ${MANDATORY_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT})
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${YACMA_THREADING_CXX_FLAGS}")

# set up the python stuff
if(BUILD_DCGPY)
	include(YACMAPythonSetup)
    message(STATUS "Linking boost python.")
	list(APPEND REQUIRED_BOOST_LIBS python)
    message(STATUS "Linking serialization.")
	list(APPEND REQUIRED_BOOST_LIBS serialization)
endif()

# 1 - Boost Setup.
IF(BUILD_TESTS)
    enable_testing()
	message(STATUS "Linking unit tests to Boost.Test.")
	set(REQUIRED_BOOST_LIBS ${REQUIRED_BOOST_LIBS} unit_test_framework)
	IF(CMAKE_BUILD_TYPE STREQUAL "Release")
		message(STATUS "Linking performance tests to Boost Timer and Boost.Chrono.")
		set(REQUIRED_BOOST_LIBS ${REQUIRED_BOOST_LIBS} timer chrono system)
	ENDIF()
ENDIF()

message(STATUS "Required Boost libraries: ${REQUIRED_BOOST_LIBS}")
# Timers are available since 1.48.0.
find_package(Boost 1.48.0 REQUIRED COMPONENTS "${REQUIRED_BOOST_LIBS}")
message(STATUS "Detected Boost version: ${Boost_VERSION}")
# Include system Boost headers.
message(STATUS "Boost include dirs: ${Boost_INCLUDE_DIRS}")
message(STATUS "Boost libraries: ${Boost_LIBRARIES}")
include_directories(SYSTEM ${Boost_INCLUDE_DIRS})

# 2 - Piranha (sparse polynomial multiplication) Header only
find_package(Piranha REQUIRED)
message(STATUS "Piranha library found.")
message(STATUS "Piranha include dir is: ${Piranha_INCLUDE_DIR}")
include_directories(${Piranha_INCLUDE_DIR})

# 3 - Audi (automated differentiation) Header only
find_package(Audi REQUIRED)
message(STATUS "Audi library found.")
message(STATUS "Audi include dir is: ${Piranha_INCLUDE_DIR}")
include_directories(${Audi_INCLUDE_DIR})

# 2 - GMP setup (used by piranha)
find_package(GMP REQUIRED)
message(STATUS "GMP library found.")
message(STATUS "GMP include dir is: ${GMP_INCLUDE_DIR}")
message(STATUS "GMP library is: ${GMP_LIBRARIES}")
include_directories(${GMP_INCLUDE_DIR})

# 3 - MPFR setup (used by piranha)
find_package(MPFR REQUIRED)
message(STATUS "MPFR library found.")
message(STATUS "MPFR include dir is: ${MPFR_INCLUDE_DIR}")
message(STATUS "MPFR library is: ${MPFR_LIBRARIES}")
message(STATUS "Checking MPFR version.")
try_compile(MPFR_VERSION_CHECK ${CMAKE_BINARY_DIR} "${CMAKE_SOURCE_DIR}/cmake/mpfr_check_version.cpp"
	CMAKE_FLAGS "-DINCLUDE_DIRECTORIES:STRING=${MPFR_INCLUDE_DIR};${GMP_INCLUDE_DIR}")
IF(NOT MPFR_VERSION_CHECK)
	message(FATAL_ERROR "Unsupported MPFR version, please upgrade.")
ENDIF(NOT MPFR_VERSION_CHECK)
message(STATUS "MPFR version is ok.")
include_directories(${MPFR_INCLUDE_DIR})

# NOTE: MPFR should be linked in before GMP, that's why we link GMP here.
set(MANDATORY_LIBRARIES ${MANDATORY_LIBRARIES} ${MPFR_LIBRARIES} ${GMP_LIBRARIES})

# Add the subdirectory for the library / headers
add_subdirectory("${CMAKE_SOURCE_DIR}/include")

# Build main
IF(BUILD_MAIN)
	add_executable(main main.cpp)
	target_link_libraries(main ${MANDATORY_LIBRARIES})
    target_compile_options(main PUBLIC "$<$<CONFIG:DEBUG>:${YACMA_CXX_FLAGS_DEBUG}>")
    target_compile_options(main PUBLIC "$<$<CONFIG:RELEASE>:${YACMA_CXX_FLAGS}>")
    set_property(TARGET main PROPERTY CXX_STANDARD 14)
    set_property(TARGET main PROPERTY CXX_STANDARD_REQUIRED YES)
ENDIF(BUILD_MAIN)

# Build perf test in release and tests in debug
IF(BUILD_TESTS)
	add_subdirectory("${CMAKE_SOURCE_DIR}/tests")
ENDIF(BUILD_TESTS)

# Build examples
IF(BUILD_EXAMPLES)
	add_subdirectory("${CMAKE_SOURCE_DIR}/examples")
ENDIF(BUILD_EXAMPLES)

# Build the python module
if(BUILD_DCGPY)
	add_subdirectory("${CMAKE_SOURCE_DIR}/dcgpy")
    if(WIN32 AND MINGW)
		message(STATUS "Creating the files for the generation of a binary wheel for MinGW.")
		configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tools/mingw_wheel_setup.py" "${CMAKE_CURRENT_BINARY_DIR}/wheel/setup.py")
		configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tools/mingw_wheel_libs_python${PYTHON_VERSION_MAJOR}.txt" "${CMAKE_CURRENT_BINARY_DIR}/wheel/mingw_wheel_libs_python${PYTHON_VERSION_MAJOR}.txt")
    endif()
    if(UNIX AND NOT APPLE)
        message(STATUS "Creating the files for the generation of a manylinux binary wheel.")
        configure_file("${CMAKE_CURRENT_SOURCE_DIR}/tools/manylinux_wheel_setup.py" "${CMAKE_CURRENT_BINARY_DIR}/wheel/setup.py")
    endif()
endif()
