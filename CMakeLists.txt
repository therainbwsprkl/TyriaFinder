cmake_minimum_required(VERSION 3.16)
project(TyriaFinder CXX)

# Windows x64 DLL, loadable from <Guild Wars 2>/addons/ via Raidcore Nexus.
# Build on Linux with the MinGW cross toolchain:
#   cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=cmake/mingw-w64-x86_64.cmake
#   cmake --build build --config Release
# Or on Windows with MSVC (no toolchain file needed).
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(TyriaFinder SHARED
    src/entry.cpp
    third_party/imgui/imgui.cpp
    third_party/imgui/imgui_draw.cpp
    third_party/imgui/imgui_tables.cpp
    third_party/imgui/imgui_widgets.cpp
)

target_include_directories(TyriaFinder PRIVATE
    third_party
    third_party/imgui
    src
)

# Windows clipboard / Win32 APIs used by the addon.
if(WIN32)
    # user32: clipboard. (v1.5: winhttp was only for the v2.0 tile map,
    # removed — see archive/map_view-v2.0/.)
    target_link_libraries(TyriaFinder PRIVATE user32)
    # Static-link the MinGW runtimes: the DLL must load on a plain Windows
    # PC with no MinGW installed (no libgcc_s / libstdc++ DLLs alongside it).
    target_link_options(TyriaFinder PRIVATE -static-libgcc -static-libstdc++)
endif()

set_target_properties(TyriaFinder PROPERTIES
    OUTPUT_NAME "TyriaFinder"
    PREFIX ""
)
