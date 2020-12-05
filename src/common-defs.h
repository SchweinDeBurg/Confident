// common-defs.h - common definitions
// written by Elijah Zarezky

#if !defined(__common_defs_h)
#define __common_defs_h

// program-options.cpp
extern std::string workingDir;
extern bool recurseSubdirs;

// program-options.cpp
extern bool parseProgramOptions(int argc, char* argv[]);

#endif   // __common_defs_h
