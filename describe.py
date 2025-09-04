from dataclasses import dataclass, field
import pandas as pd

@dataclass
class Statistics:
    df: pd.DataFrame

    numeric_columns: dict = field(init=False, default_factory=dict) # this is not a numberic, do not be confused
    # Maybe here is going to be additional things like:
    #           - options to see the featrues for: numberical, object...
    #           - ?...

    series: pd.Series = field(init=False, default=None)

    def __post_init__(self):
        self.series = self._dfto_series(self.df)

    def _dfto_series(self, df: pd.DataFrame):
        for col_name, column in self.df.items():
            # Check if column is numeric
            if pd.api.types.is_numeric_dtype(column):
                self.numeric_columns[col_name] = column
        return self.numeric_columns
    
    def ft_describe(self):
        results = {}

        for col_name, col in self.numeric_columns.items():
            values = [val for val in col if pd.notna(val)]

            if not values:
                continue

            results[col_name] = {
                "Count": len(values),
                "Mean": self.mean(values),
                "Std": self.std(values),
                "Min": self.min(values) # continue
            }

        return self._formated_results(results)
    
    def mean(self, values):
        return sum(values) / len(values)
    
    def std(self, values):
        n = len(values)
        if n < 2:
            raise ValueError("Sample size lower then 2")
        var = sum((x - self.mean(values)) ** 2 for x in values) / (n - 1)
        return var ** 0.5
    
    def _formated_result(self, results):
        pass

