from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy
import os

class SevenZipCppConan(ConanFile):
    name = "7zip-cpp"
    license = "MIT"
    url = "https://github.com/systelab/7zip-cpp"
    description = "C++ wrapper for accessing the 7-zip COM-like API in 7z.dll and 7za.dll"
    topics = ("sevenzip")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    exports_sources = "7zip-cpp/*"

    header_list = [
        "7zpp.h",
        "CompressionFormat.h",
        "CompressionLevel.h",
        "Enum.h",
        "FileInfo.h",
        "ListCallback.h",
        "ProgressCallback.h",
        "SevenString.h",
        "SevenZipArchive.h",
        "SevenZipCompressor.h",
        "SevenZipException.h",
        "SevenZipExtractor.h",
        "SevenZipLibrary.h",
        "SevenZipLister.h"
    ]

    def layout(self):
        cmake_layout(self, src_folder="../")
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        include_dst = os.path.join(self.package_folder, "include", "7zip-cpp")
        include_src = os.path.join(self.source_folder, "7zpp")

        for h in self.header_list:
            copy(self, h, src=include_src, dst=include_dst)

        lib_src = os.path.join(self.build_folder, str(self.settings.build_type))
        lib_dst = os.path.join(self.package_folder, "lib")
        copy(self, "7z*.lib", src=lib_src, dst=lib_dst, keep_path=False)

        bin_dst = os.path.join(self.package_folder, "bin")
        copy(self, "7z*.pdb", src=lib_src, dst=bin_dst, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["7zpp"]