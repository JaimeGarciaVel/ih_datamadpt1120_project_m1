
def quantity_job(df_data):

    print('Empezando a agrupar por trabajo, país y zona de residencia')

    df_quantity = df_data.groupby(['Country', 'Job Title', "Rural"])["uuid"].count().reset_index().rename(
        columns={'uuid': 'Quantity'})

    print('Terminando el groupby.')
    return df_quantity


def percentage_job(df_data):

    print('Empezando el porcentaje de quantity respecto del global')

    df_data['Percentage'] = (df_data['Quantity'] / df_data['Quantity'].sum()) * 100
    df_data["Percentage"] = df_data["Percentage"].round(2).astype(str) + '%'

    print('Terminando el porcentaje de quantity respecto del global')
    return df_data


def analyze(df):
    dat_quantity = quantity_job(df)
    df_final= percentage_job(dat_quantity)

    return df_final