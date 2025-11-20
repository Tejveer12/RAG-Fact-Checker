import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/check_claim"

st.set_page_config(page_title="RAG Fact Checker", page_icon="🧐")

st.title("🧐 RAG Fact Checker")
st.write("Enter a claim or statement, and the system will check it against verified facts.")

claim_input = st.text_area("Enter claim here:", height=120)

if st.button("Check Claim"):
    if not claim_input.strip():
        st.warning("Please enter a claim!")
    else:
        with st.spinner("Checking claim..."):
            try:
                response = requests.post(API_URL, json={"text": claim_input})
                if response.status_code == 200:
                    result = response.json()
                    print(result)

                    # Check if 'verdict' is a JSON string itself
                    try:
                        verdict = result.get("verdict", "Unknown")
                        score = result.get("score", 0.0)
                        evidence = result.get("evidence", [])
                        reason = result.get("reason", "No reason provided.")
                    except json.JSONDecodeError:
                        # Fallback if it's already proper
                        verdict = result.get("verdict", "Unknown")
                        score = result.get("score", 0.0)
                        reason = result.get("reason", "No reason provided.")


                    if verdict.lower() != "unverifiable":
                        if verdict == "true":
                            st.success(f"Verdict : {verdict}")
                        elif verdict.lower() == "false":
                            st.error(f"Verdict : {verdict}")

                        st.info(f"Score : {score:.2f}")

                        st.info(f"Evidence : {evidence}")

                        st.info(f"Reason: {reason}")
                    else:
                        st.info(f"Verdict : {verdict}")


                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to reach backend: {e}")
