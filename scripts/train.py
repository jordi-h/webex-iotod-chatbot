"""This script either trains or loads the NLP models (depending on what lines are commented)"""

from mindmeld.components.nlp import NaturalLanguageProcessor
from mindmeld.core import Query
from sklearn.exceptions import UndefinedMetricWarning
import warnings
import os

# Load your app
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
nlp = NaturalLanguageProcessor(app_path=app_path)
nlp.build()
nlp.dump()
#nlp.load()