"""This module contains a template MindMeld app configuration"""

# Dictionaries for the various NLP classifier configurations

#####################
### DOMAIN CONFIG ###
#####################
### GRIDSEARCH MODEL ###
DOMAIN_CLASSIFIER_CONFIG = {
    'model_type': 'text',
    'model_settings': { 'classifier_type': 'rforest' },
    'param_selection': {
        'grid': {
            'n_estimators': [100],
            'criterion': ['gini'],
            'max_depth': [20],
            'min_samples_split': [2],
            'min_samples_leaf': [1],
            'max_features': ['sqrt'],
            'bootstrap': [True],
        },
        'k': 5,
        'type': 'shuffle'
    },
    'features': {
        "bag-of-words": {
            "lengths": [1, 2],
            "thresholds": [1, 2]
        },
        "freq": {"bins": 5},
        'enable-stemming': False,
        "in-gaz": {},
        "gaz-freq": {},
    },
}

### GRIDSEARCH MODEL ###
INTENT_CLASSIFIER_CONFIG = {
    'model_type': 'text',
    'model_settings': { 'classifier_type': 'rforest' },
    'param_selection': {
        'grid': {
            'n_estimators': [100],
            'criterion': ['gini'],
            'max_depth': [20],
            'min_samples_split': [2],
            'min_samples_leaf': [1],
            'max_features': ['sqrt'],
            'bootstrap': [True],
        },
        'k': 5,
        'type': 'shuffle'
    },
    'features': {
        "bag-of-words": {
            "lengths": [1, 2],
            "thresholds": [1, 2]
        },
        "freq": {"bins": 5},
        'enable-stemming': False,
        "in-gaz": {},
        "gaz-freq": {},
    },
}

#####################
### ENTITY CONFIG ###
#####################
# MEMM
# ENTITY_RECOGNIZER_CONFIG = {
#     'model_type': 'tagger',
#     'model_settings': {
#         'classifier_type': 'memm',
#         'tag_scheme': 'IOBES',
#         'feature_scaler': 'max-abs'
#     },
#     'param_selection': {
#         'type': 'k-fold',
#         'k': 5,
#         'scoring': 'accuracy',
#         'grid': {
#             'penalty': ['l1', 'l2'],
#             'C': [0.01, 1, 100, 10000]
#         },
#     },
#     'features': {
#         'bag-of-words-seq': {
#             'ngram_lengths_to_start_positions': {
#                 1: [-2, -1, 0, 1, 2],
#                 2: [-1, 0, 1]
#             }
#         },
#         'in-gaz-span-seq': {},
#         'sys-candidates-seq': {
#           'start_positions': [-1, 0, 1]
#         }
#     }
# }

# LSTM
# ENTITY_RECOGNIZER_CONFIG = {
#  'model_type': 'tagger',
#     'model_settings': {
#         'classifier_type': 'lstm-pytorch',
#         'tag_scheme': 'IOBES'
#     },
#     'params': {
#      'embedder_type': 'glove',
#      'use_crf_layer': True,
#      'lstm_hidden_dim': 128,
#      'lstm_bidirectional': True,
#      'char_emb_dim': 32
#  }
# }

# CNN-LSTM
# ENTITY_RECOGNIZER_CONFIG = {
#  'model_type': 'tagger',
#     'model_settings': {
#         'classifier_type': 'cnn-lstm',
#         'tag_scheme': 'IOBES'
#     },
#     'params': {
#      'embedder_type': 'glove',
#      'use_crf_layer': True,
#      'lstm_hidden_dim': 128,
#      'lstm_bidirectional': True,
#      'char_emb_dim': 32
#  }
# }

# LSTM-LSTM
# ENTITY_RECOGNIZER_CONFIG = {
#  'model_type': 'tagger',
#     'model_settings': {
#         'classifier_type': 'lstm-lstm',
#         'tag_scheme': 'IOBES'
#     },
#     'params': {
#      'embedder_type': 'glove',
#      'use_crf_layer': True,
#      'lstm_hidden_dim': 128,
#      'lstm_bidirectional': True,
#      'char_emb_dim': 32
#  }
# }

# BERT
# ENTITY_RECOGNIZER_CONFIG = {
#  'model_type': 'tagger',
#     'model_settings': {
#         'classifier_type': 'embedder',
#         'tag_scheme': 'IOBES'
#     },
#     'params': {
#         'embedder_type': 'bert',
#         'pretrained_model_name_or_path': 'bert-base-cased',
#         'use_crf_layer': True,
#         'emb_dim': 256,
#         'number_of_epochs': 5,
#         'patience': 3,
#         'batch_size': 8,
#         'device': 'cpu'
#     }
# }

TEXT_PREPARATION_CONFIG = {
    "preprocessors": [],
    "tokenizer": "WhiteSpaceTokenizer",
    "normalizers": [
        'RemoveAposAtEndOfPossesiveForm',
        'RemoveAdjacentAposAndSpace',
        'RemoveBeginningSpace',
        'RemoveTrailingSpace',
        'ReplaceSpacesWithSpace',
        'ReplaceUnderscoreWithSpace',
        'SeparateAposS',
        'Lowercase',
        'ASCIIFold'
    ],
    "regex_norm_rules": [],
    "stemmer": "EnglishNLTKStemmer"
}

################################
### DATA AUGMENTATION CONFIG ###
################################
AUGMENTATION_CONFIG = {
    "augmentor_class": "EnglishParaphraser",
    "batch_size": 8,
    "retain_entities": False,
    "paths": [
        {
            "domains": "(greeting)",
            "intents": "(greet|exit)",
            "files": ".*",
        }
    ],
    "path_suffix": "-augmented.txt"
}

# A example configuration for the parser
"""
# *** Note: these are place holder entity types ***
PARSER_CONFIG = {
    'grandparent': {
        'parent': {},
        'child': {'max_instances': 1}
    },
    'parent': {
        'child': {'max_instances': 1}
    }
}
"""