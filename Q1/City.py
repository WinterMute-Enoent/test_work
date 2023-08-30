import json
import random

class CitySelector:
    def __init__(self, file_path):
        self.city_data = self._load_data(file_path)

    def _load_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def select_city(self):
        total_population = sum(city['population'] for city in self.city_data)
        random_value = random.random()

        cumulative_prob = 0
# Перебор данных о городах и выбор города на основе накопленных вероятностей.
        for city in self.city_data:
            city_prob = city['population'] / total_population
            cumulative_prob += city_prob
            if random_value <= cumulative_prob:
                return city['name']

if __name__ == "__main__":
    input_file_path = "input.json"
    city_selector = CitySelector(input_file_path)

    selected_city = city_selector.select_city()
    print(f"Selected city: {selected_city}")
