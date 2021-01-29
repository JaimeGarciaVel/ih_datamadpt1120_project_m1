import argparse
from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man 
from p_reporting import m_reporting as mre 

def argument_parser():
    countries_list = ['All', 'Belgium', 'Greece', 'Lithuania', 'Portugal', 'Bulgaria', 'Spain',
                      'Luxembourg', 'Romania', 'Czechia', 'France', 'Hungary', 'Slovenia', 'Denmark',
                      'Croatia', 'Malta', 'Slovakia', 'Germany', 'Italy', 'Netherlands', 'Finland',
                      'Estonia', 'Cyprus', 'Austria', 'Sweden', 'Ireland', 'Latvia', 'Poland',
                      'United Kingdom']

    parser = argparse.ArgumentParser(description='Set analysis type')

    parser.add_argument("-p", "--path", type=str, dest='path', required=True,
                        help="Indicate the path to the survey data file")
    parser.add_argument("-c", "--country", type=str, choices=countries_list, required=True, dest='country',
                        help="You must indicate a country to obtain your results")

    args = parser.parse_args()
    return args

def main(path, country):
    print('Empezando Pipeline:')

    df_data_raw = mac.db_data(path)
    jobs_json=mac.title_jobs_API(df_data_raw)
    countries_list=mac.get_countries()
    df_clean = mwr.wrangle(df_data_raw, countries_list, country, jobs_json)
    df_analyzed = man.analyze(df_clean)
    mre.save_df(df_analyzed, country)

    print(f'The results of the country -{country}- are: ')
    print(df_analyzed)

    print('Terminando Pipeline.')

if __name__ == '__main__':
    arguments = argument_parser()
    main(arguments.path, arguments.country)