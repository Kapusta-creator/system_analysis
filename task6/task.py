import json

STEP = 0.01


class Ranges:
    def __init__(self, init_data):
        self.ranges = []
        self.name = init_data['id']
        self.min_value = None
        self.max_value = None
        for point_idx in range(len(init_data['points']) - 1):
            self.ranges.append(
                Range(
                    init_data['points'][point_idx][0],
                    init_data['points'][point_idx + 1][0],
                    init_data['points'][point_idx][1],
                    init_data['points'][point_idx + 1][1],
                ),
            )
            self.ranges = sorted(self.ranges, key=lambda x: x.from_value)
            self.min_value = self.ranges[0].from_value
            self.max_value = self.ranges[-1].to_value

    def get_mu(self, x):
        for rng in self.ranges:
            if rng.from_value <= x < rng.to_value:
                return rng.get_mu()(x)
        if self.ranges[0].from_value > x:
            if self.ranges[0].is_core_from:
                return 1
            else:
                return 0
        else:
            if self.ranges[-1].is_core_to:
                return 1
            else:
                return 0

    def get_min(self):
        return self.ranges[0].from_value

    def get_max(self):
        return self.ranges[-1].to_value


class Range:
    def __init__(self, from_value, to_value, is_core_from, is_core_to):
        self.from_value = from_value
        self.to_value = to_value
        self.is_core_from = is_core_from
        self.is_core_to = is_core_to

    def get_mu(self):
        if self.is_core_to and self.is_core_from:
            return lambda x: 1
        elif not self.is_core_from and not self.is_core_to:
            return lambda x: 0
        elif self.is_core_from:
            return lambda x: 1.0 - (x - self.from_value) / (self.to_value - self.from_value)
        else:
            return lambda x: (x - self.from_value) / (self.to_value - self.from_value)


def get_values_mapping(mapping):
    loaded_map = json.loads(mapping)
    values_mapping = dict()
    for current_mapping in loaded_map:
        values_mapping[current_mapping[0]] = current_mapping[1]

    return values_mapping


def task(regulator, temperature, mapping, current_temperature) -> float:
    regulator_values = dict()
    temperature_mu = dict()
    regulator_loaded = json.loads(regulator)
    for value in regulator_loaded.values():
        for reg_opts in value:
            new_ranges = Ranges(reg_opts)
            regulator_values[new_ranges.name] = new_ranges
    temperature_loaded = json.loads(temperature)
    for value in temperature_loaded.values():
        for temp_opts in value:
            new_ranges = Ranges(temp_opts)
            temperature_mu[new_ranges.name] = new_ranges.get_mu(current_temperature)
    values_mapping = get_values_mapping(mapping)
    max_s = None
    min_s = None
    for val in regulator_values.values():
        if max_s is None:
            max_s = val.get_min()
        else:
            max_s = max(max_s, val.get_max())
        if min_s is None:
            min_s = val.get_min()
        else:
            min_s = min(min_s, val.get_min())
    cur_s = min_s
    max_mu_s = 0
    ans = cur_s
    while cur_s <= max_s:
        mu_c_list = []
        mu_keys = []
        for key, val in values_mapping.items():
            mu_c_list.append(min(temperature_mu[key], regulator_values[val].get_mu(cur_s)))
            mu_keys.append([key, temperature_mu[key], val, regulator_values[val].get_mu(cur_s)])
        if max(mu_c_list) < max_mu_s:
            break
        elif max(mu_c_list) > max_mu_s:
            ans = cur_s
            max_mu_s = max(mu_c_list)
        if max_mu_s == 1:
            break
        cur_s += STEP

    return ans


if __name__ == "__main__":
    regulator_json = '''{
          "уровень нагрева": [
              {
                "id": "слабый",
                "points": [
                    [0,0],
                    [0,1],
                    [5,1],
                    [8,0]
                ]
              },
              {
                "id": "умеренный",
                "points": [
                    [5,0],
                    [8,1],
                    [13,1],
                    [16,0]
                ]
              },
              {
                "id": "интенсивный",
                "points": [
                    [13,0],
                    [18,1],
                    [23,1],
                    [26,0]
                ]
              }
          ]
        }'''
    temperature_json = '''{
          "температура": [
              {
              "id": "холодно",
              "points": [
                  [0,1],
                  [18,1],
                  [22,0],
                  [50,0]
              ]
              },
              {
              "id": "комфортно",
              "points": [
                  [18,0],
                  [22,1],
                  [24,1],
                  [26,0]
              ]
              },
              {
              "id": "жарко",
              "points": [
                  [0,0],
                  [24,0],
                  [26,1],
                  [50,1]
              ]
              }
          ]
        }'''
    mapping_json = '''[
            ["холодно", "интенсивный"],
            ["комфортно", "умеренный"],
            ["жарко", "слабый"]
        ] '''
    print(f"t = 19.0 s = {round(task(regulator_json, temperature_json, mapping_json, 19.0), 2)}")
    print(f"t = 23.0 s = {round(task(regulator_json, temperature_json, mapping_json, 23.0), 2)}")
    print(f"t = 10.0 s = {round(task(regulator_json, temperature_json, mapping_json, 10.0), 2)}")
