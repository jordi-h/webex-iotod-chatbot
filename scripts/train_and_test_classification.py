"""This script evaluates domain and intent classification performance."""

from mindmeld.components.nlp import NaturalLanguageProcessor
from mindmeld.core import Query
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.exceptions import UndefinedMetricWarning
import warnings
import os

# Load your app
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
nlp = NaturalLanguageProcessor(app_path=app_path)
# nlp.build()
# nlp.dump()
nlp.load()

# ic = nlp.domains['greeting'].intent_classifier
# res = ic.predict('lkdnfzznoiqnnoin')
# print(res)

# -----------------------------
# DOMAIN CLASSIFICATION
# -----------------------------
print("\n=== DOMAIN CLASSIFICATION ===")

test_queries = []
true_domains = []

for domain in nlp.domains:
    domain_path = os.path.join(app_path, 'domains', domain)
    for intent in nlp.domains[domain].intents:
        test_path = os.path.join(domain_path, intent, 'test.txt')
        if not os.path.exists(test_path):
            continue
        with open(test_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        test_queries.extend(lines)
        true_domains.extend([domain] * len(lines))

predicted_domains = [nlp.process(q)['domain'] for q in test_queries]

print("Domain Classification Accuracy:", accuracy_score(true_domains, predicted_domains))
print("Classification Report:\n", classification_report(true_domains, predicted_domains, digits=4))
print("Confusion Matrix:\n", confusion_matrix(true_domains, predicted_domains))

# -----------------------------
# INTENT CLASSIFICATION
# -----------------------------
print("\n=== INTENT CLASSIFICATION (Per-Domain Evaluation, Independent of Domain Prediction) ===")

for domain in nlp.domains:
    ic = nlp.domains[domain].intent_classifier

    domain_queries = []
    true_intents = []

    for intent in nlp.domains[domain].intents:
        test_path = os.path.join(app_path, 'domains', domain, intent, 'test.txt')
        if not os.path.exists(test_path):
            continue

        with open(test_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            domain_queries.extend(lines)
            true_intents.extend([intent] * len(lines))

    if not domain_queries:
        continue

    predicted_intents = []
    for q in domain_queries:
        result = nlp.domains[domain].process(q)  # Direct intent classification, scoped to domain
        predicted_intents.append(result['intent'])

    print(f"\n--- Domain: {domain} ---")
    print("Intent Classification Accuracy:", accuracy_score(true_intents, predicted_intents))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UndefinedMetricWarning)
        print("Classification Report:\n", classification_report(true_intents, predicted_intents, digits=4))
        print("Confusion Matrix:\n", confusion_matrix(true_intents, predicted_intents, labels=sorted(set(true_intents))))
