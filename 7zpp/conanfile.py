from conans import ConanFile, CMake
import os

class SevenZipCpp(ConanFile):
    name = "7zip-cpp"
    license = "MIT"
    url = "https://github.com/systelab/7zip-cpp"
    description = "C++ wrapper for accessing the 7-zip COM-like API in 7z.dll and 7za.dll"
    topics = ("sevenzip")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
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

    def source(self):
        self.run("git clone https://github.com/systelab/7zip-cpp.git 7zip-cpp --recursive")
        
    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="7zip-cpp")
        cmake.build()
        
        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        for h in self.header_list:
            self.copy(h, dst="include/7zip-cpp", src=".")
        self.copy("7z*.lib", dst="lib", src=os.environ["CONAN_LIB_DIR"], keep_path=False)
        self.copy("7z*.pdb", dst="bin", src=os.environ["CONAN_LIB_DIR"], keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["7zpp"]

