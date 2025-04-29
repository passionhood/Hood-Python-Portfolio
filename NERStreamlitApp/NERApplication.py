pip install spacy
import streamlit as st
import spacy
from spacy.pipeline import EntityRuler
from spacy import displacy
import pandas as pd
import json

# Load spaCy's small English model
nlp = spacy.load("en_core_web_sm")

# App title and intro
st.title("🧠 Named Entity Recognition (NER) App")
st.write("Customize and visualize named entities in your own text data using spaCy + Streamlit.")

# --- Sidebar: File upload and custom pattern creation ---

st.sidebar.header("Upload & Pattern Settings")

# Allow user to upload a .txt file
uploaded_file = st.sidebar.file_uploader("Upload a text file", type=["txt"])

# Or let them type in their own text
custom_text = st.text_area("Or type/paste your text here:", height=150)

# Sidebar inputs for custom entity rules
st.sidebar.subheader("Define Custom Entities")
label = st.sidebar.text_input("Entity Label (e.g., PRODUCT, ORG, PERSON)")
pattern = st.sidebar.text_input("Entity Pattern (e.g., 'iPhone')")

# Use Streamlit's session_state to persist patterns across app interactions
if "patterns" not in st.session_state:
    st.session_state.patterns = []

# When button clicked, store new pattern in session state
if st.sidebar.button("Add Pattern"):
    if label and pattern:
        st.session_state.patterns.append({"label": label.upper(), "pattern": pattern})
        st.sidebar.success(f"Added pattern: '{pattern}' as {label.upper()}")

# Display list of current patterns added
if st.session_state.patterns:
    st.sidebar.markdown("### Current Patterns")
    st.sidebar.json(st.session_state.patterns)

# --- Apply custom rules via EntityRuler ---

# Create an EntityRuler and insert user-defined patterns
ruler = EntityRuler(nlp, overwrite_ents=True)
ruler.add_patterns(st.session_state.patterns)

# Add the EntityRuler component to the pipeline by name
nlp.add_pipe("entity_ruler", before="ner")

# Access the added pipe and add custom patterns
nlp.get_pipe("entity_ruler").add_patterns(st.session_state.patterns)
# If no patterns are defined, use a default pattern

# Load text from file or user input
if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
elif custom_text:
    text = custom_text
else:
    text = "Apple is looking at buying U.K. startup for $1 billion."

# Apply the spaCy pipeline to the text
doc = nlp(text)

# --- Output Display Section ---

# Show the original text
st.subheader("📄 Input Text")
st.code(text, language="text")

# Show extracted named entities in list format
st.subheader("🔍 Named Entities")
if doc.ents:
    for ent in doc.ents:
        st.markdown(f"- **{ent.text}** — *{ent.label_}*")
else:
    st.write("No named entities found.")

# Visualize named entities using spaCy's DisplaCy
st.subheader("🖼️ Entity Visualization")
html = displacy.render(doc, style="ent", jupyter=False)
st.components.v1.html(html, scrolling=True, height=400)

# Allow user to download their custom patterns as a JSON file
if st.button("Export Patterns as JSON"):
    st.download_button("Download JSON", data=json.dumps(st.session_state.patterns), file_name="custom_patterns.json")
    st.success("Download started!")