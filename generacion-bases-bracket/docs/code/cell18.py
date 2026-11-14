from pathlib import Path

carpeta_resultados = Path("resultados bases")
carpeta_resultados.mkdir(parents=True, exist_ok=True)

msisdn_limpio = (
    df3["MSISDN"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True)
)

base_no_bracket = df3[msisdn_limpio.isin(solo_df3)].copy()
archivo = carpeta_resultados / "base no bracket.csv"

base_no_bracket.to_csv(archivo, index=False, encoding="utf-8-sig")

print(f"Registros exportados: {len(base_no_bracket):,}")
print(f"Archivo guardado en: {archivo.resolve()}")
