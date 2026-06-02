from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI
from scipy.optimize import brentq


P_ATM = 101325.0


@dataclass
class Problem1Result:
    q_w: float
    m_water: float
    correction_factor: float
    dt_lm_counterflow: float
    dt_lm_corrected: float
    area: float


@dataclass
class Problem2Result:
    T_evap_C: float
    T_cond_C: float
    P_evap_kPa: float
    P_cond_kPa: float
    qL_kJ_per_kg: float
    Q_kW: float
    T_water_out_C: float
    epsilon: float
    Re_water: float
    Pr_water: float
    Nu_water: float
    h_water: float
    U: float
    dt_lm: float
    area_m2: float
    L_required_m: float
    N_passes_continuous: float
    N_passes_selected: int
    L_selected_m: float
    Q_selected_kW: float
    T_water_out_selected_C: float


@dataclass
class Problem3DesignResult:
    D_m: float
    L_m: float
    Q_W: float
    T_hot_out_K: float
    dt_lm_K: float
    Re_cold: float
    Re_hot: float
    f_cold: float
    f_hot: float
    Nu_cold: float
    Nu_hot: float
    h_cold: float
    h_hot: float
    U: float
    dp_cold_Pa: float
    V_cold: float
    V_hot: float
    cp_cold: float
    cp_hot: float


def lmtd_counterflow(dt1: float, dt2: float) -> float:
    if dt1 <= 0 or dt2 <= 0:
        raise ValueError("La LMTD requiere diferencias terminales positivas.")
    if abs(dt1 - dt2) < 1e-12:
        return dt1
    return (dt1 - dt2) / math.log(dt1 / dt2)


def fakheri_correction_factor(Thi: float, Tho: float, Tci: float, Tco: float, shells: int) -> float:
    R = (Thi - Tho) / (Tco - Tci)
    P = (Tco - Tci) / (Thi - Tci)
    if abs(R - 1.0) < 1e-12:
        W2 = (shells - shells * P) / (shells - shells * P + P)
        num = math.sqrt(2.0) * (1.0 - W2) / W2
        den = math.log((W2 / (1.0 - W2) + 1.0 / math.sqrt(2.0)) / (W2 / (1.0 - W2) - 1.0 / math.sqrt(2.0)))
        return num / den
    W = ((1.0 - P * R) / (1.0 - P)) ** (1.0 / shells)
    S = math.sqrt(R * R + 1.0) / (R - 1.0)
    return S * math.log(W) / math.log((1.0 + W - S + S * W) / (1.0 + W + S - S * W))


def water_props(T: float) -> dict[str, float]:
    rho = PropsSI("D", "T", T, "P", P_ATM, "Water")
    mu = PropsSI("V", "T", T, "P", P_ATM, "Water")
    k = PropsSI("L", "T", T, "P", P_ATM, "Water")
    cp = PropsSI("C", "T", T, "P", P_ATM, "Water")
    pr = cp * mu / k
    return {"rho": rho, "mu": mu, "k": k, "cp": cp, "Pr": pr}


def air_props(T: float) -> dict[str, float]:
    rho = PropsSI("D", "T", T, "P", P_ATM, "Air")
    mu = PropsSI("V", "T", T, "P", P_ATM, "Air")
    k = PropsSI("L", "T", T, "P", P_ATM, "Air")
    cp = PropsSI("C", "T", T, "P", P_ATM, "Air")
    pr = cp * mu / k
    return {"rho": rho, "mu": mu, "k": k, "cp": cp, "Pr": pr}


def darcy_friction_factor(Re: float) -> float:
    if Re < 2300.0:
        return 64.0 / Re
    if Re > 3000.0:
        return (0.79 * math.log(Re) - 1.64) ** -2
    f_lam = 64.0 / 2300.0
    f_turb = (0.79 * math.log(3000.0) - 1.64) ** -2
    w = (Re - 2300.0) / 700.0
    return f_lam + w * (f_turb - f_lam)


def tube_nusselt(Re: float, Pr: float, f: float) -> float:
    if Re < 2300.0:
        return 3.66
    if Re > 3000.0:
        num = (f / 8.0) * (Re - 1000.0) * Pr
        den = 1.0 + 12.7 * math.sqrt(f / 8.0) * (Pr ** (2.0 / 3.0) - 1.0)
        return num / den
    Nu_lam = 3.66
    f_turb = (0.79 * math.log(3000.0) - 1.64) ** -2
    num = (f_turb / 8.0) * (3000.0 - 1000.0) * Pr
    den = 1.0 + 12.7 * math.sqrt(f_turb / 8.0) * (Pr ** (2.0 / 3.0) - 1.0)
    Nu_turb = num / den
    w = (Re - 2300.0) / 700.0
    return Nu_lam + w * (Nu_turb - Nu_lam)


def problem1() -> Problem1Result:
    cp_alcohol = 2670.0
    cp_water = 4190.0
    m_alcohol = 0.7
    Tci = 20.0
    Tco = 60.0
    Thi = 90.0
    Tho = 35.0
    U = 823.0

    q_w = m_alcohol * cp_alcohol * (Tco - Tci)
    m_water = q_w / (cp_water * (Thi - Tho))
    F = fakheri_correction_factor(Thi=Thi, Tho=Tho, Tci=Tci, Tco=Tco, shells=2)
    dt_cf = lmtd_counterflow(Thi - Tco, Tho - Tci)
    dt_corrected = F * dt_cf
    area = q_w / (U * dt_corrected)
    return Problem1Result(
        q_w=q_w,
        m_water=m_water,
        correction_factor=F,
        dt_lm_counterflow=dt_cf,
        dt_lm_corrected=dt_corrected,
        area=area,
    )


def _iterate_water_outlet(Q: float, m_w: float, T_in: float) -> tuple[float, dict[str, float]]:
    T_out = T_in - 5.0
    for _ in range(100):
        T_bulk = 0.5 * (T_in + T_out)
        props = water_props(T_bulk)
        T_new = T_in - Q / (m_w * props["cp"])
        if abs(T_new - T_out) < 1e-10:
            return T_new, props
        T_out = T_new
    props = water_props(0.5 * (T_in + T_out))
    return T_out, props


def problem2(
    T_evap_C: float = 0.0,
    T_cond_C: float = 40.0,
    m_refrigerant: float = 3.42,
    m_water: float = 17.0,
    T_water_in_C: float = 15.0,
    D_tube_m: float = 0.300,
    h_refrigerant: float = 5000.0,
    shell_width_m: float = 6.0,
) -> Problem2Result:
    T_evap = T_evap_C + 273.15
    T_cond = T_cond_C + 273.15
    T_water_in = T_water_in_C + 273.15

    P_evap = PropsSI("P", "T", T_evap, "Q", 1, "R134a")
    P_cond = PropsSI("P", "T", T_cond, "Q", 0, "R134a")

    h1 = PropsSI("H", "T", T_evap, "Q", 1, "R134a")
    s1 = PropsSI("S", "T", T_evap, "Q", 1, "R134a")
    _ = PropsSI("H", "P", P_cond, "S", s1, "R134a")
    h3 = PropsSI("H", "T", T_cond, "Q", 0, "R134a")
    h4 = h3
    qL = h1 - h4
    Q = m_refrigerant * qL

    T_water_out, props_w = _iterate_water_outlet(Q=Q, m_w=m_water, T_in=T_water_in)
    A_flow = math.pi * D_tube_m**2 / 4.0
    V_water = m_water / (props_w["rho"] * A_flow)
    Re_water = props_w["rho"] * V_water * D_tube_m / props_w["mu"]
    f_water = darcy_friction_factor(Re_water)
    Nu_water = tube_nusselt(Re_water, props_w["Pr"], f_water)
    h_water = Nu_water * props_w["k"] / D_tube_m
    U = 1.0 / (1.0 / h_refrigerant + 1.0 / h_water)
    dt_lm = lmtd_counterflow(T_water_in - T_evap, T_water_out - T_evap)
    area = Q / (U * dt_lm)
    L_required = area / (math.pi * D_tube_m)
    N_cont = L_required / shell_width_m

    epsilon = Q / (m_water * props_w["cp"] * (T_water_in - T_evap))

    N_selected = max(1, int(round(N_cont)))
    L_selected = N_selected * shell_width_m
    area_selected = math.pi * D_tube_m * L_selected
    NTU_selected = U * area_selected / (m_water * props_w["cp"])
    epsilon_selected = 1.0 - math.exp(-NTU_selected)
    Q_selected = epsilon_selected * m_water * props_w["cp"] * (T_water_in - T_evap)
    T_out_selected = T_water_in - Q_selected / (m_water * props_w["cp"])

    return Problem2Result(
        T_evap_C=T_evap_C,
        T_cond_C=T_cond_C,
        P_evap_kPa=P_evap / 1000.0,
        P_cond_kPa=P_cond / 1000.0,
        qL_kJ_per_kg=qL / 1000.0,
        Q_kW=Q / 1000.0,
        T_water_out_C=T_water_out - 273.15,
        epsilon=epsilon,
        Re_water=Re_water,
        Pr_water=props_w["Pr"],
        Nu_water=Nu_water,
        h_water=h_water,
        U=U,
        dt_lm=dt_lm,
        area_m2=area,
        L_required_m=L_required,
        N_passes_continuous=N_cont,
        N_passes_selected=N_selected,
        L_selected_m=L_selected,
        Q_selected_kW=Q_selected / 1000.0,
        T_water_out_selected_C=T_out_selected - 273.15,
    )


def problem2_temperature_profile(result: Problem2Result, n_points: int = 200) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    T_ref = result.T_evap_C + 273.15
    T_in = 15.0 + 273.15
    T_out = result.T_water_out_C + 273.15
    x = np.linspace(0.0, result.L_required_m, n_points)
    ratio = (T_out - T_ref) / (T_in - T_ref)
    Tw = T_ref + (T_in - T_ref) * ratio ** (x / result.L_required_m)
    Tr = np.full_like(x, T_ref)
    return x, Tw - 273.15, Tr - 273.15


def _solve_hot_outlet(m_dot: float, Tco: float, Thi: float, Tci: float) -> tuple[float, float, float]:
    Tho = Thi - (Tco - Tci)
    for _ in range(100):
        Tcb = 0.5 * (Tci + Tco)
        Thb = 0.5 * (Thi + Tho)
        cp_c = air_props(Tcb)["cp"]
        cp_h = air_props(Thb)["cp"]
        Q = m_dot * cp_c * (Tco - Tci)
        Tho_new = Thi - Q / (m_dot * cp_h)
        if abs(Tho_new - Tho) < 1e-10:
            return Tho_new, cp_c, cp_h
        Tho = Tho_new
    cp_c = air_props(0.5 * (Tci + Tco))["cp"]
    cp_h = air_props(0.5 * (Thi + Tho))["cp"]
    return Tho, cp_c, cp_h


def _problem3_performance(D: float, L: float, m_dot: float, Thi: float, Tci: float, Tco: float) -> dict[str, float]:
    Tho, cp_c, cp_h = _solve_hot_outlet(m_dot=m_dot, Tco=Tco, Thi=Thi, Tci=Tci)
    Tcb = 0.5 * (Tci + Tco)
    Thb = 0.5 * (Thi + Tho)
    cold = air_props(Tcb)
    hot = air_props(Thb)
    area_flow = math.pi * D**2 / 4.0
    V_cold = m_dot / (cold["rho"] * area_flow)
    V_hot = m_dot / (hot["rho"] * area_flow)
    Re_cold = cold["rho"] * V_cold * D / cold["mu"]
    Re_hot = hot["rho"] * V_hot * D / hot["mu"]
    f_cold = darcy_friction_factor(Re_cold)
    f_hot = darcy_friction_factor(Re_hot)
    Nu_cold = tube_nusselt(Re_cold, cold["Pr"], f_cold)
    Nu_hot = tube_nusselt(Re_hot, hot["Pr"], f_hot)
    h_cold = Nu_cold * cold["k"] / D
    h_hot = Nu_hot * hot["k"] / D
    U = 1.0 / (1.0 / h_cold + 1.0 / h_hot)
    dt_lm = lmtd_counterflow(Thi - Tco, Tho - Tci)
    Q = m_dot * cp_c * (Tco - Tci)
    Q_hx = U * math.pi * D * L * dt_lm
    dp_cold = f_cold * (L / D) * (cold["rho"] * V_cold**2 / 2.0)
    return {
        "Tho": Tho,
        "cp_c": cp_c,
        "cp_h": cp_h,
        "Re_cold": Re_cold,
        "Re_hot": Re_hot,
        "f_cold": f_cold,
        "f_hot": f_hot,
        "Nu_cold": Nu_cold,
        "Nu_hot": Nu_hot,
        "h_cold": h_cold,
        "h_hot": h_hot,
        "U": U,
        "dt_lm": dt_lm,
        "Q": Q,
        "Q_hx": Q_hx,
        "dp_cold": dp_cold,
        "V_cold": V_cold,
        "V_hot": V_hot,
    }


def problem3_design(
    m_dot: float = 0.0025,
    Tci: float = 250.0,
    Tco_target: float = 350.0,
    Thi: float = 400.0,
    dp_allow_Pa: float = 15000.0,
) -> Problem3DesignResult:
    Tho, cp_c, cp_h = _solve_hot_outlet(m_dot=m_dot, Tco=Tco_target, Thi=Thi, Tci=Tci)
    dt_lm = lmtd_counterflow(Thi - Tco_target, Tho - Tci)
    Q = m_dot * cp_c * (Tco_target - Tci)

    def length_for_diameter(D: float) -> tuple[float, dict[str, float]]:
        perf = _problem3_performance(D=D, L=1.0, m_dot=m_dot, Thi=Thi, Tci=Tci, Tco=Tco_target)
        U = perf["U"]
        L = Q / (U * math.pi * D * dt_lm)
        perf = _problem3_performance(D=D, L=L, m_dot=m_dot, Thi=Thi, Tci=Tci, Tco=Tco_target)
        return L, perf

    def residual(D: float) -> float:
        L, perf = length_for_diameter(D)
        return perf["dp_cold"] - dp_allow_Pa

    D = brentq(residual, 0.006, 0.007)
    L, perf = length_for_diameter(D)
    return Problem3DesignResult(
        D_m=D,
        L_m=L,
        Q_W=Q,
        T_hot_out_K=perf["Tho"],
        dt_lm_K=perf["dt_lm"],
        Re_cold=perf["Re_cold"],
        Re_hot=perf["Re_hot"],
        f_cold=perf["f_cold"],
        f_hot=perf["f_hot"],
        Nu_cold=perf["Nu_cold"],
        Nu_hot=perf["Nu_hot"],
        h_cold=perf["h_cold"],
        h_hot=perf["h_hot"],
        U=perf["U"],
        dp_cold_Pa=perf["dp_cold"],
        V_cold=perf["V_cold"],
        V_hot=perf["V_hot"],
        cp_cold=cp_c,
        cp_hot=cp_h,
    )


def _problem3_residual_for_tco(Tco: float, D: float, L: float, m_dot: float, Thi: float, Tci: float) -> float:
    perf = _problem3_performance(D=D, L=L, m_dot=m_dot, Thi=Thi, Tci=Tci, Tco=Tco)
    return perf["Q_hx"] - perf["Q"]


def problem3_parametric(
    D: float,
    L: float,
    m_values: Iterable[float],
    Thi: float = 400.0,
    Tci: float = 250.0,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for m_dot in m_values:
        Tco = brentq(_problem3_residual_for_tco, Tci + 1e-6, Thi - 1e-6, args=(D, L, m_dot, Thi, Tci))
        perf = _problem3_performance(D=D, L=L, m_dot=m_dot, Thi=Thi, Tci=Tci, Tco=Tco)
        rows.append(
            {
                "m_dot": m_dot,
                "Tco_K": Tco,
                "Tho_K": perf["Tho"],
                "Q_W": perf["Q"],
                "dp_Pa": perf["dp_cold"],
            }
        )
    return rows


def generate_problem2_figure(result: Problem2Result, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    x, Tw, Tr = problem2_temperature_profile(result)
    plt.figure(figsize=(7.2, 4.4))
    plt.plot(x, Tw, label="Agua", linewidth=2.3)
    plt.plot(x, Tr, label="R134a (Tsat)", linewidth=2.3, linestyle="--")
    plt.xlabel("Longitud acumulada del tubo [m]")
    plt.ylabel("Temperatura [°C]")
    plt.title("Punto 2: Perfil de temperaturas a lo largo del evaporador")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()
    return output_path


def generate_problem3_figure(rows: list[dict[str, float]], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    m = np.array([row["m_dot"] for row in rows])
    Tco = np.array([row["Tco_K"] for row in rows]) - 273.15
    Q = np.array([row["Q_W"] for row in rows])
    dp = np.array([row["dp_Pa"] for row in rows]) / 1000.0

    fig, axes = plt.subplots(3, 1, figsize=(7.2, 9.0), sharex=True)
    axes[0].plot(m, Tco, color="#0a6c74", linewidth=2.2)
    axes[0].set_ylabel(r"$T_{c,salida}$ [°C]")
    axes[0].grid(True, alpha=0.25)

    axes[1].plot(m, Q, color="#bc4b0a", linewidth=2.2)
    axes[1].set_ylabel(r"$\dot Q$ [W]")
    axes[1].grid(True, alpha=0.25)

    axes[2].plot(m, dp, color="#5a3d9a", linewidth=2.2)
    axes[2].set_ylabel(r"$\Delta p_f$ [kPa]")
    axes[2].set_xlabel(r"Flujo másico equilibrado [kg/s]")
    axes[2].grid(True, alpha=0.25)

    fig.suptitle("Punto 3: Respuesta del intercambiador con D y L fijos")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def generate_all_figures(output_dir: str | Path) -> dict[str, Path]:
    output_dir = Path(output_dir)
    p2 = problem2()
    p3 = problem3_design()
    rows = problem3_parametric(D=p3.D_m, L=p3.L_m, m_values=np.linspace(0.002, 0.004, 21))
    fig2 = generate_problem2_figure(p2, output_dir / "taller5_p2_temperaturas.png")
    fig3 = generate_problem3_figure(rows, output_dir / "taller5_p3_parametrico.png")
    return {"p2": fig2, "p3": fig3}


def to_dict(obj: object) -> dict:
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    raise TypeError(f"Objeto no serializable: {type(obj)!r}")
