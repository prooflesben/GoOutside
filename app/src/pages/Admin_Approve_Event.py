# pages/admin_event_moderation.py
import streamlit as st
import requests, pandas as pd

API_BASE   = "http://web-api:4000"   # change if your host/port differ
ADMIN_ID   = 1                       # ← hard‑coded admin ID

st.title("🗂️  Moderation – Pending Events")

# ------------------------------------------------------------
# Load all events that still need approval
# ------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_pending():
    r = requests.get(f"{API_BASE}/events/not-approved")
    return pd.DataFrame(r.json()) if r.status_code == 200 else pd.DataFrame()

def reload():
    st.cache_data.clear()            # flush cache → next call reloads
    st.experimental_rerun()

df = load_pending()

if df.empty:
    st.info("No pending events to review.")
    st.stop()

# Move “name” to first column for readability
if "name" in df.columns:
    df.insert(0, "name", df.pop("name"))

st.dataframe(df, hide_index=True, use_container_width=True)

st.divider()
st.markdown("### Actions")

for _, row in df.iterrows():
    event_id   = row["event_id"]
    event_name = row["name"]

    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"✅ Approve  •  {event_name}", key=f"approve_{event_id}"):
            resp = requests.put(f"{API_BASE}/admin/{ADMIN_ID}/event/{event_id}")
            if resp.status_code == 200:
                st.success(f"Approved: {event_name}")
                reload()
            else:
                st.error(f"Approve failed ({resp.status_code})")

    with c2:
        if st.button(f"🗑️ Delete  •  {event_name}", key=f"delete_{event_id}"):
            resp = requests.delete(f"{API_BASE}/admin/{ADMIN_ID}/event/{event_id}")
            if resp.status_code == 200:
                st.warning(f"Deleted: {event_name}")
                reload()
            else:
                st.error(f"Delete failed ({resp.status_code})")
