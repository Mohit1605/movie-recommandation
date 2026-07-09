def dataframe_to_response(df):
    """Converts a recommendation DataFrame into a dictionary format.

    Args:
    df: A pandas DataFrame containing recommendation results.

    Returns:
    dict: A dictionary with the key "recommendations" mapping to the 
            DataFrame records.
    """
    return {
        "recommendations": df.to_dict(orient="records")
    }