// filesystem-tasks.cpp - filesystem specific routines
// written by Elijah Zarezky

 // STL headers
#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>

// Boost headers
#include <boost/filesystem.hpp>

// our headers
#include "common-defs.h"

// shortcuts
namespace bfs = boost::filesystem;

// impementation helpers

static size_t initExtensions(const char* cppExtensions, TStringSet& extensionsSet)
{
	extensionsSet.clear();

	if (cppExtensions != NULL && *cppExtensions != 0)
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

// public functions

size_t searchForFiles(const char* workingDir, bool recurseSubdirs, TStringVector& filesList)
{
	filesList.clear();

	if (workingDir != NULL && *workingDir != 0)
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

