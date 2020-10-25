class MapGenerator(object):
    def __init__(self, data):
        self.data = data
        self.terrain_dictionary = {0: (0, 0, 89),
                                   0.2: (144, 152, 204),
                                   0.3: (253, 223, 119),
                                   0.6: (124, 252, 0),
                                   0.8: (222, 165, 33),
                                   0.9: (151, 124, 83),
                                   0.95: (134, 126, 112),
                                   1: (240, 240, 236)}

    def generate_map(self):
        for i in range(0, len(self.data)):
            point = self.data[i]
            keys = list(self.terrain_dictionary.keys())
            for boundary in range(0, len(keys)-1):
                if keys[boundary] <= point <= keys[boundary+1]:
                    distance = (point - keys[boundary]) / (keys[boundary+1] - keys[boundary])
                    if distance > 0.5:
                        point = self.terrain_dictionary[keys[boundary+1]]
                    else:
                        point = self.terrain_dictionary[keys[boundary]]
                    break
            self.data[i] = point
        return self.data
