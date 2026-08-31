MIN_REG_TEMP_C = 45.0 # temp at which circulation of CO2 starts
MAX_REG_TEMP_C = 65.0 # temp at which DAC operates. source : https://neg8carbon.com/direct-air-capture-use-cases/ 
DAC_ENERGY_GJ_PER_TONNE = 2.88 # thermal energy(via waste heat)needed per tonne of CO2 captured. source : https://neg8carbon.com/direct-air-carbon-capture/
RESIDUAL_ELECTRICAL_GJ_PER_TONNE = 1.44 # energy needed on top of thermal energy. obtained via electricity.
LATENT_HEAT_CO2_KJ_KG = 180.0 # design assumption.
DIVERSION_FRACTION = 0.15 # the fraction of total waste heat diverted to the DAC instead of just rejected to ambient.
AMBIENT_TEMP_C = 25.0 # Assumed ambient temperature at 0% workload.

def run_thermodynamic_simulation(
    workload_percent: float,
    rack_capacity_kw: float = 100.0,
) -> dict:
    """
    Return value meanings
    dict
        workload_pct          - clamped workload (%)
        heat_generated_kw     - total rack heat output (kW)
        coolant_return_temp_c - CO2 coolant temperature leaving cold plates (°C)
        flow_rate_kg_min      - coolant flow rate required (kg/min)
        heat_diverted_kw      - portion of waste heat sent to DAC (kW)
        co2_captured_kg_hr    - CO2 removed from air by the DAC (kg/hr);
                                 0.0 if coolant is below MIN_REG_TEMP_C
    """
 
    #    limit workload to valid range
    workload_pct = max(0.0, min(100.0, float(workload_percent))) 
    #    Heat generated scales linearly with load up to full rack rating
    heat_generated_kw = (workload_pct / 100.0) * rack_capacity_kw
 
    #    Coolant return temperature — linear interpolation from ambient at
    #    0 % load up to MAX_REG_TEMP_C at 100 % load
    coolant_return_temp_c = AMBIENT_TEMP_C + (workload_pct / 100.0) * (
        MAX_REG_TEMP_C - AMBIENT_TEMP_C
    )
 
    #    Coolant flow rate (kg/min)
    #    unit conversion: heat_generated_kw [kJ/s] ÷ LATENT_HEAT_CO2_KJ_KG [kJ/kg] = kg/s × 60 = kg/min
    flow_rate_kg_min = (heat_generated_kw / LATENT_HEAT_CO2_KJ_KG) * 60.0
 
    #    Heat diverted to DAC (kW)
    heat_diverted_kw = heat_generated_kw * DIVERSION_FRACTION
 
    #    CO2 captured per hour (kg/hr)
    #    Zero below the minimum regeneration threshold.
    #    Above it: convert diverted heat to GJ/hr, divide by the DAC's
    #    thermal energy requirement per tonne, convert tonnes → kg.
    #    Strictly linear — no curve shaping, no exponents.
    if coolant_return_temp_c < MIN_REG_TEMP_C:
        co2_captured_kg_hr = 0.0
    else:
        # kW = kJ/s → ×3600 s/hr ÷ 1,000,000 kJ/GJ = GJ/hr
        heat_diverted_gj_hr = heat_diverted_kw * 3600.0 / 1_000_000.0
        co2_captured_tonnes_hr = heat_diverted_gj_hr / DAC_ENERGY_GJ_PER_TONNE
        co2_captured_kg_hr = co2_captured_tonnes_hr * 1000.0
 
    return {
        "workload_pct":           round(workload_pct,           2),
        "heat_generated_kw":      round(heat_generated_kw,      3),
        "coolant_return_temp_c":  round(coolant_return_temp_c,  2),
        "flow_rate_kg_min":       round(flow_rate_kg_min,        4),
        "heat_diverted_kw":       round(heat_diverted_kw,        3),
        "co2_captured_kg_hr":     round(co2_captured_kg_hr,      4),
    }
 
 
#  Sanity-check loop 
 
if __name__ == "__main__":
    header = (
        f"{'Load %':>6}  {'Heat (kW)':>10}  {'Coolant °C':>10}  "
        f"{'Flow kg/min':>12}  {'DAC heat kW':>12}  {'CO2 kg/hr':>10}"
    )
    print(header)
    print("─" * len(header))
 
    for load in [0, 25, 50, 75, 100]:
        r = run_thermodynamic_simulation(load)
        print(
            f"{r['workload_pct']:>6.0f}  "
            f"{r['heat_generated_kw']:>10.3f}  "
            f"{r['coolant_return_temp_c']:>10.2f}  "
            f"{r['flow_rate_kg_min']:>12.4f}  "
            f"{r['heat_diverted_kw']:>12.3f}  "
            f"{r['co2_captured_kg_hr']:>10.4f}"
        )
     