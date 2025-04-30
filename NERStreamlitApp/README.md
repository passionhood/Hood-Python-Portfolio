# Named Entity Recognition (NER) Streamlit App

This interactive app allows users to explore and customize Named Entity Recognition using spaCy and Streamlit. Built with a clean interface and rule-based pattern matching, it's perfect for learning or demoing custom NER pipelines.

---

##  Features
- Upload `.txt` files or directly enter text
- Add custom entity labels and rules (e.g., "PRODUCT: iPhone")
- Visualize extracted named entities using spaCy's DisplaCy
- Download your rules as a JSON pattern file

---

## About Named Entity Recognition (NER)

NER is a sub-task of information extraction that seeks to locate and classify named entities in text into predefined categories such as PERSON, ORGANIZATION, LOCATION, etc.  
This app enhances that by allowing **custom labels and rules** using spaCy's `EntityRuler`.

---

## Visuals 
![NER App Interface](images/NER_App_Interface.png)

--- 

## Requirements

```bash
pip install -r requirements.txt