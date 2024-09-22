from setuptools import setup, find_packages

with open("_build/html/index.html", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="MinexAI",
    version="0.0.1",
    description="MinexAI is a Graphing and Machine Learning Program designed to handle elemental data",    
    packages=find_packages('src'),
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/html",
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
        'numpy',
        'matplotlib',
        'pandas',
        'scikit-learn',
        'Pillow',
        'opencv-python',
        'customtkinter',
        'seaborn',
        'yellowbrick',
        'openpyxl',
        'Pillow',
        'typing_extensions',
        'pyttk',
        'thread6',
        'tkscrolledframe',
    ],
    entry_points={
        'console_scripts': [
            'minexai=main_program.minexai:main',
        ],
    },
)
