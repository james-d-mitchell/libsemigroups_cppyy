"""
A minimal cppyy wrapper for the libsemigroups C++ library.
"""
from setuptools import find_packages, setup

setup(
    name="libsemigroups_cppyy",
    version="0.0.1",
    description="A minimal cppyy wrapper for the libsemigroups C++ library",
    url="http://github.com/libsemigroups/libsemigroups_cppyy",
    author="James D. Mitchell, Nicolas Thiéry",
    author_email="jdm3@st-andrews.ac.uk, Nicolas.Thiery@u-psud.fr",
    license="GPL3",
    install_requires=["cppyy", "networkx", "pkgconfig", "packaging"],
    packages=find_packages(exclude=["tests"]),
    tests_require=["tox"],
    zip_safe=False,
    include_package_data=True,
)
