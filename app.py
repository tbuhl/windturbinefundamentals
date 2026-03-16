import math

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


st.set_page_config(
    page_title="Vindmøllens Grundprincipper",
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
HERO_INK = "#f7faf9"


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
            --hero-ink: #f7faf9;
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
                linear-gradient(140deg, #13343c, #0f6c74),
                linear-gradient(40deg, rgba(141, 199, 195, 0.35), transparent);
            color: var(--hero-ink);
            box-shadow: 0 20px 60px rgba(16, 42, 50, 0.16);
            margin-bottom: 1.2rem;
            overflow: hidden;
            position: relative;
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
            background: radial-gradient(circle, rgba(201, 106, 58, 0.38), transparent 65%);
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


def create_betz_figure(current_a: float) -> go.Figure:
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
            name="Cp for aktuatordisk",
            line=dict(color=AMBER, width=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[current_a],
            y=[current_cp],
            mode="markers",
            name="Valgt driftspunkt",
            marker=dict(size=14, color=TEAL, line=dict(color=HERO_INK, width=2)),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[betz_a],
            y=[betz_limit],
            mode="markers",
            name="Betz-optimum",
            marker=dict(size=14, color=RUST, symbol="diamond"),
        )
    )
    fig.add_vline(x=betz_a, line_dash="dot", line_color=RUST, opacity=0.6)
    fig.add_annotation(
        x=betz_a,
        y=betz_limit,
        text="Betz-grænse 16/27",
        showarrow=True,
        arrowhead=2,
        ax=55,
        ay=-45,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PAPER_ALT,
        font=dict(color=INK, family="Space Grotesk, Trebuchet MS, sans-serif"),
        legend=dict(orientation="h", y=1.05, x=0),
        xaxis_title="Aksial induktionsfaktor a",
        yaxis_title="Effektkoefficient Cp",
    )
    fig.update_xaxes(gridcolor=GRID, color=INK)
    fig.update_yaxes(gridcolor=GRID, color=INK, range=[0, 0.65])
    return fig


def create_velocity_figure(a: float) -> go.Figure:
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
            name="Induktion opstrøms",
            line=dict(color=TEAL, width=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_down,
            y=u_down,
            mode="lines",
            name="Hastighed i nedstrømsvåge",
            line=dict(color=RUST, width=4),
        )
    )
    fig.add_vline(x=0, line_color=INK, line_dash="dash")
    fig.add_hline(y=1, line_color="rgba(16, 42, 50, 0.3)", line_dash="dot")
    fig.add_annotation(
        x=-2.7,
        y=1.02,
        text="Fri strøm",
        showarrow=False,
        font=dict(color=INK),
    )
    fig.add_annotation(
        x=0.22,
        y=1 - a + 0.03,
        text=f"Hastighed ved rotor = {(1 - a):.2f} U∞",
        showarrow=False,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.add_annotation(
        x=6.8,
        y=1 - 2 * a - 0.04,
        text=f"Fjernvåge = {(1 - 2 * a):.2f} U∞",
        showarrow=False,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PAPER_ALT,
        font=dict(color=INK, family="Space Grotesk, Trebuchet MS, sans-serif"),
        legend=dict(orientation="h", y=1.05, x=0),
        xaxis_title="Afstand x / D",
        yaxis_title="Centerlinjehastighed / U∞",
    )
    fig.update_xaxes(gridcolor=GRID, color=INK)
    fig.update_yaxes(gridcolor=GRID, color=INK, range=[max(0, 1 - 2.3 * a), 1.08])
    return fig


def create_streamtube_figure(a: float) -> go.Figure:
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
            name="Strømrørets grænse",
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
            name="Rotorskive",
        )
    )
    fig.add_annotation(
        x=-3.2,
        y=upstream_radius + 0.18,
        text=f"Strømrør opstrøms = {upstream_radius:.2f} R",
        showarrow=False,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.add_annotation(
        x=6.6,
        y=wake_radius + 0.2,
        text=f"Fjernvåge = {wake_radius:.2f} R",
        showarrow=False,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PAPER_ALT,
        font=dict(color=INK, family="Space Grotesk, Trebuchet MS, sans-serif"),
        xaxis_title="Afstand x / D",
        yaxis_title="Relativ strømrørsradius / R",
        legend=dict(orientation="h", y=1.05, x=0),
    )
    fig.update_xaxes(gridcolor=GRID, color=INK)
    fig.update_yaxes(gridcolor=GRID, color=INK, scaleanchor="x", scaleratio=1)
    return fig


def create_power_curve_figure(speeds: np.ndarray, power_curve_kw: np.ndarray, rated_power_kw: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=speeds,
            y=power_curve_kw,
            mode="lines",
            name="Effektkurve",
            line=dict(color=AMBER, width=4),
        )
    )
    fig.add_hline(
        y=rated_power_kw,
        line_color=TEAL,
        line_dash="dot",
        annotation_text=f"Mærkeeffekt = {rated_power_kw:,.0f} kW",
    )
    fig.update_layout(
        height=390,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PAPER_ALT,
        font=dict(color=INK, family="Space Grotesk, Trebuchet MS, sans-serif"),
        xaxis_title="Vindhastighed (m/s)",
        yaxis_title="Elektrisk effekt (kW)",
    )
    fig.update_xaxes(gridcolor=GRID, color=INK)
    fig.update_yaxes(gridcolor=GRID, color=INK)
    return fig


def create_weibull_figure(
    speeds: np.ndarray,
    pdf: np.ndarray,
    energy_weight: np.ndarray,
    mean_speed: float,
    k: float,
) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=speeds,
            y=pdf,
            mode="lines",
            name="Weibull-sandsynlighedstæthed",
            line=dict(color=TEAL, width=4),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=speeds,
            y=energy_weight,
            mode="lines",
            name="Relativt energibidrag",
            line=dict(color=RUST, width=3, dash="dot"),
        ),
        secondary_y=True,
    )
    fig.add_vline(x=mean_speed, line_color=INK, line_dash="dash")
    fig.add_annotation(
        x=mean_speed,
        y=float(pdf.max()) * 0.92,
        text=f"Middelvind = {mean_speed:.1f} m/s",
        showarrow=True,
        arrowhead=2,
        ax=50,
        ay=-35,
        font=dict(color=INK),
        bgcolor=PAPER,
    )
    fig.update_layout(
        height=390,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PAPER_ALT,
        font=dict(color=INK, family="Space Grotesk, Trebuchet MS, sans-serif"),
        legend=dict(orientation="h", y=1.05, x=0),
        title=f"Vindklima med Weibull-formfaktor k = {k:.1f}",
    )
    fig.update_xaxes(title_text="Vindhastighed (m/s)", gridcolor=GRID, color=INK)
    fig.update_yaxes(
        title_text="Sandsynlighedstæthed",
        gridcolor=GRID,
        color=INK,
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Relativt energibidrag",
        color=INK,
        secondary_y=True,
        rangemode="tozero",
    )
    return fig


def render_formula_cards() -> None:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """
            <div class="formula-card">
                <strong>Effekt i vinden</strong>
                <div><code>P_\u200bwind = 0.5 \u03c1 A U^3</code></div>
                <p>Den tilgængelige effekt vokser med rotorarealet og med vindhastigheden i tredje potens.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="formula-card">
                <strong>Betz / momentteori</strong>
                <div><code>Cp = 4a(1-a)^2</code></div>
                <p>Aksial induktion <code>a</code> kobler rotorens opbremsning, vågehastighed og energiudtag sammen.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="formula-card">
                <strong>Weibull-klima</strong>
                <div><code>f(U) = (k/c)(U/c)^(k-1)e^{-(U/c)^k}</code></div>
                <p>Middelvind og formfaktoren <code>k</code> bestemmer, hvor ofte hver vindhastighed forekommer.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    inject_styles()

    with st.sidebar:
        st.header("Designinput")
        radius = st.slider("Rotorradius (m)", min_value=10.0, max_value=90.0, value=45.0, step=1.0)
        wind_speed = st.slider("Referencevindhastighed (m/s)", min_value=4.0, max_value=18.0, value=9.0, step=0.5)
        rho = st.slider("Luftdensitet (kg/m^3)", min_value=1.0, max_value=1.35, value=1.225, step=0.005)

        st.header("Induktion og våge")
        induction = st.slider("Aksial induktionsfaktor a", min_value=0.05, max_value=0.45, value=0.33, step=0.01)

        st.header("Simpel effektkurve")
        cp_design = st.slider("Antaget Cp under mærkeeffekt", min_value=0.20, max_value=0.55, value=0.44, step=0.01)
        drivetrain_eff = st.slider("Drivlinjevirkningsgrad", min_value=0.80, max_value=0.98, value=0.92, step=0.01)
        cut_in = st.slider("Indkoblingshastighed (m/s)", min_value=2.0, max_value=6.0, value=3.0, step=0.5)
        rated_speed = st.slider("Mærkevindhastighed (m/s)", min_value=8.0, max_value=16.0, value=12.0, step=0.5)
        cut_out = st.slider("Udkoblingshastighed (m/s)", min_value=18.0, max_value=30.0, value=25.0, step=1.0)

        st.header("Vindklima")
        mean_speed = st.slider("Middelvindhastighed (m/s)", min_value=4.0, max_value=12.0, value=7.5, step=0.1)
        weibull_k = st.slider("Weibull-formfaktor k", min_value=1.2, max_value=4.0, value=2.0, step=0.1)

        st.markdown(
            """
            <div class="mini-note">
            Lavere <code>k</code> betyder et bredere og mere gustent vindklima. Højere <code>k</code> betyder, at hastighederne samler sig tættere omkring middelvinden.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if rated_speed <= cut_in:
        st.error("Mærkevindhastigheden skal være større end indkoblingshastigheden.")
        st.stop()

    if cut_out <= rated_speed:
        st.error("Udkoblingshastigheden skal være større end mærkevindhastigheden.")
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
            <div class="eyebrow">Pædagogisk Streamlit-app</div>
            <h1>Vindmøllens Grundprincipper</h1>
            <p>Udforsk hvordan en rotor bremser vinden, hvordan vågen udvider sig, hvorfor Betz-grænsen betyder noget, og hvordan vindklimaet former den årlige energiproduktion.</p>
            <p>Værktøjet er bevidst enkelt og fokuserer på førsteordensfysik, som er let at undersøge, justere og forklare i undervisning eller designgennemgang.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_formula_cards()
    st.write("")

    top_metrics = st.columns(5)
    top_metrics[0].metric("Rotorareal", f"{area:,.0f} m^2")
    top_metrics[1].metric("Tilgængelig vindeffekt", f"{free_stream_power_kw:,.0f} kW")
    top_metrics[2].metric("Aktuel Cp fra a", f"{cp_from_induction:.3f}")
    top_metrics[3].metric("Hastighed ved rotor", f"{disk_speed:.2f} m/s")
    top_metrics[4].metric("Hastighed i fjernvåge", f"{wake_speed:.2f} m/s")

    tab1, tab2, tab3 = st.tabs(
        ["Betz og induktion", "Våge og effektkurve", "Vindklima og AEP"]
    )

    with tab1:
        left, right = st.columns([1.15, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Betz' lov via aksial induktion")
            st.write(
                "For en ideel aktuatordisk styrer den aksiale induktionsfaktor `a`, hvor meget strømningen bremses ved rotoren. "
                "Den samme `a` bestemmer også den ideelle effektkoefficient `Cp = 4a(1-a)^2`."
            )
            st.plotly_chart(create_betz_figure(induction), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Hastighed opstrøms og nedstrøms")
            st.write(
                "Rotoren inducerer et hastighedstab før skiven og efterlader derefter en langsommere fjernvåge bag sig. "
                "I ideel 1D-momentteori gælder:"
            )
            st.latex(r"U_{disk} = U_{\infty}(1-a) \qquad U_{wake} = U_{\infty}(1-2a)")
            st.plotly_chart(create_velocity_figure(induction), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Tre induktionseksempler")
        example_cols = st.columns(3)
        example_cases = [
            ("Let belastning", 0.15),
            ("Nær Betz-optimum", 1 / 3),
            ("Høj belastning", 0.45),
        ]
        for col, (label, a_case) in zip(example_cols, example_cases):
            cp_case = betz_cp(a_case)
            disk_case = wind_speed * (1 - a_case)
            wake_case = wind_speed * (1 - 2 * a_case)
            wake_factor_case = math.sqrt((1 - a_case) / (1 - 2 * a_case))
            with col:
                st.metric(label, f"a = {a_case:.2f}")
                st.write(f"Cp = {cp_case:.3f}")
                st.write(f"Hastighed ved rotor = {disk_case:.2f} m/s")
                st.write(f"Fjernvåge = {wake_case:.2f} m/s")
                st.write(f"Vågeradius = {wake_factor_case:.2f} R")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        left, right = st.columns([1.1, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Vågeudvidelse")
            st.write(
                "Når vågen bremses ned, må den udvide sig for at føre den samme massestrøm videre. "
                "I simpel momentteori er forholdet for fjernvågens areal:"
            )
            st.latex(r"\frac{A_{wake}}{A_{disk}} = \frac{1-a}{1-2a}")
            st.plotly_chart(create_streamtube_figure(induction), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Grundprincipper i effektkurven")
            st.write(
                "Under mærkevindhastigheden bruger denne forenklede model en konstant `Cp`, så effekten følger vindhastigheden i tredje potens. "
                "Over mærkevindhastigheden holder reguleringen maskinen på konstant effekt indtil udkobling."
            )
            st.plotly_chart(
                create_power_curve_figure(speeds, power_curve_kw, rated_power_kw),
                width="stretch",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        bottom_metrics = st.columns(4)
        bottom_metrics[0].metric("Udtaget effekt nu", f"{extracted_power_kw:,.0f} kW")
        bottom_metrics[1].metric("Effekt ved Betz-grænsen", f"{betz_limit_kw:,.0f} kW")
        bottom_metrics[2].metric("Antaget mærkeeffekt", f"{rated_power_kw:,.0f} kW")
        bottom_metrics[3].metric("Fjernvågeradius", f"{wake_radius_factor:.2f} x rotorradius")

    with tab3:
        left, right = st.columns([1.15, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Vindfeltets indflydelse med Weibull `k`")
            st.write(
                "Den samme vindmølle opfører sig meget forskelligt i forskellige vindklimaer. "
                "Middelvinden flytter fordelingen, mens `k` ændrer, hvor smal eller bred den er."
            )
            st.plotly_chart(
                create_weibull_figure(speeds, pdf, relative_energy, mean_speed, weibull_k),
                width="stretch",
            )
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Årsenergi i hovedtræk")
            st.write(
                "Årsenergiproduktionen kommer fra overlappet mellem effektkurven og sandsynlighedsfordelingen for vindhastigheden."
            )
            st.metric("Middel elektrisk effekt", f"{avg_power_kw:,.0f} kW")
            st.metric("Årlig energiproduktion", f"{aep_kwh:,.0f} kWh/år")
            st.metric("Kapacitetsfaktor", f"{capacity_factor:.1%}")
            st.write("")
            st.write("Sådan kan sliderne læses:")
            st.write("- Højere middelvind øger både energioptaget og tiden tæt på mærkeeffekt.")
            st.write("- Lavere `k` spreder vindhastighederne mere, hvilket kan hjælpe eller skade afhængigt af, hvor effektkurven ligger.")
            st.write("- Fordi effekten skalerer med `U^3`, kommer en stor del af energien ofte fra vinde over middelvinden.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown(
            """
            <div class="mini-note">
            Dette er en undervisningsmodel baseret på førsteordensprincipper. Den omfatter ikke tiptab, yaw-fejl, turbulensintensitet, vindskæring, drivlinjebegrænsninger ud over en simpel virkningsgrad eller detaljeret vågerecovery.
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
