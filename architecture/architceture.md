# 🏗️ Architecture SOA - Real Estate Loan Composite Web Service

## 🌍 Vue d’ensemble
Cette application illustre une **architecture orientée services (SOA)** appliquée au domaine du **prêt immobilier**.  
Elle se compose de plusieurs **services web indépendants** communiquant via **WSDL (SOAP)**, orchestrés par un **service principal**.

---

## ⚙️ Composants principaux

## 📦 Liste des Services

| Service | Rôle |
|----------|------|
| **ClientInfoService** | Gère les données personnelles du client (identité, adresse, etc.). |
| **CreditService** | Gère les informations liées aux crédits en cours (historique, montants, remboursements, incidents). |
| **ExplainService** | Génère des rapports explicatifs sur les décisions de scoring ou d’évaluation. |
| **FinancialDataService** | Centralise les données financières du client : revenus, charges, patrimoine, transactions bancaires. |
| **LoanAppService** | Gère les demandes de prêts : création, validation, suivi et décision. |
| **ScoringService** | Calcule le score de risque du client à partir de ses données financières et de son historique de crédit. |
| **SolvacyService** | Évalue la solvabilité du client (capacité de remboursement selon revenus et dettes). |

---

### 🧩 Main Service (LoanAppService)
Le **service principal** orchestre le processus global de demande de prêt :
1. **Extract_Information** – extraction des données du dossier.
2. **Check_solvability** – vérification de la solvabilité du client.
3. **Assess_property** – évaluation du bien immobilier.
4. **Make_decision** – décision finale (acceptation ou refus du prêt).

Ce service expose un **WSDL** pour être consommé par les clients externes et interagit avec une **base de données**.

---

### 💾 Base de données
Stocke les informations des clients, des biens, des évaluations et des décisions de prêt.  
Reliée au **Main Service**, qui orchestre la persistance des données.

---

### 👥 Clients
Les clients ou applications front-end interagissent **uniquement avec le Main Service** via son **WSDL**, sans contact direct avec les autres services.

---

## 🔁 Flux de traitement
1. Le client soumet une demande de prêt.
2. Le **Main Service** :
   - extrait les données,
   - appelle les services de solvabilité et d’évaluation,
   - valide les résultats,
   - prend une décision finale.
3. Le résultat (acceptation/refus) est renvoyé au client.

___

### 🧮 LoanExpenseAnalyzer Service (MainService)

> Service principal SOAP pour l’analyse des dépenses de prêt et l’évaluation de la solvabilité client.

---

### 📘 Description

Le **LoanExpenseAnalyzer** est le point d’entrée principal du système d’analyse de crédit.  
Il orchestre plusieurs microservices SOAP afin de produire un **rapport complet de solvabilité** à partir d’un contenu client (par ex. une demande de prêt ou un profil textuel).

---

### ⚙️ Objectif

Le service reçoit une requête SOAP contenant un champ `content` (texte ou JSON).  
Il :
1. Extrait les informations du contenu,
2. Récupère les données client, financières et de crédit,
3. Calcule le score de crédit et la solvabilité,
4. Génère une explication interprétable,
5. Retourne un objet structuré `SolvencyReportType`.

---

### 🧩 Dépendances

| Service | Description | URL (constante) |
|----------|--------------|----------------|
| **ServiceExtractor** | Extrait les données brutes à partir du texte client. | `SERVICE_APP_EXTRACTOR_URL` |
| **ClientInfos** | Fournit les informations d’identité du client. | `SERVICE_APP_CLIENT_INFO_URL` |
| **FinancialDataService** | Récupère les données financières (revenus, dépenses mensuelles). | `FINANCE_APP_CLIENT_INFO_URL` |
| **CreditService** | Retourne l’historique de crédit et les dettes. | `CREDIT_BUREAU_APP_CLIENT_URL` |
| **ScoringService** | Calcule le score de crédit selon l’historique et les données du client. | `SCORING_APP_CLIENT_URL` |
| **SolvacyService** | Évalue la solvabilité selon le revenu, les charges et le score. | `SOLVACY_APP_CLIENT_URL` |
| **ExplanantionService** | Génère une explication interprétable du résultat. | `EXPLANATION_APP_CLIENT_URL` |

---

## ✅ Principes SOA respectés
- **Interopérabilité** : communication standardisée via WSDL/SOAP.  
- **Réutilisabilité** : chaque service peut être réutilisé ailleurs.  
- **Modularité** : composants indépendants et faciles à maintenir.  
- **Orchestration** : le Main Service coordonne l’exécution des autres services.

---

## 🚀 Conclusion
Cette architecture met en œuvre les principes fondamentaux de la **SOA (Service-Oriented Architecture)** :  
- chaque service est **autonome**, **réutilisable** et **accessible via une interface standardisée (WSDL)** ;  
- le **Main Service** agit comme un **orchestrateur**, coordonnant l’ensemble du processus métier ;  
- les **clients** interagissent uniquement avec le service principal, ce qui simplifie la consommation et la maintenance ;  
- la **base de données** centralise les résultats et les décisions du flux de prêt immobilier.

En résumé, cette approche garantit **modularité**, **interopérabilité** et **extensibilité**, tout en posant les bases d’une évolution naturelle vers une architecture **microservices**.
