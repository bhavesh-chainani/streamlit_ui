import streamlit as st
import time
import pandas as pd

# Set page config
st.set_page_config(page_title="Grant Proposal Assistant", layout="centered")


# Display PwC logo
st.image("images/pwc_logo.png", width=200)

st.title("🧠 Grant Proposal Assistant (Demo)")

# Initialize session state
if 'chat_submitted' not in st.session_state:
    st.session_state.chat_submitted = False
if 'report_requested' not in st.session_state:
    st.session_state.report_requested = False
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'schema_checked' not in st.session_state:
    st.session_state.schema_checked = False

# Step 1: Chatbot Input
user_input = st.text_input("Ask anything about Grant Proposal:")

if st.button("Submit Query"):
    if user_input.strip() != "":
        st.session_state.chat_submitted = True
        st.session_state.report_requested = False
        st.session_state.report_generated = False
        st.session_state.schema_checked = False

        with st.spinner("Searching resources and preparing guidance..."):
            time.sleep(2)  # Simulated loading
            with open("data/chatbot_response.txt", "r") as file:
                chatbot_response = file.read()
            st.success("Here's the guidance based on your query:")
            st.markdown(chatbot_response)

        if st.session_state.chat_submitted:
            if st.button("📄 Would you like me to leverage the best resources and create a grant report for this?"):
                st.session_state.report_requested = True
    else:
        st.warning("Please enter a valid query.")

# Step 2: Generate Dummy Grant Report
if st.session_state.report_requested:
    with st.spinner("Compiling grant report with references..."):
        time.sleep(2)
        with open("data/dummy_report.txt", "r") as file:
            report = file.read()
        st.success("Grant Report Generated")
        st.text_area("📑 Full Grant Report", report, height=400)

    if st.button("✅ Would you like to check if this report aligns with the required template?"):
        st.session_state.report_generated = True

# Step 3: Schema Validation
if st.session_state.report_generated:
    with st.spinner("Validating against required schema..."):
        time.sleep(2)
        with open("data/dummy_report.txt", "r") as file:
            report = file.read().lower()

        # Simulated schema checks
        schema_checklist = {
            "Sample Letter": "sample letter" in report,
            "Number of Personnel": any(x in report for x in ["personnel", "team", "staff"]),
            "Grant Amount": any(x in report for x in ["grant amount", "total funding", "budget"]),
            "Research Objectives": "objectives" in report,
            "Source Citations": "source:" in report
        }

        results_df = pd.DataFrame(list(schema_checklist.items()), columns=["Field", "Present"])
        st.success("📋 Schema Validation Checklist")
        st.dataframe(results_df)
