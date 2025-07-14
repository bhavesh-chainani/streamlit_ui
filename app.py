import streamlit as st
import time
import pandas as pd
import re

# Set page config
st.set_page_config(page_title="Grant Proposal Assistant", layout="centered")

# Custom CSS
custom_css = """
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
.grant-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
}
.grant-table th, .grant-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
    vertical-align: middle;
}
.grant-table th {
    background-color: #f57c00;
    color: white;
}
.grant-table td a {
    text-decoration: none;
    color: #1a73e8;
    font-weight: bold;
}
.grant-table p {
    margin: 0.3em 0;
    text-align: left;
}
.grant-table ul {
    padding-left: 1.2em;
    text-align: left;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Display PwC logo
st.image("images/pwc_logo.png", width=100)

st.title("🧠 Grant Proposal Assistant")

default_prompt = "Climate resilience, Singapore"

# Session state setup
for key in [
    "chat_submitted",
    "report_generated",
    "schema_checked",
    "research_uploaded",
    "chatbot_output",
    "selected_grant_button",
    "grant_input",
]:
    if key not in st.session_state:
        st.session_state[key] = False if key != "chatbot_output" else ""

# User input
user_input = st.text_area(
    "Please specify your research area and location to view available funding opportunities/programmes.",
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

# Display chatbot response
if st.session_state.chat_submitted and st.session_state.chatbot_output:
    st.success("Here's the response:")
    st.markdown(st.session_state.chatbot_output)

    st.markdown(
        "### 📑 These are the grant proposals below, which grant would you like us to choose?"
    )

    try:
        grant_df = pd.read_excel("data/grant_companies.xlsx")

        # Format Link column to be clickable
        if "Link" in grant_df.columns:
            grant_df["Link"] = grant_df["Link"].apply(
                lambda url: (
                    f'<a href="{url}" target="_blank">Visit Link</a>'
                    if pd.notnull(url)
                    else ""
                )
            )

        # Format Summary column to show bullets and paragraphs correctly
        def format_summary(text):
            if pd.isnull(text):
                return ""
            lines = text.strip().split("\n")
            formatted_lines = []
            in_list = False
            for line in lines:
                if line.strip().startswith("-"):
                    if not in_list:
                        formatted_lines.append("<ul>")
                        in_list = True
                    formatted_lines.append(f"<li>{line.strip()[1:].strip()}</li>")
                else:
                    if in_list:
                        formatted_lines.append("</ul>")
                        in_list = False
                    formatted_lines.append(f"<p>{line.strip()}</p>")
            if in_list:
                formatted_lines.append("</ul>")
            return "".join(formatted_lines)

        if "Summary" in grant_df.columns:
            grant_df["Summary"] = grant_df["Summary"].apply(format_summary)

        html_table = grant_df.to_html(escape=False, index=False, classes="grant-table")
        st.markdown(html_table, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to load grant_companies.xlsx: {e}")

    st.markdown("### 🧾 Specify Grant Provider Name")
    grant_input = st.text_input(
        "Please type the name of the grant provider (e.g., A*STAR):"
    )
    if st.button("Submit Grant Provider"):
        if grant_input.strip():
            st.session_state.selected_grant_button = grant_input.strip()
            st.success(f"✅ Selected: {st.session_state.selected_grant_button}")

# Display selected grant template
if st.session_state.selected_grant_button:
    try:
        with st.spinner(
            f"🧾 Generating template report for {st.session_state.selected_grant_button}..."
        ):
            time.sleep(2)
            with open("data/template.txt", "r", encoding="utf-8") as f:
                template_text = f.read()
        st.success(f"📄 Showing Template for {st.session_state.selected_grant_button}")
        st.markdown(template_text, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Could not load template: {e}")

# Upload research paper
if st.session_state.chat_submitted and st.session_state.selected_grant_button:
    st.markdown(
        "**📄 Would you like me to leverage the best resources and create a grant report that aligns with this template?**"
    )
    st.markdown("**If yes, upload your initial research paper below 👇**")
    uploaded_file = st.file_uploader(
        "Upload your research paper (PDF, TXT, or DOCX)", type=["pdf", "txt", "docx"]
    )
    if uploaded_file is not None:
        st.session_state.research_uploaded = True
        st.success("Research paper uploaded successfully!")

# Generate report
if st.session_state.research_uploaded:
    if st.button("📝 Generate Report"):
        st.session_state.report_generated = True
        with st.spinner("Creating A*STAR-style report..."):
            loading_steps = [
                "Generating 1. 🧾 General Information",
                "Generating 2. 🧪 Scientific Abstract of the Proposal",
                "Generating 3. 🎯 Objectives",
                "Generating 4. 🔬 Methodology",
                "Generating 5. 📊 Expected Scientific Results of the Joint Research",
                "Generating 6. 🌍 Expected Economic and Social Impact of the Joint Research",
                "Generating 7. 🏷️ Keywords",
                "Generating 8. 📅 Research Topic and Work Plan",
                "Generating 9. 📘 Detailed Description of Joint Project",
                "Generating 10. ❗ Problem Statement",
                "Generating 11. 🔮 Future Prospect of Research",
                "Generating 12. 📚 Bibliography",
                "Generating 13. 💰 Budget Description",
                "Generating 14. 🤝 Work Contribution",
                "Generating 15. 📄 Curriculum Vitae",
                "Generating 16. 🙏 Acknowledgment",
                "Generating 17. 📎 Appendices",
            ]
            for step in loading_steps:
                st.text(step)
                time.sleep(0.6)
            time.sleep(1)

# Render report
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

# Check data schema
if st.session_state.report_generated:
    if st.button("🔍 Check Data Schema"):
        st.session_state.schema_checked = True
        try:
            table_data_df = pd.read_excel("data/table_data.xlsx")
            st.success("✅ Proposal Section Checklist")
            st.dataframe(table_data_df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Failed to load table_data.xlsx: {e}")
