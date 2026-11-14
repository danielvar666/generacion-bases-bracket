for bracket, grupo in df_msisdn_bracket.dropna(subset=["bracket"]).groupby("bracket", sort=True):
    archivo = carpeta_resultados / f"bracket_{bracket:g}.csv"
    grupo.to_csv(archivo, index=False, encoding="utf-8-sig")
    print(f"Guardado: {archivo}")
