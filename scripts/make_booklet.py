import argparse
from dataclasses import dataclass, field
import pandas as pd
import os

@dataclass
class ResponseData:
    path: str
    df: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.df = pd.read_excel(self.path, engine='openpyxl')
        self._check_df()

    def _check_df(self):
        columns = ['name', 'fmt', 'title', 'abstract', 'authors', 'department', 'lab']
        if not all(col in self.df.columns for col in columns):
            raise ValueError('Columns missing from dataframe')

def clean_text_for_tex(text):
    text = text.replace("%", "\\%")
    text = text.replace("&", "\\&")
    return text

def create_abstract_entry(title, authors, lab, dpt, abstract):
    return f'\\dosabstract{{{title}}}{{{authors}}}{{{lab}, Dpt. {dpt}}}{{{abstract}}}'

def create_abstract_texfile(response_data: ResponseData, pres_fmt, output_dir) -> None:
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{pres_fmt}s.tex')
    entries = response_data.df.itertuples()
    with open(output_file, 'w') as f:
        for entry in entries:
            if entry.fmt == pres_fmt:
                title = clean_text_for_tex(entry.title if not pd.isna(entry.title) else '<Title missing>')
                authors = clean_text_for_tex(entry.authors if not pd.isna(entry.authors) else entry.name)
                abstract = clean_text_for_tex(entry.abstract if not pd.isna(entry.abstract) else '<Abstract missing>')
                lab = clean_text_for_tex(entry.lab if not pd.isna(entry.lab) else '<Lab missing>')
                dpt = clean_text_for_tex(entry.department if not pd.isna(entry.department) else '<Dpt missing>')
                dosabstract = create_abstract_entry(title, authors, lab, dpt, abstract)
                f.write(f'{dosabstract}\n')

def main():
    parser = argparse.ArgumentParser(description='Generate LaTeX abstract booklet entries from Excel data.')
    parser.add_argument('input_file', help='Path to the input Excel file')
    parser.add_argument('output_dir', help='Directory to save the output LaTeX files')
    args = parser.parse_args()

    try:
        data = ResponseData(args.input_file)
        for pres_fmt in ['talk', 'poster']:
            create_abstract_texfile(data, pres_fmt, args.output_dir)
        print(f"Abstract booklet entries generated in {args.output_dir}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
