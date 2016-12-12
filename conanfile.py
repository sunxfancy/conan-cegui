from conans import ConanFile
from conans.tools import get
from conans import CMake
from multiprocessing import cpu_count


class CeguiConan(ConanFile):
    name = "CEGUI"
    version = "0.8.7"
    folder = 'cegui-0.8.7'
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt"]
    # requires = 
    url="http://github.com/sixten-hilborn/conan-cegui"
    license="https://opensource.org/licenses/mit-license.php"

    def source(self):
        get("https://bitbucket.org/cegui/cegui/downloads/cegui-0.8.7.zip")

    def build(self):
        self.makedir('_build')
        cmake = CMake(self.settings)
        cd_build = 'cd _build'
        options = ''
        build_options = '-- -j{0}'.format(cpu_count()) if self.settings.compiler == 'gcc' else ''
        self.run_and_print('%s && cmake .. %s %s' % (cd_build, cmake.command_line, options))
        self.run_and_print("%s && cmake --build . %s %s" % (cd_build, cmake.build_config, build_options))

    def makedir(self, path):
        if self.settings.os == "Windows":
            self.run("IF not exist {0} mkdir {0}".format(path))
        else:
            self.run("mkdir {0}".format(path))

    def package(self):
        lib_dir = "_build/{0}/lib".format(self.folder)
        bin_dir = "_build/{0}/bin".format(self.folder)
        self.copy(pattern="*.h", dst="include/CEGUI", src="{0}/cegui/include/CEGUI".format(self.folder))
        self.copy("*.lib", dst="lib", src=lib_dir, keep_path=False)
        self.copy("*.a", dst="lib", src=lib_dir, keep_path=False)
        self.copy("*.so", dst="lib", src=lib_dir, keep_path=False)
        self.copy("*.dll", dst="bin", src=bin_dir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [
            'CEGUIBase-0',
            'CEGUIOpenGLRenderer-0'
        ]

        #if self.settings.os == "Windows":
        #    if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
        #        self.cpp_info.libs = [lib+'_d' for likb in self.cpp_info.libs]

    def run_and_print(self, command):
        self.output.warn(command)
        self.run(command)
