Streamlit Insights Application

Objective
      This application allows users to upload a CSV file and generate interactive visualizations that provide valuable insights for Data Engineering/Analytics.

Features
 1. Data Handling & Exploration
 2. Upload a CSV file and load it into a Pandas DataFrame.
 3. Normalize column names to uppercase.
 4. Detect and convert datetime columns (CREATED_DATE_TIME, MODIFIED_DATE_TIME).
 5. Display dataset preview, key statistics, and data types.
 6. Handle missing values with an option to fill them using mode.
 7. Remove duplicate rows.

Insightful Visualizations
 1. Bar Chart & Pie Chart: Display distribution of categorical data.
 2. Line Chart: Visualize trends over time for datetime columns.
 3. Word Cloud: Generate word clouds from categorical column text data.
    
User-Friendly UI/UX
 1. Clean and interactive UI with sidebar navigation.
 2. Dynamic selection of columns for visualization.
 3. Sidebar-based options for missing value handling and duplicate row removal.
 4. Option to download the cleaned dataset.

Tech Stack Used
 1. Python – Core programming language
 2. Streamlit – Interactive UI
 3. Pandas – Data handling & processing
 4. Plotly – Data visualization
 5. Matplotlib & WordCloud – Graphical representations
    
Setup Instructions
1. Clone the repository:
   git clone https://github.com/pratikshayadav10/Pratiksha-Yadav.git  
   cd Pratiksha-Yadav  
2. Install dependencies:
   pip install -r requirements.txt  
3. Run the Streamlit application:
   streamlit run app.py
   
GitHub Repository
  GitHub Link: https://github.com/pratikshayadav10/Pratiksha-Yadav.git
