import platform

from conan.packager import ConanMultiPackager

available_versions = ["5.0.0-alpha12",]

if __name__ == "__main__":

    builder = ConanMultiPackager()

    for version in available_versions:
        builder.add({}, {}, {}, {}, reference="cmake_installer/%s" % version)

    builder.run()