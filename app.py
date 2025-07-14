import streamlit as st
import time
import pandas as pd
import re

# Set page config
st.set_page_config(page_title="Grant Proposal Assistant", layout="centered")

# Custom CSS for highlighting and buttons
custom_css = '''
<style>
.missing-info {
    background-color: #fff2ac;
    padding: 2px 4px;
    border-radius: 2px;
}
.button {
    background-color: #f57c00;
    color: white;
    padding: 0.8em 1.5em;
    margin: 0.4em auto;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    width: 60%;
    display: block;
    text-align: center;
    transition: background-color 0.3s ease;
}
.button:hover {
    background-color: #ef6c00;
}
</style>
'''
st.markdown(custom_css, unsafe_allow_html=True)

# Display PwC logo
st.image("images/pwc_logo.png", width=100)

st.title("🧠 Grant Proposal Assistant")

# Default prompt
default_prompt = (
    "I would like to apply for a grant to fund research in healthcare in Singapore,"
    " which companies provide these grants?"
)

# Initialize session state
if "chat_submitted" not in st.session_state:
    st.session_state.chat_submitted = False
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "schema_checked" not in st.session_state:
    st.session_state.schema_checked = False
if "research_uploaded" not in st.session_state:
    st.session_state.research_uploaded = False
if "chatbot_output" not in st.session_state:
    st.session_state.chatbot_output = ""
if "selected_grant_button" not in st.session_state:
    st.session_state.selected_grant_button = None

# Step 1: Initial Chatbot
user_input = st.text_area(
    "Ask me anything about your grant proposal:",
    value=default_prompt,
    height=68,
)

if st.button("Submit Query"):
    if user_input.strip():
        st.session_state.chat_submitted = True
        st.session_state.report_generated = False
        st.session_state.schema_checked = False
        st.session_state.research_uploaded = False
        st.session_state.selected_grant_button = None
        with st.spinner("Generating response..."):
            time.sleep(2)
            with open("data/initial_chatbot_response.txt", "r", encoding="utf-8") as f:
                st.session_state.chatbot_output = f.read()

# Display chatbot response if available
if st.session_state.chat_submitted and st.session_state.chatbot_output:
    st.success("Here's the response:")
    st.markdown(st.session_state.chatbot_output)

    # Grant Proposal Selection
    st.markdown("### 📑 These are the grant proposals above, which grant would you like us to choose?")
    
    try:
        grant_df = pd.read_excel("data/grant_companies.xlsx")
        st.dataframe(grant_df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Failed to load grant_companies.xlsx: {e}")

    st.markdown("### 🎯 Select Grant Provider")

    # Central aligned button-based selection (one per line)
    providers = [
        "A*STAR",
        "NMRC (MOH)",
        "National Research Foundation",
        "Enterprise Singapore",
        "Temasek Foundation",
    ]
    for provider in providers:
        if st.button(provider, key=provider):
            st.session_state.selected_grant_button = provider
            st.success(f"✅ Selected: {provider}")

# Display selected grant template with buffer time
if st.session_state.selected_grant_button:
    try:
        with st.spinner(f"🧾 Generating template report for {st.session_state.selected_grant_button}..."):
            time.sleep(2)
            with open("data/template.txt", "r", encoding="utf-8") as f:
                template_text = f.read()
        st.success(f"📄 Showing Template for {st.session_state.selected_grant_button}")
        st.markdown(template_text, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Could not load template: {e}")

# Step 2: Upload Research Paper
if st.session_state.chat_submitted and st.session_state.selected_grant_button:
    st.markdown("**📄 Would you like me to leverage the best resources and create a grant report that aligns with this template?**")
    st.markdown("**If yes, upload your initial research paper below 👇**")
    uploaded_file = st.file_uploader("Upload your research paper (PDF, TXT, or DOCX)", type=["pdf", "txt", "docx"])
    if uploaded_file is not None:
        st.session_state.research_uploaded = True
        st.success("Research paper uploaded successfully!")

# Step 3: Generate Report
if st.session_state.research_uploaded:
    if st.button("📝 Generate Report"):
        st.session_state.report_generated = True
        with st.spinner("Creating A*STAR-style report..."):
            loading_steps = [
                "Generating 1. 🧬 Introduction",
                "Generating 2. 🎯 Scientific Objectives",
                "Generating 3. 🧪 Methodology",
                "Generating 4. 📈 Expected Outcomes",
                "Generating 5. 🇸🇬 Relevance to Singapore & A*STAR RIE2025 Priorities",
                "Generating 6. 👥 Personnel & Team Composition",
                "Generating 7. 🗓️ Workplan & Milestones",
                "Generating 8. ⚖️ Ethics & Regulatory Considerations",
                "Generating 9. 💸 Detailed Budget",
                "Generating 10. 📎 Appendices",
            ]
            for step in loading_steps:
                st.text(step)
                time.sleep(1)
            time.sleep(1)

# Step 4: Render Final Report
if st.session_state.report_generated:
    try:
        with open("data/dummy_report.txt", "r", encoding="utf-8") as f:
            report = f.read()

        st.success("📝 Grant Proposal Report")

        highlighted_report = re.sub(
            r"(Information Not Available)",
            r"<span class='missing-info'>\1</span>",
            report,
        )

        with st.expander("🔍 View Full Grant Report", expanded=True):
            st.markdown(highlighted_report, unsafe_allow_html=True)

        st.download_button(
            label="📄 Download Report as .txt",
            data=report,
            file_name="grant_proposal.txt",
            mime="text/plain",
        )
    except Exception as e:
        st.error(f"❌ Failed to load grant report: {e}")

# Step 5: Data Schema Match
if st.session_state.report_generated:
    if st.button("🔍 Check Data Schema"):
        st.session_state.schema_checked = True
        try:
            table_data_df = pd.read_excel("data/table_data.xlsx")
            st.success("✅ Proposal Section Checklist")
            st.dataframe(table_data_df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Failed to load table_data.xlsx: {e}")
