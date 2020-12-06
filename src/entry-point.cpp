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
	int exitCode = EXIT_SUCCESS;

	try
	{
		if (parseProgramOptions(argc, argv))
		{
			exitCode = createReport() ? EXIT_SUCCESS : EXIT_FAILURE;
		}
	}
	catch (const std::exception& err)
	{
		std::cerr << err.what() << std::endl;
		exitCode = EXIT_FAILURE;
	}

	return (exitCode);
}
