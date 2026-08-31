import streamlit as st
import pandas as pd

from engine import run_thermodynamic_simulation

st.set_page_config(
    page_title="CO2 Cooling + Carbon Capture Simulator",
    page_icon="🌀",
    layout="centered",
)

st.title("Supercritical CO2 Cooling → Direct Air Capture")
st.caption(
    "Live simulation of a data center cooling loop that diverts waste heat "
    "to power a direct air capture (DAC) unit."
)

# --- Workload slider -------------------------------------------------
workload = st.slider("Server workload (%)", min_value=0, max_value=100, value=50, step=1)

# --- Run engine at current slider value, display metrics --------------
result = run_thermodynamic_simulation(workload)

col1, col2, col3 = st.columns(3)
col1.metric("Heat generated", f"{result['heat_generated_kw']:.1f} kW")
col2.metric("Coolant temperature", f"{result['coolant_return_temp_c']:.1f} °C")
col3.metric("Coolant flow rate", f"{result['flow_rate_kg_min']:.1f} kg/min")

col4, col5 = st.columns(2)
col4.metric("Heat diverted to DAC", f"{result['heat_diverted_kw']:.1f} kW")
col5.metric("CO2 captured", f"{result['co2_captured_kg_hr']:.2f} kg/hr")

if result["co2_captured_kg_hr"] == 0:
    st.info(
        "Coolant is below the DAC sorbent's regeneration threshold (45°C) — "
        "no carbon capture yet at this workload."
    )

# --- Chart sweeping the full 0-100 range -------------------------------
st.subheader("CO2 captured across the full workload range")

sweep = [run_thermodynamic_simulation(w) for w in range(0, 101)]
chart_df = pd.DataFrame(
    {
        "Workload (%)": [r["workload_pct"] for r in sweep],
        "CO2 captured (kg/hr)": [r["co2_captured_kg_hr"] for r in sweep],
    }
).set_index("Workload (%)")

st.line_chart(chart_df)
st.caption(
    "Capture stays at zero below the regeneration threshold, then rises "
    "linearly with diverted waste heat."
)

# --- Static context panel ----------------------------------------------
st.divider()
st.subheader("Context: what this could mean at scale")

st.markdown(
    """
**Freshwater eliminated** (for a representative 50 MW data center):
**~0.4–2.2 million litres/day**

This range comes from two different published benchmarks, not one confirmed
figure: the industry-average Water Usage Effectiveness figure of **1.8 L/kWh**
(Green Grid / Meta benchmark), and a lower India-specific estimate of
**~8,000 L/MW/day** (CEEW).

---

**CO2 capture potential at full scale**: **~55,000–82,000 tonnes/year**

Based on diverting 10–15% of total waste heat and NEG8 Carbon's published
2.88 GJ/tonne thermal energy requirement. This is a **theoretical,
heat-availability-based ceiling** — not a guaranteed output, since real DAC
deployments are also limited by unit size and capital cost, not just
available heat.
"""
)

with st.expander("Sources & assumptions"):
    st.markdown(
        """
- DAC regeneration temperature (65°C) and thermal energy requirement
  (2.88 GJ/tonne with waste heat) are from NEG8 Carbon's published figures:
  [neg8carbon.com/direct-air-capture-use-cases](https://neg8carbon.com/direct-air-capture-use-cases/),
  [neg8carbon.com/direct-air-carbon-capture](https://neg8carbon.com/direct-air-carbon-capture/)
- The 45°C "capture starts" threshold, CO2 latent heat (180 kJ/kg), and 15%
  heat-diversion fraction are conservative design assumptions, not measured
  values — chosen so the main chip-cooling loop is never starved.
- The CO2-captured-vs-workload relationship is modeled as linear once above
  threshold — intentionally, no invented curve shape.
"""
    )
