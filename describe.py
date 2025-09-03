from dataclasses import dataclass, field
import pandas as pd

@dataclass
class Statistics:
    df: pd.DataFrame
    numeric_columns: dict = field(init=False, default_factory=dict)
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
                # Print moved inside the if statement so it only prints numeric columns
                # print(f"Numeric column: {self.numeric_columns[col_name]}")
        return self.numeric_columns
    
    def get_series(self):
        return self.series

