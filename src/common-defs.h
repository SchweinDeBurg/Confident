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
extern std::string includeDirs;
extern std::string outputDir;

// program-options.cpp
extern bool parseProgramOptions(int argc, char* argv[]);

// filesystem-tasks.cpp
extern bool createReport(void);

#endif   // __common_defs_h
