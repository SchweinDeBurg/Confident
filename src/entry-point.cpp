// entry-point.cpp - application entry point
// written by Elijah Zarezky

// GNU libc headers
#include <stdlib.h>

// STL headers
#include <exception>
#include <iostream>
#include <string>

// our headers
#include "common-defs.h"

// entry point itself
int main(int argc, char* argv[])
{
	int result = EXIT_SUCCESS;

	try
	{
		if (parseProgramOptions(argc, argv))
		{
			TStringVector filesList;
			if (searchForFiles(workingDir.c_str(), recurseSubdirs, filesList))
			{
				for (auto& it: filesList)
				{
					std::cout << it << std::endl;
				}
			}
		}
		else
		{
			result = EXIT_FAILURE;
		}
	}
	catch (const std::exception& err)
	{
		std::cerr << err.what() << std::endl;
		result = EXIT_FAILURE;
	}

	return (result);
}
