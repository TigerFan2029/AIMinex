from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Function to collect all the image files and other static assets
def get_data_files():
    data_files = []
    
    # All image files in the images directory
    image_dirs = ['images/doc', 'images/favicons', 'images/icons']
    
    for directory in image_dirs:
        for root, dirs, files in os.walk(directory):
            for file in files:
                data_files.append(os.path.join(root, file).replace(os.path.sep, '/'))
    
    # All Excel data files
    for root, dirs, files in os.walk('data'):
        for file in files:
            if file.endswith('.xlsx'):
                data_files.append(os.path.join(root, file).replace(os.path.sep, '/'))
    
    return data_files

setup(
    name="AIMinex",
    version="1.0.0",
    description="AIMinex is an Open-Source, Cross-Platform GUI for Geochemical and Mineral Exploration Data Analysis and Visualization Using AI",
    author="Hom Nath Gharti & Tiger Fan",
    author_email="",
    license="GNU General Public License v3 (GPLv3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DigitalEarthScience/AIMinex",
    packages=find_packages(where='aiminex'),  # Find all packages inside the 'aiminex' directory
    include_package_data=True,  # Include non-Python files as specified below
    package_data={  
        '': get_data_files(),  # Include images, Excel files, and other static assets
        'aiminex': ['*.py'],   # Include Python files from the 'aiminex' folder
        'tktooltip': ['*.py'], # Include Python files from the 'tktooltip' folder
    },        
    
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
    
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    
    entry_points={
        'console_scripts': [
            'aiminex=main:main',
        ],
    },
)
