// common-defs.h - common definitions
// written by Elijah Zarezky

#if !defined(__common_defs_h)
#define __common_defs_h

// STL headers
#include <set>
#include <string>
#include <vector>

// shortcuts
typedef std::set<std::string> TStringSet;
typedef std::vector<std::string> TStringVector;

// program-options.cpp
extern std::string workingDir;
extern bool recurseSubdirs;
extern std::string cppExtensions;

// program-options.cpp
extern bool parseProgramOptions(int argc, char* argv[]);

// filesystem-tasks.cpp
extern size_t searchForFiles(const char* workingDir, bool recurseSubdirs, TStringVector& filesList);
extern size_t searchForIncludes(const char* filePath, TStringVector& systemList, TStringVector& ownList);

#endif   // __common_defs_h
