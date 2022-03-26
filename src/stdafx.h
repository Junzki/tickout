#pragma once
#pragma warning(push)
#pragma warning(disable : 4820)
#pragma warning(disable : 4619)
#pragma warning(disable : 4548)
#pragma warning(disable : 4668)
#pragma warning(disable : 4365)
#pragma warning(disable : 4710)
#pragma warning(disable : 4371)
#pragma warning(disable : 4826)
#pragma warning(disable : 4061)
#pragma warning(disable : 4640)

#ifndef TICKOUT_STDAFX_H
#define TICKOUT_STDAFX_H

#include <iostream>
#include <string>
#include <fstream>
#include <sstream>


#ifdef _WIN32
#include <Windows.h>
#include <Shlwapi.h>
#endif

#include <nlohmann/json.hpp>

// cURLpp
#include "curlpp/cURLpp.hpp"
#include "curlpp/Easy.hpp"
#include "curlpp/Options.hpp"
#include <curlpp/Infos.hpp>


#endif  // TICKOUT_STDAFX_H



#pragma warning(pop)
