import pandas as pd

def load_resume_data(path: str):
    """
    Loads resume dataset and performs basic cleaning.
    """
    df = pd.read_csv(path)
    df.dropna(inplace=True)
    return df
