import os
from conans import tools, ConanFile
from conans import __version__ as conan_version
from conans.model.version import Version
from conans.tools import download, unzip

available_versions = ["5.0.0-alpha12",]

class Premake(ConanFile):
    name = "premake_installer"
    license = "https://github.com/premake/premake-core/raw/master/LICENSE.txt"
    url = "https://github.com/ulricheck/conan-premake_installer"
    if conan_version < Version("1.0.0"):
        settings = {"os": ["Windows", "Linux", "Macos"],
                    "arch": ["x86", "x86_64"]}
    else:
        settings = "os_build", "arch_build"
    options = {"version": available_versions}
    default_options = "version=" + available_versions[0]
    build_policy = "missing"

    @property
    def arch(self):
        return self.settings.get_safe("arch_build") or self.settings.get_safe("arch")

    @property
    def os(self):
        return self.settings.get_safe("os_build") or self.settings.get_safe("os")

    @property
    def premake_version(self):
        if "version" in self.options:
            return str(self.options.version)
        else:
            return self.version

    def build(self):
        archive = "premake.zip"
        download("https://github.com/premake/premake-core/releases/download/v%s/premake-%s-src.zip" % (self.premake_version, self.premake_version), archive)
        unzip(archive)
        os.unlink(archive)

        if self.settings.os_build == "Windows":
            os.chdir("premake-%s/build/gmake.windows" % self.premake_version)
            self.run("nmake")
            os.chdir("../..")

        elif self.settings.os_build == "Macos":
            os.chdir("premake-%s/build/gmake.macosx" % self.premake_version)
            self.run("make")

        elif self.settings.os_build == "Linux":
           os.chdir("premake-%s/build/gmake.unix" % self.premake_version)
           self.run("make")
           os.chdir("../..")

    def package(self):
        self.copy("premake*", dst="bin", src="premake-%s/bin/release" % self.premake_version)

    def package_info(self):
        if self.package_folder is not None:
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
            self.env_info.PREMAKE_ROOT = self.package_folder