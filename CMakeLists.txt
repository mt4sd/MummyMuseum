cmake_minimum_required(VERSION 3.5)

project(MummyMuseum)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/MummyMuseum")
set(EXTENSION_CATEGORY "Museum")
set(EXTENSION_CONTRIBUTORS "CarlosLuque (ULPGC), Guillermo Socorro (ULPGC),  Nayra Carrera (ULPGC)")
set(EXTENSION_DESCRIPTION "The first interface for mummy Museum")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/MummyMuseum.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/MummyMuseum/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(MummyInterface)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
