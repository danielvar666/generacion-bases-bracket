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
