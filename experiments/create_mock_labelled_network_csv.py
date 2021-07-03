import os

import pandas as pd
import numpy as np

from be.configuration import data_folder

# load the medium graph and substitute some node addresses with addresses present in the label list.
# This is done because otherwise no node in the medium graph would match a node in the label list.
MEDIUM_GRAPH_RAW_PATH = os.path.join(data_folder, 'medium.csv')
LABELS_PATH = os.path.join(data_folder, 'labels.csv')

raw = pd.read_csv(MEDIUM_GRAPH_RAW_PATH, dtype={'amount': object})
labels = pd.read_csv(LABELS_PATH)

column_values = raw[["source", "target"]].values.ravel()
unique_values_graph = pd.unique(column_values)

column_values = labels[["address"]].values.ravel()
unique_values_labels = pd.unique(column_values)

choice_g = np.random.choice(unique_values_graph, size=100, replace=False)
choice_l = np.random.choice(unique_values_labels, size=100, replace=False)
i = dict(zip(choice_g, choice_l))

data = raw.replace(i)
data = data.drop(columns=['eventName', 'blockNumber'])
data.to_csv('mock_net_labelled.csv', index=False)
