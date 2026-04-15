import pandas as pd
from preprocess import clean_email_content

if __name__ == '__main__':
    df = pd.read_csv('DATASETS/SpamAssassin/SA.csv')
    df['processed_text'] = df['data'].apply(clean_email_content)
    df.to_csv('DATASETS/SA_preprocessed.csv', index=False)
    print("Preprocessing Completed")