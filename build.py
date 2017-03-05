from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(args="--build RapidJSON --build Boost --build OGRE")
    builder.add_common_builds(shared_option_name="CEGUI:shared", pure_c=False)
    builder.run()

