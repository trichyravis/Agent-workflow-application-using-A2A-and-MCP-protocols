
import streamlit as st

st.set_page_config(page_title="Adjunct Faculty Eligibility Checker", layout="wide")

st.title("🎓 Adjunct Faculty Eligibility Checker (US Universities)")

st.markdown("### Check if you can apply for adjunct roles like Aurora University")

# -----------------------
# INPUT SECTION
# -----------------------

col1, col2 = st.columns(2)

with col1:
    citizenship = st.selectbox(
        "Citizenship Status",
        ["Indian (Non-US Citizen)", "US Citizen", "Permanent Resident (Green Card)"]
    )

    visa_status = st.selectbox(
        "Current Visa Status",
        ["No US Visa", "F1 (OPT/CPT)", "H1B", "H4 EAD", "Other Work Authorization"]
    )

with col2:
    qualification = st.selectbox(
        "Highest Qualification",
        ["Master’s Degree", "PhD"]
    )

    experience = st.selectbox(
        "Teaching/Industry Experience",
        ["< 1 year", "1–3 years", "3+ years"]
    )

# -----------------------
# LOGIC ENGINE
# -----------------------

def evaluate_candidate(citizenship, visa_status, qualification, experience):
    score = 0
    remarks = []

    # Work Authorization (CRITICAL)
    if visa_status in ["H1B", "H4 EAD", "Other Work Authorization"]:
        score += 50
        remarks.append("✔ Valid US work authorization")
    elif visa_status == "F1 (OPT/CPT)":
        score += 30
        remarks.append("⚠ Limited work authorization")
    else:
        score -= 50
        remarks.append("❌ No US work authorization")

    # Qualification
    if qualification == "PhD":
        score += 30
        remarks.append("✔ Strong academic profile")
    else:
        score += 15
        remarks.append("✔ Meets minimum requirement")

    # Experience
    if experience == "3+ years":
        score += 20
    elif experience == "1–3 years":
        score += 10

    return score, remarks

score, remarks = evaluate_candidate(citizenship, visa_status, qualification, experience)

# -----------------------
# OUTPUT SECTION
# -----------------------

st.markdown("---")
st.subheader("📊 Evaluation Result")

col3, col4 = st.columns(2)

with col3:
    st.metric("Eligibility Score", score)

with col4:
    if score >= 70:
        st.success("✅ High Chance")
    elif score >= 40:
        st.warning("⚠ Moderate Chance")
    else:
        st.error("❌ Very Low Chance")

# -----------------------
# DETAILS
# -----------------------

st.markdown("### 🧾 Key Insights")
for r in remarks:
    st.write(r)

# -----------------------
# FINAL VERDICT
# -----------------------

st.markdown("### 🎯 Final Recommendation")

if visa_status == "No US Visa":
    st.error("👉 You can apply, but cannot work without US authorization.")
    st.info("💡 Strategy: First secure a job/visa, then apply for adjunct roles.")
elif score >= 70:
    st.success("👉 You are well-positioned to apply for adjunct roles.")
elif score >= 40:
    st.warning("👉 You can apply, but competition may be high.")
else:
    st.error("👉 Focus on improving visa status or qualifications.")

# -----------------------
# STRATEGY SECTION
# -----------------------

st.markdown("### 🚀 Suggested Strategy")

st.write("""
1. Secure US work authorization (H1B / EAD)
2. Target local universities
3. Apply for online adjunct roles
4. Build teaching portfolio
""")
