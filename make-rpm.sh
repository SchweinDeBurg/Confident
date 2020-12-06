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

rpmbuild -ba --clean "${thisDir}/dist/rpm/Confident-0.1.0-fedora.spec" \
	--define "GitRepoDir ${thisDir}" \
	--with gitsource --with gitupdate --with gitvernum --with ccache \
2>&1 | tee "$(rpm --eval='%{_builddir}')/Confident-0.1.0-rpmbuild.log"
