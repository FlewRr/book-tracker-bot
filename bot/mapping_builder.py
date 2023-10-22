from lightfm import LightFM
from lightfm.data import Dataset as LFMDataset
import pandas as pd
import pickle
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from database.books_db import get_id, get_dict_for_ids
import os


PATH = "recs/data/"

def create_mappings(engine: Engine, database_name: str, book_storage_db: Session):
    df = pd.read_sql_table(table_name=database_name, con=engine.connect())

    os.system('rm -rf recs/data/') 
    os.system('mkdir recs/data')

    dict_for_ids = get_dict_for_ids(book_storage_db)
    df['book_id'] = df.book.apply(lambda x: dict_for_ids[x])

    lfm_dataset = LFMDataset()
    lfm_dataset.fit(
        users=df["user_id"].values,
        items=df["book_id"].values,
        user_features=df['rating'].values,
    )

    train_matrix, _ = lfm_dataset.build_interactions(zip(*df[["user_id", "book_id", "rating"]].values.T))

    lfm_model = LightFM(
        learning_rate=0.01, 
        loss='warp', 
        no_components=32,
        random_state=42
    )
    lfm_model.fit(
        interactions=train_matrix, 
        epochs=15,
        num_threads=20
    )

    user_vectors = lfm_model.user_embeddings
    item_vectors = lfm_model.item_embeddings
    item_id_mapping = {k: v for k, v in lfm_dataset._item_id_mapping.items()}
    user_id_mapping = lfm_dataset._user_id_mapping

    with open(PATH + 'user_vectors.pkl', 'wb') as outp:
        pickle.dump(user_vectors, outp, pickle.HIGHEST_PROTOCOL)
    with open(PATH + 'item_vectors.pkl', 'wb') as outp:
        pickle.dump(item_vectors, outp, pickle.HIGHEST_PROTOCOL)
    with open(PATH + 'item_id_mapping.pkl', 'wb') as outp:
        pickle.dump(item_id_mapping, outp, pickle.HIGHEST_PROTOCOL)
    with open(PATH + 'user_id_mapping.pkl', 'wb') as outp:
        pickle.dump(user_id_mapping, outp, pickle.HIGHEST_PROTOCOL)