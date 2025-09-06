from dataclasses import dataclass, field
import pandas as pd

@dataclass
class Statistics:
    df: pd.DataFrame
    numeric_columns: dict = field(init=False, default_factory=dict)
    series: pd.Series = field(init=False, default=None)

    def __post_init__(self):
        """Post init stores converted values into a Series"""
        self.series = self._dfto_series()

    def _dfto_series(self):
        """
        Checks if column values has type of dtype
        Stores int numberic columns with type of dict
        """
        for col_name, column in self.df.items():
            # Check if column is numeric
            if pd.api.types.is_numeric_dtype(column):
                self.numeric_columns[col_name] = column
        return self.numeric_columns
    
    def ft_describe(self):
        """
        Calls and stores each features of central tendency,
        it does it inside of the results dict
        and returns formated values.
        """
        results = {}

        for col_name, col in self.numeric_columns.items():
            values = [val for val in col if pd.notna(val)]

            if not values:
                continue

            results[col_name] = {
                "Count": len(values),
                "Mean": self.mean(values),
                "Std": self.std(values),
                "Min": self.min_max(values, find="min"),
                "25%": self.percentile(values, 25),
                "50%": self.percentile(values, 50),
                "75%": self.percentile(values, 75),
                "Max": self.min_max(values, find="max")
            }

        return self._format_results(results)
    
    def mean(self, values):
        """Finds an average"""
        return sum(values) / len(values)
    
    def std(self, values):
        """Finds standard deviation"""
        n = len(values)
        if n < 2:
            raise ValueError("Sample size lower then 2")
        var = sum((x - self.mean(values)) ** 2 for x in values) / (n - 1)
        return var ** 0.5
    
    def min_max(self, values, find):
        """Finds min or max depending on find"""
        sorted_values = self.sorting_algorithm(values)
        if (find == 'min'):
            result = sorted_values[0]
        else:
            result = sorted_values[-1]
        return result

    @staticmethod
    def sorting_algorithm(values: list) -> list:
        for i in range(len(values) - 1):
            swapped = False
            for j in range(len(values) - i - 1):
                if values[j + 1] < values[j]:
                    swapped = True
                    values[j + 1], values[j] = values[j], values[j + 1]
            if not swapped:
                break
        return values

    def percentile(self, values, p):
        sorted_values = self.sorting_algorithm(values)
        n = len(sorted_values)
        if n == 0:
            return 0
            
        idx = (p / 100) * (n - 1)
        
        if idx.is_integer():
            return sorted_values[int(idx)]
            
        lower_idx = int(idx)
        upper_idx = lower_idx + 1
        lower_val = sorted_values[lower_idx]
        upper_val = sorted_values[upper_idx]
        
        fraction = idx - lower_idx
        return lower_val + fraction * (upper_val - lower_val)

    def _format_results(self, results: dict) -> dict:
        """Format results as a table"""
        if not results:
            return "No numerical features found."
            
        length_stat = 5 # length between statistical features and row names
        length_cal = 15
        col_names = [col for col in results.keys() if 'Index' not in col]
        
        output = " ".ljust(length_stat)
        for col in col_names:
            display_name = col[:7] + "..." if len(col) > 9 else col
            output += f"{display_name}".rjust(length_cal)
        output += "\n"
        
        stats = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
        for stat in stats:
            output += stat.ljust(length_stat)
            for col in col_names:
                value = results[col][stat]
                output += f"{value:.6f}".rjust(length_cal)
            output += "\n"
            
        return output

