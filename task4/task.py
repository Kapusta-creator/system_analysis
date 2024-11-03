import json
import math


def get_states():
    a_states = dict()
    b_states = dict()
    ab_states = dict()
    for i in range(1, 7):
        for j in range(1, 7):
            a_state_cnt = a_states.get(i + j, 0)
            a_states[i + j] = a_state_cnt + 1
            b_state_cnt = b_states.get(i * j, 0)
            b_states[i * j] = b_state_cnt + 1
            ab_state_cnt = ab_states.get(f"{i + j}-{i * j}", 0)
            ab_states[f"{i + j}-{i * j}"] = ab_state_cnt + 1
    return a_states, b_states, ab_states


def get_single_entropy(states):
    h = 0.0
    states_cnt = sum(states.values())
    for cnt in states.values():
        h += cnt / states_cnt * math.log2(cnt / states_cnt)
    return -h


def task():
    a_states, b_states, ab_states = get_states()
    h_a = get_single_entropy(a_states)
    h_b = get_single_entropy(b_states)
    h_ab = get_single_entropy(ab_states)
    h_b_a = h_ab - h_a
    i_ab = h_b - h_b_a
    return [round(h_ab, 2), round(h_a, 2), round(h_b, 2), round(h_b_a, 2), round(i_ab, 2)]


if __name__ == "__main__":
    print(task())
