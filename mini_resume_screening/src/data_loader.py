import pandas as pd

IMPORTANT_COLUMNS = [
    "skills",
    "related_skils_in_job",
    "positions",
    "responsibilities",
    "major_field_of_studies",
    "degree_names",
    "job_position_name"
]

def load_resume_data(path: str):
    df = pd.read_csv(path)

    # Drop rows where target label is missing
    df = df.dropna(subset=["job_position_name"])

    # Fill remaining NaNs with empty string (for text columns)
    df[IMPORTANT_COLUMNS] = df[IMPORTANT_COLUMNS].fillna("")

    return df
