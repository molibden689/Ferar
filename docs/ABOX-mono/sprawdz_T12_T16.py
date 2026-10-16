"""Quasistatic load-line estimate; not a SPICE or thermal-transient model.

Symmetric constant-VBE approximation, two parallel output devices per branch.
The CSV records the upper branch; lower branch is its sign-reversed analogue.
Gain values are scenario assumptions, not guaranteed manufacturer minima.
"""
import csv
import math
from pathlib import Path

import numpy as np

VBE = 0.65
BETA_PRE = 70.0
RE = 0.22
RB = 4.7
RBE = 68.0
R19 = 1200.0
R20 = 100.0
VPK = math.sqrt(2 * 100 * 6)


def load_line(vout, iout, rail, beta_output, beta_driver):
    """Return active-branch IC12, VCE12 and instantaneous dissipation.

    Includes the base-emitter bleeder current in each output emitter resistor
    and base stopper, driver emitter/base current, R19 current, R20 current,
    and contribution of driver and predriver currents to the output node.
    The small crossover/idle region is excluded, not treated as verified.
    """
    q = VBE / RBE
    a = ((RE * (1 + 1 / beta_output) + RB / beta_output) / R19
         + 2 / (beta_output * (beta_driver + 1)))
    b = ((RE * q + 2 * VBE + RB * q) / R19
         + 2 * q / (beta_driver + 1))
    emitter_factor = 1 + 1 / BETA_PRE
    denominator = (2 + 2 / beta_output * beta_driver / (beta_driver + 1)
                   + emitter_factor * a)
    offset = 2 * q * beta_driver / (beta_driver + 1) + emitter_factor * b
    ic_output = np.maximum((iout - offset) / denominator, 0)
    ic12 = a * ic_output + b
    ie12 = emitter_factor * ic12
    ir19 = (RE * ((1 + 1 / beta_output) * ic_output + q)
            + 2 * VBE + RB * (ic_output / beta_output + q)) / R19
    base_driver = rail - R19 * ir19
    vce12 = base_driver - (vout + R20 * ie12)
    active = (iout > offset) & (vce12 > 0)
    power = np.where(active, vce12 * ic12, 0)
    return ic12, vce12, power, active


def main():
    theta = np.linspace(0, 2 * math.pi, 100_000, endpoint=False)
    rows = []
    for rail in (50, 55):
        for impedance in (6, 4):
            for phase in (0, 60, 90):
                vout = VPK * np.sin(theta)
                iout = VPK / impedance * np.sin(theta - math.radians(phase))
                for beta_output in (20, 40, 80):
                    for beta_driver in (25, 40, 80):
                        ic, vce, power, active = load_line(
                            vout, iout, rail, beta_output, beta_driver)
                        k = int(np.argmax(power))
                        rows.append({
                            'rail_V': rail,
                            'impedance_magnitude_ohm': impedance,
                            'current_lag_deg': phase,
                            'beta_output_assumed': beta_output,
                            'beta_driver_assumed': beta_driver,
                            'beta_T12_assumed': int(BETA_PRE),
                            'P_peak_W': round(float(power[k]), 6),
                            'P_mean_active_branch_W': round(float(power.mean()), 6),
                            'Ic_peak_active_mA': round(float(ic[active].max()) * 1000, 6),
                            'Vout_at_P_peak_V': round(float(vout[k]), 6),
                            'Iout_at_P_peak_A': round(float(iout[k]), 6),
                            'Ic_at_P_peak_mA': round(float(ic[k]) * 1000, 6),
                            'Vce_at_P_peak_V': round(float(vce[k]), 6),
                        })
    path = Path(__file__).resolve().parent / 'T12-T16-wyniki.csv'
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        if (row['rail_V'] == 55 and row['beta_output_assumed'] == 20
                and row['beta_driver_assumed'] == 25):
            print(row)
    print(f'Wrote {len(rows)} scenarios to {path.name}')


if __name__ == '__main__':
    main()
