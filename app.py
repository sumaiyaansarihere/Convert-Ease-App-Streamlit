
import streamlit as st
import pandas as pd
import os
from io import BytesIO

#  App Configuration
st.set_page_config(page_title="Data Sweeper 🚀", layout='wide')

# App Ttle
st.title("🔄 **CONVERT EASE:**")

# subtle
st.markdown('<h2 style="color: #B22222; font-weight: bold;">🚀 Effortlessly Switch Between CSV & Excel – Clean, Convert, and Download in One Click!</h2>', unsafe_allow_html=True)

#  File Upload Section
uploaded_files = st.file_uploader("📤 Upload your files (CSV or EXCEL):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # Display File 
        st.write(f"**📄 File Name:** `{file.name}`")
        st.write(f"**📏 File Size:** `{file.size / 1024:.2f} KB`")

        #  **Data Preview**
        st.subheader("🔍 **Preview of Your Data:**")
        st.dataframe(df.head())

        # Data Cleaning Options**
        st.subheader("🧼 **Data Cleaning Options**")
        if st.checkbox(f"✅ Clean Data for `{file.name}`"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove Duplicates from `{file.name}`"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"📊 Fill Missing Values for `{file.name}`"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Have Been Filled!")

        #  **Column Selection**
        st.subheader("🎯 **Select Columns to Convert**")
        columns = st.multiselect(f"📌 Choose Columns for `{file.name}`", df.columns, default=df.columns)
        df = df[columns]

        # **Data Visualization**
        st.subheader("📈 **Data Visualization & Insights**")  

        # **Stylish Visualization Subtitle (Dark Red)**
        st.markdown('<h3 style="color: #B22222; font-weight: bold;">📊 Visualize Your Data with Interactive Charts!</h3>', unsafe_allow_html=True)

        if st.checkbox(f"📊 Show Visualization for `{file.name}`"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #  **File Conversion Options**
        st.subheader("🔄 **Conversion Options**")
        conversion_type = st.radio(f"🔀 Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

        # **Convert & Download Button**
        if st.button(f"💾 Convert & Download `{file.name}`"):
            buffer = BytesIO()
            converted_file_name = file.name.rsplit(".", 1)[0]  # Extract file name without extension

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = f"{converted_file_name}.csv"
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                file_name = f"{converted_file_name}.xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            #  **Download Button**
            st.download_button(
                label=f"⬇️ Download `{file_name}`",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    #  Success Message
    st.success("🎉 **All files processed successfully!**")



 #MY FOOTER
footer = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #262730;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 3px solid #B22222; /* Make it bolder if needed */
        }
    </style>
    <div class="footer">
        🚀 <b>ConvertEase</b> | Developed by <b>Sumaiya Ansari</b> | © 2025 All Rights Reserved.
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
