#!/bin/sh -

# cygwin-scripts
# Copyright (C) 2008 Red Hat Inc., Richard W.M. Jones.
# Copyright (C) 2008 Levente Farkas
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

# This is a useful command-line script through which one can use the
# macros from /etc/rpm/macros.cross, macros.cygwin32 and macros.cygwin64

if [ "`basename $0`" = "i686-pc-cygwin-pkg-config" ] ; then
    NAME="cygwin32_pkg_config"
elif [ "`basename $0`" = "x86_64-pc-cygwin-pkg-config" ] ; then
    NAME="cygwin64_pkg_config"
else
    NAME="`basename $0|tr -- - _`"
fi

# When using the CMake wrappers, prevent CFLAGS and CXXFLAGS from being set
# unless they're already set in the current environment (RHBZ #1136069)
if [[ $NAME == *cmake* ]] ; then
    CYGWIN32_CFLAGS=${CYGWIN32_CFLAGS:-""}
    CYGWIN32_CXXFLAGS=${CYGWIN32_CXXFLAGS:-""}
    CYGWIN64_CFLAGS=${CYGWIN64_CFLAGS:-""}
    CYGWIN64_CXXFLAGS=${CYGWIN64_CXXFLAGS:-""}
fi

# NOTE: The use of 'eval' in combination with '$@' is a potential security risk
#       We should find a more safe replacement for this command
#       Suggestions are welcome at the Fedora MinGW mailing list
eval "CYGWIN_CMAKE_NO_VERBOSE=1 `rpm --eval "%{$NAME}"`" '"$@"'
