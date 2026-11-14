import pandas as pd
df1=pd.read_csv(r"C:\Users\danie\Downloads\BASES MIGRA TIGO LUEGO DE PRE A HOME\MIGRA\PRE A HOME.csv")
df2=pd.read_csv(r"C:\Users\danie\Downloads\BASES MIGRA TIGO LUEGO DE PRE A HOME\MIGRA\PRE A POS.csv")
df3=pd.read_csv(r"C:\Users\danie\Downloads\BASES MIGRA TIGO LUEGO DE PRE A HOME\MIGRA\PRE A POS ADICIONAL.csv")


print(len(df1))
print(len(df2))
print(len(df3))


df4=pd.read_csv(r"C:\Users\danie\Downloads\Migra Tigo\Ecomerce televentas.csv")
print(len(df4))


%pip install matplotlib


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def _area_interseccion(r1, r2, d):
    """Área de la lente que forman dos círculos de radios r1 y r2 con centros a distancia d."""
    if d >= r1 + r2:
        return 0.0
    if d <= abs(r1 - r2):
        return np.pi * min(r1, r2) ** 2
    a1 = r1**2 * np.arccos((d**2 + r1**2 - r2**2) / (2 * d * r1))
    a2 = r2**2 * np.arccos((d**2 + r2**2 - r1**2) / (2 * d * r2))
    tri = 0.5 * np.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
    return a1 + a2 - tri


def _distancia_centros(r1, r2, area_objetivo, tol=1e-9):
    """Distancia entre centros para que la lente tenga el área objetivo (bisección)."""
    lo, hi = abs(r1 - r2), r1 + r2
    for _ in range(200):
        mid = (lo + hi) / 2
        if _area_interseccion(r1, r2, mid) > area_objetivo:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2


def diagrama_venn(n_solo_a, n_inter, n_solo_b, nombre_a, nombre_b, sim_a, sim_b,
                  titulo, etq_solo_a, etq_inter, etq_solo_b,
                  color_a="#1F4E79", color_b="#C55A11"):
    """Diagrama de Venn de dos conjuntos con áreas proporcionales al número de MSISDN distintos."""
    from matplotlib.patches import Patch

    n_a, n_b = n_solo_a + n_inter, n_solo_b + n_inter
    union = n_a + n_b - n_inter
    jaccard = n_inter / union
    r1, r2 = np.sqrt(n_a / np.pi), np.sqrt(n_b / np.pi)
    d = _distancia_centros(r1, r2, n_inter)
    if n_inter == 0:
        d *= 1.06  # separación visual cuando los conjuntos son disjuntos
    rmax = max(r1, r2)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.add_patch(Circle((0, 0), r1, fc=color_a, ec=color_a, alpha=0.55, lw=2))
    ax.add_patch(Circle((d, 0), r2, fc=color_b, ec=color_b, alpha=0.55, lw=2))

    def texto(n, etq):
        return f"{etq}\n{n:,}\n({n / union:.1%})"

    kw = dict(ha="center", va="center", fontsize=10.5, weight="bold", color="#1a1a1a")
    x_min, x_max = -r1 * 1.08, d + r2 * 1.08

    if n_inter > 0:
        borde_izq, borde_der = d - r2, r1          # extremos de la lente A ∩ B
        ancho_solo_a, ancho_solo_b = borde_izq + r1, d + r2 - borde_der
        ax.text((borde_izq + borde_der) / 2, 0, texto(n_inter, etq_inter), **kw)
        flecha = dict(arrowstyle="-", color="#555555", lw=1)
        if ancho_solo_a < 0.7 * r1:                # región estrecha: etiqueta fuera del círculo
            ax.annotate(texto(n_solo_a, etq_solo_a), xy=((-r1 + borde_izq) / 2, 0),
                        xytext=(-r1 * 1.45, -rmax * 0.25), arrowprops=flecha, **kw)
            x_min = -r1 * 1.8
        else:
            ax.text((-r1 + borde_izq) / 2, 0, texto(n_solo_a, etq_solo_a), **kw)
        if ancho_solo_b < 0.7 * r2:
            ax.annotate(texto(n_solo_b, etq_solo_b), xy=((borde_der + d + r2) / 2, 0),
                        xytext=(d + r2 * 1.45, -rmax * 0.25), arrowprops=flecha, **kw)
            x_max = d + r2 * 1.8
        else:
            ax.text((borde_der + d + r2) / 2, 0, texto(n_solo_b, etq_solo_b), **kw)
    else:
        ax.text(0, 0, texto(n_solo_a, etq_solo_a), **kw)
        ax.text(d, 0, texto(n_solo_b, etq_solo_b), **kw)
        ax.text((r1 + d - r2) / 2, -rmax * 1.18, f"{sim_a} ∩ {sim_b} = ∅   (0 registros en común)",
                ha="center", va="center", fontsize=11, style="italic", color="#444444")

    ax.legend(handles=[Patch(fc=color_a, ec=color_a, alpha=0.6, label=f"{sim_a}: {nombre_a}  (n = {n_a:,})"),
                       Patch(fc=color_b, ec=color_b, alpha=0.6, label=f"{sim_b}: {nombre_b}  (n = {n_b:,})")],
              loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=1, frameon=False, fontsize=10.5)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-rmax * 1.3, rmax * 1.45)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(titulo, fontsize=13, weight="bold", pad=14)
    fig.text(0.5, 0.02,
             f"Áreas proporcionales al número de MSISDN distintos  ·  Índice de Jaccard J({sim_a}, {sim_b}) = {jaccard:.3f}",
             ha="center", fontsize=9.5, color="#555555")
    plt.show()


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


# Figura 1. Diagrama de Venn: PRE A POS ADICIONAL (A) vs Ecommerce Televentas (E)
n_solo_a = len(solo_df3)                       # A \ E  -> No Bracket
n_solo_e = len(solo_df4)                       # E \ A
n_inter  = len(valores_df3) - len(solo_df3)    # A ∩ E  -> Bracket

diagrama_venn(
    n_solo_a, n_inter, n_solo_e,
    "PRE A POS ADICIONAL", "Ecommerce Televentas", "A", "E",
    "Figura 1. Cruce de PRE A POS ADICIONAL (A) con Ecommerce Televentas (E)",
    "A \\ E\nNo Bracket", "A ∩ E\nBracket", "E \\ A",
)


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


# Figura 2. Diagrama de Venn: PRE A HOME (H) vs Ecommerce Televentas (E)
n_solo_h  = len(solo_df1_vs_df4)                          # H \ E  -> Base Pre a Home
n_solo_e2 = len(solo_df4_vs_df1)                          # E \ H
n_inter_h = len(valores_df1) - len(solo_df1_vs_df4)       # H ∩ E

diagrama_venn(
    n_solo_h, n_inter_h, n_solo_e2,
    "PRE A HOME", "Ecommerce Televentas", "H", "E",
    "Figura 2. Cruce de PRE A HOME (H) con Ecommerce Televentas (E)",
    "H \\ E\nBase Pre a Home", "H ∩ E", "E \\ H",
)


msisdn_df1_limpio = (
    df1["MSISDN"].astype("string").str.strip()
    .str.replace(r"\.0$", "", regex=True)
)

base_pre_a_home = df1[msisdn_df1_limpio.isin(solo_df1_vs_df4)].copy()
archivo_pre_a_home = carpeta_resultados / "base pre a home.csv"

base_pre_a_home.to_csv(archivo_pre_a_home, index=False, encoding="utf-8-sig")

print(f"Registros exportados: {len(base_pre_a_home):,}")
print(f"Archivo guardado en: {archivo_pre_a_home.resolve()}")


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


df_merge = df3_cruce.merge(
    df4_cruce,
    left_on="MSISDN",
    right_on="msisdn",
    how="inner",
    suffixes=("_prepos", "_ecommerce")
)

print(f"Registros unidos: {len(df_merge):,}")


df5=pd.read_csv(r"C:\Users\danie\Downloads\Migra Tigo\PRE A POS.csv")


df_nuevo = pd.concat([df2, df5], ignore_index=True)


df_final = pd.concat([df_nuevo, df_merge], ignore_index=True)


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


for bracket, grupo in df_msisdn_bracket.dropna(subset=["bracket"]).groupby("bracket", sort=True):
    archivo = carpeta_resultados / f"bracket_{bracket:g}.csv"
    grupo.to_csv(archivo, index=False, encoding="utf-8-sig")
    print(f"Guardado: {archivo}")


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


import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

fig, ax = plt.subplots(figsize=(10, 5.6))

etiquetas = [f"{b:g}" for b in df_conteo_brackets["bracket"]]
valores = df_conteo_brackets["cantidad_registros"]
barras = ax.barh(etiquetas, valores, color="#1F4E79", alpha=0.85)
ax.invert_yaxis()

margen = valores.max() * 0.012
for barra, n, p in zip(barras, valores, df_conteo_brackets["pct_con_bracket"]):
    ax.text(barra.get_width() + margen, barra.get_y() + barra.get_height() / 2,
            f"{n:,}  ({p:.1f} %)", va="center", fontsize=10, color="#1a1a1a")

ax.set_xlim(0, valores.max() * 1.25)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.set_xlabel("Número de registros", fontsize=10.5)
ax.set_ylabel("Bracket (valor del plan)", fontsize=10.5)
ax.grid(axis="x", alpha=0.25)
ax.set_axisbelow(True)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)

ax.set_title("Figura 3. Registros por bracket (menor valor entre los planes recomendados)",
             fontsize=13, weight="bold", pad=14)
fig.text(0.5, 0.01,
         f"Total con bracket: {total_con_bracket:,} filas  ·  Sin bracket (no exportadas): "
         f"{total_sin_bracket:,} ({total_sin_bracket / TOTAL_FILAS_DF_FINAL:.1%} de df_final)",
         ha="center", fontsize=9.5, color="#555555")
plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.show()
