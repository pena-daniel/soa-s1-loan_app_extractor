import re

CLIENTS = [
  {
    "client_id": "client-001",
    "name": "John Doe",
    "adresse": "123 Rue de la Liberté, Paris"
  },
  {
    "client_id": "client-002",
    "name": "Alice Martin",
    "adresse": "456 Avenue des Fleurs, Lyon"
  },
  {
    "client_id": "client-003",
    "name": "Bob Johnson",
    "adresse": "789 Oak St, Marseille"
  },
  {
    "client_id": "client-004",
    "name": "Emma Dupont",
    "adresse": "22 Boulevard Victor Hugo, Nice"
  },
  {
    "client_id": "client-005",
    "name": "Marc Leroy",
    "adresse": "18 Rue du Lac, Toulouse"
  }
]
FINANCES = [
    {
        "client_id": "client-001",
        "income": 5000,
        "expenses": 3000
    },
    {
        "client_id": "client-002",
        "income": 4500,
        "expenses": 2500,
    },
    {
        "client_id": "client-003",
        "income": 6000,
        "expenses": 3500
    }
]
CREDITS = [
    {
        "client_id": "client-001",
        "debt": 20000,
        "late": False,
        "bankruptcy": False
    },
    {
        "client_id": "client-002",
        "debt": 15000,
        "late": True,
        "bankruptcy": False
    },
    {
        "client_id": "client-003",
        "debt": 30000,
        "late": False,
        "bankruptcy": True
    }
]

class Database:
    
    @staticmethod
    def get_client_infos_by_name(name):
        for client in CLIENTS:
            if client["name"].lower() == name.lower():
                return client
        return None
    
    @staticmethod
    def get_client_info(client_id):
        for client in CLIENTS:
            if client["client_id"] == client_id:
                return client
        return None

    @staticmethod
    def get_financial_info(client_id):
        for finance in FINANCES:
            if finance["client_id"] == client_id:
                return finance
        return None

    @staticmethod
    def get_credit_info(client_id):
        for credit in CREDITS:
            if credit["client_id"] == client_id:
                return credit
        return None