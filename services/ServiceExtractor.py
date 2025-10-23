import json
import re
import logging
import spacy
from spyne import Application, rpc, ServiceBase, Unicode,Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from helpers.server import APP_HOST
from helpers.types import TextInfosServiceReturn, TypeOfExtraction



# Extract text class from block content (not implemented yet)
class ContentBlockExtractor:
    @staticmethod
    def extract_info(texte) -> dict:
        # Choose french model, fallback to english if not found
        try:
            nlp = spacy.load("fr_core_news_md")
        except:
            try:
                nlp = spacy.load("en_core_web_md")
            except:
                raise Exception("⚠️ Modèle spaCy non trouvé. Installe avec : "
                                "'python -m spacy download fr_core_news_md'")
                
        """
        Extract information from unstructured text using NLP techniques.
        """
        doc = nlp(texte)
        resultat = {
            "client_id": None,
            "client_name": None,
            "adresse": None,
            "email": None,
            "phone_numer": None,
            "loan_amount": None,
            "loan_times": None,
            "description": None,
        }

        clientid_regex = r"(client-\d{3})"
        m_id = re.search(clientid_regex, texte)
        if m_id:
            resultat["client_id"] = m_id.group(1)

        # 1. Nom du client — heuristique : entité PERSON + "Je m'appelle" ou signature à la fin
        for ent in doc.ents:
            if ent.label_ in ("PER", "PERSON") and resultat["client_name"] is None:
                # vérifier s’il y a “Je m'appelle …” autour
                if re.search(r"\bJe m['’]appelle\s+" + re.escape(ent.text), texte) or re.search(r"\bI am\s+" + re.escape(ent.text), texte):
                    resultat["client_name"] = ent.text
                    break
        # fallback : signature à la fin, “Cordialement, John Doe”  
        if resultat["client_name"] is None:
            m = re.search(r"Cordialement[,]?\s*([A-Z][A-Za-zÀ-ÿ'\-]+\s+[A-Z][A-Za-zÀ-ÿ'\-]+)", texte)
            if m:
                resultat["client_name"] = m.group(1)

        # 2. Email
        email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        em = re.search(email_regex, texte)
        if em:
            resultat["email"] = em.group(0)

        # 3. Téléphone
        tel_regex = r"(\+?\d{1,3}[\s\.\-]?\(?\d{1,4}\)?[\s\.\-]?\d{1,4}[\s\.\-]?\d{2,4}[\s\.\-]?\d{2,4})"
        t = re.search(tel_regex, texte)
        if t:
            resultat["phone_numer"] = t.group(0)

        # 4. Montant du prêt
        m = re.search(r"(\d{1,3}(?:[\s.,]?\d{3})*)(?:\s*)(?:€|EUR|euros?)", texte, re.IGNORECASE)
        if m:
            montant = m.group(1).replace(" ", "").replace(",", "").replace(".", "")
            resultat["loan_amount"] = int(montant)

        # 5. Durée du prêt
        duree_regex = r"durée\s+(?:de\s+)?(\d{1,3})\s*(?:ans|years?)"
        d = re.search(duree_regex, texte, re.IGNORECASE)
        if d:
            resultat["loan_times"] = int(d.group(1))

        # 6. Adresse client complète — heuristique
        adresse_client_regex = r"réside\s+actuellement\s+au\s+(.+?)(?:\.\s|,|;|\n)"
        ac = re.search(adresse_client_regex, texte, re.IGNORECASE)
        if ac:
            resultat["adresse"] = ac.group(1).strip()

        # 7. Description du bien
        desc_regex = r"(maison|appartement|villa|logement)[^\.!\n]{0,100}"
        d2 = re.search(desc_regex, texte, re.IGNORECASE)
        if d2:
            resultat["description"] = d2.group(0).strip()

        # 8. Adresse de la propriété (dans même phrase que description ou après “située à”)
        adresse_prop_regex = r"située\s+dans\s+(.+?)(?:\.\s|,|\n)"
        ap = re.search(adresse_prop_regex, texte, re.IGNORECASE)
        if ap:
            resultat["adresse"] = ap.group(1).strip()

        return resultat


# Extract text class from file content where each line is in "Key: Value" format
class ContentLineExtractor:
    @staticmethod
    def extract_info(content) -> dict:
        try:
            info = {}
            # Gestion des lignes multi-lignes (ex: Description)
            lines = content.splitlines()
            current_key = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # On essaie de capturer "Clé: Valeur"
                match = re.match(r"^([^:]+):\s*(.*)$", line)
                if match:
                    key = match.group(1).strip()
                    value = match.group(2).strip()
                    info[key] = value
                    current_key = key
                else:
                    # Si la ligne ne contient pas de ':', on considère que c'est la suite
                    # de la valeur précédente (cas de description multi-ligne)
                    if current_key:
                        info[current_key] += " " + line

            return info
        except Exception as e:
            logging.error(f"Error extracting info from content: {e}")
            raise e


class RequestInfoReader:
    def extract_info(type: TypeOfExtraction, content: str) -> dict:
        if type == TypeOfExtraction.line:
            info = ContentLineExtractor.extract_info(content)
        if type == TypeOfExtraction.block:
            info = ContentBlockExtractor.extract_info(content)
        return info

class InfoExtractor(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def extract_info(ctx, content):
        if not content or content.strip() == "":
            raise Fault(faultcode="Client.ContentEmpty", faultstring="The content is not set or is empty.")
        try:
            info = RequestInfoReader.extract_info(TypeOfExtraction.line, content)
            return json.dumps(info, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Error in extract_info service method: {e}")
            raise Fault(faultcode="Server.ExtractionError", faultstring=str(e))
    
# App configuration
application_ex = Application(
    [InfoExtractor], 
    tns='spyne.infoextractor',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

SERVICE_APP_EXTRACTOR = WsgiApplication(application_ex)
SERVICE_APP_EXTRACTOR_PORT = 8000
SERVICE_APP_EXTRACTOR_URL = f'http://{APP_HOST}:{SERVICE_APP_EXTRACTOR_PORT}/'