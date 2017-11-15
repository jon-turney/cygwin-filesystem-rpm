#!/bin/bash

# This script reads filenames from STDIN and outputs any relevant provides
# information that needs to be included in the package.

[ -z "$OBJDUMP" ] && OBJDUMP=cygwin-objdump

targets=$@
if [ -z "$targets" ] ; then
    echo "Usage: $0 [ cygwin32 ] [ cygwin64 ]"
    exit 1
fi

# Get the list of files.

filelist=`sed "s/['\"]/\\\&/g"`

dlls=$(echo $filelist | tr [:blank:] '\n' | grep -Ei '\.(dll|exe)$')

for target in $targets; do
	dll_found=false
	host_triplet=`rpm --eval "%{${target}_target}"`
	for f in $dlls; do
		if [[ $f =~ .*$host_triplet.* ]]; then
			$OBJDUMP -p $f | grep 'DLL Name' | grep -Eio '[-._\+[:alnum:]]+\.dll' |
				tr [:upper:] [:lower:] |
				sed "s/\(.*\)/$target(\1)/"
			dll_found=true
		fi
	done
	# Add a dependency on filesystem and crt if necessary
	if [ $dll_found = true ]; then
		echo "${target}-filesystem >= 8"
	fi
done | sort -u
