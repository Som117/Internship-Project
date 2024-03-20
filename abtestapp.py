import streamlit as st
from scipy.stats import norm


def perform_ab_test(
    control_visitors,
    control_conversions,
    treatment_visitors,
    treatment_conversions,
    confidence_level,
):
    # Calculate conversion rates
    control_conversion_rate = control_conversions / control_visitors
    treatment_conversion_rate = treatment_conversions / treatment_visitors

    # Calculate pooled probability
    pooled_probability = (control_conversions + treatment_conversions) / (
        control_visitors + treatment_visitors
    )

    # Calculate pooled standard error
    pooled_std_error = (
        pooled_probability
        * (1 - pooled_probability)
        * ((1 / control_visitors) + (1 / treatment_visitors))
    ) ** 0.5

    # Calculate z-score
    z_score = (treatment_conversion_rate - control_conversion_rate) / pooled_std_error

    # Determine critical value based on confidence level
    if confidence_level == 90:
        critical_value = norm.ppf(0.95)
    elif confidence_level == 95:
        critical_value = norm.ppf(0.975)
    elif confidence_level == 99:
        critical_value = norm.ppf(0.995)
    else:
        raise ValueError("Invalid confidence level. Choose from 90, 95, or 99.")

    # Compare z-score with critical value
    if z_score > critical_value:
        return "Experiment Group is Better"
    elif z_score < -critical_value:
        return "Control Group is Better"
    else:
        return "Indeterminate"


def main():
    st.title("A/B Test Hypothesis Testing App")

    st.sidebar.title("Input Parameters")

    control_visitors = st.sidebar.number_input("Control Group Visitors", min_value=1)
    control_conversions = st.sidebar.number_input(
        "Control Group Conversions", min_value=0
    )
    treatment_visitors = st.sidebar.number_input(
        "Treatment Group Visitors", min_value=1
    )
    treatment_conversions = st.sidebar.number_input(
        "Treatment Group Conversions", min_value=0
    )

    confidence_level = st.sidebar.radio("Confidence Level", [90, 95, 99])

    if st.sidebar.button("Run Test"):
        result = perform_ab_test(
            control_visitors,
            control_conversions,
            treatment_visitors,
            treatment_conversions,
            confidence_level,
        )
        st.write("AB Test Result:", result)


if __name__ == "__main__":
    main()
