import argparse
import configparser
import re

import pandas as pd

def parse_formats(s):
    s = s.fillna('').str.lower()
    
    def _encode_formats(a):
        if 'poster' in a:
            return 'poster'
        elif 'talk' in a:
            return 'talk'
        else:
            return ''
    
    return s.apply(_encode_formats)

def read_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    switch_to_poster = config.get('Settings', 'switch_to_poster').split(', ')

    return switch_to_poster

def process_responses(input_file, output_file, config_file):
    colnames = ['', 'fmt', 'title', 'abstract', 'authors', '', '', '', 'name', '', '']
    keep = ['name', 'fmt', 'title', 'abstract', 'authors']

    try:
        data = pd.read_excel(input_file, engine='openpyxl', names=colnames).filter(keep)
    except Exception as e:
        print(f'Error reading file: {e}')
        return

    data = data.assign(fmt=lambda df: parse_formats(df['fmt']))
    data = data.dropna(subset=['name'])
    data = data.query("name != 'test if there is a confirmation link'")
    data = data.drop_duplicates(subset=['name'])

    # Switch the following talk presenters to poster
    switch_to_poster = read_config(config_file)
    data = pd.concat([
        data[data['name'].isin(switch_to_poster)].assign(fmt='poster'),
        data[~data['name'].isin(switch_to_poster)]
    ])
    
    # Misc cleaning
    data['abstract'] = data['abstract'].fillna('').apply(lambda x: re.sub(r'\n', ' ', x))
    data = data[data['name'] != 'Aydan Bulut-Karslıoğlu ']
    data = pd.concat([
        data[data['name'].str.contains('second registration')].assign(name='Alexandra Martitz'),
        data[~data['name'].str.contains('Alexandra Martitz')]
    ])
    data = pd.concat([
        data[data['name'].str.contains('moelling@molgen.mpg.de')].assign(name='Karin Moelling'),
        data[~data['name'].str.contains('Karin Moelling')]
    ])
    data = data.query("title != 'I will present 5 min on our lab'")

    data = data.sort_values(by=['name', 'fmt'])

    # Add new columns for department and lab
    data = data.assign(department='', lab='')

    try:
        data.to_csv(output_file, index=False)
        print(f'Data successfully written to {output_file}')
    except Exception as e:
        print(f'Error writing file: {e}')

def main():
    parser = argparse.ArgumentParser(description='Process registration data for booklet.')
    parser.add_argument('input_file', help='Input Excel file path')
    parser.add_argument('output_file', help='Output CSV file path')
    parser.add_argument('config_file', help='Config file path')
    args = parser.parse_args()

    process_responses(args.input_file, args.output_file, args.config_file)

if __name__ == '__main__':
    main()
