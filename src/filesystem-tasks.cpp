// filesystem-tasks.cpp - filesystem specific routines
// written by Elijah Zarezky

// GNU libc headers
#include <stdio.h>

 // STL headers
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>

// Boost headers
#include <boost/filesystem.hpp>
#include <boost/regex.hpp>

// our headers
#include "common-defs.h"

// shortcuts
namespace bfs = boost::filesystem;

// impementation helpers

static size_t initExtensions(const char* cppExtensions, TStringSet& extensionsSet)
{
	extensionsSet.clear();

	if (cppExtensions != nullptr && *cppExtensions != 0)
	{
		std::istringstream inputStream(cppExtensions);
		std::string curExt;
		while (std::getline(inputStream, curExt, ','))
		{
			curExt.insert(curExt.begin(), '.');
			extensionsSet.insert(curExt);
		}
	}

	return (extensionsSet.size());
}

template <typename IteratorType>
static void iterateDirectory(const bfs::path& rootPath, TStringVector& filesList)
{
	TStringSet extensionsSet;
	initExtensions(cppExtensions.c_str(), extensionsSet);

	for (auto& it: IteratorType(rootPath))
	{
		if (bfs::is_regular_file(it.path()) && extensionsSet.find(it.path().extension().string()) != extensionsSet.end())
		{
			filesList.push_back(it.path().string());
		}
	}
}

static size_t executeProcess(const char* processText, std::string& processOutput)
{
	processOutput.clear();

	std::array<char, 1024> pipeBuf;
	pipeBuf.fill(0);
	std::unique_ptr<FILE, decltype(&pclose)> processPipe(popen(processText, "r"), pclose);

	if (processPipe != nullptr)
	{
		while (fgets(pipeBuf.data(), pipeBuf.size(), processPipe.get()) != nullptr)
		{
		  processOutput += pipeBuf.data();
		}
	}
	else
	{
		throw std::runtime_error("popen() failed!");
	}

	return (processOutput.length());
}

static size_t getSystemIncludePaths(TStringVector& pathsList)
{
	pathsList.clear();

	static const char scriptText[] =
		"for curLine in $(gcc -E -Wp,-v -xc++ /dev/null 2>&1 | grep \'^[[:blank:]]\\+/\'); "
		"do readlink -e ${curLine}; done";
	std::string scriptOutput;

	if (executeProcess(scriptText, scriptOutput) > 0)
	{
		std::istringstream inputStream(scriptOutput);
		std::string curPath;
		while (std::getline(inputStream, curPath, '\n'))
		{
			curPath.append(1, '/');
			pathsList.push_back(curPath);
		}
	}

	return (pathsList.size());
}

// public functions

size_t searchForFiles(const char* workingDir, bool recurseSubdirs, TStringVector& filesList)
{
	filesList.clear();

	if (workingDir != nullptr && *workingDir != 0)
	{
		bfs::path rootPath(workingDir);

		if (bfs::exists(rootPath) && bfs::is_directory(rootPath))
		{
			if (recurseSubdirs)
			{
				iterateDirectory<bfs::recursive_directory_iterator>(rootPath, filesList);
			}
			else
			{
				iterateDirectory<bfs::directory_iterator>(rootPath, filesList);
			}
			if (filesList.size() > 0)
			{
				std::sort(filesList.begin(), filesList.end());
			}
		}
	}

	return (filesList.size());
}

size_t searchForIncludes(const char* filePath, TStringVector& systemList, TStringVector& ownList)
{
	systemList.clear();
	ownList.clear();

	if (filePath != nullptr && *filePath != 0)
	{
		TStringVector pathsList;
		getSystemIncludePaths(pathsList);

		boost::regex regExpr("(#include\\s+)([<\"])(.*)([>\"])");
		boost::smatch matchResults;
		std::ifstream inputFile(filePath);
		std::string curLine;

		while (std::getline(inputFile, curLine))
		{
			if (boost::regex_match(curLine, matchResults, regExpr))
			{
				if (matchResults[2] == "<" && matchResults[4] == ">")
				{
					bool fileFound = false;
					for (auto& it: pathsList)
					{
						bfs::path curPath(it + matchResults[3]);
						if (bfs::exists(curPath) && bfs::is_regular_file(curPath))
						{
							fileFound = true;
							systemList.push_back(curPath.string());
							break;
						}
					}
					if (!fileFound)
					{
						systemList.push_back(matchResults[2] + matchResults[3] + matchResults[4]);
					}
				}
				else if (matchResults[2] == "\"" && matchResults[4] == "\"")
				{
					ownList.push_back(matchResults[3]);
				}
			}
		}
		if (systemList.size() > 0)
		{
			std::sort(systemList.begin(), systemList.end());
		}
		if (ownList.size() > 0)
		{
			std::sort(ownList.begin(), ownList.end());
		}
	}

	return (systemList.size() + ownList.size());
}
