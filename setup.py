from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="AIMinex",
    version="1.0.0",
    description="AIMinex is a Graphing and Machine Learning Program designed to handle elemental data",
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    include_package_data=True,
    package_data={
        'aiminex': [
            'images/*.*',
            '_build/*.*',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Hom Nath Gharti & Tiger Fan",
    author_email="",
    license="GNU GENERAL PUBLIC LICENSE",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        'numpy>=1.23.0',
        'matplotlib',
        'pandas',
        'scikit-learn',
        'Pillow',
        'opencv-python',
        'customtkinter',
        'seaborn',
        'yellowbrick',
        'openpyxl',
        'typing_extensions',
        'tkscrolledframe',
        'tkinter-tooltip',
    ],
    entry_points={
        'console_scripts': [
            'aiminex=aiminex.aiminex:main',
        ],
    },
)
