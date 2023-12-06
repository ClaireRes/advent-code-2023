import re
from typing import NamedTuple, List

INPUT = "input5.txt"
# INPUT = "testinput5.txt"


class MapRange(NamedTuple):
    dest_start: int
    source_start: int
    length: int


class SeedRange(NamedTuple):
    start: int
    length: int


class SeedMappings:
    SEED_TEXT = "seeds:"
    RANGE_PATTERN = r"(\d+)\s+(\d+)\s+(\d+)"
    
    def __init__(self):
        self.seed_soil: List[MapRange] = []
        self.soil_fertilizer: List[MapRange] = []
        self.fertilizer_water: List[MapRange] = []
        self.water_light: List[MapRange] = []
        self.light_temperature: List[MapRange] = []
        self.temperature_humidity: List[MapRange] = []
        self.humidity_location: List[MapRange] = []
        self.seeds = set()

        self._section_list_map = {
            "seed-to-soil": self.seed_soil,
            "soil-to-fertilizer": self.soil_fertilizer,
            "fertilizer-to-water": self.fertilizer_water,
            "water-to-light": self.water_light,
            "light-to-temperature": self.light_temperature,
            "temperature-to-humidity": self.temperature_humidity,
            "humidity-to-location": self.humidity_location
        }
    
    def add_seeds(self, line: str):
        _, seed_text = line.split(": ", maxsplit=1)
        seeds_as_str = [s for s in seed_text.split(" ") if s != " " and s]
        for i in range(len(seeds_as_str) // 2):
            start_seed = int(seeds_as_str[2*i])
            seed_range = int(seeds_as_str[2*i + 1])
            self.seeds.add(SeedRange(start_seed, seed_range))

    def add_mapping_row(self, section: str, line: str):
        range_match = re.match(self.RANGE_PATTERN, line)
        map_range = MapRange(int(range_match.group(1)), int(range_match.group(2)), int(range_match.group(3)))

        self._section_list_map.get(section).append(map_range)

    def get_seed_location(self, seed: int) -> int:
        soil = self.get_dest_value(seed, self.seed_soil)
        fertilizer = self.get_dest_value(soil, self.soil_fertilizer)
        water = self.get_dest_value(fertilizer, self.fertilizer_water)
        light = self.get_dest_value(water, self.water_light)
        temperature = self.get_dest_value(light, self.light_temperature)
        humid = self.get_dest_value(temperature, self.temperature_humidity)
        return self.get_dest_value(humid, self.humidity_location)

    def get_dest_value(self, source: int, map_ranges: List[MapRange]) -> int:
        for map_range in map_ranges:
            if map_range.source_start <= source < map_range.source_start + map_range.length:
                offset = source - map_range.source_start
                return map_range.dest_start + offset
        # if not mapped, dest matches source
        return source

    def find_min_location_for_seed_range(self, seed_range: SeedRange) -> int:
        # print(f"Looking for min location for range {seed_range}")
        source_ranges = [seed_range]
        soil_ranges = self.get_all_dest_ranges(source_ranges, self.seed_soil)
        fert_ranges = self.get_all_dest_ranges(soil_ranges, self.soil_fertilizer)
        water_ranges = self.get_all_dest_ranges(fert_ranges, self.fertilizer_water)
        light_ranges = self.get_all_dest_ranges(water_ranges, self.water_light)
        temp_ranges = self.get_all_dest_ranges(light_ranges, self.light_temperature)
        humid_ranges = self.get_all_dest_ranges(temp_ranges, self.temperature_humidity)
        loc_ranges = self.get_all_dest_ranges(humid_ranges, self.humidity_location)
        loc_ranges.sort(key=lambda source: source.start)
        return loc_ranges[0].start

    def get_all_dest_ranges(self, source_ranges: List[SeedRange], map_ranges: List[MapRange]) -> List[SeedRange]:
        dest_ranges = []
        for source_range in source_ranges:
            this_range_dests = self.get_mapped_ranges(source_range, map_ranges)
            if this_range_dests:
                dest_ranges.extend(this_range_dests)
        return dest_ranges

    def get_mapped_ranges(self, source_range: SeedRange, map_ranges: List[MapRange]) -> List[SeedRange]:
        # can we just pass through ranges which satisfy the initial source seed range?
        dest_ranges = []
        mapped_ranges = []
        x_1 = source_range.start
        x_2 = x_1 + source_range.length
        for map_range in map_ranges:
            y_1 = map_range.source_start
            y_2 = y_1 + map_range.length

            if x_1 >= y_1 and x_2 <= y_2:
                # full overlap of source
                offset = x_1 - y_1
                dest_ranges.append(SeedRange(map_range.dest_start + offset, source_range.length))
                mapped_ranges.append(SeedRange(map_range.source_start + offset, source_range.length))
            elif x_1 <= y_1 and x_2 >= y_2:
                # entire mapping range has source value
                dest_ranges.append(SeedRange(map_range.dest_start, map_range.length))
                mapped_ranges.append(SeedRange(map_range.source_start, map_range.length))
            # partial overlap cases
            elif x_1 < y_1 <= x_2 < y_2:
                dest_ranges.append(SeedRange(map_range.dest_start, x_2 - y_1))
                mapped_ranges.append(SeedRange(map_range.source_start, x_2 - y_1))
            elif x_2 > y_2 >= x_1 > y_1:
                offset = x_1 - y_1
                dest_ranges.append(SeedRange(map_range.dest_start + offset, y_2 - x_1))
                mapped_ranges.append(SeedRange(map_range.source_start + offset, y_2 - x_1))

        if not mapped_ranges:
            # no mappings found, use original range as is as dest
            return [source_range]

        # Find sub-ranges which are not mapped
        # assume ranges are non overlapping
        mapped_ranges.sort(key=lambda r: r.start)
        unmapped = []
        next_expected_start = source_range.start
        for sub_range in mapped_ranges:
            if sub_range.start > next_expected_start:
                unmapped.append(SeedRange(next_expected_start, sub_range.start - next_expected_start))
            next_expected_start = sub_range.start + sub_range.length

        if next_expected_start < (source_range.start + source_range.length):
            missing = source_range.start + source_range.length - next_expected_start
            unmapped.append(SeedRange(next_expected_start, missing))

        # if unmapped:
        #     dest_ranges.extend(unmapped)

        combined = [*dest_ranges, *unmapped]
        total = sum([s.length for s in combined])
        assert total == source_range.length

        return combined


def find_lowest_location(seed_mappings: SeedMappings):
    """
    Using these maps, find the lowest location number that corresponds to any of the initial seeds.
    What is the lowest location number that corresponds to any of the initial seed numbers?
    """
    min_location = -1
    min_seed_for_location = -1
    for seed in seed_mappings.seeds:
        location = seed_mappings.get_seed_location(seed)
        if min_location < 0 or location < min_location:
            min_location = location
            min_seed_for_location = seed

    print(f"Min location = {min_location} for seed {min_seed_for_location}")


def find_lowest_location_part2(seed_mappings: SeedMappings):
    min_location = -1
    for seed_range in seed_mappings.seeds:
        min_range_location = seed_mappings.find_min_location_for_seed_range(seed_range)
        if min_location < 0 or min_range_location < min_location:
            min_location = min_range_location
        print(f"Min location for range {seed_range} is {min_range_location}")

    print(f"\nOverall min location is {min_location}")


def main1():
    seed_mappings = SeedMappings()
    current_section = ""
    
    with open(INPUT, 'r') as f_in:
        for raw_line in f_in:
            line = raw_line.strip()
            if line.startswith(SeedMappings.SEED_TEXT):
                seed_mappings.add_seeds(line)
            elif line.endswith("map:"):
                current_section, _ = line.split(" map:", maxsplit=1)
            elif line == "":
                # end of section
                current_section = ""
            else:
                # should be mapping row of numbers
                seed_mappings.add_mapping_row(current_section, line)

    find_lowest_location_part2(seed_mappings)


if __name__ == "__main__":
    main1()
