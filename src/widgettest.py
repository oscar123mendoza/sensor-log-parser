import os
import re
import numpy as np
import json

class WidgetTest:
    def __init__(self, filename, sensor_pattern):
        with open(filename) as f:
            self.lines = [line.rstrip() for line in f]
        self.thermometer_control = float(self.set_control()[1])
        self.humidistat_control = float(self.set_control()[2])

        self.sensor_pattern = sensor_pattern
        with open(filename) as f:
            self.parts = re.findall(self.regex_search(), f.read(), re.DOTALL)
        self.Dict = self.set_dict()
        self.log_response = self.sort_dict()

    def regex_search(self):
        first_pattern = ''
        second_pattern = ''
        pattern = ''
        for i, parts in enumerate(self.sensor_pattern.split(', ')):
            if i == 0:
                first_pattern = parts + '\d+.*?'
                second_pattern = parts + '\d+|$'
            else:
                first_pattern = first_pattern + '|' + parts + '\d+.*?'
                second_pattern = second_pattern + '|' + parts + '\d+|$'
        pattern = '(%s)(?=%s)' % (first_pattern, second_pattern)
        return pattern

    def value_search(self, sub, array):
        constant = "\n".join(s for s in array if sub.lower() in s.lower())
        return constant

    def set_control(self):
        control = self.value_search('reference', self.lines).split(" ")
        return control

    def set_dict(self):
        Dict = {}
        for i, part in enumerate(self.parts):
            clean_parts = part.rstrip().split(" \n")
            dict_key = clean_parts.pop(0)
            Dict[dict_key] = []
            for j, values in enumerate(clean_parts):
                Dict[dict_key].append(float(values.split(" ")[1]))
            Dict[dict_key].sort()
        return Dict

    def sort_dict(self):
        Final_dict = {}
        for key, value in self.Dict.items():
            m = np.mean(value)
            key_final = key.split(" ")[1]
            if "thermometer" in key:
                s = np.std(value)
                if (m < (self.thermometer_control+0.5) and m > (self.thermometer_control-0.5)):
                    if s < 3:
                        Final_dict[key_final] = 'ultra precise'
                    elif s < 5:
                        Final_dict[key_final] = 'very precise'
                    else:
                        Final_dict[key_final] = 'precise'
            if "humidity" in key:
                a = (m / self.humidistat_control) * 100
                if a > 99 and a < 101:
                    Final_dict[key_final] = 'keep'
                else:
                    Final_dict[key_final] = 'discard'
        json_data = Final_dict
        json_object = json.dumps(json_data, indent=2)
        return json_object