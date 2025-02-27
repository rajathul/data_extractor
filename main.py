# import streamlit as st
# import pandas as pd
# import numpy as np

# st.title("Uber pickups in NYC")

# DATE_COLUMN = 'date/time'
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache_data
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache_data)")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')

# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# st.subheader('Map of all pickups')
# hour_to_filter = st.slider('hour', 0, 23, 17) #hour_to_filter = 17
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
# st.subheader(f"Map of all pickups at {hour_to_filter}:00")
# st.map(filtered_data)

import streamlit as st
import pandas as pd
import io
from extract_text import extract_text
from validation_check import is_valid_document
from extract_info import extract_info
from save_data import save_to_csv

# Streamlit UI
st.title("Finance Document Processor")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    st.write("Processing document...")

    # Extract text from PDF
    document_text = extract_text(uploaded_file)

    # Validate document
    status, document_type, message = is_valid_document(document_text)

    if status:
        st.success(f"Document type: {document_type}")
        
        # Extract information
        extracted_data = extract_info(document_text)
        
        #
        for key, value in extracted_data.items():
            if isinstance(value, tuple):
                extracted_data[key] = ", ".join(map(str, value))  # Convert tuple to a comma-separated string

        # Convert dictionary to DataFrame
        df = pd.DataFrame(list(extracted_data.items()), columns=["Field", "Value"])
        st.dataframe(df)  # Display data

        # Convert to CSV for download
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="extracted_data.csv",
            mime="text/csv"
        )
    else:
        st.error(message)