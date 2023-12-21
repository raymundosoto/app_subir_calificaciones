import pandas as pd

def process_excel_file(file):
    df = pd.read_excel(file)
    return df.values.tolist()
