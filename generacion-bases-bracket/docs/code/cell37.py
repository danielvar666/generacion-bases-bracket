columnas_plan = [
    "ID_PLAN_RECOMMENDED_1",
    "ID_PLAN_RECOMMENDED_2",
]

# Extraer el precio inicial de cada plan y convertirlo a número
precios = df_final[columnas_plan].apply(
    lambda columna: pd.to_numeric(
        columna.astype("string").str.extract(r"(\d+(?:\.\d+)?)", expand=False),
        errors="coerce",
    )
)

# min(axis=1) ignora los valores faltantes; si ambos faltan, el resultado queda vacío
df_msisdn_bracket = pd.DataFrame({
    "MSISDN": df_final["MSISDN"].to_numpy(),
    "bracket": precios.min(axis=1).to_numpy(),
})

# Añadir a cada fila el total de registros de su bracket
conteos = df_msisdn_bracket["bracket"].value_counts()
df_msisdn_bracket["cantidad_registros_bracket"] = (
    df_msisdn_bracket["bracket"].map(conteos)
)

# Resumen: una fila por bracket
df_conteo_brackets = (
    df_msisdn_bracket.dropna(subset=["bracket"])
    .groupby("bracket")
    .size()
    .rename("cantidad_registros")
    .reset_index()
    .sort_values("bracket")
)

display(df_msisdn_bracket)
display(df_conteo_brackets)
