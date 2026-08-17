import streamlit as st
import pandas as pd

# 1. Setup the Webpage Title
st.set_page_config(page_title="Campus Directory", page_icon="📱")
st.title("🎓 Student Directory Lookup")

# 2. Load the Data (We use @st.cache_data so it loads instantly!)
@st.cache_data
def load_data():
    file_name = "Hall ticket no. 2025-26.xlsx"
    df = pd.read_excel(file_name, sheet_name='Hall Ticket Nos ', header=4)
    
    # Clean data just like before
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    name_col = 'Full Name( Surname First Name Middle Name) name as per 12th Marksheet'
    df = df.dropna(subset=[name_col])
    df['HTNo'] = df['HTNo'].fillna(0).astype('int64').astype(str)
    
    for col in ['Parent Mobile', 'Student Mobile']:
        df[col] = df[col].fillna(0).astype('int64').astype(str).replace('0', 'N/A')
        
    return df, name_col

# 3. Build the User Interface
try:
    df, name_col = load_data()
    
    # Create a nice search box
    query = st.text_input("🔍 Enter student name to search:", placeholder="Type a name here...")
    
    # 4. Search Logic
    if query:
        match = df[df[name_col].astype(str).str.lower().str.contains(query.lower().strip(), na=False)]
        
        if not match.empty:
            st.success(f"✅ Found {len(match)} match(es)")
            
            # Display results in neat cards
            for index, row in match.iterrows():
                with st.expander(f"👤 {row[name_col]}", expanded=True):
                    st.write(f"**Serial No (Div):** {row['Sno']}")
                    st.write(f"**Hall Ticket No:** {row['HTNo']}")
                    st.write(f"**DOB:** {row['DOB']}")
                    st.write(f"**Category:** {row['Caste Category']}")
                    st.write(f"**Mother Name:** {row['Mother Name']}")
                    st.write(f"**Student Mobile:** {row['Student Mobile']}")
                    st.write(f"**Parent Mobile:** {row['Parent Mobile']}")
                    st.write(f"**Email:** {row['Email']}")
        else:
            st.error("❌ No records found for that name.")

except FileNotFoundError:
    st.error("⚠️ Error: 'Hall ticket no. 2025-26.xlsx' not found in this folder.")
except Exception as e:
    st.error(f"⚠️ An error occurred: {e}")
