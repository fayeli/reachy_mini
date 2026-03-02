"""Dance sequence for Reachy Mini.

Phases:
  1. Wave hello  - antennas alternate left/right
  2. Head nods   - friendly acknowledgement
  3. Dance sway  - rhythmic body + head + antenna boogie
  4. Ta-da finish - proud pose, then return to neutral
"""

import time

import numpy as np

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

BPM = 120
DANCE_DURATION_S = 4.0

with ReachyMini() as mini:
    print("Starting hello dance!")

    # --- Center everything ---
    mini.goto_target(
        head=create_head_pose(),
        antennas=[0.0, 0.0],
        body_yaw=0.0,
        duration=1.0,
    )

    # === Phase 1: Wave hello ===
    print("Waving hello...")
    for _ in range(3):
        mini.goto_target(antennas=[0.6, -0.2], duration=0.25)
        mini.goto_target(antennas=[-0.2, 0.6], duration=0.25)
    mini.goto_target(antennas=[0.0, 0.0], duration=0.3)

    # === Phase 2: Head nods ===
    print("Nodding...")
    for _ in range(2):
        mini.goto_target(head=create_head_pose(pitch=20, degrees=True), duration=0.35)
        mini.goto_target(head=create_head_pose(pitch=-10, degrees=True), duration=0.35)
    mini.goto_target(head=create_head_pose(), duration=0.35)

    # === Phase 3: Dance sway (real-time control loop) ===
    print("Dancing!")
    start = time.monotonic()
    while time.monotonic() - start < DANCE_DURATION_S:
        elapsed = time.monotonic() - start
        t = elapsed * BPM / 60.0  # beat units

        roll = np.deg2rad(15) * np.sin(2 * np.pi * t)
        pitch = np.deg2rad(8) * np.sin(2 * np.pi * 2 * t)
        left_ant = 0.3 * np.sin(2 * np.pi * t)
        right_ant = 0.3 * np.sin(2 * np.pi * t + np.pi)  # opposite phase

        mini.set_target(
            head=create_head_pose(roll=roll, pitch=pitch, degrees=False),
            antennas=[left_ant, right_ant],
        )
        time.sleep(0.02)  # ~50 Hz

    # === Phase 4: Ta-da finish ===
    print("Ta-da!")
    mini.goto_target(
        head=create_head_pose(pitch=10, degrees=True),
        antennas=[0.5, 0.5],
        body_yaw=0.0,
        duration=0.5,
    )
    time.sleep(0.6)

    # Return to neutral
    mini.goto_target(
        head=create_head_pose(),
        antennas=[0.0, 0.0],
        duration=0.8,
    )

    print("Hello dance complete!")
