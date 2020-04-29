from conans import ConanFile, tools, CMake
import os


class CefalConan(ConanFile):
    name = "cefal"
    description = "(Concepts-enabled) Functional Abstraction Layer for C++"
    topics = ("conan", "cefal", "monad")
    url = "https://github.com/bincrafters/conan-cefal"
    homepage = "https://github.com/dkormalev/cefal"
    license = "BSD-3-Clause"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    no_copy_source = True

    _source_subfolder = "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.install()
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)

    def package_id(self):
        self.info.header_only()
