import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------
# Configuración inicial
# -------------------------------
st.set_page_config(page_title="App Analizadora de Datasets", layout="wide")

# Sidebar principal
st.sidebar.title("Menú de navegación")
seccion = st.sidebar.radio("Ir a:", ["Home", "Carga y perfil", "Procesamiento", "Análisis visual"])

# -------------------------------
# Módulo 1: Home
# -------------------------------
if seccion == "Home":
    st.title("App analizadora de datasets con Streamlit")
    st.write("Autor: Henry - 2026")
    st.write("Objetivo: Construir una aplicación flexible para explorar distintos datasets.")
    st.write("Tecnologías: Python, Pandas, Streamlit, Plotly, Matplotlib, Seaborn, GitHub")

    st.info("Nota: Los resultados son exploratorios y no reemplazan validación técnica o profesional.")
"""
# -------------------------------
# Módulo 2: Carga y perfil
# -------------------------------
elif seccion == "Carga y perfil":
    st.header("Carga y perfil del dataset")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df

        st.subheader("Vista previa")
        st.dataframe(df.head())

        st.write(f"Dimensiones: {df.shape[0]} filas, {df.shape[1]} columnas")
        st.write("Columnas:", list(df.columns))
        st.write("Tipos de datos:", df.dtypes)

        st.metric("Variables numéricas", len(df.select_dtypes(include=np.number).columns))
        st.metric("Variables categóricas", len(df.select_dtypes(exclude=np.number).columns))
        st.metric("Valores nulos", df.isnull().sum().sum())
        st.metric("Duplicados", df.duplicated().sum())

# -------------------------------
# Módulo 3: Procesamiento
# -------------------------------
elif seccion == "Procesamiento":
    st.header("Procesamiento de datos")

    if "df" in st.session_state:
        df = st.session_state["df"]

        # Limpieza básica
        st.write("Valores nulos por columna:")
        st.bar_chart(df.isnull().sum())

        st.write("Duplicados:", df.duplicated().sum())

        # Outliers con IQR
        num_cols = df.select_dtypes(include=np.number).columns
        for col in num_cols:
            q1, q3 = df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            outliers = ((df[col] < (q1 - 1.5*iqr)) | (df[col] > (q3 + 1.5*iqr))).sum()
            st.write(f"{col}: {outliers} outliers detectados")
    else:
        st.warning("Primero carga un dataset en la sección anterior.")

# -------------------------------
# Módulo 4: Análisis visual
# -------------------------------
elif seccion == "Análisis visual":
    st.header("Análisis visual")

    if "df" in st.session_state:
        df = st.session_state["df"]

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            ["Resumen", "Univariado", "Bivariado", "Multivariado", "Temporal", "Insights"]
        )

        with tab1:
            st.write(df.describe())

        with tab2:
            col = st.selectbox("Selecciona variable numérica", df.select_dtypes(include=np.number).columns)
            fig = px.histogram(df, x=col)
            st.plotly_chart(fig)

        with tab3:
            x = st.selectbox("Variable X", df.columns)
            y = st.selectbox("Variable Y", df.columns)
            fig = px.scatter(df, x=x, y=y)
            st.plotly_chart(fig)

        with tab4:
            corr = df.select_dtypes(include=np.number).corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, ax=ax, cmap="coolwarm", annot=False)
            st.pyplot(fig)

        with tab5:
            if any(df.dtypes == "datetime64[ns]"):
                fecha_col = st.selectbox("Selecciona columna de fecha", df.select_dtypes("datetime64[ns]").columns)
                num_col = st.selectbox("Selecciona variable numérica", df.select_dtypes(include=np.number).columns)
                fig = px.line(df, x=fecha_col, y=num_col)
                st.plotly_chart(fig)
            else:
                st.info("Este dataset no contiene columnas de fecha.")

        with tab6:
            st.write("Aquí puedes redactar hallazgos clave y conclusiones.")
    else:
        st.warning("Primero carga un dataset en la sección anterior.")
"""
