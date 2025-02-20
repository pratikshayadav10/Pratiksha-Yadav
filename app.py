import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to set the Streamlit page configuration and styling
def set_page_config():
    st.set_page_config(page_title="Streamlit Insights Application", layout="wide")

    # Custom CSS to enhance UI design
    st.markdown("""
        <style>
            body {
                background-color:rgb(247, 248, 250);
                color: #e0e0e0;
                font-family: 'Poppins', sans-serif;
            }
            .stApp, .stDataFrame, .css-2trqyj, .css-1d391kg, .stSidebar {
                background-color:rgb(252, 251, 251) !important;
                color: #ffffff !important;
                padding: 15px;
                border-radius: 10px;
            }
            .stButton>button {
                background: linear-gradient(90deg, #06b6d4, #3b82f6);
                color: white !important;
                border-radius: 10px;
                font-weight: bold;
            }
            .stButton>button:hover {
                background: linear-gradient(90deg, #0284c7, #2563eb);
            }
            h1, h2, h3, h4, h5, h6 {
                color: #06b6d4 !important;
                font-weight: bold;
            }
            .custom-box {
                background: rgba(255, 255, 255, 0.1);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                color: #e0e0e0 !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Function to upload CSV file using Streamlit's sidebar
def upload_data():
    st.sidebar.header("Upload Your Data")
    return st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Function to preprocess data (handle datetime columns)
def preprocess_data(df):
    # Identify columns that contain 'date' in their name
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    
    if date_cols:
        # Convert first detected date column to datetime format
        df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors='coerce')
        
        # Extract Year-Month for trend analysis
        df['Year-Month'] = df[date_cols[0]].dt.to_period("M")
        st.write(f"Converted {date_cols[0]} to datetime format")
    
    return df

# Function to display the dataset preview and missing values
def display_data(df):
    st.write("### Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    st.write("### Missing Values")
    st.write(df.isnull().sum())

# Function to plot the distribution of numeric columns
def plot_distribution(df):
    numeric_cols = df.select_dtypes(include=["int", "float"]).columns
    
    if not numeric_cols.empty:
        column = st.selectbox("Select a Numeric Column:", numeric_cols)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df[column], bins=20, kde=True, ax=ax, color="#06b6d4")
        ax.set_title(f"Distribution of {column}", color="white")
        
        st.pyplot(fig)
    else:
        st.warning("No numeric columns found in the dataset.")

# Function to plot correlation heatmap of numeric columns
def plot_correlation(df):
    numeric_df = df.select_dtypes(include=["number"])
    
    if numeric_df.shape[1] > 1:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap", color="white")
        
        st.pyplot(fig)
    else:
        st.warning("Not enough numeric data to generate a correlation heatmap.")

# Function to visualize the most frequent categories in categorical columns
def plot_top_categories(df):
    categorical_cols = df.select_dtypes(include=["object"]).columns
    
    if not categorical_cols.empty:
        category_col = st.selectbox("Select a Categorical Column:", categorical_cols)
        st.bar_chart(df[category_col].value_counts())
    else:
        st.warning("No categorical columns found in the dataset.")

# Function to plot a trend analysis based on date column
def plot_trend_analysis(df):
    if 'Year-Month' in df.columns:
        numeric_cols = df.select_dtypes(include=["int", "float"]).columns
        
        if not numeric_cols.empty:
            trend_col = st.selectbox("Select a Numeric Column for Trend Analysis:", numeric_cols)
            
            if trend_col:
                trend_data = df.groupby('Year-Month')[trend_col].sum()
                st.line_chart(trend_data)
        else:
            st.warning("No numeric columns found for trend analysis.")
    else:
        st.warning("No datetime column available for trend analysis.")

# Function to detect and visualize outliers using boxplots
def plot_outliers(df):
    numeric_cols = df.select_dtypes(include=["int", "float"]).columns
    
    if not numeric_cols.empty:
        column = st.selectbox("Select a Numeric Column for Outlier Detection:", numeric_cols)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(y=df[column], ax=ax, color="#06b6d4")
        ax.set_title(f"Boxplot of {column}", color="white")
        
        st.pyplot(fig)
    else:
        st.warning("No numeric columns found in the dataset.")

# Main function to drive the Streamlit application
def main():
    set_page_config()
    
    st.title("Streamlit Insights Application")
    st.markdown("<div class='custom-box'><b>Upload a CSV file to explore and visualize key insights interactively.</b></div>", unsafe_allow_html=True)
    
    uploaded_file = upload_data()
    
    if uploaded_file:
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Preprocess the data (convert datetime columns)
        df = preprocess_data(df)
        
        # Display data preview and missing values
        display_data(df)
        
        # Sidebar for selecting analysis type
        st.sidebar.header("Data Insights")
        insights_option = st.sidebar.selectbox("Select an Analysis Type", [
            "Distribution", "Correlation", "Top Categories", "Trend Analysis", "Outliers"
        ])
        
        # Call respective functions based on user selection
        if insights_option == "Distribution":
            plot_distribution(df)
        elif insights_option == "Correlation":
            plot_correlation(df)
        elif insights_option == "Top Categories":
            plot_top_categories(df)
        elif insights_option == "Trend Analysis":
            plot_trend_analysis(df)
        elif insights_option == "Outliers":
            plot_outliers(df)
        
        st.success("Data Analysis Completed!!")
    else:
        st.info("Upload a CSV file to get insights!")

# Entry point of the Streamlit application
if __name__ == "__main__":
    main()
