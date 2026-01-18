import re

def clean_text(text: str) -> str:
    text = str(text).lower()

    #remove emails
    text = re.sub(r'\S+@\S+', ' ',text)


    #remove phone numbers
    text = re.sub(r'\+?\d[\d -]{8,}\d', ' ',text)

    # Remove URLs
    text = re.sub(r'http\S+', ' ',text)

    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', ' ',text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ',text).strip()

    return text