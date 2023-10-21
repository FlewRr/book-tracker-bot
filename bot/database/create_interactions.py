import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

interactions_engine = create_engine("sqlite:///database.db")

def create_interactions_db():
    df_interactions = pd.read_csv("database/books_data/data.csv", index_col=False)

    l = df_interactions.id.size
    df_interactions['label'] = [1 for j in range(l)]
    df_interactions = df_interactions.rename(columns={'id': 'user_id', 'title': 'book'})
    df_interactions['id'] = [i for i in range(l)]
    df_interactions = df_interactions[['id', 'user_id', 'book', 'label', 'rating']]

    df_interactions.to_sql('books', interactions_engine, if_exists='replace')
