import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# --- Configuración de la página ---
st.set_page_config(layout="wide")
st.title("🍎 Simulador de Decisiones de Búsqueda de Alimentos 🌳")

# --- Sliders ---
col1, col2 = st.columns(2)
with col1:
    st.header("Parámetros de la Simulación")
    dias_simulacion = st.slider("Días a simular", 1, 365, 30)
    utilidad_base_manzana = st.slider("Utilidad Base por Manzana", 10, 200, 100)
    utilidad_base_madera = st.slider("Utilidad Base por Madera", 10, 200, 150)
    esfuerzo_talar_arbol = st.slider("Esfuerzo para Talar un Árbol", 2, 10, 4)

with col2:
    st.header("Decisiones Diarias")
    acciones_maximas_diarias = st.slider("Acciones Máximas por Día", 10, 100, 50)
    manzanas_elegidas = st.slider("Manzanas a recolectar por día", 0, acciones_maximas_diarias, 10)
    
    # Calcular cuántos árboles puedes talar con las acciones restantes
    arboles_posibles = (acciones_maximas_diarias - manzanas_elegidas) // esfuerzo_talar_arbol
    st.info(f"Con esta elección, puedes talar **{arboles_posibles}** árboles por día.")

# --- Indicador de acciones no utilizadas ---
acciones_usadas = manzanas_elegidas + (arboles_posibles * esfuerzo_talar_arbol)
acciones_restantes = acciones_maximas_diarias - acciones_usadas

if acciones_restantes > 0:
    st.warning(f"⚠️ Estás dejando **{acciones_restantes} acciones diarias sin usar**. Podrías recolectar más manzanas o talar más árboles para optimizar tu tiempo.")
else:
    st.success("✅ Estás usando todas tus acciones diarias de manera eficiente.")

# --- Gráfico 3D de utilidad ---
m_range = np.arange(0, acciones_maximas_diarias + 1, max(1, acciones_maximas_diarias // 50))
a_range = np.arange(0, (acciones_maximas_diarias // esfuerzo_talar_arbol) + 1, max(1, acciones_maximas_diarias // (esfuerzo_talar_arbol * 50)))
M, A = np.meshgrid(m_range, a_range)
Utilidad = (utilidad_base_manzana * np.log1p(M)) + (utilidad_base_madera * np.log1p(A))
restriccion = M + (A * esfuerzo_talar_arbol)
Utilidad[restriccion > acciones_maximas_diarias] = np.nan

fig = go.Figure(data=[go.Surface(z=Utilidad, x=m_range, y=a_range, colorscale='Viridis')])
fig.update_layout(scene=dict(xaxis_title='Manzanas', yaxis_title='Árboles', zaxis_title='Felicidad'),
                  width=800, height=800)
st.plotly_chart(fig)

# --- Acumulación diaria ---
manzanas_diarias = np.full(dias_simulacion, manzanas_elegidas)
arboles_diarios = np.full(dias_simulacion, arboles_posibles)
madera_diaria = arboles_diarios * utilidad_base_madera
cumsum_manzanas = np.cumsum(manzanas_diarias)
cumsum_madera = np.cumsum(madera_diaria)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(y=cumsum_manzanas, x=np.arange(1, dias_simulacion+1),
                          mode='lines+markers', name='Manzanas acumuladas'))
fig2.add_trace(go.Scatter(y=cumsum_madera, x=np.arange(1, dias_simulacion+1),
                          mode='lines+markers', name='Madera acumulada'))
fig2.update_layout(xaxis_title='Día', yaxis_title='Cantidad acumulada')
st.plotly_chart(fig2)

# --- Tabla de óptimos ---
st.header("Óptimos de Decisión por Criterio")
df_optimos = pd.DataFrame(columns=['Criterio', 'Manzanas', 'Árboles', 'Felicidad'])

# Felicidad máxima
idx_f = np.nanargmax(Utilidad)
m_opt_f, a_opt_f = M.flatten()[idx_f], A.flatten()[idx_f]
f_max = Utilidad.flatten()[idx_f]
df_optimos.loc[len(df_optimos)] = ['Máx Felicidad', m_opt_f, a_opt_f, f_max]

# Árboles máximos (máxima madera)
idx_a = np.nanargmax(A)
m_opt_a, a_opt_a = M.flatten()[idx_a], A.flatten()[idx_a]
f_a = (utilidad_base_manzana*np.log1p(m_opt_a)) + (utilidad_base_madera*np.log1p(a_opt_a))
df_optimos.loc[len(df_optimos)] = ['Máx Madera', m_opt_a, a_opt_a, f_a]

# Manzanas máximas
idx_m = np.nanargmax(M)
m_opt_m, a_opt_m = M.flatten()[idx_m], A.flatten()[idx_m]
f_m = (utilidad_base_manzana*np.log1p(m_opt_m)) + (utilidad_base_madera*np.log1p(a_opt_m))
df_optimos.loc[len(df_optimos)] = ['Máx Manzanas', m_opt_m, a_opt_m, f_m]

st.table(df_optimos)

# --- Mensaje interactivo de optimización ---
st.header("Sugerencia de Optimización")
felicidad_actual = (utilidad_base_manzana*np.log1p(manzanas_elegidas)) + (utilidad_base_madera*np.log1p(arboles_posibles))

mensaje = ""
if felicidad_actual >= f_max * 0.95:
    mensaje = "🌟 Estás cerca de **maximizar la felicidad**!"
elif arboles_posibles >= a_opt_a * 0.95:
    mensaje = "🌲 Estás cerca de **maximizar la madera**!"
elif manzanas_elegidas >= m_opt_m * 0.95:
    mensaje = "🍎 Estás cerca de **maximizar las manzanas**!"
else:
    mensaje = "⚖️ Tu combinación es equilibrada, ajusta los sliders para optimizar un criterio."

st.success(mensaje)

# --- Recomendación para usar todas las acciones ---
st.header("Combinación Recomendada para Usar Todas las Acciones")
manzanas_sugeridas = manzanas_elegidas
arboles_sugeridos = (acciones_maximas_diarias - manzanas_sugeridas) // esfuerzo_talar_arbol
st.info(f"Para usar todas tus acciones diarias, puedes recolectar **{manzanas_sugeridas} manzanas** y talar **{arboles_sugeridos} árboles**.")
