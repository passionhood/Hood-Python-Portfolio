# Import the Streamlit library
import streamlit as st

#ls lists everything in the directory to view in current directory python folder
#cd navagiates in and out of folders 
#cd.. moves you back to the python folder 

# Display a simple text message
st.write("Hello, streamlit!")
st.markdown("# This is my first streamlit app!")

# Display a large title on the app
st.title("This is my first Streamlit app.")

# ------------------------
# INTERACTIVE BUTTON
# ------------------------

# Create a button that users can click.
# If the button is clicked, the message changes.
if st.button("Click me!"):
    st.write("You clicked the button! Great job! 🥳")
else:
    st.write("I dare you to click the button...")

# ------------------------
# COLOR PICKER WIDGET
# ------------------------

# Creates an interactive color picker where users can choose a color.
# The selected color is stored in the variable 'color'.
color = st.color_picker("Pick a color", "#1a1f8e")

# Display the chosen color value
st.write(f"You picked: {color}")

# ------------------------
# ADDING DATA TO STREAMLIT
# ------------------------

# Import pandas for handling tabular data
import pandas as pd

# Display a section title
st.subheader("Now, let's look at some data!")

# Create a simple Pandas DataFrame with sample data
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],  # Column of names
    'Age': [25, 30, 35, 40],  # Column of ages
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']  # Column of cities
})

# Display a descriptive message
st.write("Here's a simple table:")

# Display the dataframe in an interactive table.
# Users can scroll and sort the data within the table.
st.dataframe(df)

# ------------------------
# INTERACTIVE DATA FILTERING
# ------------------------

# Create a dropdown (selectbox) for filtering the DataFrame by city.
# The user selects a city from the unique values in the "City" column.
city = st.selectbox("Select a city", df["City"].unique())

# Create a filtered DataFrame that only includes rows matching the selected city.
filtered_df = df[df["City"] == city]

# Display the filtered results with an appropriate heading.
st.write(f"People in {city}:")
st.dataframe(filtered_df)  # Show the filtered table