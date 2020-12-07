// program-options.cpp - application options
// written by Elijah Zarezky

// GNU libc headers
#include <limits.h>
#include <unistd.h>

// STL headers
#include <exception>
#include <iostream>
#include <string>

// Boost headers
#include <boost/program_options.hpp>

// our headers
#include "common-defs.h"

// shortcuts
namespace bpo = boost::program_options;

// public variables

std::string workingDir;
bool recurseSubdirs = false;
std::string cppExtensions("h,hh,hpp,c,cc,cpp,cxx");
std::string includeDirs;
std::string outputDir;

// impementation helpers

static bool getCurrentWorkingDirectory(std::string& workingDir)
{
	char dirBuf[PATH_MAX] = { 0 };
	if (getcwd(dirBuf, sizeof(dirBuf)) != nullptr)
	{
		workingDir.assign(dirBuf);
		return (true);
	}
	else
	{
		workingDir.clear();
		return (false);
	}
}

static void prepareProgramOptions(bpo::options_description& bpoDescription)
{
	bpo::options_description genericArgs("Generic options");

	getCurrentWorkingDirectory(workingDir);
	genericArgs.add_options()("directory,d",
		bpo::value<std::string>(&workingDir)->default_value(workingDir),
		"working directory to scan");
	genericArgs.add_options()("recursive,r", "scan directories recursively");
	genericArgs.add_options()("extensions,e",
		bpo::value<std::string>(&cppExtensions)->default_value(cppExtensions),
		"comma-separated list of file extensions to search for");
	genericArgs.add_options()("includes,i",
		bpo::value<std::string>(&includeDirs)->default_value(includeDirs),
		"colon-separated list of the additional include directories");
	genericArgs.add_options()("output,o",
		bpo::value<std::string>(&outputDir)->default_value(outputDir),
		"output directory to write report");
	genericArgs.add_options()("help,h", "display this help and exit");
	genericArgs.add_options()("version,v", "print version string");

	bpoDescription.add(genericArgs);
}

// public functions

bool parseProgramOptions(int argc, char* argv[])
{
	bpo::options_description bpoDescription;
	bpo::variables_map vmOptions;

	prepareProgramOptions(bpoDescription);
	bpo::store(bpo::parse_command_line(argc, argv, bpoDescription), vmOptions);
	bpo::notify(vmOptions);

	if (vmOptions.count("help") > 0)
	{
		std::cout << bpoDescription << std::endl;
		return (false);
	}
	else if (vmOptions.count("version") > 0)
	{
		std::cout << "Confident version 0.1.1" << std::endl;
		return (false);
	}
	else
	{
		recurseSubdirs = vmOptions.count("recursive") > 0;
		return (true);
	}
}
