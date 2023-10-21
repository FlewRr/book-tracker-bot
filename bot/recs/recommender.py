from __future__ import annotations

from itertools import islice
from typing import Callable, Dict, Hashable, Literal, Sequence, Tuple

import numpy as np
from annoy import AnnoyIndex
from numpy.typing import NDArray

class AnnoyRecommender:
    def __init__(
            self,
            item_vectors: NDArray[np.float32],
            user_vectors: NDArray[np.float32],
            user_id_user_index_id_mapping: Dict[Hashable, int],
            item_id_item_index_id_mapping: Dict[Hashable, int],
            top_k: int,
            dim: int,
            metric: Literal['angular', 'euclidian', 'manhattan', 'hamming', 'dot'] = 'dot',
            n_trees: int = 10,
            n_jobs: int = -1,
            search_k: int = -1,
            n_neighbors: int = 500
    ):
        self.item_vectors = item_vectors
        self.user_vectors = user_vectors
        self.user_to_num = user_id_user_index_id_mapping
        self.item_to_num = item_id_item_index_id_mapping
        self.num_to_user = {v: k for k, v in user_id_user_index_id_mapping.items()}
        self.num_to_item = {v: k for k, v in item_id_item_index_id_mapping.items()}
        self.top_k = top_k
        self.dim = dim
        self.metric = metric
        self.n_trees = n_trees
        self.n_jobs = n_jobs
        self.search_k = search_k
        self.n_neighbors = n_neighbors


    def fit(self) -> AnnoyRecommender:
        self._build()
        return self

    def _build(self) -> None:
        index = AnnoyIndex(f=self.dim, metric=self.metric)
        for idx, vector in enumerate(self.item_vectors):
            index.add_item(idx, vector)
        index.build(n_trees=self.n_trees, n_jobs=self.n_jobs)
        self.index = index

    def recommend_single_user(
            self, user_id : Hashable, item_whitelist: Sequence[Hashable]
    ) -> Sequence[Hashable]:
        id, item_ids = self.user_to_num[user_id], [
            self.item_to_num[item] for item in item_whitelist
        ]

        user_vector = self.user_vectors[id]

        if len(item_whitelist) == 0:
            item_ids = list(self.item_to_num.values())

        closest = self._get_similar(user_vector=user_vector)
        closest = self._get_filtered_top(
            candidates=closest, allowed_items=item_ids
        )

        recs = [self.num_to_item[item] for item in closest]
        
        return recs
    
    def _get_similar(
            self, user_vector: NDArray[np.float32]
        ) -> Sequence[int]:
        nearest_neighbours = self.index.get_nns_by_vector(
            user_vector, 
            self.n_neighbors,
            self.search_k,
            include_distances=False,
        )

        return nearest_neighbours

    def _get_filtered_top(
            self, candidates: Sequence[int], allowed_items: Sequence[int]
        ) -> Sequence[int]:
            allowed_items_set = set(allowed_items)
            return list(
                islice(
                    (cand for cand in candidates if cand in allowed_items_set), self.top_k
                )
            )
