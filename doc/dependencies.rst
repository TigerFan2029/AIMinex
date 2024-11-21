Dependencies
============
MineralAI uses prebuilt functions and libraries from:

import customtkinter
import tkinter
from tkinter import ttk, scrolledtext, IntVar, Menu
from tkinter import *
from tkinter import filedialog as fd
from customtkinter import CTkImage

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import MouseButton
from matplotlib.lines import Line2D

from sklearn.decomposition import PCA, KernelPCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import AgglomerativeClustering, DBSCAN, SpectralClustering, MeanShift, AffinityPropagation, AgglomerativeClustering, Birch
from sklearn.mixture import GaussianMixture
from yellowbrick.cluster import KElbowVisualizer  

import re
from PIL import Image, ImageTk
from tktooltip import ToolTip
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import webbrowser

import threading
import code
import sys

from typing import Union, Callable