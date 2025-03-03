import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set Streamlit page configuration
st.set_page_config(page_title="🚀 Streamlit Data Insights Application", layout="wide")

# Function to load dataset
@st.cache_data  # Cache data to optimize performance

def load_data(uploaded_file):
    """Loads a CSV file and preprocesses it by normalizing column names and handling datetime columns."""
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip().str.upper()  # Normalize column names to uppercase

        # Convert datetime columns safely
        for col in ["CREATED_DATE_TIME", "MODIFIED_DATE_TIME"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')  # Convert to datetime format
                df[col].fillna(df[col].min() if pd.notna(df[col].min()) else pd.Timestamp.today(), inplace=True)  # Handle missing dates

        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Function to display dataset summary
def display_summary(df):
    """Displays dataset preview, key statistics, and data types."""
    st.subheader("📊 Original Data Preview")
    st.write(df.head())  # Show first few rows

    st.subheader("📌 Dataset Summary:")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())  # Total missing values
    col4.metric("Duplicate Rows", df.duplicated().sum())  # Count duplicate rows

    st.subheader("📝 Data Types of Each Column")
    dtype_df = pd.DataFrame({"Column Name": df.columns, "Data Type": df.dtypes.values})
    st.dataframe(dtype_df)  # Display data types

# Function to handle missing values
def handle_missing_values(df):
    """Handles missing values by displaying missing data and providing an option to fill them with mode values."""
    st.subheader("⚠️ Handle Missing Values")

    missing_before = df.isnull().sum()
    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Before": missing_before.values
    })

    if missing_df["Missing Before"].sum() > 0:
        st.subheader("📋 Missing Values Before & After Imputation")
        missing_df["Missing After"] = missing_df["Missing Before"].values  # Placeholder for missing values after handling
        missing_table = st.dataframe(missing_df)

        # Button to fill missing values with mode
        if st.sidebar.button("Fill Missing with Mode"):
            df_copy = df.copy()
            for col in df_copy.columns:
                if df_copy[col].isnull().sum() > 0:
                    try:
                        mode_value = df_copy[col].mode()[0]  # Get most frequent value
                        df_copy[col].fillna(mode_value, inplace=True)
                    except IndexError:
                        pass  # Skip columns where mode is undefined

            missing_df["Missing After"] = df_copy.isnull().sum().values  # Update missing count after imputation
            missing_table.dataframe(missing_df)

            st.subheader("🆕 Imputed Dataset")
            st.dataframe(df_copy.head())
            return df_copy

    return df  # Return updated dataset

# Function to generate visualizations
def generate_visualizations(df):
    """Generates different types of visualizations based on user selection."""
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()  # Get categorical columns
    datetime_cols = [col for col in ["CREATED_DATE_TIME", "MODIFIED_DATE_TIME"] if col in df.columns]  # Get datetime columns

    st.sidebar.subheader("📊 Select Visualization Type")
    vis_option = st.sidebar.selectbox("Choose a chart type:", ["Bar Chart", "Pie Chart", "Line Chart", "Top Frequent Words"])

    # Bar Chart & Pie Chart for categorical columns
    if vis_option in ["Bar Chart", "Pie Chart"] and categorical_cols:
        column = st.sidebar.selectbox("📌 Select Categorical Column:", categorical_cols)
        value_counts_df = df[column].value_counts().reset_index()
        value_counts_df.columns = [column, "Count"]

        if vis_option == "Bar Chart":
            fig = px.bar(value_counts_df, x=column, y="Count", title=f"Distribution of {column}")
            st.plotly_chart(fig)
        elif vis_option == "Pie Chart":
            fig = px.pie(value_counts_df, names=column, values="Count", title=f"Distribution of {column}")
            st.plotly_chart(fig)

    # Line Chart for datetime columns
    elif vis_option == "Line Chart" and datetime_cols:
        date_column = st.sidebar.selectbox("📅 Select Date Column:", datetime_cols)
        count_df = df[date_column].dropna().dt.date.value_counts().reset_index()
        count_df.columns = [date_column, "Count"]
        count_df.sort_values(by=date_column, inplace=True)

        if not count_df.empty:
            fig = px.line(count_df, x=date_column, y="Count", title=f"Trend of {date_column}")
            st.plotly_chart(fig)
        else:
            st.warning("No valid date data available for visualization.")

    # Word Cloud for text data
    elif vis_option == "Top Frequent Words" and categorical_cols:
        column = st.sidebar.selectbox("📌 Select Categorical Column:", categorical_cols)
        text_data = " ".join(df[column].dropna().astype(str))
        
        if text_data.strip():
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.warning("No text data available for word cloud.")
    else:
        st.warning("No suitable columns available for selected visualization.")

# File uploader section
uploaded_file = st.sidebar.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

    # Remove duplicate rows if selected
    remove_duplicates = st.sidebar.checkbox("Remove Duplicate Rows")
    if remove_duplicates:
        df = df.drop_duplicates()
        st.sidebar.success("Duplicate rows removed!")

    # Display dataset preview and summary
    display_summary(df)

    # Handle missing values and update dataset
    df = handle_missing_values(df)

    # Generate visualizations
    generate_visualizations(df)

    # Export cleaned dataset
    st.sidebar.subheader("💾 Export Cleaned Data")
    cleaned_csv = df.to_csv(index=False).encode("utf-8")
    
    st.sidebar.download_button(
        label="📥 Download CSV",
        data=cleaned_csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )
