def profile_data(df):
    return {
        "rows": len(df),
        "missing_values": int(df.isnull().sum().sum()),
        "dtypes": df.dtypes.astype(str).to_dict()
    }
