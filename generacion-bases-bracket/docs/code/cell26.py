# Limpia los números para comparar igual
# Limpia los números para comparar igual
msisdn_df3 = (
    df3["MSISDN"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True)
    .dropna()
)

msisdn_df4 = (
    df4["msisdn"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True)
    .dropna()
)

# Valores que sí coinciden entre df3 y df4
cruzan = set(msisdn_df3) & set(msisdn_df4)

print(f"Cantidad que sí cruzan entre df3 y df4: {len(cruzan):,}")

# Registros completos que cruzan
df3_cruce = df3[
    df3["MSISDN"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True)
    .isin(cruzan)
].copy()

df4_cruce = df4[
    df4["msisdn"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True)
    .isin(cruzan)
].copy()

# Opcional: guardar los MSISDN cruzados
msisdn_cruzados = list(cruzan)

msisdn_df4 = (
    df4["msisdn"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True)
    .dropna()
)
