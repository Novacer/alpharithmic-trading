# Zipline API
from zipline.api import attach_pipeline, pipeline_output
from zipline.pipeline import Pipeline
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.factors import AverageDollarVolume

# Math
import numpy as np
import pandas as pd
from scipy import optimize
from scipy import stats
import statsmodels.api as sm

# Machine Learning
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Data structures
from collections import deque
