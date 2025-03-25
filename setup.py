from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import sys
import numpy
import os
import os.path as path
import multiprocessing

threads = multiprocessing.cpu_count()
force = False
profile = False

if "--force" in sys.argv:
    force = True
    del sys.argv[sys.argv.index("--force")]

if "--profile" in sys.argv:
    profile = True
    del sys.argv[sys.argv.index("--profile")]

compilation_includes = [".", numpy.get_include()]

setup_path = path.dirname(path.abspath(__file__))

# build extension list
extensions = []
for root, dirs, files in os.walk(setup_path):
    for file in files:
        if path.splitext(file)[1] == ".pyx":
            pyx_file = path.relpath(path.join(root, file), setup_path)
            module = path.splitext(pyx_file)[0].replace("/", ".")
            extensions.append(
                Extension(module, [pyx_file], include_dirs=compilation_includes),
            )

if profile:
    directives = {"profile": True}
else:
    directives = {}


setup(
    name="cherab-contrib",
    version="1.0.0",
    license="EUPL 1.1",
    description="Cherab spectroscopy framework: extra features",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    url="https://github.com/cherab",
    project_urls=dict(
        Tracker="https://github.com/cherab/experimental/issues",
    ),
    namespace_packages=["cherab"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["cherab>=1.4"],
    ext_modules=cythonize(
        extensions, nthreads=threads, force=force, compiler_directives=directives
    ),
)
