# TidyData-Project
The project aims to clean and reshape a Federal R&D Budgets dataset using tidy data concepts. The intention is to reshape the dataset to a more organized form so it can be more easily analyzed and visualized to see trends in government R&D expenditures over time.

Tidy Data Principles
To make data tidy:
Each variable has its own column.
Each observation is its own row.
Each sort of observational unit is its own table.

Steps in the Notebook
- Load and Inspect Data
- Read in the dataset as a Pandas DataFrame.
- Identify structure and missing value problems.

Data Cleaning & Transformation
- Melt the dataset from wide to long form.
- Extract and clean the Year column from column labels.
- Convert the Budget column to numeric type for analysis.
- Fill in missing values.

Exploratory Data Analysis (EDA)
- Make summary statistics.
- Create a pivot table to observe budget trends over time.

Visualizations
- Line plot of the total federal R&D spending over time.
- Bar plot of the departmental R&D budgets for the most recent year.

Instructions to Run the Notebook

Prerequisites
- Ensure that you have the following Python libraries installed:
- pip install pandas matplotlib seaborn

Running the Notebook
- Open up the Jupyter Notebook environment.
- Execute each cell sequentially to preprocess, analyze, and visualize the data.

Dataset Description
Source: Federal R&D Budgets dataset
Structure: Departments in rows, yearly budgets in columns with GDP values added.
Pre-processing: Reworked broad-format data to a long format for ease of analysis.

References
Pandas Cheat Sheet, https://www.geeksforgeeks.org/pandas-cheat-sheet/
Tidy Data Paper, https://vita.had.co.nz/papers/tidy-data.pdf 

Example Visuals
Examples of the plots are attached. 
[def]: image.png 
![alt text](image-1.png) 


# Tidy Data Project – U.S. Federal R&D Budget Analysis

This project demonstrates the transformation and analysis of messy financial data using the principles of **Tidy Data**, as outlined by Hadley Wickham. The dataset includes multi-year U.S. federal R&D spending across various government departments. By reshaping and cleaning the data using Python libraries, we produce visual insights that are easier to interpret and analyze.

---

## Project Overview

Tidy data refers to a standardized way of organizing datasets where:
- Each variable forms a column
- Each observation forms a row
- Each type of observational unit forms a table

This project applies these principles to transform a wide-format dataset into a long, tidy format. We then use visualizations to uncover trends in federal R&D spending over time.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/passionhood/Hood-Python-Portfolio.git
cd Hood-Python-Portfolio/TidyData-Project-main
```

### 2. Install Required Dependencies

Make sure Python 3.7+ is installed, then run:

```bash
pip install pandas matplotlib seaborn jupyterlab
```

### 3. Launch the Notebook

```bash
jupyter lab
```

Open and run the notebook file: `TidyData_Project_Notebook.ipynb`

---

## Dataset Description

- **Source**: U.S. federal R&D budget data (publicly available dataset used for educational purposes)
- **Structure**: Initially in wide format, with separate columns for each year’s spending per department
- **Preprocessing**:
  - Used `.melt()` to convert wide format into long format
  - Cleaned department labels and parsed numeric columns
  - Grouped and summarized spending by department and fiscal year

---

## Key Features & Output

- **Data Cleaning**: Removal of null values, standardization of labels
- **Transformation**: Used Tidy Data principles to restructure dataset
- **Visual Insights**:
  - Line plot: total R&D spending by year
  - Bar chart: department-level budget comparisons
  - Optional filters for department and year

---

## Visual Examples

> _Note: Screenshots should be saved to the `/images` folder in this repo for full display._

**Line Chart – Total Spending Over Time**  
![Line Chart](images/Spending_Trend_Line_Chart.png)

**Bar Chart – Spending by Department**  
![Bar Chart](images/Top_Agencies_Bar_Chart.png)

---

## References

- [Hadley Wickham: Tidy Data Paper (PDF)](https://vita.had.co.nz/papers/tidy-data.pdf)  
- [RStudio Tidyverse Cheat Sheet](https://github.com/rstudio/cheatsheets/blob/main/data-import.pdf)  
- [Pandas Documentation](https://pandas.pydata.org/docs/)  
- [Seaborn Documentation](https://seaborn.pydata.org/)  
- [Matplotlib Documentation](https://matplotlib.org/)

---


