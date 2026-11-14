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
