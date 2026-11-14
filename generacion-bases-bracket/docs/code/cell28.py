df_merge = df3_cruce.merge(
    df4_cruce,
    left_on="MSISDN",
    right_on="msisdn",
    how="inner",
    suffixes=("_prepos", "_ecommerce")
)

print(f"Registros unidos: {len(df_merge):,}")
