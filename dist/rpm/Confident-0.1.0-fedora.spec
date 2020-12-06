# Confident utility RPM .spec file
#
# Common usage:
#   rpmbuild -ba --clean "$(rpm --eval='%{_specdir}')/Confident-0.1.0-fedora.spec"
#
# Possible additional switches:
#   --without nativearch (don't tune the performance of the code code for the host machine)
#   --without makejobslimit (don't limit number of make jobs to run simultaneously)
#   --without todayepoch (don't set "Epoch" field to the current YYYYMMDD, leave it unspecified)
#   --without ownsourcedir (don't use separate "Confident-x.x.x/" folder inside "rpmbuild/SOURCES/")
#   --with gitsource (use source tarball generated from Git source tree)
#   --with gitupdate (pull changes from a remote repository into the current branch)
#   --with gitvernum (use version number generated from "git describe" command)
#   --define 'SysTempDir value' (default is /var/tmp)
#   --define 'GitRepoDir value' (default is $HOME/Sources/GitHub/Confident.git)
#   --with nostrip (don't create separate "debuginfo" package)
#   --with gnudebug (turn off optimizations and and make debugging produce the expected results)
#   --with clang (use LLVM/Clang compiler toolchain)
#   --with ccache (use a fast C/C++ compiler cache during build)
#
# Saving rpmbuild output:
#   2>&1 | tee "$(rpm --eval='%{_builddir}')/Confident-0.1.0-rpmbuild.log"

# Acceptable build conditions

%bcond_without nativearch
%bcond_without makejobslimit
%bcond_without todayepoch
%bcond_without ownsourcedir

%bcond_with gitsource
%bcond_with gitupdate
%bcond_with gitvernum

%bcond_with nostrip
%bcond_with gnudebug
%bcond_with clang
%bcond_with ccache

# Package name and version information

%define PackageName        Confident
%define RepoOwner          SchweinDeBurg
%define RemoteRepo         https://github.com/%{RepoOwner}/%{PackageName}.git

%define VerMajor           0
%define VerMinor           1
%define VerMicro           0

%define Revision           1

%define ShortVersion       %{VerMajor}.%{VerMinor}
%define LongVersion        %{ShortVersion}.%{VerMicro}

%if 0%{?fedora}
%define DistroTag          .fedora%{fedora}
%else
%define DistroTag          %{?centos:.centos%{?centos_ver}%{!?centos_ver:%{centos}}}%{!?centos:%{?dist}}
%endif
%global PackageEpoch       %(date +%Y%m%d)

# Default directories

%{!?SysTempDir: %global SysTempDir %{?_tmppath}%{!?_tmppath:/var/tmp}}
%{!?GitRepoDir: %global GitRepoDir %{getenv:HOME}/Sources/GitHub/%{PackageName}.git}

%if 0%{?rhel} && 0%{?rhel} < 7
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{PackageName}-%{LongVersion}}
%else
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{PackageName}}
%endif
%if 0%{?fedora} && 0%{?fedora} < 28
%{!?_metainfodir: %global _metainfodir %{_datadir}/appdata}
%else
%{!?_metainfodir: %global _metainfodir %{_datadir}/metainfo}
%endif
%{!?_iconsdir: %global _iconsdir %{_datadir}/icons}
%{!?_desktopdir: %global _desktopdir %{_datadir}/applications}

# Auxiliary build tools

%{!?__gettextize: %global __gettextize gettextize}
%{!?__gtkdocize: %global __gtkdocize gtkdocize}
%{!?__intltoolize: %global __intltoolize intltoolize}

# Other globals and defines

%define GitUpdateLog       %{SysTempDir}/%{PackageName}-update.log
%define VersionFile        %{_sourcedir}/%{PackageName}-pkg-version.txt

%define GitTreeish         HEAD

%define CMakeRunDir        %{_cmake_version}-%{_target_platform}

# this hack allows us to use native optimizations when host and target has different CPUs
%define GetCpuinfoFlags    %{__cat} /proc/cpuinfo | %{__grep} -w -m 1 'flags'
%global DisableAES         %(%{GetCpuinfoFlags} | %{__grep} -w -q 'aes' && echo -n "-mno-aes" || echo -n "%{nil}")
%global DisableSSE4        %(%{GetCpuinfoFlags} | %{__grep} -w -q 'sse4' && echo -n "-mno-sse4" || echo -n "%{nil}")

# Conditional builds crap

%if %{with nativearch}
%global optflags           %(echo %{optflags} | %{__sed} -e 's/-mtune=generic/-march=native -mtune=native/')
%global optflags           %{optflags} %{DisableAES} %{DisableSSE4}
%endif

%if %{with makejobslimit}
%define _smp_mflags        -j 1
%else
%define GetNumMakeJobs \
	HalfOfCPUs=`bc <<< "$(%{_bindir}/getconf _NPROCESSORS_ONLN) / 2"`; \
	if [ $HalfOfCPUs -ge 1 ]; then echo $HalfOfCPUs; else echo 1; fi \
%{nil}
%global NumMakeJobs        %(%{GetNumMakeJobs})
%define _smp_mflags        -j %{NumMakeJobs} -l 2.0
%endif

%if %{with ownsourcedir}
%define _sourcedir         %{_topdir}/SOURCES/%{PackageName}-%{LongVersion}
%endif

%if %{with gitsource}
%define SourceName         %{PackageName}-%{LongVersion}-git
%else
%define SourceName         %{PackageName}-%{LongVersion}
%endif

%if %{with gitupdate}
%define UpdateGitRepo \
	if [ -d %{GitRepoDir} ] && $(git ls-remote -h %{RemoteRepo} >/dev/null 2>&1); then \
		git -C %{GitRepoDir} pull --no-edit >%{GitUpdateLog} 2>&1 \
		if [ -f %{GitRepoDir}/.gitmodules ]; then \
			git -C %{GitRepoDir} submodule update --init --recursive >>%{GitUpdateLog} 2>&1 \
		fi \
	fi \
%{nil}
%global RepoUpToDate       %(%{UpdateGitRepo})
%endif

%if %{with gitvernum}
%define GitReleaseTag      $(git -C %{GitRepoDir} rev-parse %{LongVersion}^{})
%define GitNumCommits      $(git -C %{GitRepoDir} rev-list --count %{GitReleaseTag}..%{GitTreeish})
%define GitHashSuffix      $(git -C %{GitRepoDir} rev-parse --short=12 %{GitTreeish})
%define MakeGitVersion \
	if [ -d %{GitRepoDir} ]; then \
		echo %{LongVersion}.%{GitNumCommits}.%{GitHashSuffix} \
	elif [ -f %{VersionFile} ]; then \
		echo $(cat %{VersionFile}) \
	else \
		echo %{LongVersion}.git \
	fi \
%{nil}
%global GitVersion         %(%{MakeGitVersion})
%else
%global GitVersion         %{nil}
%endif

%if %{with nostrip}
%global debug_package      %{nil}
%global __os_install_post  %{nil}
%endif

%if %{with gnudebug}
%global optflags           %(echo "%{optflags}" | %{__sed} -e 's/^/ /;s/$/ /')
%global optflags           %(echo "%{optflags}" | %{__sed} -e 's/ -g / -g3 -ggdb3 -gdwarf-4 /')
%global optflags           %(echo "%{optflags}" | %{__sed} -e 's/ -O[1-9a-z]* / -O0 /')
%global optflags           %(echo "%{optflags}" | %{__sed} -e 's/^[ \t]*//;s/[ \t]*$//')
%endif

%if %{with clang}
%global __cc               %(readlink -en $(clang -print-prog-name=clang))
%global __cxx              %(readlink -en $(clang++ -print-prog-name=clang++))
%else
%define WhichProgram() \
	function whichp() \
	{ \
		for curFile in $(type -afp $1 | %{__sed} 's|^[^/]*/|/|'); do \
			[ -L "$curFile" ] || [ -L $(dirname "$curFile") ] || (echo -n "$curFile" && break); \
		done \
	}; \
	whichp %1 \
%{nil}
%global __cc               %(%WhichProgram %{__cc})
%global __cxx              %(%WhichProgram %{__cxx})
%endif

%if %{with ccache}
%define GetCCacheVersion \
	CCachePkgVersion=$(rpm -q --qf '%{VERSION}' ccache) \
	if [ $? -ne 0 ]; then \
		CCachePkgVersion="0.0.0" \
	fi \
	echo $CCachePkgVersion \
%{nil}
%global CCacheVersion      %(%{GetCCacheVersion})

%define TestCCache30 \
	IFS="." read CCacheMajor CCacheMinor CCacheMicro <<< "%{CCacheVersion}"; \
	if [ $CCacheMajor -ge 3 -a $CCacheMinor -ge 0 ]; then echo YES; else echo NO; fi \
%{nil}
%global HasCCache          %(%{TestCCache30})
%else
%global HasCCache          %{nil}
%endif

# Header

Name: %{PackageName}

%if %{with gitvernum}
Version: %{GitVersion}
%else
Version: %{LongVersion}
%endif
Release: %{Revision}%{DistroTag}
%if %{with todayepoch}
Epoch: %{PackageEpoch}
%endif

Summary: Dependency analyzer for C/C++ projects
Group: Development/Tools
License: MIT

URL: https://github.com/SchweinDeBurg/Confident/

Vendor: Zarezky.spb.ru
Packager: Elijah Zarezky <elijah@zarezky.spb.ru>

# Sources

%if %{with gitsource}
Source0: %{SourceName}.tar.gz
%else
Source0: https://github.com/SchweinDeBurg/Confident/archive/%{SourceName}.tar.gz
%endif

%if %{with gitvernum}
Source1: %{VersionFile}
%endif

# Patches

# Directory for the (fake) install step

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Build requirements

BuildRequires: boost-devel >= 1.64.0
BuildRequires: glibc-devel >= 2.26
BuildRequires: libstdc++-devel >= 7.3.1

%if 0%{?rhel}
# available from EPEL repos
BuildRequires: cmake3 >= 3.13.5
%else
BuildRequires: cmake >= 3.14.7
%endif
BuildRequires: gcc-c++ >= 7.3.1
%if %{with gitsource}
BuildRequires: git >= 2.29.2
%endif
BuildRequires: ninja-build >= 1.10.2
BuildRequires: sed >= 4.2.2

# Run-time requirements

Requires: boost-filesystem >= 1.64.0
Requires: boost-program-options >= 1.64.0
Requires: boost-regex >= 1.64.0
Requires: boost-system >= 1.64.0
Requires: glibc >= 2.26
Requires: libgcc >= 7.3.1
Requires: libstdc++ >= 7.3.1

# Virtual package names

# Description

%description
Confident is a very simple dependency analyzer for C/C++ projects.

# Subpackages

# Build scripts

%prep
[ -f %{GitUpdateLog} ] && %{__cat} %{GitUpdateLog} && %{__rm} -f %{GitUpdateLog}

%if %{with gitsource}
if [ -d %{GitRepoDir} ]; then
	%{__rm} -f %{_sourcedir}/%{SourceName}.tar.gz
	pushd %{GitRepoDir}
	git archive --format=tar.gz --prefix=%{SourceName}/ --output=%{_sourcedir}/%{SourceName}.tar.gz %{GitTreeish}
	popd
%if %{with gitvernum}
	echo %{GitVersion} > %{VersionFile}
%endif
fi
%endif

# in case of "ccache" usage this will speed-up the build after version change
%{__rm} -rf %{PackageName} && %{__mkdir} %{PackageName}
%{__tar} --strip-components=1 -C %{PackageName} -xf %{SOURCE0}
%setup -q -n %{PackageName} -T -D

%build
%if %{with ccache} && "%{HasCCache}" == "YES"
export CC="ccache %{__cc}"
export CXX="ccache %{__cxx}"
%else
export CC="%{__cc}"
export CXX="%{__cxx}"
%endif

# prepare GCC/Binutils environment
export CFLAGS="%{optflags} -w"
export CXXFLAGS="%{optflags} -w"

# disable GTK-Doc warnings
export GTKDOC_TRACE="ERROR"

[ -n "$LD_RUN_PATH" ] && unset LD_RUN_PATH

%{__mkdir} -p %{CMakeRunDir} && pushd %{CMakeRunDir}
%if 0%{?rhel}
%{__cmake3} \
%else
%{__cmake} \
%endif
	-D CMAKE_INSTALL_PREFIX=%{_prefix} \
	-D CMAKE_BUILD_TYPE=RelWithDebInfo \
	-D CMAKE_C_FLAGS="%{optflags} -w" \
	-D CMAKE_CXX_FLAGS="%{optflags} -w" \
	-Wno-dev \
	-G "Ninja" \
	..
popd
%{__ninja} -C %{CMakeRunDir} %{?_smp_mflags}

%check

%install
%{__rm} -rf %{buildroot}

DESTDIR=%{buildroot} %{__ninja} -C %{CMakeRunDir} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -exec %{__rm} -f {} ';'

%if 0%{?fedora}
%{_rpmconfigdir}/check-rpaths
%endif

%clean
%{__rm} -rf %{buildroot}

# Install/uninstall scripts

%pretrans

%pre

%post

%preun

%postun

%posttrans

# Files to install

%files
%defattr(-, root, root, -)
%license MIT-LICENSE.txt
%doc README
%{_bindir}/%{name}

# Changes in the package

%changelog
* Sun Dec 06 2020 Elijah Zarezky <elijah@zarezky.spb.ru> - 0.1.0-1
- Initial package.
- Built using "--with gitsource --with gitvernum".
