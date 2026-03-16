import math

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


if "language" not in st.session_state:
    st.session_state.language = "da"


st.set_page_config(
    page_title="Wind Turbine Fundamentals"
    if st.session_state.language == "en"
    else "Vindmøllens Grundprincipper",
    page_icon="W",
    layout="wide",
)


TRAPEZOID_INTEGRAL = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
INK = "#102a32"
MUTED = "#4d626a"
TEAL = "#0f6c74"
SKY = "#8dc7c3"
AMBER = "#c96a3a"
RUST = "#8f3f23"
PAPER = "#fbfcfb"
PAPER_ALT = "#f3f7f6"
GRID = "rgba(16, 42, 50, 0.12)"
HERO_INK = INK


TRANSLATIONS = {
    "da": {
        "language_label": "Language / Sprog",
        "sidebar_design": "Designinput",
        "slider_radius": "Rotorradius (m)",
        "slider_wind_speed": "Referencevindhastighed (m/s)",
        "slider_density": "Luftdensitet (kg/m^3)",
        "sidebar_induction": "Induktion og kølvand",
        "slider_induction": "Aksial induktionsfaktor a",
        "sidebar_power": "Simpel effektkurve",
        "slider_cp_design": "Antaget Cp under mærkeeffekt",
        "slider_drivetrain": "Drivlinjevirkningsgrad",
        "slider_cut_in": "Indkoblingshastighed (m/s)",
        "slider_rated_speed": "Mærkevindhastighed (m/s)",
        "slider_cut_out": "Udkoblingshastighed (m/s)",
        "sidebar_climate": "Vindklima",
        "slider_mean_speed": "Middelvindhastighed (m/s)",
        "slider_weibull": "Weibull-formfaktor k",
        "k_note": "Lavere <code>k</code> betyder et bredere og mere variabelt vindklima. Højere <code>k</code> betyder, at hastighederne samler sig tættere omkring middelvinden.",
        "error_rated": "Mærkevindhastigheden skal være større end indkoblingshastigheden.",
        "error_cut_out": "Udkoblingshastigheden skal være større end mærkevindhastigheden.",
        "hero_eyebrow": "Pædagogisk Streamlit-app",
        "hero_title": "Vindmøllens Grundprincipper",
        "hero_text_1": "Udforsk hvordan en rotor bremser vinden, hvordan kølvandet udvider sig, hvorfor Betz-grænsen betyder noget, og hvordan vindklimaet former den årlige energiproduktion.",
        "hero_text_2": "Værktøjet er bevidst enkelt og fokuserer på førsteordensfysik, som er let at undersøge, justere og forklare i undervisning eller designgennemgang.",
        "formula_power_title": "Effekt i vinden",
        "formula_power_body": "Den tilgængelige effekt vokser med rotorarealet og med vindhastigheden i tredje potens.",
        "formula_betz_title": "Betz / momentteori",
        "formula_betz_body": "Aksial induktion <code>a</code> kobler rotorens opbremsning, kølvandshastighed og energiudtag sammen.",
        "formula_weibull_title": "Weibull-klima",
        "formula_weibull_body": "Middelvind og formfaktoren <code>k</code> bestemmer, hvor ofte hver vindhastighed forekommer.",
        "metric_area": "Rotorareal",
        "metric_available_power": "Tilgængelig vindeffekt",
        "metric_cp_from_a": "Aktuel Cp fra a",
        "metric_disk_speed": "Hastighed ved rotor",
        "metric_far_wake_speed": "Hastighed i fjernkølvand",
        "tab_betz": "Betz og induktion",
        "tab_wake": "Kølvand og effektkurve",
        "tab_climate": "Vindklima og AEP",
        "betz_subheader": "Betz' lov via aksial induktion",
        "betz_body": "For en ideel aktuatordisk styrer den aksiale induktionsfaktor `a`, hvor meget strømningen bremses ved rotoren. Den samme `a` bestemmer også den ideelle effektkoefficient `Cp = 4a(1-a)^2`.",
        "velocity_subheader": "Hastighed opstrøms og nedstrøms",
        "velocity_body": "Rotoren inducerer et hastighedstab før skiven og efterlader derefter et langsommere fjernkølvand bag sig. I ideel 1D-momentteori gælder:",
        "velocity_formula": r"U_{\text{rotor}} = U_{\infty}(1-a) \qquad U_{\text{kølvand}} = U_{\infty}(1-2a)",
        "examples_subheader": "Tre induktionseksempler",
        "example_labels": ["Let belastning", "Nær Betz-optimum", "Høj belastning"],
        "example_disk_speed": "Hastighed ved rotor",
        "example_far_wake": "Fjernkølvand",
        "example_wake_radius": "Kølvandsradius",
        "wake_subheader": "Udvidelse af kølvand",
        "wake_body": "Når kølvandet bremses ned, må det udvide sig for at føre den samme massestrøm videre. I simpel momentteori er forholdet for fjernkølvandets areal:",
        "wake_formula": r"\frac{A_{\text{kølvand}}}{A_{\text{rotor}}} = \frac{1-a}{1-2a}",
        "power_subheader": "Grundprincipper i effektkurven",
        "power_body": "Under mærkevindhastigheden bruger denne forenklede model en konstant `Cp`, så effekten følger vindhastigheden i tredje potens. Over mærkevindhastigheden holder reguleringen maskinen på konstant effekt indtil udkobling.",
        "metric_extracted_power": "Udtaget effekt nu",
        "metric_betz_limit_power": "Effekt ved Betz-grænsen",
        "metric_rated_power": "Antaget mærkeeffekt",
        "metric_far_wake_radius": "Fjernkølvandsradius",
        "radius_multiplier": "x rotorradius",
        "climate_subheader": "Vindfeltets indflydelse med Weibull `k`",
        "climate_body": "Den samme vindmølle opfører sig meget forskelligt i forskellige vindklimaer. Middelvinden flytter fordelingen, mens `k` ændrer, hvor smal eller bred den er.",
        "annual_subheader": "Årsenergi i hovedtræk",
        "annual_body": "Årsenergiproduktionen kommer fra overlappet mellem effektkurven og sandsynlighedsfordelingen for vindhastigheden.",
        "metric_avg_power": "Middel elektrisk effekt",
        "metric_aep": "Årlig energiproduktion",
        "aep_unit": "kWh/år",
        "metric_capacity_factor": "Kapacitetsfaktor",
        "slider_help_title": "Sådan kan sliderne læses:",
        "slider_help_1": "- Højere middelvind øger både energioptaget og tiden tæt på mærkeeffekt.",
        "slider_help_2": "- Lavere `k` spreder vindhastighederne mere, hvilket kan hjælpe eller skade afhængigt af, hvor effektkurven ligger.",
        "slider_help_3": "- Fordi effekten skalerer med `U^3`, kommer en stor del af energien ofte fra vinde over middelvinden.",
        "footnote": "Dette er en undervisningsmodel baseret på førsteordensprincipper. Den omfatter ikke tiptab, yaw-fejl, turbulensintensitet, vindskæring, drivlinjebegrænsninger ud over en simpel virkningsgrad eller detaljeret genopretning af kølvandet.",
        "betz_line": "Cp for aktuatordisk",
        "betz_selected": "Valgt driftspunkt",
        "betz_optimum": "Betz-optimum",
        "betz_annotation": "Betz-grænse 16/27",
        "betz_xaxis": "Aksial induktionsfaktor a",
        "betz_yaxis": "Effektkoefficient Cp",
        "velocity_upstream": "Induktion opstrøms",
        "velocity_downstream": "Hastighed i nedstrømskølvand",
        "velocity_free_stream": "Fri strøm",
        "velocity_disk_annotation": "Hastighed ved rotor = {value:.2f} U∞",
        "velocity_far_annotation": "Fjernkølvand = {value:.2f} U∞",
        "velocity_xaxis": "Afstand x / D",
        "velocity_yaxis": "Centerlinjehastighed / U∞",
        "streamtube_boundary": "Strømrørets grænse",
        "streamtube_rotor": "Rotorskive",
        "streamtube_upstream_annotation": "Strømrør opstrøms = {value:.2f} R",
        "streamtube_far_annotation": "Fjernkølvand = {value:.2f} R",
        "streamtube_xaxis": "Afstand x / D",
        "streamtube_yaxis": "Relativ strømrørsradius / R",
        "power_curve_name": "Effektkurve",
        "power_curve_rated_annotation": "Mærkeeffekt = {value:,.0f} kW",
        "power_curve_xaxis": "Vindhastighed (m/s)",
        "power_curve_yaxis": "Elektrisk effekt (kW)",
        "weibull_pdf": "Weibull-sandsynlighedstæthed",
        "weibull_energy": "Relativt energibidrag",
        "weibull_mean_annotation": "Middelvind = {value:.1f} m/s",
        "weibull_title": "Vindklima med Weibull-formfaktor k = {value:.1f}",
        "weibull_xaxis": "Vindhastighed (m/s)",
        "weibull_yaxis_left": "Sandsynlighedstæthed",
        "weibull_yaxis_right": "Relativt energibidrag",
    },
    "en": {
        "language_label": "Language / Sprog",
        "sidebar_design": "Design Inputs",
        "slider_radius": "Rotor radius (m)",
        "slider_wind_speed": "Reference wind speed (m/s)",
        "slider_density": "Air density (kg/m^3)",
        "sidebar_induction": "Induction and Wake",
        "slider_induction": "Axial induction factor a",
        "sidebar_power": "Simple Power Curve",
        "slider_cp_design": "Assumed Cp below rated",
        "slider_drivetrain": "Drivetrain efficiency",
        "slider_cut_in": "Cut-in speed (m/s)",
        "slider_rated_speed": "Rated speed (m/s)",
        "slider_cut_out": "Cut-out speed (m/s)",
        "sidebar_climate": "Wind Climate",
        "slider_mean_speed": "Average wind speed (m/s)",
        "slider_weibull": "Weibull shape factor k",
        "k_note": "Lower <code>k</code> means a broader, more gusty wind climate. Higher <code>k</code> means speeds cluster more tightly around the mean.",
        "error_rated": "Rated speed must be greater than cut-in speed.",
        "error_cut_out": "Cut-out speed must be greater than rated speed.",
        "hero_eyebrow": "Educational Streamlit App",
        "hero_title": "Wind Turbine Fundamentals",
        "hero_text_1": "Explore how a rotor slows the wind, how the wake expands, why the Betz limit matters, and how the wind climate shapes annual energy production.",
        "hero_text_2": "This tool is intentionally simple and focuses on first-order physics you can inspect, tweak, and explain in a classroom or design review.",
        "formula_power_title": "Power in the Wind",
        "formula_power_body": "The available power rises with rotor area and with the cube of wind speed.",
        "formula_betz_title": "Betz / Momentum Theory",
        "formula_betz_body": "Axial induction <code>a</code> links rotor slowdown, wake speed, and extraction efficiency.",
        "formula_weibull_title": "Weibull Climate",
        "formula_weibull_body": "The mean wind and shape factor <code>k</code> determine how often each wind speed occurs.",
        "metric_area": "Rotor area",
        "metric_available_power": "Available wind power",
        "metric_cp_from_a": "Current Cp from a",
        "metric_disk_speed": "Disk speed",
        "metric_far_wake_speed": "Far-wake speed",
        "tab_betz": "Betz and Induction",
        "tab_wake": "Wake and Power Curve",
        "tab_climate": "Wind Climate and AEP",
        "betz_subheader": "Betz law through axial induction",
        "betz_body": "For an ideal actuator disk, the axial induction factor `a` controls how much the flow slows at the rotor. The same `a` also sets the ideal power coefficient `Cp = 4a(1-a)^2`.",
        "velocity_subheader": "Upstream and downstream speed",
        "velocity_body": "The rotor induces a velocity deficit before the disk and leaves a slower far wake behind it. In ideal 1D momentum theory:",
        "velocity_formula": r"U_{\text{rotor}} = U_{\infty}(1-a) \qquad U_{\text{wake}} = U_{\infty}(1-2a)",
        "examples_subheader": "Three induction examples",
        "example_labels": ["Light loading", "Near Betz optimum", "Heavy loading"],
        "example_disk_speed": "Disk speed",
        "example_far_wake": "Far wake",
        "example_wake_radius": "Wake radius",
        "wake_subheader": "Wake expansion",
        "wake_body": "As the wake slows down, it must expand to carry the same mass flow. In simple momentum theory, the far-wake area ratio is:",
        "wake_formula": r"\frac{A_{\text{wake}}}{A_{\text{rotor}}} = \frac{1-a}{1-2a}",
        "power_subheader": "Power curve fundamentals",
        "power_body": "Below rated speed, this simplified model uses a constant `Cp`, so power follows the cubic wind-speed law. Above rated, control holds the machine at constant power until cut-out.",
        "metric_extracted_power": "Extracted power now",
        "metric_betz_limit_power": "Betz-limit power",
        "metric_rated_power": "Assumed rated power",
        "metric_far_wake_radius": "Far-wake radius",
        "radius_multiplier": "x rotor radius",
        "climate_subheader": "Wind field influence with Weibull `k`",
        "climate_body": "The same turbine behaves very differently in different wind climates. Average wind speed shifts the distribution, while `k` changes how narrow or broad it is.",
        "annual_subheader": "Annual energy overview",
        "annual_body": "Annual energy production comes from the overlap between the power curve and the wind-speed probability distribution.",
        "metric_avg_power": "Average electrical power",
        "metric_aep": "Annual energy production",
        "aep_unit": "kWh/year",
        "metric_capacity_factor": "Capacity factor",
        "slider_help_title": "How to read the sliders:",
        "slider_help_1": "- Higher mean wind speed raises both energy capture and time spent near rated power.",
        "slider_help_2": "- Lower `k` spreads the wind speeds out, which can help or hurt depending on where the power curve sits.",
        "slider_help_3": "- Because power scales with `U^3`, a large share of the energy often comes from winds above the mean.",
        "footnote": "This is a first-principles teaching model. It does not include tip losses, yaw misalignment, turbulence intensity, shear, drivetrain limits beyond a simple efficiency factor, or detailed wake recovery.",
        "betz_line": "Actuator-disk Cp",
        "betz_selected": "Selected operating point",
        "betz_optimum": "Betz optimum",
        "betz_annotation": "Betz limit 16/27",
        "betz_xaxis": "Axial induction factor a",
        "betz_yaxis": "Power coefficient Cp",
        "velocity_upstream": "Upstream induction",
        "velocity_downstream": "Downstream wake speed",
        "velocity_free_stream": "Free stream",
        "velocity_disk_annotation": "Disk speed = {value:.2f} U∞",
        "velocity_far_annotation": "Far wake = {value:.2f} U∞",
        "velocity_xaxis": "Distance x / D",
        "velocity_yaxis": "Centerline speed / U∞",
        "streamtube_boundary": "Streamtube boundary",
        "streamtube_rotor": "Rotor disk",
        "streamtube_upstream_annotation": "Upstream streamtube = {value:.2f} R",
        "streamtube_far_annotation": "Far wake = {value:.2f} R",
        "streamtube_xaxis": "Distance x / D",
        "streamtube_yaxis": "Relative streamtube radius / R",
        "power_curve_name": "Power curve",
        "power_curve_rated_annotation": "Rated power = {value:,.0f} kW",
        "power_curve_xaxis": "Wind speed (m/s)",
        "power_curve_yaxis": "Electrical power (kW)",
        "weibull_pdf": "Weibull probability density",
        "weibull_energy": "Relative energy contribution",
        "weibull_mean_annotation": "Mean speed = {value:.1f} m/s",
        "weibull_title": "Wind climate with Weibull shape factor k = {value:.1f}",
        "weibull_xaxis": "Wind speed (m/s)",
        "weibull_yaxis_left": "Probability density",
        "weibull_yaxis_right": "Relative energy contribution",
    },
}


def fmt(ui: dict[str, object], key: str, **kwargs: float) -> str:
    return str(ui[key]).format(**kwargs)


def apply_axis_style(fig: go.Figure, xaxis_title: str, yaxis_title: str) -> None:
    fig.update_xaxes(
        title_text=xaxis_title,
        showline=True,
        linecolor=INK,
        linewidth=1.4,
        mirror=False,
        showgrid=True,
        gridcolor=GRID,
        ticks="outside",
        tickcolor=INK,
        tickfont=dict(color=INK, size=12),
        title_font=dict(color=INK, size=15),
        automargin=True,
        showticklabels=True,
        zeroline=False,
        color=INK,
    )
    fig.update_yaxes(
        title_text=yaxis_title,
        showline=True,
        linecolor=INK,
        linewidth=1.4,
        mirror=False,
        showgrid=True,
        gridcolor=GRID,
        ticks="outside",
        tickcolor=INK,
        tickfont=dict(color=INK, size=12),
        title_font=dict(color=INK, size=15),
        automargin=True,
        showticklabels=True,
        zeroline=False,
        color=INK,
    )


def apply_secondary_y_axis_style(fig: go.Figure, yaxis_title: str) -> None:
    fig.update_yaxes(
        title_text=yaxis_title,
        showline=True,
        linecolor=INK,
        linewidth=1.4,
        mirror=False,
        showgrid=False,
        ticks="outside",
        tickcolor=INK,
        tickfont=dict(color=INK, size=12),
        title_font=dict(color=INK, size=15),
        automargin=True,
        showticklabels=True,
        zeroline=False,
        color=INK,
        secondary_y=True,
    )


def apply_chart_layout(fig: go.Figure) -> None:
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER_ALT,
        font=dict(color=INK, family="Space Grotesk, Trebuchet MS, sans-serif"),
        legend=dict(font=dict(color=INK), orientation="h", y=1.05, x=0),
        margin=dict(l=24, r=24, t=24, b=24),
    )


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Space+Grotesk:wght@400;500;700&display=swap');

        :root {
            --bg-top: #e5efec;
            --bg-bottom: #f5efe4;
            --paper: #fbfcfb;
            --paper-alt: #f3f7f6;
            --ink: #102a32;
            --muted: #4d626a;
            --teal: #0f6c74;
            --sky: #8dc7c3;
            --amber: #c96a3a;
            --rust: #8f3f23;
            --hero-ink: #102a32;
            --line: rgba(16, 42, 50, 0.12);
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(141, 199, 195, 0.36), transparent 28%),
                radial-gradient(circle at 10% 14%, rgba(201, 106, 58, 0.16), transparent 24%),
                linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
            color: var(--ink);
        }

        .main > div {
            padding-top: 1.5rem;
        }

        .stApp, .stApp p, .stApp li, .stApp label, .stApp .stMarkdown, .stApp [data-testid="stMarkdownContainer"] * {
            color: var(--ink);
        }

        h1, h2, h3 {
            font-family: "Fraunces", Georgia, serif;
            color: var(--ink);
            letter-spacing: -0.02em;
        }

        p, li, div[data-testid="stMarkdownContainer"] {
            font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15, 108, 116, 0.12), rgba(251, 252, 251, 0.98));
            border-right: 1px solid var(--line);
        }

        section[data-testid="stSidebar"] * {
            color: var(--ink) !important;
        }

        .hero {
            padding: 1.7rem 1.9rem;
            border-radius: 28px;
            background:
                radial-gradient(circle at top right, rgba(201, 106, 58, 0.18), transparent 32%),
                linear-gradient(140deg, rgba(251, 252, 251, 0.98), rgba(229, 239, 236, 0.98));
            color: var(--hero-ink);
            box-shadow: 0 20px 60px rgba(16, 42, 50, 0.16);
            margin-bottom: 1.2rem;
            overflow: hidden;
            position: relative;
            border: 1px solid var(--line);
        }

        .hero, .hero * {
            color: var(--hero-ink) !important;
        }

        .hero:after {
            content: "";
            position: absolute;
            right: -40px;
            top: -40px;
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(15, 108, 116, 0.16), transparent 65%);
        }

        .hero h1 {
            margin-bottom: 0.35rem;
            font-size: 3rem;
        }

        .hero p {
            margin: 0.25rem 0;
            font-size: 1.02rem;
            max-width: 52rem;
            line-height: 1.5;
        }

        .eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.18em;
            font-size: 0.75rem;
            opacity: 0.78;
            font-weight: 700;
        }

        .panel {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 30px rgba(16, 42, 50, 0.05);
        }

        .panel, .panel * {
            color: var(--ink) !important;
        }

        .formula-card {
            background: linear-gradient(180deg, var(--paper), var(--paper-alt));
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1rem 1.1rem;
            min-height: 130px;
        }

        .formula-card, .formula-card * {
            color: var(--ink) !important;
        }

        .formula-card strong {
            color: var(--rust);
            display: block;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.8rem;
        }

        .mini-note {
            border-left: 4px solid var(--teal);
            padding: 0.8rem 1rem;
            background: rgba(251, 252, 251, 0.96);
            border-radius: 0 16px 16px 0;
            margin: 0.6rem 0 0.5rem 0;
        }

        .mini-note, .mini-note * {
            color: var(--ink) !important;
        }

        div[data-testid="metric-container"] {
            background: rgba(251, 252, 251, 0.98);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 0.85rem 0.95rem;
            box-shadow: 0 8px 24px rgba(16, 42, 50, 0.05);
        }

        div[data-testid="metric-container"] * {
            color: var(--ink) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(251, 252, 251, 0.9);
            border-radius: 999px;
            padding: 0.65rem 1rem;
            border: 1px solid var(--line);
            font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
            color: var(--ink) !important;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(15, 108, 116, 0.16);
            border-color: rgba(15, 108, 116, 0.28);
            color: var(--ink) !important;
        }

        .stSlider [data-baseweb="thumb"] {
            background: var(--amber);
        }

        .stSlider [data-baseweb="track"] {
            background: linear-gradient(90deg, var(--teal), var(--sky));
        }

        code, .stCode {
            color: var(--rust) !important;
            background: rgba(201, 106, 58, 0.08) !important;
            border-radius: 0.35rem;
            padding: 0.08rem 0.3rem;
        }

        .stApp a {
            color: var(--teal);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def betz_cp(a: np.ndarray | float) -> np.ndarray | float:
    return 4 * a * (1 - a) ** 2


def rotor_area(radius: float) -> float:
    return math.pi * radius**2


def available_wind_power(rho: float, radius: float, wind_speed: np.ndarray | float) -> np.ndarray | float:
    return 0.5 * rho * rotor_area(radius) * np.power(wind_speed, 3)


def extracted_power(rho: float, radius: float, wind_speed: np.ndarray | float, cp: float) -> np.ndarray | float:
    return available_wind_power(rho, radius, wind_speed) * cp


def build_power_curve(
    speeds: np.ndarray,
    rho: float,
    radius: float,
    cp_design: float,
    cut_in: float,
    rated_speed: float,
    cut_out: float,
    drivetrain_efficiency: float,
) -> tuple[np.ndarray, float]:
    aero_power = extracted_power(rho, radius, speeds, cp_design) * drivetrain_efficiency
    rated_power = float(
        extracted_power(rho, radius, rated_speed, cp_design) * drivetrain_efficiency
    )
    curve = np.zeros_like(speeds)

    below_rated = (speeds >= cut_in) & (speeds < rated_speed)
    rated_region = (speeds >= rated_speed) & (speeds <= cut_out)

    curve[below_rated] = aero_power[below_rated]
    curve[rated_region] = rated_power

    return curve, rated_power


def weibull_scale_from_mean(mean_speed: float, k: float) -> float:
    return mean_speed / math.gamma(1 + 1 / k)


def weibull_pdf(v: np.ndarray, mean_speed: float, k: float) -> np.ndarray:
    c = weibull_scale_from_mean(mean_speed, k)
    pdf = (k / c) * np.power(v / c, k - 1) * np.exp(-np.power(v / c, k))
    pdf[v < 0] = 0
    return pdf


def annual_energy_from_distribution(power_curve_kw: np.ndarray, pdf: np.ndarray, speeds: np.ndarray) -> float:
    expected_power_kw = TRAPEZOID_INTEGRAL(power_curve_kw * pdf, speeds)
    return expected_power_kw * 8760


def create_betz_figure(current_a: float, ui: dict[str, object]) -> go.Figure:
    a_values = np.linspace(0.0, 0.49, 400)
    cp_values = betz_cp(a_values)
    current_cp = float(betz_cp(current_a))
    betz_a = 1 / 3
    betz_limit = 16 / 27

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=a_values,
            y=cp_values,
            mode="lines",
            name=str(ui["betz_line"]),
            line=dict(color=AMBER, width=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[current_a],
            y=[current_cp],
            mode="markers",
            name=str(ui["betz_selected"]),
            marker=dict(size=14, color=TEAL, line=dict(color=HERO_INK, width=2)),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[betz_a],
            y=[betz_limit],
            mode="markers",
            name=str(ui["betz_optimum"]),
            marker=dict(size=14, color=RUST, symbol="diamond"),
        )
    )
    fig.add_vline(x=betz_a, line_dash="dot", line_color=RUST, opacity=0.6)
    fig.add_annotation(
        x=betz_a,
        y=betz_limit,
        text=str(ui["betz_annotation"]),
        showarrow=True,
        arrowhead=2,
        ax=55,
        ay=-45,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.update_layout(
        height=420,
        xaxis_title=str(ui["betz_xaxis"]),
        yaxis_title=str(ui["betz_yaxis"]),
    )
    apply_chart_layout(fig)
    apply_axis_style(fig, str(ui["betz_xaxis"]), str(ui["betz_yaxis"]))
    fig.update_yaxes(range=[0, 0.65])
    return fig


def create_velocity_figure(a: float, ui: dict[str, object]) -> go.Figure:
    x_up = np.linspace(-4, 0, 160)
    x_down = np.linspace(0, 10, 260)

    u_up = 1 - a * np.exp(x_up / 1.15)
    u_down = 1 - 2 * a + a * np.exp(-x_down / 2.1)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_up,
            y=u_up,
            mode="lines",
            name=str(ui["velocity_upstream"]),
            line=dict(color=TEAL, width=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_down,
            y=u_down,
            mode="lines",
            name=str(ui["velocity_downstream"]),
            line=dict(color=RUST, width=4),
        )
    )
    fig.add_vline(x=0, line_color=INK, line_dash="dash")
    fig.add_hline(y=1, line_color="rgba(16, 42, 50, 0.3)", line_dash="dot")
    fig.add_annotation(
        x=-2.7,
        y=1.02,
        text=str(ui["velocity_free_stream"]),
        showarrow=False,
        font=dict(color=INK),
    )
    fig.add_annotation(
        x=0.22,
        y=1 - a + 0.03,
        text=fmt(ui, "velocity_disk_annotation", value=(1 - a)),
        showarrow=False,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.add_annotation(
        x=6.8,
        y=1 - 2 * a - 0.04,
        text=fmt(ui, "velocity_far_annotation", value=(1 - 2 * a)),
        showarrow=False,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.update_layout(
        height=360,
        xaxis_title=str(ui["velocity_xaxis"]),
        yaxis_title=str(ui["velocity_yaxis"]),
    )
    apply_chart_layout(fig)
    apply_axis_style(fig, str(ui["velocity_xaxis"]), str(ui["velocity_yaxis"]))
    fig.update_yaxes(range=[max(0, 1 - 2.3 * a), 1.08])
    return fig


def create_streamtube_figure(a: float, ui: dict[str, object]) -> go.Figure:
    upstream_radius = math.sqrt(1 - a)
    disk_radius = 1.0
    wake_radius = math.sqrt((1 - a) / max(1e-6, 1 - 2 * a))

    x_up = np.linspace(-4, 0, 80)
    x_down = np.linspace(0, 10, 180)
    top_up = upstream_radius + (disk_radius - upstream_radius) * np.power((x_up + 4) / 4, 1.25)
    top_down = disk_radius + (wake_radius - disk_radius) * (1 - np.exp(-x_down / 2.8))

    x_all = np.concatenate([x_up, x_down])
    top_all = np.concatenate([top_up, top_down])
    bottom_all = -top_all

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=np.concatenate([x_all, x_all[::-1]]),
            y=np.concatenate([top_all, bottom_all[::-1]]),
            fill="toself",
            fillcolor="rgba(124, 198, 207, 0.35)",
            line=dict(color="rgba(0,0,0,0)"),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_all,
            y=top_all,
            mode="lines",
            line=dict(color=TEAL, width=4),
            name=str(ui["streamtube_boundary"]),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_all,
            y=bottom_all,
            mode="lines",
            line=dict(color=TEAL, width=4),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, 0],
            y=[-1, 1],
            mode="lines",
            line=dict(color=RUST, width=8),
            name=str(ui["streamtube_rotor"]),
        )
    )
    fig.add_annotation(
        x=-3.2,
        y=upstream_radius + 0.18,
        text=fmt(ui, "streamtube_upstream_annotation", value=upstream_radius),
        showarrow=False,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.add_annotation(
        x=6.6,
        y=wake_radius + 0.2,
        text=fmt(ui, "streamtube_far_annotation", value=wake_radius),
        showarrow=False,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.update_layout(
        height=420,
        xaxis_title=str(ui["streamtube_xaxis"]),
        yaxis_title=str(ui["streamtube_yaxis"]),
    )
    apply_chart_layout(fig)
    apply_axis_style(fig, str(ui["streamtube_xaxis"]), str(ui["streamtube_yaxis"]))
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


def create_power_curve_figure(
    speeds: np.ndarray, power_curve_kw: np.ndarray, rated_power_kw: float, ui: dict[str, object]
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=speeds,
            y=power_curve_kw,
            mode="lines",
            name=str(ui["power_curve_name"]),
            line=dict(color=AMBER, width=4),
        )
    )
    fig.add_hline(
        y=rated_power_kw,
        line_color=TEAL,
        line_dash="dot",
        annotation_text=fmt(ui, "power_curve_rated_annotation", value=rated_power_kw),
    )
    fig.update_layout(
        height=390,
        xaxis_title=str(ui["power_curve_xaxis"]),
        yaxis_title=str(ui["power_curve_yaxis"]),
    )
    apply_chart_layout(fig)
    apply_axis_style(fig, str(ui["power_curve_xaxis"]), str(ui["power_curve_yaxis"]))
    return fig


def create_weibull_figure(
    speeds: np.ndarray,
    pdf: np.ndarray,
    energy_weight: np.ndarray,
    mean_speed: float,
    k: float,
    ui: dict[str, object],
) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=speeds,
            y=pdf,
            mode="lines",
            name=str(ui["weibull_pdf"]),
            line=dict(color=TEAL, width=4),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=speeds,
            y=energy_weight,
            mode="lines",
            name=str(ui["weibull_energy"]),
            line=dict(color=RUST, width=3, dash="dot"),
        ),
        secondary_y=True,
    )
    fig.add_vline(x=mean_speed, line_color=INK, line_dash="dash")
    fig.add_annotation(
        x=mean_speed,
        y=float(pdf.max()) * 0.92,
        text=fmt(ui, "weibull_mean_annotation", value=mean_speed),
        showarrow=True,
        arrowhead=2,
        ax=50,
        ay=-35,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.update_layout(
        height=390,
        title=fmt(ui, "weibull_title", value=k),
    )
    apply_chart_layout(fig)
    fig.update_layout(title_font=dict(color=INK, size=17))
    fig.update_xaxes(
        title_text=str(ui["weibull_xaxis"]),
        showline=True,
        linecolor=INK,
        linewidth=1.4,
        showgrid=True,
        gridcolor=GRID,
        ticks="outside",
        tickcolor=INK,
        tickfont=dict(color=INK, size=12),
        title_font=dict(color=INK, size=15),
        automargin=True,
        showticklabels=True,
        zeroline=False,
        color=INK,
    )
    fig.update_yaxes(
        title_text=str(ui["weibull_yaxis_left"]),
        showline=True,
        linecolor=INK,
        linewidth=1.4,
        showgrid=True,
        gridcolor=GRID,
        ticks="outside",
        tickcolor=INK,
        tickfont=dict(color=INK, size=12),
        title_font=dict(color=INK, size=15),
        automargin=True,
        showticklabels=True,
        zeroline=False,
        color=INK,
        secondary_y=False,
    )
    apply_secondary_y_axis_style(fig, str(ui["weibull_yaxis_right"]))
    fig.update_yaxes(rangemode="tozero", secondary_y=True)
    return fig


def render_formula_cards(ui: dict[str, object]) -> None:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="formula-card">
                <strong>{}</strong>
                <div><code>P_\u200bwind = 0.5 \u03c1 A U^3</code></div>
                <p>{}</p>
            </div>
            """.format(ui["formula_power_title"], ui["formula_power_body"]),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="formula-card">
                <strong>{}</strong>
                <div><code>Cp = 4a(1-a)^2</code></div>
                <p>{}</p>
            </div>
            """.format(ui["formula_betz_title"], ui["formula_betz_body"]),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="formula-card">
                <strong>{}</strong>
                <div><code>f(U) = (k/c)(U/c)^(k-1)e^{{-(U/c)^k}}</code></div>
                <p>{}</p>
            </div>
            """.format(ui["formula_weibull_title"], ui["formula_weibull_body"]),
            unsafe_allow_html=True,
        )


def main() -> None:
    inject_styles()

    with st.sidebar:
        language = st.radio(
            "Language / Sprog",
            options=["da", "en"],
            format_func=lambda code: "Dansk" if code == "da" else "English",
            key="language",
            horizontal=True,
        )
        ui = TRANSLATIONS[language]

        st.header(str(ui["sidebar_design"]))
        radius = st.slider(str(ui["slider_radius"]), min_value=10.0, max_value=90.0, value=45.0, step=1.0)
        wind_speed = st.slider(
            str(ui["slider_wind_speed"]), min_value=4.0, max_value=18.0, value=9.0, step=0.5
        )
        rho = st.slider(str(ui["slider_density"]), min_value=1.0, max_value=1.35, value=1.225, step=0.005)

        st.header(str(ui["sidebar_induction"]))
        induction = st.slider(str(ui["slider_induction"]), min_value=0.05, max_value=0.45, value=0.33, step=0.01)

        st.header(str(ui["sidebar_power"]))
        cp_design = st.slider(str(ui["slider_cp_design"]), min_value=0.20, max_value=0.55, value=0.44, step=0.01)
        drivetrain_eff = st.slider(
            str(ui["slider_drivetrain"]), min_value=0.80, max_value=0.98, value=0.92, step=0.01
        )
        cut_in = st.slider(str(ui["slider_cut_in"]), min_value=2.0, max_value=6.0, value=3.0, step=0.5)
        rated_speed = st.slider(
            str(ui["slider_rated_speed"]), min_value=8.0, max_value=16.0, value=12.0, step=0.5
        )
        cut_out = st.slider(str(ui["slider_cut_out"]), min_value=18.0, max_value=30.0, value=25.0, step=1.0)

        st.header(str(ui["sidebar_climate"]))
        mean_speed = st.slider(str(ui["slider_mean_speed"]), min_value=4.0, max_value=12.0, value=7.5, step=0.1)
        weibull_k = st.slider(str(ui["slider_weibull"]), min_value=1.2, max_value=4.0, value=2.0, step=0.1)

        st.markdown(
            """
            <div class="mini-note">
            {}
            </div>
            """.format(ui["k_note"]),
            unsafe_allow_html=True,
        )

    if rated_speed <= cut_in:
        st.error(str(ui["error_rated"]))
        st.stop()

    if cut_out <= rated_speed:
        st.error(str(ui["error_cut_out"]))
        st.stop()

    cp_from_induction = float(betz_cp(induction))
    cp_used = min(cp_design, 16 / 27)
    area = rotor_area(radius)
    disk_speed = wind_speed * (1 - induction)
    wake_speed = wind_speed * (1 - 2 * induction)
    wake_radius_factor = math.sqrt((1 - induction) / (1 - 2 * induction))

    speeds = np.linspace(0, 30, 601)
    power_curve_w, rated_power_w = build_power_curve(
        speeds=speeds,
        rho=rho,
        radius=radius,
        cp_design=cp_used,
        cut_in=cut_in,
        rated_speed=rated_speed,
        cut_out=cut_out,
        drivetrain_efficiency=drivetrain_eff,
    )
    power_curve_kw = power_curve_w / 1000
    rated_power_kw = rated_power_w / 1000

    pdf = weibull_pdf(speeds, mean_speed, weibull_k)
    relative_energy = speeds**3 * pdf
    if relative_energy.max() > 0:
        relative_energy = relative_energy / relative_energy.max()

    aep_kwh = annual_energy_from_distribution(power_curve_kw, pdf, speeds)
    avg_power_kw = aep_kwh / 8760
    capacity_factor = 0 if rated_power_kw == 0 else avg_power_kw / rated_power_kw

    free_stream_power_kw = available_wind_power(rho, radius, wind_speed) / 1000
    extracted_power_kw = extracted_power(rho, radius, wind_speed, cp_from_induction) / 1000
    betz_limit_kw = extracted_power(rho, radius, wind_speed, 16 / 27) / 1000

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">{}</div>
            <h1>{}</h1>
            <p>{}</p>
            <p>{}</p>
        </div>
        """.format(ui["hero_eyebrow"], ui["hero_title"], ui["hero_text_1"], ui["hero_text_2"]),
        unsafe_allow_html=True,
    )

    render_formula_cards(ui)
    st.write("")

    top_metrics = st.columns(5)
    top_metrics[0].metric(str(ui["metric_area"]), f"{area:,.0f} m^2")
    top_metrics[1].metric(str(ui["metric_available_power"]), f"{free_stream_power_kw:,.0f} kW")
    top_metrics[2].metric(str(ui["metric_cp_from_a"]), f"{cp_from_induction:.3f}")
    top_metrics[3].metric(str(ui["metric_disk_speed"]), f"{disk_speed:.2f} m/s")
    top_metrics[4].metric(str(ui["metric_far_wake_speed"]), f"{wake_speed:.2f} m/s")

    tab1, tab2, tab3 = st.tabs(
        [str(ui["tab_betz"]), str(ui["tab_wake"]), str(ui["tab_climate"])]
    )

    with tab1:
        left, right = st.columns([1.15, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader(str(ui["betz_subheader"]))
            st.write(str(ui["betz_body"]))
            st.plotly_chart(create_betz_figure(induction, ui), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader(str(ui["velocity_subheader"]))
            st.write(str(ui["velocity_body"]))
            st.latex(str(ui["velocity_formula"]))
            st.plotly_chart(create_velocity_figure(induction, ui), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader(str(ui["examples_subheader"]))
        example_cols = st.columns(3)
        example_cases = list(zip(list(ui["example_labels"]), [0.15, 1 / 3, 0.45]))
        for col, (label, a_case) in zip(example_cols, example_cases):
            cp_case = betz_cp(a_case)
            disk_case = wind_speed * (1 - a_case)
            wake_case = wind_speed * (1 - 2 * a_case)
            wake_factor_case = math.sqrt((1 - a_case) / (1 - 2 * a_case))
            with col:
                st.metric(str(label), f"a = {a_case:.2f}")
                st.write(f"Cp = {cp_case:.3f}")
                st.write(f"{ui['example_disk_speed']} = {disk_case:.2f} m/s")
                st.write(f"{ui['example_far_wake']} = {wake_case:.2f} m/s")
                st.write(f"{ui['example_wake_radius']} = {wake_factor_case:.2f} R")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        left, right = st.columns([1.1, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader(str(ui["wake_subheader"]))
            st.write(str(ui["wake_body"]))
            st.latex(str(ui["wake_formula"]))
            st.plotly_chart(create_streamtube_figure(induction, ui), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader(str(ui["power_subheader"]))
            st.write(str(ui["power_body"]))
            st.plotly_chart(
                create_power_curve_figure(speeds, power_curve_kw, rated_power_kw, ui),
                width="stretch",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        bottom_metrics = st.columns(4)
        bottom_metrics[0].metric(str(ui["metric_extracted_power"]), f"{extracted_power_kw:,.0f} kW")
        bottom_metrics[1].metric(str(ui["metric_betz_limit_power"]), f"{betz_limit_kw:,.0f} kW")
        bottom_metrics[2].metric(str(ui["metric_rated_power"]), f"{rated_power_kw:,.0f} kW")
        bottom_metrics[3].metric(str(ui["metric_far_wake_radius"]), f"{wake_radius_factor:.2f} {ui['radius_multiplier']}")

    with tab3:
        left, right = st.columns([1.15, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader(str(ui["climate_subheader"]))
            st.write(str(ui["climate_body"]))
            st.plotly_chart(
                create_weibull_figure(speeds, pdf, relative_energy, mean_speed, weibull_k, ui),
                width="stretch",
            )
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader(str(ui["annual_subheader"]))
            st.write(str(ui["annual_body"]))
            st.metric(str(ui["metric_avg_power"]), f"{avg_power_kw:,.0f} kW")
            st.metric(str(ui["metric_aep"]), f"{aep_kwh:,.0f} {ui['aep_unit']}")
            st.metric(str(ui["metric_capacity_factor"]), f"{capacity_factor:.1%}")
            st.write("")
            st.write(str(ui["slider_help_title"]))
            st.write(str(ui["slider_help_1"]))
            st.write(str(ui["slider_help_2"]))
            st.write(str(ui["slider_help_3"]))
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown(
            """
            <div class="mini-note">
            {}
            </div>
            """.format(ui["footnote"]),
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
