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
