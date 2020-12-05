// entry-point.cpp - application entry point
// written by Elijah Zarezky

// GNU libc headers
#include <stdlib.h>

// STL headers
#include <exception>

// entry point itself
int main(int argc, char* argv[])
{
	int result = EXIT_SUCCESS;

	try
	{
	}
	catch (const std::exception& err)
	{
		result = EXIT_FAILURE;
	}

	return (result);
}
