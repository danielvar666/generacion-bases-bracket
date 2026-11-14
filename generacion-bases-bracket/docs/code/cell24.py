msisdn_df1_limpio = (
    df1["MSISDN"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True)
)

base_pre_a_home = df1[msisdn_df1_limpio.isin(solo_df1_vs_df4)].copy()
archivo_pre_a_home = carpeta_resultados / "base pre a home.csv"

base_pre_a_home.to_csv(archivo_pre_a_home, index=False, encoding="utf-8-sig")

print(f"Registros exportados: {len(base_pre_a_home):,}")
print(f"Archivo guardado en: {archivo_pre_a_home.resolve()}")
