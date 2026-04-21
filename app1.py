import streamlit as st

def evaluate_metric(value, weak, strong):
    if value < weak:
        return "🚨 Weak"
    elif value < strong:
        return "⚠️ Average"
    else:
        return "✅ Strong"

st.title("📊 Product Analytics Health Checker")

st.header("Enter Your Metrics")

# --- Dropdown with default "Select"
business_type = st.selectbox(
    "Business Type",
    ["Select", "SaaS", "D2C", "Marketplace"]
)

tracking = st.selectbox(
    "Tracking Quality",
    ["Select", "Good", "Average", "Poor"]
)

# --- Numeric inputs (default = None using empty input)
visitors = st.number_input("Monthly Visitors", min_value=0, value=None, placeholder="Enter value")
signups = st.number_input("Signups", min_value=0, value=None, placeholder="Enter value")
activated = st.number_input("Activated Users", min_value=0, value=None, placeholder="Enter value")
paying = st.number_input("Paying Users", min_value=0, value=None, placeholder="Enter value")

d1 = st.number_input("Day 1 Retention (%)", min_value=0.0, value=None, placeholder="Enter %")
d7 = st.number_input("Day 7 Retention (%)", min_value=0.0, value=None, placeholder="Enter %")
d30 = st.number_input("Day 30 Retention (%)", min_value=0.0, value=None, placeholder="Enter %")

# --- Submit Button
submit = st.button("Run Audit")

# --- Run logic only after submit
if submit:

    # Validation
    if business_type == "Select" or tracking == "Select":
        st.error("⚠️ Please select Business Type and Tracking Quality")
    
    elif None in [visitors, signups, activated, paying, d1, d7, d30]:
        st.error("⚠️ Please fill all input fields")
    
    else:
        # --- Calculations
        signup_rate = (signups / visitors * 100) if visitors > 0 else 0
        activation_rate = (activated / signups * 100) if signups > 0 else 0
        conversion_rate = (paying / activated * 100) if activated > 0 else 0


        st.header("📊 Benchmarking Analysis")

        signup_status = evaluate_metric(signup_rate, 15, 30)
        activation_status = evaluate_metric(activation_rate, 25, 40)
        conversion_status = evaluate_metric(conversion_rate, 5, 10)

        d1_status = evaluate_metric(d1, 20, 40)
        d7_status = evaluate_metric(d7, 15, 30)
        d30_status = evaluate_metric(d30, 10, 20)

        st.write(f"Signup Rate: {signup_rate:.2f}% → {signup_status}")
        st.write(f"Activation Rate: {activation_rate:.2f}% → {activation_status}")
        st.write(f"Conversion Rate: {conversion_rate:.2f}% → {conversion_status}")

        st.write(f"Day 1 Retention: {d1}% → {d1_status}")
        st.write(f"Day 7 Retention: {d7}% → {d7_status}")
        st.write(f"Day 30 Retention: {d30}% → {d30_status}")

        # --- Recommendations
        st.header("🧠 Key Insights")

        if activation_status == "🚨 Weak":
            st.error("Your biggest issue is ACTIVATION. Users are not reaching core value.")

        elif d7_status == "🚨 Weak":
            st.warning("Retention is weak. Users are not finding long-term value.")

        elif conversion_status == "🚨 Weak":
            st.warning("Monetization issue. Users are not converting to paid.")

        else:
            st.success("Your funnel is relatively healthy. Focus on optimization.")

        # --- Score
        score = 100

        for status in [signup_status, activation_status, conversion_status, d1_status, d7_status, d30_status]:
            if status == "🚨 Weak":
                score -= 15
            elif status == "⚠️ Average":
                score -= 5

            if tracking == "Poor":
                score -= 20

        st.header(f"📈 Analytics Health Score: {score}/100")
        st.markdown("👉 Need help fixing this? DM me on LinkedIn.")
        st.markdown("[Connect with me](https://linkedin.com/in/sumit-gupta-126925a8/)")