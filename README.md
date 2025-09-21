# Financial Document Reader Case Study


## Overview

This project is a Proof of Concept (PoC) for extracting financial entities from DOCX files and chat logs using:

* Rule-based parsing for DOCX files
* NER model (spaCy) for chat messages
* FastAPI backend for file upload and JSON response

**Supported entities:**

* Counterparty
* Notional
* ISIN
* Underlying
* Maturity
* Bid
* Offer
* Payment Frequency

## Requirements

* Python 3.10+
* Windows / macOS / Linux
* Virtual environment (recommended)

**Python packages:**

* fastapi
* uvicorn
* python-multipart
* spacy
* python-docx

## Setup Instructions (Windows)

1. **Clone the repository**

   ```
   git clone https://github.com/noor-arab/Financial-Document-Reader.git
   cd Financial-Document-Reader
   ```

2. **Create a virtual environment**

   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**

   ```
   venv\Scripts\activate
   ```

4. **Install dependencies**

   ```
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

## Running the API

```bash
uvicorn app:app --reload
```

* Server runs on [http://127.0.0.1:8000](http://127.0.0.1:8000) by default
* Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in a browser to access interactive API docs

## API Endpoints

**1. Upload DOCX**

* URL: `/upload/docx`
* Method: POST
* Body: form-data with file (.docx)
* Response: JSON with extracted financial entities

**2. Upload Chat**

* URL: `/upload/chat`
* Method: POST
* Body: form-data with file (.txt, .chat, .log)
* Response: JSON with extracted financial entities

## Sample Usage

**Upload chat log:**

```bash
curl -X POST "http://127.0.0.1:8000/upload/chat" -F "file=@sample_chat.txt"
```

**Sample JSON response:**

```json
{
  "Counterparty": "BANK ABC",
  "Notional": "200 mio",
  "ISIN": "FR001400QV82",
  "Underlying": "AVMAFC FLOAT",
  "Maturity": "2Y",
  "Bid": "estr+45bps",
  "Offer": "offer 2Y EVG estr+45bps",
  "PaymentFrequency": "Quarterly"
}
```

## Notes

* DOCX parsing is rule-based; chat parsing uses spaCy NER with post-processing.
* PDFs are not supported in this PoC; methodology for PDF / LLM extraction is included in the GMD.
* Temporary files are automatically deleted after processing.
