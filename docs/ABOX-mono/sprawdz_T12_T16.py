"""Quasistatic load-line estimate; not a SPICE or thermal-transient model.

Symmetric constant-VBE approximation, one output device per branch.
The CSV records the upper branch; lower branch is its sign-reversed analogue.
Gain values are scenario assumptions, not guaranteed manufacturer minima.
The target is 100 W / 6 ohm; 4-ohm rows are unapproved comparisons.
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
OUTPUT_DEVICES_PER_BRANCH = 1


def load_line(vout, iout, rail, beta_output, beta_driver):
    """Return active-branch IC12, VCE12 and instantaneous dissipation.

    Includes the base-emitter bleeder current in each output emitter resistor
    and base stopper, driver emitter/base current, R19 current, R20 current,
    and contribution of driver and predriver currents to the output node.
    The small crossover/idle region is excluded, not treated as verified.
    """
    n = OUTPUT_DEVICES_PER_BRANCH
    q = VBE / RBE
    # IC12 = a * IC_output_per_device + b. The 2 * VBE below is the
    # sum of the output-device and driver junction drops, not two devices.
    a = ((RE * (1 + 1 / beta_output) + RB / beta_output) / R19
         + n / (beta_output * (beta_driver + 1)))
    b = ((RE * q + 2 * VBE + RB * q) / R19
         + n * q / (beta_driver + 1))
    emitter_factor = 1 + 1 / BETA_PRE
    denominator = (n + n / beta_output * beta_driver / (beta_driver + 1)
                   + emitter_factor * a)
    offset = n * q * beta_driver / (beta_driver + 1) + emitter_factor * b
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


def check_branch_balance(vout, iout, rail, beta_output, beta_driver,
                         ic12, vce12, active):
    """Reconstruct physical branch currents and check KCL/KVL and energy.

    This check does not reuse load_line's affine coefficients. It recovers
    output current from the actual resistor and junction voltage drops,
    then balances the driver node, OUTI node and all three power ports.
    Only the modeled active branch is checked; crossover is not inferred.
    """
    n = OUTPUT_DEVICES_PER_BRANCH
    vout = np.asarray(vout)[active]
    iout = np.asarray(iout)[active]
    ic12 = np.asarray(ic12)[active]
    vce12 = np.asarray(vce12)[active]
    ib12 = ic12 / BETA_PRE
    ie12 = ic12 + ib12
    ve12 = vout + R20 * ie12
    vc12 = ve12 + vce12
    ve_driver = vc12 + VBE

    # Rail -> RE -> output BE junction -> RB -> driver emitter.
    q = VBE / RBE
    ic_output = ((rail - ve_driver - VBE - (RE + RB) * q)
                 / (RE * (1 + 1 / beta_output) + RB / beta_output))
    ib_output = ic_output / beta_output
    irb = ib_output + q
    ire = ic_output + ib_output + q
    ve_output = rail - RE * ire
    vb_output = ve_output - VBE
    ie_driver = n * irb
    ib_driver = ie_driver / (beta_driver + 1)
    ic_driver = ie_driver - ib_driver
    ir19 = (rail - vc12) / R19

    driver_node_error = ic12 - (ir19 + ib_driver)
    output_node_error = iout - (n * ic_output + ic_driver + ie12)
    base_resistor_error = vb_output - ve_driver - RB * irb

    rail_current = n * ire + ir19
    input_power = rail * rail_current + (ve12 + VBE) * ib12
    output_power = vout * iout
    resistor_power = (n * (RE * ire**2 + RB * irb**2 + VBE * q)
                      + R19 * ir19**2 + R20 * ie12**2)
    transistor_power = (n * ((ve_output - vout) * ic_output
                            + VBE * ib_output)
                        + (ve_driver - vout) * ic_driver + VBE * ib_driver
                        + vce12 * ic12 + VBE * ib12)
    power_error = input_power - output_power - resistor_power - transistor_power
    residuals = {
        'KCL_A': float(max(np.abs(driver_node_error).max(),
                           np.abs(output_node_error).max())),
        'KVL_V': float(np.abs(base_resistor_error).max()),
        'energy_W': float(np.abs(power_error).max()),
    }
    if (np.any(ic_output < -1e-10) or residuals['KCL_A'] > 1e-10
            or residuals['KVL_V'] > 1e-10 or residuals['energy_W'] > 1e-8):
        raise AssertionError(f'Physical branch balance failed: {residuals}')
    return residuals


def main():
    theta = np.linspace(0, 2 * math.pi, 100_000, endpoint=False)
    rows = []
    max_residuals = {'KCL_A': 0.0, 'KVL_V': 0.0, 'energy_W': 0.0}
    for rail in (50, 55):
        for impedance in (6, 4):
            for phase in (0, 60, 90):
                vout = VPK * np.sin(theta)
                iout = VPK / impedance * np.sin(theta - math.radians(phase))
                for beta_output in (20, 40, 80):
                    for beta_driver in (25, 40, 80):
                        ic, vce, power, active = load_line(
                            vout, iout, rail, beta_output, beta_driver)
                        residuals = check_branch_balance(
                            vout, iout, rail, beta_output, beta_driver,
                            ic, vce, active)
                        for key, value in residuals.items():
                            max_residuals[key] = max(max_residuals[key], value)
                        k = int(np.argmax(power))
                        rows.append({
                            'rail_V': rail,
                            'impedance_magnitude_ohm': impedance,
                            'current_lag_deg': phase,
                            'output_devices_per_branch': OUTPUT_DEVICES_PER_BRANCH,
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
    print(f'Max physical-balance residuals: {max_residuals}')


if __name__ == '__main__':
    main()
