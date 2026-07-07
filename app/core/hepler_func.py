def dataframe_to_response(df):
    return {
        "recommendations": df.to_dict(orient="records")
    }