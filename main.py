"""
IDEA:

1. Create a staticstic class which is going to calculate all statictical measures
2. Somehow use a decorator to make inormation function to get all collumns
3. Docorator is going to have wrapper function to get any numbers of coloums and a argument
4. Understand why and how object orientation could help in case of this module.
5. Understand steps clearly
6. We will be needing a sorting algorithm.
"""
import os
import pandas as pd
import sys
from describe import Statistics


def load_validate(filename: str) -> pd.DataFrame:
    """
    This function is to validate the file, and data
    converting a raw data into a df
    @param filename || path
    @returns DataFrame
    """
    if not filename.endswith(".csv"):
        raise ValueError("Incorrect file extention.")
    if not os.path.exists(filename):
        raise FileExistsError("Given filename does not exists.")
    if not os.path.isfile(filename):
        raise FileNotFoundError("Given argument is not a file.")
    if not os.access(filename, os.R_OK):
        raise PermissionError("File is not readable.")
    
    return pd.read_csv(filename)


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Incorrect arguemnt count.")
        
        dataset = load_validate(sys.argv[1])
        stat = Statistics(dataset)
        information = stat.ft_describe()

        print(f"{information}")

    except Exception as e:
        print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()