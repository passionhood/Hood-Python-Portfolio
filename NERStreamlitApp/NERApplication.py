# Passion Hood
# CSE 10102: Elements of Computing II, Spring 2025
# NER Application: Named Entity Recognition (NER) Tool

import streamlit as st  # For building the app UI
import spacy  # Natural Language Processing
from spacy.pipeline import EntityRuler  # For custom entity patterns
from spacy import displacy  # For visualizing entities
import pandas as pd  # For working with tables and CSV
import json  # For exporting JSON pattern files
from collections import Counter  # For entity frequency counting

# --- Load NLP Model ---
nlp = spacy.load("en_core_web_sm")  # Load the default small English model

# --- Streamlit Config ---
st.set_page_config(page_title='NER Analyzer', layout='wide')
st.title("🧠 Named Entity Recognition (NER) App")
st.write("Customize, visualize, and export named entities using spaCy + Streamlit.")

# --- Sidebar Upload & Pattern Input ---
st.sidebar.header("📁 Upload & Pattern Settings")
uploaded_file = st.sidebar.file_uploader("Upload a .txt file", type=["txt"])  # Allow .txt upload
custom_text = st.text_area("Or type/paste your text here:", height=150)  # Manual text input

# Inputs for defining custom entity patterns
st.sidebar.subheader("🔧 Define Custom Entities")
label = st.sidebar.text_input("Entity Label (e.g., PRODUCT, ORG, TICKER)")
pattern = st.sidebar.text_input("Entity Pattern (e.g., 'iPhone')")

# Initialize session state to store patterns
if "patterns" not in st.session_state:
    st.session_state.patterns = []

# Add new custom pattern
if st.sidebar.button("Add Pattern"):
    if label and pattern:
        st.session_state.patterns.append({"label": label.upper(), "pattern": pattern})
        st.sidebar.success(f"Added pattern: '{pattern}' as {label.upper()}")

# Display current custom patterns
if st.session_state.patterns:
    st.sidebar.markdown("### Current Patterns")
    st.sidebar.json(st.session_state.patterns)

# --- EntityRuler Setup ---
ruler = EntityRuler(nlp, overwrite_ents=True)
ruler.add_patterns(st.session_state.patterns)
nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True})  # Insert before built-in NER
nlp.get_pipe("entity_ruler").add_patterns(st.session_state.patterns)

# --- Load Text ---
if uploaded_file:
    text = uploaded_file.read().decode("utf-8")  # Read from uploaded file
elif custom_text:
    text = custom_text  # Use typed text
else:
    # Default sample text
    text = "Apple's earnings report showed a dividend yield increase. Goldman Sachs is bullish on AAPL."

# --- NLP Processing ---
doc = nlp(text)  # Apply NLP pipeline to input text

# --- Display Input Text ---
st.subheader("📄 Input Text")
st.code(text, language="text")

# --- Filter Entities ---
unique_labels = sorted(set([ent.label_ for ent in doc.ents]))  # List of unique entity types found
selected_labels = st.multiselect("Filter entities by label:", unique_labels, default=unique_labels)  # Allow filtering
filtered_ents = [ent for ent in doc.ents if ent.label_ in selected_labels]  # Apply filter

# --- Named Entities Display ---
st.subheader("🔍 Named Entities")
if filtered_ents:
    for ent in filtered_ents:
        st.markdown(f"- **{ent.text}** — *{ent.label_}*")  # Show entity and label
else:
    st.write("No named entities found for the selected labels.")

# --- Entity Frequency Chart ---
st.subheader("📊 Entity Frequency")
ent_counts = Counter([ent.label_ for ent in filtered_ents])  # Count each entity label
if ent_counts:
    st.bar_chart(pd.Series(ent_counts))  # Display as bar chart

# --- Entity Visualization ---
st.subheader("🖼️ Entity Visualization")
html = displacy.render(doc, style="ent", jupyter=False)  # Create HTML visualization
st.components.v1.html(html, scrolling=True, height=400)  # Render inside app

# --- Export Entities as CSV ---
entity_data = [{"Text": ent.text, "Label": ent.label_} for ent in filtered_ents]  # Prepare export data

df = pd.DataFrame(entity_data)
if not df.empty:
    csv = df.to_csv(index=False)
    st.download_button("📥 Download Entities as CSV", data=csv, file_name="named_entities.csv", mime="text/csv")

# --- Export Custom Patterns as JSON ---
if st.button("📤 Export Patterns as JSON"):
    st.download_button("Download JSON", data=json.dumps(st.session_state.patterns), file_name="custom_patterns.json")
    st.success("Download started!")