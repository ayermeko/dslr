import sys
import os
import pandas as pd
import numpy as np

def load_validate(filename: str) -> pd.DataFrame:
    if not filename.endswith(".csv"):
        raise ValueError("Incorrect file extention.")
    if not os.path.exists(filename):
        raise FileExistsError("Given filename does not exists.")
    if not os.path.isfile(filename):
        raise FileNotFoundError("Given argument is not a file.")
    if not os.access(filename, os.R_OK):
        raise PermissionError("File is not readable.")
    
    return pd.read_csv(filename)


def information(dataset: np.ndarray) -> None:
    features = {
        "Count" : "function to count for each datapoint",
        "Mean" : "function to find mean fed",
        "Std" : "function to find std fed",
        "Min" : "function to find min fed",
        "Quartile": "funciton to find 25% & 50% & 75% /fed",
        "Max" : "function to find max fed"
    }

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("Incorrect arguemnt count.")
        
        dataset = load_validate(sys.argv[1])

        information(dataset)
        

    except Exception as e:
        print(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()