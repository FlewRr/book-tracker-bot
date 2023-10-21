import pickle
from recs.recommender import AnnoyRecommender
from recs.config.config import recommender_conf, path_conf
from typing import Optional
import os

def load_object(path):
    with open(path, "rb") as fh:
        obj = pickle.load(fh)
    return obj

def read_vectors_and_mappings(
    user_vectors_path, item_vectors_path, user_map_path, item_map_path
):
    return (
        load_object(user_vectors_path),
        load_object(item_vectors_path),
        load_object(user_map_path),
        load_object(item_map_path),
    )


def build_annoy():
    user_vectors, item_vectors, user_mappings, item_mappings = read_vectors_and_mappings(**path_conf)

    ann = AnnoyRecommender(
        item_vectors=item_vectors,
        user_vectors=user_vectors,
        user_id_user_index_id_mapping=user_mappings,
        item_id_item_index_id_mapping=item_mappings,
        **recommender_conf
    )
    ann.fit()

    return ann

def get_recs_for_user(ann: AnnoyRecommender, user_id: int, whitelist : Optional[list]=[]):
    try:
        recommendations = ann.recommend_single_user(
            user_id, whitelist
        )
    except KeyError:
        raise Exception("Item or user not found")

    return recommendations
