import pandas as pd

class Climate:

    def __init__(self, config):

        data = pd.read_csv(
            config["climate"]["climate_file"],
            parse_dates=["date"],
            index_col="date",
        )
        self.temperature = data["temperature"]
        self.check_coverage(config["general"]["start_date"], config["general"]["end_date"])

    def print(self):
        print("Test Climate Is Represented by Temperature Only")
        print("Temperature is ")
        print(self.temperature)

    def check_coverage(self, start, end):
        needed = pd.date_range(start, end, freq="D")
        missing = needed.difference(self.temperature.index)
        if len(missing):
            raise ValueError(
                f"Climate file is missing {len(missing)} dates, "
                f"first missing: {missing[0].date()}"
            )