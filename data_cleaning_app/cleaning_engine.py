import pandas as pd
import numpy as np


def clean_data(df, options):
    report = {}

    # ===============================
    # 1. STRUCTURAL CLEANING
    # ===============================
    before_rows = len(df)
    df = df.drop_duplicates()
    report["duplicates_removed"] = before_rows - len(df)

    exclude_cols = options.get("exclude_columns", [])
    report["excluded_columns"] = exclude_cols
    work_df = df.drop(columns=exclude_cols, errors="ignore").copy()

    # Drop fully empty columns
    before_cols = work_df.shape[1]
    work_df = work_df.dropna(axis=1, how="all")
    report["empty_columns_removed"] = before_cols - work_df.shape[1]

    # ===============================
    # 2. DATA TYPE CONVERSION
    # ===============================
    if options.get("auto_numeric"):
        for col in work_df.columns:
            work_df[col] = pd.to_numeric(work_df[col], errors="ignore")
    report["auto_numeric"] = options.get("auto_numeric", False)

    if options.get("auto_datetime"):
        for col in work_df.columns:
            try:
                converted = pd.to_datetime(work_df[col], errors="raise")
                work_df[col] = converted
            except:
                pass
    report["auto_datetime"] = options.get("auto_datetime", False)

    # ===============================
    # 3. TEXT STANDARDIZATION
    # ===============================
    if options.get("normalize_text"):
        for col in work_df.select_dtypes(include="object"):
            work_df[col] = (
                work_df[col]
                .astype(str)
                .str.strip()
                .str.lower()
            )
    report["normalize_text"] = options.get("normalize_text", False)

    # ===============================
    # 4. MISSING VALUE HANDLING
    # ===============================
    strategy = options.get("missing_strategy", "none")
    report["missing_strategy"] = strategy

    for col in work_df.columns:
        if work_df[col].isnull().any():

            if strategy == "none":
                continue

            elif strategy == "drop":
                work_df = work_df.dropna(subset=[col])

            elif pd.api.types.is_numeric_dtype(work_df[col]):
                if strategy == "mean":
                    work_df[col] = work_df[col].fillna(work_df[col].mean())
                elif strategy == "median":
                    work_df[col] = work_df[col].fillna(work_df[col].median())

            else:
                mode_val = work_df[col].mode()
                if not mode_val.empty:
                    work_df[col] = work_df[col].fillna(mode_val[0])

    # ===============================
    # 5. OUTLIER HANDLING
    # ===============================
    before_outliers = len(work_df)

    if options.get("handle_outliers"):
        for col in work_df.select_dtypes(include=["int64", "float64"]):
            Q1 = work_df[col].quantile(0.25)
            Q3 = work_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            work_df = work_df[
                (work_df[col] >= lower) &
                (work_df[col] <= upper)
            ]

    report["outlier_handling"] = options.get("handle_outliers", False)
    report["outliers_removed"] = before_outliers - len(work_df)

    # ===============================
    # 6. CATEGORICAL ENCODING
    # ===============================
    encoding = options.get("encoding", "none")
    report["encoding"] = encoding

    if encoding == "label":
        for col in work_df.select_dtypes(include="object"):
            work_df[col] = work_df[col].astype("category").cat.codes

    elif encoding == "onehot":
        work_df = pd.get_dummies(work_df, drop_first=True)

    # ===============================
    # 7. FEATURE SCALING
    # ===============================
    scaling = options.get("scaling", "none")
    report["scaling"] = scaling

    num_cols = work_df.select_dtypes(include=["int64", "float64"]).columns

    if scaling == "minmax":
        work_df[num_cols] = (
            work_df[num_cols] - work_df[num_cols].min()
        ) / (work_df[num_cols].max() - work_df[num_cols].min())

    elif scaling == "standard":
        work_df[num_cols] = (
            work_df[num_cols] - work_df[num_cols].mean()
        ) / work_df[num_cols].std()

    # ===============================
    # 8. LOGICAL VALIDATION
    # ===============================
    if options.get("logical_validation"):
        for col in work_df.select_dtypes(include=["int64", "float64"]):
            work_df = work_df[work_df[col] >= 0]

    report["logical_validation"] = options.get("logical_validation", False)

    return work_df, report
