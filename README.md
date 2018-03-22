## This repository holds a conan recipe to install premake as a build requirement.

[Conan.io](https://conan.io) package to install [premake](https://github.com/premake/premake-core)

## For Users: Use this package

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [build_requires]
    premake_installer/5.0.0-alpha12@camposs/stable

    [generators]
    premake


