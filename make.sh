#!/bin/bash

# early checks

if [ "${BASH_SOURCE[0]}" != "$0" ]; then
	echo -e "\nThis script uses 'exit' calls and thus must \e[1mNOT\e[0m to be launched source-d."
	read -p "Press [Enter] key to terminate execution and then try again properly..."
	return
fi

# global variables

thisFile=$(readlink -e -n $0)
thisDir=$(dirname "${thisFile}")

cmakeDir="${thisDir}/build"

# helper functions

function atExit()
{
	local exitCode=$?
	set +e
	echo -ne "\n\e[1m[ $(basename ${thisFile}) ] : \e[0m"
	if [ ${exitCode} == 0 ]; then
		echo -e "\e[1;38;5;28mDone, succeeded.\e[0m\n"
	else
		echo -e "\e[1;38;5;160mDone, failed.\e[0m\n"
	fi
	[ "${BASH_SOURCE[0]}" == "$0" ] && exit ${exitCode}
}

# entry point

set -e
trap atExit EXIT

rm -rf "${cmakeDir}"/*

export CC="ccache /usr/bin/gcc"
export CXX="ccache /usr/bin/g++"

export NINJA_TERM=dumb
export CLICOLOR_FORCE=yes

pushd "${cmakeDir}"
cmake -D CMAKE_INSTALL_PREFIX=/usr -D CMAKE_BUILD_TYPE="Debug" -Wno-dev -G "Ninja" ..
popd
ninja -C "${cmakeDir}" -j 1
