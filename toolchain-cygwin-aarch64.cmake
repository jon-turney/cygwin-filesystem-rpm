SET(CMAKE_SYSTEM_NAME CYGWIN)
SET(CMAKE_SYSTEM_PROCESSOR aarch64)
SET(CMAKE_LEGACY_CYGWIN_WIN32 0)

# specify the cross compiler
IF(NOT DEFINED ENV{CC})
    SET(CMAKE_C_COMPILER aarch64-pc-cygwin-gcc)
ENDIF()
IF(NOT DEFINED ENV{CXX})
    SET(CMAKE_CXX_COMPILER aarch64-pc-cygwin-g++)
ENDIF()
IF(NOT DEFINED ENV{FC})
    SET(CMAKE_Fortran_COMPILER aarch64-pc-cygwin-gfortran)
ENDIF()

# where is the target environment
SET(CMAKE_FIND_ROOT_PATH /usr/aarch64-pc-cygwin/sys-root/usr)

# search for programs in the build host directories
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
# for libraries, headers and packages in the target directories
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Make sure Qt can be detected by CMake
SET(QT_BINARY_DIR /usr/aarch64-pc-cygwin/bin /usr/bin)

# set the resource compiler (RHBZ #652435)
IF(NOT $ENV{RC})
    SET(CMAKE_RC_COMPILER /usr/bin/aarch64-pc-cygwin-windres)
ENDIF()

# These are needed for compiling lapack (RHBZ #753906)
SET(CMAKE_AR:FILEPATH /usr/bin/aarch64-pc-cygwin-ar)
SET(CMAKE_RANLIB:FILEPATH /usr/bin/aarch64-pc-cygwin-ranlib)

# Workaround failure to detect boost (see #2037724)
SET(Boost_ARCHITECTURE "-aarc64")
