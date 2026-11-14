conteos_esperados = (
    df_msisdn_bracket
    .dropna(subset=["bracket"])
    .groupby("bracket", sort=True)
    .size()
    .rename("esperado")
)

conteos_guardados = {}
for archivo in carpeta_resultados.glob("bracket_*.csv"):
    bracket = float(archivo.stem[len("bracket_"):])
    conteos_guardados[bracket] = len(pd.read_csv(archivo))

resumen = pd.DataFrame({"esperado": conteos_esperados}).join(
    pd.Series(conteos_guardados, name="en_archivo"),
    how="outer",
).fillna(0).astype(int)

resumen["correcto"] = resumen["esperado"] == resumen["en_archivo"]

print(resumen.sort_index().to_string())
print(f"\n¿Todas las cantidades coinciden? {resumen['correcto'].all()}")
