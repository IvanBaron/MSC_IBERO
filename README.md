# ¿Quién pudo quedarse en casa?

Análisis de las redes diarias de movilidad de la Zona Metropolitana del Valle de México
(ZMVM) durante la pandemia de COVID-19, del 1 de enero de 2020 al 31 de marzo de 2021.

El notebook [`quien_pudo_quedarse_en_casa.ipynb`](quien_pudo_quedarse_en_casa.ipynb)
responde dos preguntas:

1. **¿Se puede pronosticar cuántos viajes tendrá mañana cada conexión entre AGEBs?**
   Un modelo XGBoost casi empata con el promedio de los últimos 7 días (CPC de 0.857
   contra 0.843, diferencia no significativa). Con estos datos, el pronóstico está topado.
2. **¿Qué zonas pudieron quedarse en casa?** Con el cambio en el porcentaje de los viajes
   de cada AGEB entre febrero de 2020 y octubre de 2020, y usando solo cómo era cada AGEB
   antes de la pandemia, el modelo alcanza un R² espacial de 0.21 ± 0.14 (0.08 con
   variables básicas y −0.02 en un control sin pandemia). Lo que más pesa es el ratio de
   viajes de fin de semana contra entre semana: las zonas de oficinas se apagaron más.

## Datos

Los datos no están en este repositorio porque pesan unos 6.5 GB. Vienen del proyecto de
OSF [gwq6u](https://osf.io/gwq6u/), con licencia
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Descárgalos y colócalos así, en esta carpeta o en cualquier carpeta superior:

```
data_garrido/
└── gwq6u-osfstorage-archive/
    ├── Networks/            # un archivo od_cvegeo_09_01_AAAA_MM_DD.csv por día
    └── agebs_ZMVM.csv       # catálogo de AGEBs con coordenadas
```

`datos.py` busca esa carpeta automáticamente.

## Cómo correrlo

```bash
pip install -r requirements.txt
```

En Mac, XGBoost necesita OpenMP:

```bash
brew install libomp
```

Después abre el notebook y ejecuta todas las celdas. La primera vez construye
`matriz_nucleo.parquet` con `construir_matriz_modelo.py` (tarda unos minutos); las
siguientes lo reutiliza.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `quien_pudo_quedarse_en_casa.ipynb` | El análisis completo, con texto, gráficas y resultados |
| `datos.py` | Localiza la carpeta de datos y lee la red de un día |
| `construir_matriz_modelo.py` | Construye la matriz de conexiones estables que usa la primera parte |
| `descargar_mapa_base.py` | Descarga el mapa base de OpenStreetMap (ya incluido como PNG) |
| `mapa_base_zmvm.png`, `mapa_base_zmvm.json` | Mapa base para el mapa final. © OpenStreetMap contributors (ODbL) |
