import re

def clean_countries(countries_list,df_data):
    # we clean the list of countries and put them in a library

    print('Empezando a limpiar la lista de ciudades')

    countries = []

    for i in countries_list:
        sub1 = re.sub('\n', '', i)
        sub2 = re.sub(' ', '', sub1)

        try:
            if sub2[0] == '(':
                sub2 = sub2[1:3]
        except:
            continue

        countries.append(sub2)

    countries_dictionary = {}

    for i in range(1, 64, 2):
        countries_dictionary[f'{countries[i]}'] = countries[i - 1]

    countries_dictionary["GR"] = countries_dictionary["EL"]
    countries_dictionary["GB"] = countries_dictionary["UK"]
    countries_dictionary.update({'GB': 'United Kingdom'})

    del countries_dictionary["EL"]
    del countries_dictionary["UK"]

    df_data.rename(columns={'country_code': 'Country'}, inplace=True)

    row = 0
    for i in df_data['Country']:
        df_data.loc[row, 'Country'] = countries_dictionary[i]
        row += 1

    print('Finalización de limpiar la lista de ciudades.')
    return df_data


def choice_country(df_complete, country):
    # we choose all the countries ('All') or filter the DF by the specific country

    if country == 'All':
        return df_complete
    else:
        df_country = df_complete[df_complete['Country'] == f'{country}'].reset_index()
        df_country.drop(['index'], axis=1, inplace=True)
        return df_country


def clean_rural(df_data):
    # we clean the 'rural' column of the df.

    print('Empezando a limpiar la columna rural')

    df_data['rural'] = df_data['rural'].str.capitalize()
    df_data['rural'] = df_data['rural'].replace('City', 'Urban')
    df_data['rural'] = df_data['rural'].replace('Non-rural', 'Urban')
    df_data['rural'] = df_data['rural'].replace('Countryside', 'Rural')
    df_data['rural'] = df_data['rural'].replace('Country', 'Rural')

    df_data.rename(columns={'rural': 'Rural'}, inplace=True)

    print('Terminando de limpiar la columna rural')

    return df_data


def clean_jobs(df_data, titles_jobs):

    print('Empezando a limpiar la columna jobs')

    count = 0
    for i in df_data['normalized_job_code']:
        for j in titles_jobs:
            if (j.get('uuid') == i):
                df_data.loc[count, 'normalized_job_code'] = j.get('title')
        count += 1

    count2 = 0
    for i in df_data['normalized_job_code']:
        if i == None:
            df_data.loc[count2, 'normalized_job_code'] = 'Unemployed'
        count2 += 1

    df_data.rename(columns={'normalized_job_code': 'Job Title'}, inplace=True)


    print('Terminando de limpiar la columna jobs')

    return df_data


def wrangle(df_data_raw, countries_list, country, jobs_json):
    countries_clean = clean_countries(countries_list,df_data_raw)
    filter_country = choice_country(countries_clean, country)
    dat_clean_rural = clean_rural(filter_country)
    dat_clean = clean_jobs(dat_clean_rural, jobs_json)
    return dat_clean

