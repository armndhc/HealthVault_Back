""" import spacy
from dateutil.parser import parse
import re


class NLPService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.field_mapping = {
            "name": ["name", "first name", "patient name"],
            "lastName": ["last name", "surname"],
            "bloodType": [
                "blood type", "blood group", "type", 
                "blood o+", "o positive", "type o+", "blood a-", "a negative", "type ab-", "ab positive"
            ],
            "sugarBlood": ["blood sugar", "sugar level"],
            "familyHistory": ["family history", "family conditions"],
            "birthDate": ["birthdate", "date of birth", "born"],
            "gender": ["gender", "sex"],
            "medicalHistory": ["medical history", "health history"],
            "weight": ["weight", "body weight"],
            "height": ["height", "body height"],
            "bloodPressure": ["blood pressure"],
            "email": ["email", "mail"],
            "phone": ["phone", "contact number", "número de contacto",],
            "emergencyContact": ["emergency contact", "emergency name"],
        }

    def parse_query(self, user_query):
        doc = self.nlp(user_query.lower())  
        query = {}

        i = 0
        while i < len(doc):
            token = doc[i]
            field = self._identify_field(token.text)

            if field:
                if i + 1 < len(doc) and doc[i + 1].text in [
                    "above", "greater than", ">", "below", "less than", "<", 
                    "at least", "at most", "more than", "less than or equal to"
                ]:
                    comparator = {
                        "above": "$gt",
                        "greater than": "$gt",
                        ">": "$gt",
                        "below": "$lt",
                        "less than": "$lt",
                        "<": "$lt",
                        "at least": "$gte",
                        "at most": "$lte",
                        "more than": "$gt",
                        "less than or equal to": "$lte"
                    }.get(doc[i + 1].text)
                    value = doc[i + 2].text if i + 2 < len(doc) else None
                    if comparator and value:
                        query[field] = {comparator: self._convert_value(value, field)}
                        i += 2  
                elif i + 1 < len(doc) and doc[i + 1].text in ["is", "equal to", "=", "es", "igual a"]:
                    value = doc[i + 2].text if i + 2 < len(doc) else None
                    if value:
                        query[field] = self._convert_value(value, field)
                        i += 2
                else:
                    value = " ".join([t.text for t in doc[i + 1:]])
                    query[field] = self._convert_value(value, field)
                    break
            i += 1

        print(f"Generated query: {query}")

        return query

    def _identify_field(self, text):
        text = re.sub(r"[^a-zA-Z0-9 ]", "", text.strip())  
        for db_field, synonyms in self.field_mapping.items():
            if text in synonyms:
                return db_field
        return None

    def _convert_value(self, value, field=None):
        try:
            if field == "bloodType":
                value = value.strip().upper()
                if "POSITIVE" in value:
                    return value.replace("POSITIVE", "+")
                if "NEGATIVE" in value:
                    return value.replace("NEGATIVE", "-")
                return value  

            if re.match(r"^\d+(\.\d+)?$", value):
                return float(value) if "." in value else int(value)

            return parse(value).isoformat()
        except (ValueError, TypeError):
            return value.strip()
 """