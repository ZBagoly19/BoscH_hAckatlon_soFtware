# this brake distance definition is from the book: A Policy on Geometric Design of Highways and Streets
def brake_distance_calc__AASHTO(reaction_time, velocity, slope, friction=0.7):
    return (0.278 * reaction_time * velocity) + velocity*velocity / (254 * (friction + slope))

# a_max: maximal deceleration [m/s^2]; max_jerk: [m/s^3]
def brake_distance_calc__challenge_hint(v0, t_lat, a_ego, a_max=-9, max_jerk=-30):
    d1 = v0 * t_lat + a_max / 2 * t_lat * t_lat

    t_2 = (a_max - a_ego) / max_jerk
    d2 = max_jerk / 6 * t_2 * t_2 * t_2 + a_max / 2 * t_2 * t_2 + v0 * t_2

    delta_v1 = max_jerk /2 * t_2*t_2  +  a_ego * t_2
    v1 = v0 + delta_v1
    delta_v2 = -v1
    t_3 = delta_v2 / a_max
    d3 = a_max /2 * t_3*t_3  +  v1 * t_3

    return d1 + d2 + d3