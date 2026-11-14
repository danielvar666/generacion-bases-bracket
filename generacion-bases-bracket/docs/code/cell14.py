msisdn_df4 = (
    df4["msisdn"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True).dropna()
)
msisdn_df3 = (
    df3["MSISDN"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True).dropna()
)

valores_df4 = set(msisdn_df4)
valores_df3 = set(msisdn_df3)

solo_df4 = valores_df4 - valores_df3
solo_df3 = valores_df3 - valores_df4

print(f"MSISDN de df4 que no están en df3: {len(solo_df4):,}")
print(f"MSISDN de df3 que no están en df4: {len(solo_df3):,}")
print(f"Total de MSISDN distintos que no coinciden: {len(solo_df4 | solo_df3):,}")
