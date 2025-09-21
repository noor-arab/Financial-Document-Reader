import re
import spacy

nlp = spacy.load("en_core_web_sm")

def map_entities_to_financial(spacy_entities, text):
    """
    Map generic spaCy entities to a financial schema.
    """
    financial_entities = {
        "Counterparty": None,
        "Notional": None,
        "ISIN": None,
        "Underlying": None,
        "Maturity": None,
        "Bid": None,
        "Offer": None,
        "PaymentFrequency": None
    }

    # Counterparty: ORG containing known bank keywords
    for org in spacy_entities.get("ORG", []):
        for keyword in ["BANK", "CACIB", "GS", "BNP", "JPM", "HSBC"]:
            if keyword in text and org in text:
                financial_entities["Counterparty"] = org
                break

    # Notional: CARDINAL followed by "mio"
    for cardinal in spacy_entities.get("CARDINAL", []):
        if f"{cardinal} mio" in text:
            financial_entities["Notional"] = f"{cardinal} mio"

    # Maturity: look for 1Y, 2Y, etc.
    for cardinal in spacy_entities.get("CARDINAL", []):
        if "Y" in cardinal:
            financial_entities["Maturity"] = cardinal

    # PaymentFrequency: DATE labels containing Monthly/Quarterly/Annually
    for date in spacy_entities.get("DATE", []):
        if date.lower() in ["quarterly", "monthly", "annually"]:
            financial_entities["PaymentFrequency"] = date

    # ISIN: regex match
    match = re.search(r'\b[A-Z]{2}[0-9A-Z]{10}\b', text)
    if match:
        financial_entities["ISIN"] = match.group()

    # Underlying: words after ISIN up to a date
    if financial_entities["ISIN"]:
        pattern = financial_entities["ISIN"] + r'\s+([A-Z0-9\s]+)'
        match = re.search(pattern, text)
        if match:
            underlying = match.group(1).strip()
            underlying = re.sub(r'\d{2}/\d{2}/\d{2,4}', '', underlying).strip()
            financial_entities["Underlying"] = underlying

    # Bid: estr+<number>bps
    bid_match = re.search(r'estr\+?\d+bps', text, re.IGNORECASE)
    if bid_match:
        financial_entities["Bid"] = bid_match.group()

    # Offer: line starting with "offer"
    offer_match = re.search(r'(?i)^offer.*', text, re.MULTILINE)
    if offer_match:
        financial_entities["Offer"] = offer_match.group().strip()

    # Fallback for Counterparty if not detected
    if financial_entities["Counterparty"] is None:
        match = re.search(r'\b(BANK\s+[A-Z]+)\b', text)
        if match:
            financial_entities["Counterparty"] = match.group(1)

    return financial_entities


def parse_chat_ner(text: str):
    """
    Run spaCy NER on chat text and map generic entities to financial schema.
    """
    doc = nlp(text)
    spacy_entities = {}

    for ent in doc.ents:
        label = ent.label_
        value = ent.text.strip()
        spacy_entities.setdefault(label, []).append(value)

    return map_entities_to_financial(spacy_entities, text)
