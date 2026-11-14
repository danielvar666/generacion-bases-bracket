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
