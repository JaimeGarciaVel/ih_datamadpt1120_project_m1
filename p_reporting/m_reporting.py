import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
import re

def save_df(df_data, country):

    df_data.to_csv(f'./data/data_project_m1_{country}.csv', index=False, sep=',')
    print(f'df guardado en la carpeta data con nombre data_project_m1_{country}.csv')