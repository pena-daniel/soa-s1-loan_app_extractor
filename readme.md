# Loan Expense Analyzer - SOAP Services

## 1️⃣ Objectif

Service web SOAP pour l'analyse des dépenses de prêt et le scoring de solvabilité.

---

## 2️⃣ Prérequis

- Python 3.11+
- Installer les dépendances :

```bash
pip install -r requirements.txt
```

- Installer les modèles spaCy :

```bash
python -m spacy download fr_core_news_md
python -m spacy download en_core_web_md
```

## 3️⃣ Installation

git clone <repo-url>
cd <project-folder>
pip install -r requirements.txt

## 4️⃣ Lancement

Chaque service dispose de son propre port (8000‑8007).
Exemple pour LoanExpenseAnalyzer :

```bash
python main.py
```

## 5️⃣ Endpoints SOAP

| Service              | WSDL URL                      | Description                            |
| -------------------- | ----------------------------- | -------------------------------------- |
| ClientInfo           | `http://localhost:8000/?wsdl` | Récupère les informations d’un client  |
| CreditService        | `http://localhost:8001/?wsdl` | Historique et dettes du client         |
| ExplanationService   | `http://localhost:8002/?wsdl` | Explications du score                  |
| FinancialDataService | `http://localhost:8003/?wsdl` | Informations financières du client     |
| LoanExpenseAnalyzer  | `http://localhost:8004/?wsdl` | Analyse complète du prêt               |
| ScoringService       | `http://localhost:8005/?wsdl` | Calcul du score de crédit              |
| ServiceExtractor     | `http://localhost:8006/?wsdl` | Extraction d’informations depuis texte |
| SolvacyService       | `http://localhost:8007/?wsdl` | Calcul de la solvabilité               |

## 6️⃣ Exemple d’utilisation

```python
from zeep import Client

client = Client("http://localhost:8004/?wsdl")
result = client.service.analyze_loan_expense("Contenu de la demande de prêt")
print(result)
```

## 7️⃣ SLA / QoS

### Objectifs de performance

| Indicateur             | Cible                                     |
| ---------------------- | ----------------------------------------- |
| Temps de réponse moyen | < 300 ms par appel SOAP                   |
| Disponibilité          | 99%                                       |
| Fiabilité              | Gestion des exceptions et retours `Fault` |

### Mécanismes

- Logs centralisés (logging.info, logging.error)

- Vérification des entrées (Fault si client_id ou contenu invalide)

- Gestion des erreurs réseau (ConnectionError)
Exemple de log :

```pgsql
    INFO: Client informations retrieved for loan expense analysis
    ERROR: No client information found for the extracted client name.
```

## 8️⃣ Note d’architecture

### Choix techniques

- Spyne pour SOAP → standard WSDL, facile à mocker pour tests

- Zeep pour appeler les services SOAP en Python

- Services séparés → modulaire, facile à tester et maintenir

- Types personnalisés → SolvencyReportType, ExplanationsType pour une interface propre

### Schéma BPMN simplifié

```csharp
[Client] 
   |
   v
[ServiceExtractor] -> extract info from text
   |
   v
[ClientInfoService] -> client data
   |
   v
[FinancialDataService] -> financial info
   |
   v
[CreditService] -> credit history
   |
   v
[ScoringService] -> credit score
   |
   v
[SolvacyService] -> solvency
   |
   v
[ExplanationService] -> explanations
   |
   v
[LoanExpenseAnalyzer] -> aggregated report
   |
   v
[Client]

```
