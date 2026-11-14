msisdn_df1 = (
    df1["MSISDN"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True).dropna()
)

valores_df1 = set(msisdn_df1)
valores_df4 = set(msisdn_df4)

solo_df1_vs_df4 = valores_df1 - valores_df4
solo_df4_vs_df1 = valores_df4 - valores_df1

print(f"MSISDN de df1 que no están en df4: {len(solo_df1_vs_df4):,}")
print(f"MSISDN de df4 que no están en df1: {len(solo_df4_vs_df1):,}")
print(f"Total de MSISDN distintos que no coinciden: {len(solo_df1_vs_df4 | solo_df4_vs_df1):,}")
