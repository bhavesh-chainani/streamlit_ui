import streamlit as st
import time
import pandas as pd
import re

# Set page config
st.set_page_config(page_title="Grant Proposal Assistant", layout="centered")

# Custom CSS for highlighting missing info
highlight_css = """
<style>
.missing-info {
    background-color: #fff2ac;
    padding: 2px 4px;
    border-radius: 2px;
}
</style>
"""
st.markdown(highlight_css, unsafe_allow_html=True)

# Display PwC logo
st.image("images/pwc_logo.png", width=100)

st.title("🧠 Grant Proposal Assistant")

# Default prompt
default_prompt = (
    "I would like to apply for a grant to fund research in healthcare "
    "following ASTAR Singapore format, what are the specific instructions "
    "that provide this funding?"
)

# Initialize session state (fixed to preserve existing values)
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

# Step 1: Initial Chatbot
user_input = st.text_input(
    "Ask me anything about your grant proposal:", value=default_prompt
)

if st.button("Submit Query"):
    if user_input.strip():
        st.session_state.chat_submitted = True
        st.session_state.report_generated = False
        st.session_state.schema_checked = False
        st.session_state.research_uploaded = False
        with st.spinner("Generating response..."):
            time.sleep(2)
            with open("data/chatbot_response.txt", "r", encoding="utf-8") as f:
                st.session_state.chatbot_output = f.read()

# Display chatbot response if available
if st.session_state.chat_submitted and st.session_state.chatbot_output:
    st.success("Here's the response:")
    st.markdown(st.session_state.chatbot_output)
    st.markdown(
        "**📄 Would you like me to leverage the best resources and create a grant report "
        "that aligns with this template?**"
    )
    st.markdown("**If yes, upload your initial research paper below 👇**")

# Step 2: Upload Research Paper
if st.session_state.chat_submitted:
    uploaded_file = st.file_uploader(
        "Upload your research paper (PDF, TXT, or DOCX)", type=["pdf", "txt", "docx"]
    )
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
                time.sleep(0.3)
            time.sleep(1)

        with open("data/dummy_report.txt", "r", encoding="utf-8") as f:
            report = f.read()

        st.success("📝 Grant Proposal Report")

        # Highlight "Information Not Available" inside bullet points
        highlighted_report = re.sub(
            r"(Information Not Available)",
            r"<span class='missing-info'>\1</span>",
            report,
        )

        # Render the markdown with highlights
        with st.expander("🔍 View Full Grant Report", expanded=True):
            st.markdown(highlighted_report, unsafe_allow_html=True)

        # Allow the user to download the report
        st.download_button(
            label="📄 Download Report as .txt",
            data=report,
            file_name="grant_proposal.txt",
            mime="text/plain",
        )

# Step 4: Data Schema Match
if st.session_state.report_generated:
    if st.button("🔍 Check Data Schema"):
        st.session_state.schema_checked = True
        with open("data/dummy_report.txt", "r", encoding="utf-8") as f:
            report_text = f.read().lower()

        schema_results = {
            "Summary": "summary" in report_text,
            "Number of Personnel present": any(
                kw in report_text for kw in ("personnel", "team", "staff")
            ),
            "Grant amount": any(
                kw in report_text for kw in ("grant", "amount", "funding")
            ),
        }

        results_df = pd.DataFrame(
            list(schema_results.items()), columns=["Field", "Present"]
        )
        st.success("Schema Validation Result:")
        st.table(results_df)
