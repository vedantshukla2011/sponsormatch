import streamlit as st
import pandas as pd
import urllib.parse
from leads import get_leads
from generator import generate_pitch

# Page Setup
st.set_page_config(
    page_title="SponsorMatch | Robotics CRM",
    page_icon="🤖",
    layout="wide"
)

# Sidebar - API Credentials
with st.sidebar:
    st.header("🔑 API Credentials")
    google_key = st.text_input("Google Places API Key", type="password")
    groq_key = st.text_input("Groq API Key ($0 Free Tier)", type="password")
    st.markdown("[Get Free Groq Key](https://console.groq.com/keys)")

st.title("🤖 SponsorMatch")
st.subheader("AI-Driven CRM for Robotics Team Fundraising")

# Layout into two equal columns
col1, col2 = st.columns([1, 1])

# Column 1: Team Search & Controls
with col1:
    st.header("📋 Team Parameters")
    league = st.selectbox(
        "League",
        ["VEX Robotics Competition", "FIRST Robotics Competition (FRC)", "FIRST Tech Challenge (FTC)", "BEST Robotics"]
    )
    key_highlight = st.text_input("Key Highlight", value="World Championships Qualifier")
    request_details = st.text_input("Request Details", value="Corporate/Business Sponsorship")
    zip_code = st.text_input("Team Zip Code", value="75078")
    radius = st.slider("Search Radius (Miles)", min_value=5, max_value=50, value=25)

    search_clicked = st.button("🔍 Find Local Corporate Sponsors", type="primary", use_container_width=True)

# Initialize Session State Variables
if "leads" not in st.session_state:
    st.session_state["leads"] = []

if "generated_pitch" not in st.session_state:
    st.session_state["generated_pitch"] = ""

# Handle Lead Search Action
if search_clicked:
    if not google_key or not groq_key:
        st.error("Please enter both your Google Places API Key and Groq API Key in the sidebar.")
    else:
        with st.spinner("Searching for local corporate sponsors..."):
            try:
                leads = get_leads(zip_code, radius, google_key)
                if not leads:
                    st.warning("No local sponsors found within this radius. Try increasing the search radius.")
                else:
                    st.session_state["leads"] = leads
                    st.success(f"Found {len(leads)} potential corporate sponsors!")
            except Exception as e:
                st.error(f"Error fetching leads: {e}")

# Column 2: Lead CRM Table & Pitch Generator
with col2:
    st.header("🎯 Local Sponsor Leads")
    
    if st.session_state["leads"]:
        df = pd.DataFrame(st.session_state["leads"])
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.header("⚡ AI Pitch Generator")

        lead_names = [lead["Name"] for lead in st.session_state["leads"]]
        selected_lead_name = st.selectbox("Select a Business to Pitch", lead_names)

        selected_lead = next((lead for lead in st.session_state["leads"] if lead["Name"] == selected_lead_name), None)

        if st.button("⚡ Generate Custom Pitch Proposal", use_container_width=True):
            if selected_lead:
                with st.spinner("Generating customized sponsorship pitch with Llama 3..."):
                    try:
                        team_info = {
                            "league": league,
                            "highlight": key_highlight,
                            "request": request_details,
                            "zip_code": zip_code
                        }
                        pitch = generate_pitch(team_info, selected_lead, groq_key)
                        st.session_state["generated_pitch"] = pitch
                    except Exception as e:
                        st.error(f"Error generating pitch: {e}")

        if st.session_state["generated_pitch"]:
            edited_pitch = st.text_area("Customized Pitch Draft", value=st.session_state["generated_pitch"], height=250)
            
            # Encode mailto string for one-click email opening
            subject = urllib.parse.quote(f"Sponsorship Opportunity - {league} Team")
            body = urllib.parse.quote(edited_pitch)
            mailto_url = f"mailto:?subject={subject}&body={body}"
            
            st.markdown(
                f'<a href="{mailto_url}" target="_blank">'
                f'<button style="width:100%; background-color:#FF4B4B; color:white; padding:12px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; font-size:16px;">'
                f'✉️ Open Pre-Filled Pitch in Email Client</button>a>',
                unsafe_allow_html=True
            )
    else:
        st.info("Enter your API credentials in the sidebar and click 'Find Local Corporate Sponsors' to populate local leads.")