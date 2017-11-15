#!/bin/sh
# cygwin-find-debuginfo.sh - automagically generate debug info and file list
# for inclusion in an rpm spec file for cygwin-* packages.

if [ "$#" -lt 2 ] ; then
    echo "Usage: $0 <BUILDDIR> [TARGET]..."
    exit 1
fi

BUILDDIR=$1
shift

for f in `find $RPM_BUILD_ROOT -type f -name "*.exe" -or -name "*.dll"`
do
	case $(cygwin-objdump -h $f 2>/dev/null | egrep -o '(debug[\.a-z_]*|gnu.version)') in
	    *debuglink*) continue ;;
	    *debug*) ;;
	    *gnu.version*)
		echo "WARNING: "`echo $f | sed -e "s,^$RPM_BUILD_ROOT/*,/,"`" is already stripped!"
		continue
		;;
	    *) continue ;;
	esac

	echo extracting debug info from $f
	cygwin-objcopy --only-keep-debug $f $f.debug || :
	pushd `dirname $f`
	keep_symbols=`mktemp`
	cygwin-nm --format=sysv --defined-only $f.debug | awk -F \| '{ if ($4 ~ "Function") print $1 }' | sort > "$keep_symbols"
	cygwin-objcopy --add-gnu-debuglink=`basename $f.debug` --strip-unneeded --keep-symbols="$keep_symbols" `basename $f` || :
	rm -f "$keep_symbols"
	popd
done

for target in $@; do
	prefix=`rpm --eval "%{${target}_prefix}"`
	if [ ! -d $RPM_BUILD_ROOT$prefix ] ; then
		continue
	fi
	find $RPM_BUILD_ROOT$prefix -type f -name "*.exe.debug" -or -name "*.dll.debug" |
		sed -n -e "s#^$RPM_BUILD_ROOT##p" > $BUILDDIR/${target}-debugfiles.list
done
