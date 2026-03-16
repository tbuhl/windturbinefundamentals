import math

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


st.set_page_config(
    page_title="Wind Turbine Fundamentals Lab",
    page_icon="W",
    layout="wide",
)


TRAPEZOID_INTEGRAL = np.trapezoid if hasattr(np, "trapezoid") else np.trapz


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Space+Grotesk:wght@400;500;700&display=swap');

        :root {
            --sand: #f4efe6;
            --paper: rgba(255, 250, 243, 0.88);
            --ink: #16343b;
            --teal: #1f6b75;
            --sky: #7cc6cf;
            --amber: #db7c3d;
            --rust: #a64b2a;
            --line: rgba(22, 52, 59, 0.14);
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(124, 198, 207, 0.32), transparent 26%),
                radial-gradient(circle at 12% 16%, rgba(219, 124, 61, 0.24), transparent 24%),
                linear-gradient(180deg, #f7f2e7 0%, #eef4f1 100%);
            color: var(--ink);
        }

        .main > div {
            padding-top: 1.5rem;
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
            background: linear-gradient(180deg, rgba(31, 107, 117, 0.12), rgba(255, 250, 243, 0.94));
            border-right: 1px solid rgba(22, 52, 59, 0.08);
        }

        .hero {
            padding: 1.7rem 1.9rem;
            border-radius: 28px;
            background:
                linear-gradient(140deg, rgba(22, 52, 59, 0.95), rgba(31, 107, 117, 0.88)),
                linear-gradient(40deg, rgba(124, 198, 207, 0.35), transparent);
            color: #f7f2e7;
            box-shadow: 0 20px 60px rgba(22, 52, 59, 0.18);
            margin-bottom: 1.2rem;
            overflow: hidden;
            position: relative;
        }

        .hero:after {
            content: "";
            position: absolute;
            right: -40px;
            top: -40px;
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(219, 124, 61, 0.45), transparent 65%);
        }

        .hero h1 {
            color: #f7f2e7;
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
            box-shadow: 0 10px 30px rgba(22, 52, 59, 0.06);
        }

        .formula-card {
            background: linear-gradient(180deg, rgba(255, 250, 243, 0.94), rgba(255, 255, 255, 0.72));
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1rem 1.1rem;
            min-height: 130px;
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
            border-left: 4px solid var(--amber);
            padding: 0.8rem 1rem;
            background: rgba(255, 250, 243, 0.74);
            border-radius: 0 16px 16px 0;
            margin: 0.6rem 0 0.5rem 0;
        }

        div[data-testid="metric-container"] {
            background: rgba(255, 250, 243, 0.75);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 0.85rem 0.95rem;
            box-shadow: 0 8px 24px rgba(22, 52, 59, 0.05);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 250, 243, 0.65);
            border-radius: 999px;
            padding: 0.65rem 1rem;
            border: 1px solid rgba(22, 52, 59, 0.08);
            font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(31, 107, 117, 0.16);
            border-color: rgba(31, 107, 117, 0.25);
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
            name="Actuator-disk Cp",
            line=dict(color="#db7c3d", width=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[current_a],
            y=[current_cp],
            mode="markers",
            name="Selected operating point",
            marker=dict(size=14, color="#1f6b75", line=dict(color="#f7f2e7", width=2)),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[betz_a],
            y=[betz_limit],
            mode="markers",
            name="Betz optimum",
            marker=dict(size=14, color="#a64b2a", symbol="diamond"),
        )
    )
    fig.add_vline(x=betz_a, line_dash="dot", line_color="#a64b2a", opacity=0.6)
    fig.add_annotation(
        x=betz_a,
        y=betz_limit,
        text="Betz limit 16/27",
        showarrow=True,
        arrowhead=2,
        ax=55,
        ay=-45,
        font=dict(color="#16343b"),
        bgcolor="rgba(255,250,243,0.85)",
    )
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,250,243,0.5)",
        legend=dict(orientation="h", y=1.05, x=0),
        xaxis_title="Axial induction factor a",
        yaxis_title="Power coefficient Cp",
    )
    fig.update_xaxes(gridcolor="rgba(22,52,59,0.08)")
    fig.update_yaxes(gridcolor="rgba(22,52,59,0.08)", range=[0, 0.65])
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
            name="Upstream induction",
            line=dict(color="#1f6b75", width=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_down,
            y=u_down,
            mode="lines",
            name="Downstream wake speed",
            line=dict(color="#a64b2a", width=4),
        )
    )
    fig.add_vline(x=0, line_color="#16343b", line_dash="dash")
    fig.add_hline(y=1, line_color="rgba(22,52,59,0.35)", line_dash="dot")
    fig.add_annotation(
        x=-2.7,
        y=1.02,
        text="Free stream",
        showarrow=False,
        font=dict(color="#16343b"),
    )
    fig.add_annotation(
        x=0.22,
        y=1 - a + 0.03,
        text=f"Disk speed = {(1 - a):.2f} U∞",
        showarrow=False,
        font=dict(color="#16343b"),
        bgcolor="rgba(255,250,243,0.85)",
    )
    fig.add_annotation(
        x=6.8,
        y=1 - 2 * a - 0.04,
        text=f"Far wake = {(1 - 2 * a):.2f} U∞",
        showarrow=False,
        font=dict(color="#16343b"),
        bgcolor="rgba(255,250,243,0.85)",
    )
    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,250,243,0.5)",
        legend=dict(orientation="h", y=1.05, x=0),
        xaxis_title="Distance x / D",
        yaxis_title="Centerline speed / U∞",
    )
    fig.update_xaxes(gridcolor="rgba(22,52,59,0.08)")
    fig.update_yaxes(gridcolor="rgba(22,52,59,0.08)", range=[max(0, 1 - 2.3 * a), 1.08])
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
            line=dict(color="#1f6b75", width=4),
            name="Streamtube boundary",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_all,
            y=bottom_all,
            mode="lines",
            line=dict(color="#1f6b75", width=4),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, 0],
            y=[-1, 1],
            mode="lines",
            line=dict(color="#a64b2a", width=8),
            name="Rotor disk",
        )
    )
    fig.add_annotation(
        x=-3.2,
        y=upstream_radius + 0.18,
        text=f"Upstream streamtube = {upstream_radius:.2f} R",
        showarrow=False,
        font=dict(color="#16343b"),
        bgcolor="rgba(255,250,243,0.85)",
    )
    fig.add_annotation(
        x=6.6,
        y=wake_radius + 0.2,
        text=f"Far wake = {wake_radius:.2f} R",
        showarrow=False,
        font=dict(color="#16343b"),
        bgcolor="rgba(255,250,243,0.85)",
    )
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,250,243,0.5)",
        xaxis_title="Distance x / D",
        yaxis_title="Relative streamtube radius / R",
        legend=dict(orientation="h", y=1.05, x=0),
    )
    fig.update_xaxes(gridcolor="rgba(22,52,59,0.08)")
    fig.update_yaxes(gridcolor="rgba(22,52,59,0.08)", scaleanchor="x", scaleratio=1)
    return fig


def create_power_curve_figure(speeds: np.ndarray, power_curve_kw: np.ndarray, rated_power_kw: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=speeds,
            y=power_curve_kw,
            mode="lines",
            name="Power curve",
            line=dict(color="#db7c3d", width=4),
        )
    )
    fig.add_hline(
        y=rated_power_kw,
        line_color="#1f6b75",
        line_dash="dot",
        annotation_text=f"Rated power = {rated_power_kw:,.0f} kW",
    )
    fig.update_layout(
        height=390,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,250,243,0.5)",
        xaxis_title="Wind speed (m/s)",
        yaxis_title="Electrical power (kW)",
    )
    fig.update_xaxes(gridcolor="rgba(22,52,59,0.08)")
    fig.update_yaxes(gridcolor="rgba(22,52,59,0.08)")
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
            name="Weibull probability density",
            line=dict(color="#1f6b75", width=4),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=speeds,
            y=energy_weight,
            mode="lines",
            name="Relative energy content",
            line=dict(color="#a64b2a", width=3, dash="dot"),
        ),
        secondary_y=True,
    )
    fig.add_vline(x=mean_speed, line_color="#16343b", line_dash="dash")
    fig.add_annotation(
        x=mean_speed,
        y=float(pdf.max()) * 0.92,
        text=f"Mean speed = {mean_speed:.1f} m/s",
        showarrow=True,
        arrowhead=2,
        ax=50,
        ay=-35,
        font=dict(color="#16343b"),
        bgcolor="rgba(255,250,243,0.85)",
    )
    fig.update_layout(
        height=390,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,250,243,0.5)",
        legend=dict(orientation="h", y=1.05, x=0),
        title=f"Wind climate with Weibull shape factor k = {k:.1f}",
    )
    fig.update_xaxes(title_text="Wind speed (m/s)", gridcolor="rgba(22,52,59,0.08)")
    fig.update_yaxes(
        title_text="Probability density",
        gridcolor="rgba(22,52,59,0.08)",
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Relative energy contribution",
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
                <strong>Power In Wind</strong>
                <div><code>P_\u200bwind = 0.5 \u03c1 A U^3</code></div>
                <p>The available power rises with rotor area and with the cube of wind speed.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="formula-card">
                <strong>Betz / Momentum</strong>
                <div><code>Cp = 4a(1-a)^2</code></div>
                <p>Axial induction <code>a</code> links rotor slowing, wake speed, and extraction efficiency.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="formula-card">
                <strong>Weibull Climate</strong>
                <div><code>f(U) = (k/c)(U/c)^(k-1)e^{-(U/c)^k}</code></div>
                <p>The mean wind and shape factor <code>k</code> set how often each wind speed occurs.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    inject_styles()

    with st.sidebar:
        st.header("Design Inputs")
        radius = st.slider("Rotor radius (m)", min_value=10.0, max_value=90.0, value=45.0, step=1.0)
        wind_speed = st.slider("Reference wind speed (m/s)", min_value=4.0, max_value=18.0, value=9.0, step=0.5)
        rho = st.slider("Air density (kg/m^3)", min_value=1.0, max_value=1.35, value=1.225, step=0.005)

        st.header("Induction And Wake")
        induction = st.slider("Axial induction factor a", min_value=0.05, max_value=0.45, value=0.33, step=0.01)

        st.header("Simple Power Curve")
        cp_design = st.slider("Assumed Cp below rated", min_value=0.20, max_value=0.55, value=0.44, step=0.01)
        drivetrain_eff = st.slider("Drivetrain efficiency", min_value=0.80, max_value=0.98, value=0.92, step=0.01)
        cut_in = st.slider("Cut-in speed (m/s)", min_value=2.0, max_value=6.0, value=3.0, step=0.5)
        rated_speed = st.slider("Rated speed (m/s)", min_value=8.0, max_value=16.0, value=12.0, step=0.5)
        cut_out = st.slider("Cut-out speed (m/s)", min_value=18.0, max_value=30.0, value=25.0, step=1.0)

        st.header("Wind Climate")
        mean_speed = st.slider("Average wind speed (m/s)", min_value=4.0, max_value=12.0, value=7.5, step=0.1)
        weibull_k = st.slider("Weibull shape factor k", min_value=1.2, max_value=4.0, value=2.0, step=0.1)

        st.markdown(
            """
            <div class="mini-note">
            Lower <code>k</code> means a broader, gustier wind climate. Higher <code>k</code> means speeds cluster more tightly around the mean.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if rated_speed <= cut_in:
        st.error("Rated speed must be greater than cut-in speed.")
        st.stop()

    if cut_out <= rated_speed:
        st.error("Cut-out speed must be greater than rated speed.")
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
            <div class="eyebrow">Educational Streamlit App</div>
            <h1>Wind Turbine Fundamentals Lab</h1>
            <p>Explore how a rotor slows the wind, how the wake expands, why the Betz limit matters, and how the wind climate shapes annual energy production.</p>
            <p>This tool is intentionally simple: it focuses on first-order physics you can inspect, tweak, and explain in a classroom or design review.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_formula_cards()
    st.write("")

    top_metrics = st.columns(5)
    top_metrics[0].metric("Rotor area", f"{area:,.0f} m^2")
    top_metrics[1].metric("Available wind power", f"{free_stream_power_kw:,.0f} kW")
    top_metrics[2].metric("Current Cp from a", f"{cp_from_induction:.3f}")
    top_metrics[3].metric("Disk speed", f"{disk_speed:.2f} m/s")
    top_metrics[4].metric("Far wake speed", f"{wake_speed:.2f} m/s")

    tab1, tab2, tab3 = st.tabs(
        ["Betz And Induction", "Wake And Power Curve", "Wind Climate And AEP"]
    )

    with tab1:
        left, right = st.columns([1.15, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Betz law through axial induction")
            st.write(
                "For an ideal actuator disk, the axial induction factor `a` controls how much the flow slows at the rotor. "
                "The same `a` also sets the ideal power coefficient `Cp = 4a(1-a)^2`."
            )
            st.plotly_chart(create_betz_figure(induction), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Upstream and downstream speed")
            st.write(
                "The rotor induces a velocity deficit before the disk, then leaves a slower far wake behind it. "
                "In ideal 1D momentum theory:"
            )
            st.latex(r"U_{disk} = U_{\infty}(1-a) \qquad U_{wake} = U_{\infty}(1-2a)")
            st.plotly_chart(create_velocity_figure(induction), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Three induction examples")
        example_cols = st.columns(3)
        example_cases = [
            ("Light loading", 0.15),
            ("Near Betz optimum", 1 / 3),
            ("Heavy loading", 0.45),
        ]
        for col, (label, a_case) in zip(example_cols, example_cases):
            cp_case = betz_cp(a_case)
            disk_case = wind_speed * (1 - a_case)
            wake_case = wind_speed * (1 - 2 * a_case)
            wake_factor_case = math.sqrt((1 - a_case) / (1 - 2 * a_case))
            with col:
                st.metric(label, f"a = {a_case:.2f}")
                st.write(f"Cp = {cp_case:.3f}")
                st.write(f"Disk speed = {disk_case:.2f} m/s")
                st.write(f"Far wake = {wake_case:.2f} m/s")
                st.write(f"Wake radius = {wake_factor_case:.2f} R")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        left, right = st.columns([1.1, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Wake expansion")
            st.write(
                "As the wake slows down, it must expand to carry the same mass flow. "
                "In simple momentum theory, the far-wake area ratio is:"
            )
            st.latex(r"\frac{A_{wake}}{A_{disk}} = \frac{1-a}{1-2a}")
            st.plotly_chart(create_streamtube_figure(induction), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Power curve fundamentals")
            st.write(
                "Below rated speed, this simplified model uses constant `Cp` so power follows the cubic wind-speed law. "
                "Above rated, control holds the machine at constant power until cut-out."
            )
            st.plotly_chart(
                create_power_curve_figure(speeds, power_curve_kw, rated_power_kw),
                width="stretch",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        bottom_metrics = st.columns(4)
        bottom_metrics[0].metric("Extracted power now", f"{extracted_power_kw:,.0f} kW")
        bottom_metrics[1].metric("Betz-limit power", f"{betz_limit_kw:,.0f} kW")
        bottom_metrics[2].metric("Assumed rated power", f"{rated_power_kw:,.0f} kW")
        bottom_metrics[3].metric("Far-wake radius", f"{wake_radius_factor:.2f} x rotor radius")

    with tab3:
        left, right = st.columns([1.15, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Wind field influence with Weibull `k`")
            st.write(
                "The same turbine behaves very differently in different wind climates. "
                "Average wind speed shifts the distribution, while `k` changes how narrow or broad it is."
            )
            st.plotly_chart(
                create_weibull_figure(speeds, pdf, relative_energy, mean_speed, weibull_k),
                width="stretch",
            )
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("Annual energy picture")
            st.write(
                "Annual energy production comes from the overlap between the power curve and the wind-speed probability distribution."
            )
            st.metric("Average electrical power", f"{avg_power_kw:,.0f} kW")
            st.metric("Annual energy production", f"{aep_kwh:,.0f} kWh/year")
            st.metric("Capacity factor", f"{capacity_factor:.1%}")
            st.write("")
            st.write("Helpful reading of the sliders:")
            st.write("- Higher mean wind speed raises both energy capture and time spent near rated power.")
            st.write("- Lower `k` spreads the wind speeds out, which can help or hurt depending on where the power curve sits.")
            st.write("- Because power scales with `U^3`, energy often comes from winds above the mean speed.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown(
            """
            <div class="mini-note">
            This is a first-principles teaching model. It does not include tip losses, yaw misalignment, turbulence intensity, shear, drivetrain limits beyond a simple efficiency factor, or detailed wake recovery.
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
