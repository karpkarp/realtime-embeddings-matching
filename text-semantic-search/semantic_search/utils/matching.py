#!/usr/bin/python
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from annoy import AnnoyIndex
import numpy as np
import logging
import pickle

VECTOR_LENGTH = 512


class MatchingUtil:

  def __init__(self, index_file):
    print('Initialising matching utility...')
    self.index = AnnoyIndex(VECTOR_LENGTH)
    self.index.load(index_file, prefault=True)
    print('Annoy index {} is loaded'.format(index_file))
    with open(index_file + '.mapping', 'rb') as handle:
      self.mapping = pickle.load(handle)
    print('Mapping file {} is loaded'.format(index_file + '.mapping'))
    print('Matching utility initialised.')

  def find_similar_items(self, vector, num_matches):
    item_ids = self.index.get_nns_by_vector(
      vector, num_matches, search_k=-1, include_distances=False)
    print("MATCHING -1", item_ids)
    
    print("MATCHING 10",self.index.get_nns_by_vector(
      vector, num_matches, search_k=10, include_distances=False) )

    print("MATCHING 100",self.index.get_nns_by_vector(
      vector, num_matches, search_k=100, include_distances=False) )

    print("MATCHING 1000",self.index.get_nns_by_vector(
          vector, num_matches, search_k=1000, include_distances=False) )

    print("MATCHING 10000",self.index.get_nns_by_vector(
              vector, num_matches, search_k=10000, include_distances=False) )


    identifiers = [self.mapping[item_id]
                   for item_id in item_ids]
    return identifiers

  def find_similar_vectors(self, vector, num_matches):
    items = self.find_similar_items(vector, num_matches)
    vectors = [np.array(self.index.get_item_vector(item))
               for item in items]
    return vectors


