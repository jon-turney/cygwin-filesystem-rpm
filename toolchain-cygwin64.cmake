SET(CMAKE_SYSTEM_NAME CYGWIN)
SET(CMAKE_SYSTEM_PROCESSOR x86_64)
SET(CMAKE_LEGACY_CYGWIN_WIN32 0)

# specify the cross compiler
SET(CMAKE_C_COMPILER /usr/bin/x86_64-pc-cygwin-gcc)
SET(CMAKE_CXX_COMPILER /usr/bin/x86_64-pc-cygwin-g++)
SET(CMAKE_Fortran_COMPILER /usr/bin/x86_64-pc-cygwin-gfortran)
SET(CMAKE_RC_COMPILER /usr/bin/x86_64-pc-cygwin-windres)
SET(CMAKE_AR:FILEPATH /usr/bin/x86_64-pc-cygwin-ar)
SET(CMAKE_RANLIB:FILEPATH /usr/bin/x86_64-pc-cygwin-ranlib)

# where is the target environment
SET(CMAKE_FIND_ROOT_PATH /usr/x86_64-pc-cygwin/sys-root/usr)

# search for programs in the build host directories
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
# for libraries and headers in the target directories
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

SET(PKG_CONFIG_EXECUTABLE /usr/bin/x86_64-pc-cygwin-pkg-config)
SET(PKGCONFIG_EXECUTABLE /usr/bin/x86_64-pc-cygwin-pkg-config)

# FindQt4.cmake queries qmake to get information,
# which doesn't work when crosscompiling
SET(QT_QMAKE_EXECUTABLE /usr/bin/x86_64-pc-cygwin-qmake)
SET(QT_MOC_EXECUTABLE   /usr/bin/x86_64-pc-cygwin-moc)
SET(QT_RCC_EXECUTABLE /usr/bin/x86_64-pc-cygwin-rcc)
SET(QT_UIC_EXECUTABLE /usr/bin/x86_64-pc-cygwin-uic)
SET(QT_UIC3_EXECUTABLE /usr/bin/x86_64-pc-cygwin-uic3)
SET(QT_LRELEASE_EXECUTABLE /usr/bin/x86_64-pc-cygwin-lrelease)
SET(QT_LUPDATE_EXECUTABLE /usr/bin/x86_64-pc-cygwin-lupdate)
SET(QT_DBUSCPP2XML_EXECUTABLE /usr/bin/x86_64-pc-cygwin-qdbuscpp2xml)
SET(QT_DBUSXML2CPP_EXECUTABLE /usr/bin/x86_64-pc-cygwin-qdbusxml2cpp)
SET(QT_HEADERS_DIR ${CMAKE_FIND_ROOT_PATH}/include)
SET(QT_LIBRARY_DIR ${CMAKE_FIND_ROOT_PATH}/lib)
