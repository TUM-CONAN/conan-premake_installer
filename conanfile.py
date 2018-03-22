import os
from conans import tools, ConanFile
from conans import __version__ as conan_version
from conans.model.version import Version
from conans.tools import download, unzip, untargz

available_versions = ["5.0.0-alpha12",]

class Premake(ConanFile):
    name = "premake_installer"
    license = "https://github.com/premake/premake-core/raw/master/LICENSE.txt"
    url = "https://github.com/ulricheck/conan-premake_installer"
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
        self.output.warn("Fetching binaries for platform: %s" % self.settings.os_build)
        archive = "premake.zip"
        osname = {
            "Windows":"windows",
            "Linux": "linux",
            "Macos": "macosx",
        }[str(self.settings.os_build)]
        suffix = ".zip" if self.settings.os_build == "Windows" else ".tar.gz"
        download("https://github.com/premake/premake-core/releases/download/v%s/premake-%s-%s%s" % (self.premake_version, self.premake_version, osname, suffix), archive)
        if suffix == ".zip":
            unzip(archive)
        else:
            untargz(archive)
        os.unlink(archive)

    def package(self):
        self.copy("premake*", dst="bin")

    def package_info(self):
        if self.package_folder is not None:
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
            self.env_info.PREMAKE_ROOT = self.package_folder