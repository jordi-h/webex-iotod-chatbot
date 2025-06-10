"""This script evaluates entity recognition performance."""

from mindmeld.components.nlp import NaturalLanguageProcessor
from mindmeld.core import Query
from sklearn.exceptions import UndefinedMetricWarning
import warnings
import os

# Load your app
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
nlp = NaturalLanguageProcessor(app_path=app_path)
# nlp.build()
# nlp.dump()
nlp.load()

# er = nlp.domains['device'].intents['get_device_by_name'].entity_recognizer
# result = er.predict_proba('More details on cOd6ySbRCpIzcH, please.')
# print(result)

#! This script requires a change to Mindmeld's evaluate() method in order to be executable with some models, including BERT. See below #*
er = nlp.domains['device'].intents['get_device_by_name'].entity_recognizer
eval = er.evaluate()
eval.print_stats()

#* === REQUIRED CHANGE TO MINDMELD ===
#* In mindmeld/components/classifier.py, inside the `evaluate()` method:
#* Replace this:
#*     if self.config.model_type == 'tagger':
#*         kwargs["fetch_distribution"] = fetch_distribution
#*
#* With this:
#*     if (
#*         self.config.model_type == 'tagger' and
#*         self.config.model_settings.get("classifier_type") != "embedder"
#*     ):
#*         kwargs["fetch_distribution"] = fetch_distribution
#*
#* This prevents the `fetch_distribution` argument from being passed to BERT-based models,
#* which do not support it and will raise a TypeError.
#*