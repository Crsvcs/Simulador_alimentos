# Simulador_alimentos
Este proyecto es un simulador interactivo desarrollado en Python con Streamlit, que intenta recrear un modelo simple (FPP) donde se debe escoger entre recolectar arboles o manzanas de manera que se pueda optimizar tiempo y felicidad (costo oportunidad). Inspirado en "Primer"..
Uso

Abre la app en tu navegador o ejecuta localmente:

streamlit run simulador_final.py

Ajusta los sliders:

Días a simular: número de días a evaluar.
Utilidad base por manzana/madera: peso de cada acción en la felicidad.
Esfuerzo para talar un árbol: acciones necesarias por árbol.
Acciones máximas por día: total de acciones posibles.
Manzanas a recolectar: cuántas recolectas cada día; la app calcula automáticamente los árboles posibles.

Qué muestra
Acciones no utilizadas: te indica si estás dejando acciones libres y sugiere cómo aprovecharlas.
Gráfico 3D de felicidad: combina manzanas y árboles para mostrar la utilidad de cada decisión.
Acumulación diaria: líneas de manzanas y madera acumuladas a lo largo de los días.
Tabla de óptimos: combina decisiones que maximizan felicidad, madera o manzanas.
Sugerencia interactiva: mensaje que indica si estás cerca del óptimo y cómo ajustar las acciones.

Requisitos
Python ≥ 3.8
Librerías: streamlit, numpy, pandas, plotly

Instalación rápida:
pip install streamlit numpy pandas plotly

Nota
La “felicidad” combina manzanas y árboles con una función logarítmica, mostrando decisiones óptimas de forma intuitiva.
La app es interactiva: al cambiar sliders se actualizan gráficos, tabla y mensajes automáticamente.
