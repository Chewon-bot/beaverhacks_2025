#Importing basic packages:
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from csv import DictWriter
from csv import DictReader


#import given dataset as :
kbeauty_100_korea = pd.read_csv('products.csv')
kbeauty_100_usa = pd.read_csv('soko_glam.csv')



plt.show()