import re
from typing import List

import numpy as np
import pandas as pd


def to_snake_case(column_name: str) -> str:
    """
    Convert a string to snake_case.
    """
    column_name = column_name.strip() 
    column_name = re.sub(r"[^\w\s]", "", column_name)
    column_name = re.sub(r"\s+", "_", column_name)
    return column_name.lower()


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename DataFrame columns to snake_case.
    """
    df.columns = [to_snake_case(col) for col in df.columns]
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates().reset_index(drop=True)


def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trim leading and trailing whitespace from string columns.
    """
    object_cols = df.select_dtypes(include=["object"]).columns
    for col in object_cols:
        df[col] = df[col].astype(str).str.strip()
    return df


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert columns to appropriate data types.
    - Numeric conversion where possible
    - Datetime conversion for date-like columns
    """
    for col in df.columns:
        # Attempt numeric conversion
        df[col] = pd.to_numeric(df[col], errors="ignore")

        # Attempt datetime conversion for date-like columns
        if "date" in col or "time" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values:
    - Numeric columns -> fill with median
    - Categorical columns -> fill with mode
    - Datetime columns -> forward fill
    """
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].fillna(method="ffill")
        else:
            mode_value = df[col].mode()
            if not mode_value.empty:
                df[col] = df[col].fillna(mode_value[0])
            else:
                df[col] = df[col].fillna("unknown")
    return df


def handle_outliers(df: pd.DataFrame,
                    numeric_columns: List[str]) -> pd.DataFrame:
    """
    Detect and cap outliers using IQR method.
    """
    for col in numeric_columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        df[col] = np.where(
            df[col] < lower_bound,
            lower_bound,
            np.where(df[col] > upper_bound, upper_bound, df[col])
        )

    return df


def clean_dataset(file_path: str,
                  output_path: str) -> None:
    """
    Complete data cleaning pipeline.
    """
    # Load dataset
    df = pd.read_csv(file_path)

    # Standardize column names
    df = rename_columns(df)

    # Remove duplicates
    df = remove_duplicates(df)

    # Trim whitespace
    df = trim_whitespace(df)

    # Convert data types
    df = convert_data_types(df)

    # Handle missing values
    df = handle_missing_values(df)

    # Detect and handle outliers in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df = handle_outliers(df, numeric_cols)

    # Save cleaned dataset
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    INPUT_FILE = "raw_dataset.csv"
    OUTPUT_FILE = "cleaned_dataset.csv"

    clean_dataset(INPUT_FILE, OUTPUT_FILE)