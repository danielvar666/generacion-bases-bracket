import pandas as pd

# Resultados registrados de las secciones 7.3 a 7.5 (df_final ya no está en memoria).
TOTAL_FILAS_DF_FINAL = 3_708_801

df_conteo_brackets = pd.DataFrame({
    "bracket": [19.9, 24.9, 29.9, 34.9, 39.9, 43.9, 47.9, 53.9, 69.9],
    "cantidad_registros": [1_539_689, 205_058, 106_111, 205_911, 66_843,
                           107_129, 136_882, 124_798, 112_074],
})

total_con_bracket = int(df_conteo_brackets["cantidad_registros"].sum())
total_sin_bracket = TOTAL_FILAS_DF_FINAL - total_con_bracket

# Control de consistencia frente a lo observado en las secciones 7.3 y 7.5
assert total_con_bracket == 2_604_495
assert total_sin_bracket == 1_104_306

df_conteo_brackets["pct_con_bracket"] = df_conteo_brackets["cantidad_registros"] / total_con_bracket * 100
df_conteo_brackets["pct_acumulado"] = df_conteo_brackets["pct_con_bracket"].cumsum()
df_conteo_brackets["pct_df_final"] = df_conteo_brackets["cantidad_registros"] / TOTAL_FILAS_DF_FINAL * 100

tabla_brackets = pd.DataFrame({
    "Bracket": df_conteo_brackets["bracket"].map(lambda b: f"{b:g}"),
    "Registros": df_conteo_brackets["cantidad_registros"].map("{:,}".format),
    "% de filas con bracket": df_conteo_brackets["pct_con_bracket"].map("{:.1f} %".format),
    "% acumulado": df_conteo_brackets["pct_acumulado"].map("{:.1f} %".format),
    "% de df_final": df_conteo_brackets["pct_df_final"].map("{:.1f} %".format),
    "Archivo exportado": df_conteo_brackets["bracket"].map(lambda b: f"bracket_{b:g}.csv"),
    "Verificación": "Correcta",
})

display(tabla_brackets)

print(f"Total con bracket asignado : {total_con_bracket:>10,}  ({total_con_bracket / TOTAL_FILAS_DF_FINAL:.1%} de df_final)")
print(f"Total sin bracket          : {total_sin_bracket:>10,}  ({total_sin_bracket / TOTAL_FILAS_DF_FINAL:.1%} de df_final)")
print(f"Total de filas df_final    : {TOTAL_FILAS_DF_FINAL:>10,}")
