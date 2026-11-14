# Generación de bases Bracket, No Bracket y Pre a Home

Cruce de audiencias de la campaña de migración de Tigo (Pre a Pos y Pre a Home) mediante operaciones de conjuntos sobre la llave MSISDN, con pandas.

## Qué genera
- `base no bracket.csv`: PRE A POS ADICIONAL que no están en Ecommerce Televentas (A \ E)
- `base pre a home.csv`: PRE A HOME que no están en Ecommerce Televentas (H \ E)
- `bracket_<valor>.csv`: un archivo por categoría de bracket (menor valor entre los dos planes recomendados)

## Estructura
- `src/generacion_bases.py`: script consolidado
- `notebook.ipynb`: notebook original
- `docs/`: documento técnico en LaTeX y PDF (compilar con `xelatex -shell-escape main.tex`)
- `img/`: diagramas de Venn y distribución de brackets

## Uso
```bash
pip install -r requirements.txt
python src/generacion_bases.py
```
Los datos de origen (CSV) no se incluyen por ser información de clientes. Las rutas de lectura en el script son locales (Windows); ajústalas a tu equipo.
