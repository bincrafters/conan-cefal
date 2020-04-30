from conans import ConanFile, tools, CMake
from conans.errors import ConanInvalidConfiguration
import os


class CefalConan(ConanFile):
    name = "cefal"
    description = "(Concepts-enabled) Functional Abstraction Layer for C++"
    topics = ("conan", "cefal", "monad")
    url = "https://github.com/bincrafters/conan-cefal"
    homepage = "https://github.com/dkormalev/cefal"
    license = "BSD-3-Clause"
    settings = "compiler", "os", "arch"
    no_copy_source = True

    _source_subfolder = "source_subfolder"

    def configure(self):
        minimal_cpp_standard = "20"
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, minimal_cpp_standard)
        minimal_version = {
            "gcc": "10",
            "clang": "10",
            "apple-clang": "10",
            "Visual Studio": "16"
        }
        compiler = str(self.settings.compiler)
        if compiler not in minimal_version:
            self.output.warn(
                "%s recipe lacks information about the %s compiler standard version support." % (self.name, compiler))
            self.output.warn(
                "%s requires a compiler that supports at least C++%s." % (self.name, minimal_cpp_standard))
            return
        version = tools.Version(self.settings.compiler.version)
        if version < minimal_version[compiler]:
            raise ConanInvalidConfiguration("%s requires a compiler that supports at least C++%s." % (self.name, minimal_cpp_standard))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib"))

    def package_id(self):
        self.info.header_only()
