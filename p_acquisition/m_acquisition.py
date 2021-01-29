import pandas as pd
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup


def db_engine(query, path):
    # connection database
    conn_str = f'sqlite:///{path}'
    engine = create_engine(conn_str)
    data = pd.read_sql_query(query, engine)
    return data

def db_data(path):
    print('Comienzo de la adquisición de los datos de la database raw_data_project_m1.db')
    query = """
                SELECT country_info.country_code,
                career_info.normalized_job_code,
                country_info.rural,
                country_info.uuid
                FROM poll_info 
                JOIN career_info ON poll_info.uuid = career_info.uuid 
                JOIN country_info ON poll_info.uuid = country_info.uuid"""
    df_raw_data = db_engine(query, path)
    print('Finalización de la adquisición de los datos de la database raw_data_project_m1.db')
    return df_raw_data

def title_jobs_API(data):
    # API

    print('Comienzo de la adquisición de los datos de la API')
    jobs = data['normalized_job_code'].unique()

    json_data = []
    for i in jobs:
        response = requests.get(f'http://api.dataatwork.org/v1/jobs/{i}')
        json_data.append(response.json())
    print('Finalización de la adquisición de los datos de la API.')
    return json_data

def get_countries():
    # Web scraping

    print('Comienzo de la adquisición de los datos de la web site...')

    url = 'https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('td')

    countries_list=[]

    for i in table:
        countries_list.append(i.text)

    print('Finalización de la adquisición de los datos de la web site.')
    return countries_list