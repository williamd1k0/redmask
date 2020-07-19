from setuptools import setup

VERSION = "1.1.0"

options = dict(
    name="redmask",
    version=VERSION,
    description="A simple tool to create palette swap mask",
    keywords=["palette", "gimp", "krita", "shaders"],
    author="William Tumeo",
    author_email="pypi@tumeo.space",
    url="https://github.com/williamd1k0/redmask",
    download_url="https://github.com/williamd1k0/redmask/archive/v%s.tar.gz" % VERSION,
    packages=["redmask"],
    entry_points={'console_scripts': ['redmask = redmask:dist_main']},
    install_requires=['pillow >= 5.0.0'],
    classifiers=[
        "Topic :: Utilities",
        "Topic :: Multimedia :: Graphics",
        "Environment :: Console",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Operating System :: Microsoft :: Windows :: Windows Vista",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License"
    ],
    package_data={"": ["LICENSE", "README.md"]},
    long_description_content_type="text/markdown",
    long_description=open("README.md").read()
)

setup(**options)