import urllib.parse
import streamlit as st

from generator import generate_pitch
from leads import fetch_leads

st.set_page_config(
    page_title="SponsorMatch | Corporate Sponsor Finder",
    page_icon="⚡",
    layout="wide",
)

# Title & Subheading
st.title("⚡ SponsorMatch CRM")
st.caption("Find local corporate sponsors and generate tailored pitch proposals.")

# Sidebar Credentials
st.sidebar.header("🔑 API Credentials")

user_google_key = st.sidebar.text_input("Google Places API Key", type="password")
user_groq_key = st.sidebar.text_input("Groq API Key ($0 Free Tier)", type="password")

# Fall back to Streamlit Secrets if sidebar inputs are empty
google_key = user_google_key or st.secrets.get("GOOGLE_MAPS_KEY", "")
groq_key = user_groq_key or st.secrets.get("GROQ_API_KEY", "")

st.sidebar.markdown("[Get Free Groq Key](https://console.groq.com/)")

# Initialize Session State Variables
if "leads" not in st.session_state:
    st.session_state["leads"] = []
if "generated_pitch" not in st.session_state:
    st.session_state["generated_pitch"] = ""

# Main App Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("🔍 Find Local Sponsors")

    location = st.text_input("Location / City", value="Austin, TX", help="City name or ZIP code")
    keyword = st.text_input("Industry / Business Type", value="Engineering, Manufacturing, Technology")
    team_info = st.text_area(
        "Team Info & Sponsorship Goals",
        value="Robotics Team competing in FIRST Robotics. Looking for engineering/machining sponsors.",
        height=100,
    )
    league = st.text_input("League / Organization Name", value="FIRST Robotics")

    if st.button("🔍 Find Local Corporate Sponsors", use_container_width=True):
        if not google_key:
            st.error("Please enter a Google Places API Key or set GOOGLE_MAPS_KEY in Streamlit Secrets.")
        else:
            with st.spinner("Searching for local business leads..."):
                try:
                    leads = fetch_leads(location=location, keyword=keyword, api_key=google_key)
                    st.session_state["leads"] = leads
                    st.success(f"Found {len(leads)} local business leads!")
                except Exception as e:
                    st.error(f"Error fetching leads: {e}")

with col2:
    st.subheader("⚡ AI Pitch Generator")

    if st.session_state["leads"]:
        lead_names = [lead["name"] for lead in st.session_state["leads"]]
        selected_name = st.selectbox("Select a Business to Pitch", lead_names)

        # Retrieve selected lead object
        selected_lead = next((item for item in st.session_state["leads"] if item["name"] == selected_name), None)

        if st.button("⚡ Generate Custom Pitch Proposal", use_container_width=True):
            if not groq_key:
                st.error("Please enter a Groq API Key or set GROQ_API_KEY in Streamlit Secrets.")
            else:
                with st.spinner("Generating customized sponsorship pitch..."):
                    try:
                        pitch = generate_pitch(team_info, selected_lead, groq_key)
                        st.session_state["generated_pitch"] = pitch
                    except Exception as e:
                        st.error(f"Error generating pitch: {e}")

        if st.session_state.get("generated_pitch"):
            edited_pitch = st.text_area(
                "Customized Pitch Draft",
                value=st.session_state["generated_pitch"],
                height=250,
            )

            # Encode mailto string for one-click email opening
            subject = urllib.parse.quote(f"Sponsorship Opportunity – {league} Team")
            body = urllib.parse.quote(edited_pitch)
            mailto_url = f"mailto:?subject={subject}&body={body}"

            st.markdown(
                f'<a href="{mailto_url}" target="_blank">'
                f'<button style="width:100%; background-color:#FF4B4B; color:white; padding:12px; border:none; border-radius:8px; cursor:pointer;">'
                f'✉️ Open Pre-Filled Pitch in Email Client</button></a>',
                unsafe_allow_html=True,
            )
    else:
        st.info("Enter your API credentials in the sidebar and click 'Find Local Corporate Sponsors' to populate local leads.")