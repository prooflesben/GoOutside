import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.title("📊 Sponsored Event Stats")


SideBarLinks()

SPONSOR_ID = 1


if st.button("Get Event Stats"):
    try:
        url = f"http://web-api:4000/sponsor/{SPONSOR_ID}/events/stats"  
        response = requests.get(url)

        if response.status_code == 200:
            events_data = response.json()
            df = pd.DataFrame(events_data)
            df.index += 1
            name_col = df.pop('name')      
            df.insert(0, 'name', name_col) 
            name_col = df.pop('engagement')
            df.insert(3, "total engagement", name_col)
            st.dataframe(df)

        elif response.status_code == 404:
            st.warning("No events found for this sponsor.")

        else:
            st.error("Something went wrong while fetching data.")

    except Exception as e:
        st.error(f"Request failed: {e}")
