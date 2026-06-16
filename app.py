import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Configuración inicial
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title="App Analizadora de Datasets", layout="wide")

st.sidebar.title("Menú de navegación")
seccion = st.sidebar.radio("Ir a:", ["Home", "Carga y perfil", "Procesamiento", "Análisis visual"])

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Módulo 1: Home
# -------------------------------
if seccion == "Home":
    st.title("App analizadora de datasets con Streamlit")
    st.write("Autor: Henry A. Vilca Yahuita")
    st.write("Objetivo: Construir una aplicación flexible para explorar distintos datasets.")
    st.write("Tecnologías: Python, Pandas, Streamlit, Plotly, Matplotlib, Seaborn, GitHub")
    st.info("Nota: Los resultados son exploratorios y no reemplazan validación técnica o profesional.")

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Módulo 2: Carga y perfil
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif seccion == "Carga y perfil":
    st.header("Carga y perfil del dataset")
    dataset_option = st.selectbox("Selecciona dataset de ejemplo o sube uno propio:",
                                  ["Subir archivo CSV", "Teen Mental Health", "Superstore", "E-commerce Risk", "AI Impact on Jobs"])

    if dataset_option == "Subir archivo CSV":
        uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state["df"] = df
    else:
        if dataset_option == "Teen Mental Health":
            df = pd.read_csv("Teen_Mental_Health_Dataset.csv")
        elif dataset_option == "Superstore":
            df = pd.read_csv("sample_-_superstore.csv")
        elif dataset_option == "E-commerce Risk":
            df = pd.read_csv("synthetic_ecommerce_order_risk_dataset.csv")
        elif dataset_option == "AI Impact on Jobs":
            df = pd.read_csv("AI_Impact_on_Jobs_2030.csv")
        st.session_state["df"] = df

    if "df" in st.session_state:
        df = st.session_state["df"]
        st.subheader("Vista previa")
        st.dataframe(df.head())
        st.write(f"Dimensiones: {df.shape[0]} filas, {df.shape[1]} columnas")
        st.write("Columnas:", list(df.columns))
        st.write("Tipos de datos:", df.dtypes)
        st.metric("Variables numéricas", len(df.select_dtypes(include=np.number).columns))
        st.metric("Variables categóricas", len(df.select_dtypes(exclude=np.number).columns))
        st.metric("Valores nulos", df.isnull().sum().sum())
        st.metric("Duplicados", df.duplicated().sum())

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Módulo 3: Procesamiento
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif seccion == "Procesamiento":
    st.header("Procesamiento de datos")
    if "df" in st.session_state:
        df = st.session_state["df"]
        st.write("Valores nulos por columna:")
        st.bar_chart(df.isnull().sum())
        st.write("Duplicados:", df.duplicated().sum())
        num_cols = df.select_dtypes(include=np.number).columns
        for col in num_cols:
            q1, q3 = df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            outliers = ((df[col] < (q1 - 1.5*iqr)) | (df[col] > (q3 + 1.5*iqr))).sum()
            st.write(f"{col}: {outliers} outliers detectados")
    else:
        st.warning("Primero carga un dataset en la sección anterior.")

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Módulo 4: Análisis visual
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif seccion == "Análisis visual":
    st.header("Análisis visual")
    if "df" in st.session_state:
        df = st.session_state["df"]
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            ["Resumen", "Univariado", "Bivariado", "Multivariado", "Temporal", "Insights"]
        )

        # --- Resumen ---
        with tab1:
            st.write(df.describe())

        # --- Univariado ---
        with tab2:
            for col in df.select_dtypes(include=np.number).columns[:3]:
                fig = px.histogram(df, x=col, nbins=10, title=f"Distribución de {col}")
                st.plotly_chart(fig)

        # --- Bivariado ---
        with tab3:
            if "Teen Mental Health" in df.columns or "anxiety_level" in df.columns:
                fig = px.scatter(df, x="daily_social_media_hours", y="sleep_hours", color="platform_usage",
                                 title="Horas de redes sociales vs horas de sueño")
                st.plotly_chart(fig)
                fig = px.scatter(df, x="physical_activity", y="stress_level", color="gender",
                                 title="Actividad física vs nivel de estrés")
                st.plotly_chart(fig)

            if "Discount" in df.columns and "Profit" in df.columns:
                fig = px.scatter(df, x="Discount", y="Profit", color="Category",
                                 title="Descuento vs Utilidad por categoría")
                st.plotly_chart(fig)

            if "order_value_eur" in df.columns and "risk_label" in df.columns:
                fig = px.box(df, x="payment_method", y="order_value_eur", color="risk_label",
                             title="Valor de orden vs método de pago según riesgo")
                st.plotly_chart(fig)

            if "AI_Replacement_Risk" in df.columns and "Future_Demand_Score" in df.columns:
                fig = px.scatter(df, x="AI_Replacement_Risk", y="Future_Demand_Score", color="Industry",
                                 title="Riesgo de reemplazo IA vs demanda futura")
                st.plotly_chart(fig)

        # --- Multivariado ---
        with tab4:
            corr = df.select_dtypes(include=np.number).corr()

            fig, ax = plt.subplots(figsize=(12, 10))

            sns.heatmap(
                corr,
                cmap="coolwarm",        
                annot=True,             
                fmt=".2f",             
                linewidths=0.5,         
                cbar_kws={"shrink": 0.8, "label": "Coeficiente de correlación"},
                square=True,          
                ax=ax
            )

            ax.set_title("Mapa de calor de correlaciones", fontsize=16, pad=20)
            st.pyplot(fig)

        # --- Temporal ---
        with tab5:
            # Conversion automatica de columnas que parezcan fechas
            for col in df.columns:
                if "date" in col.lower() or "fecha" in col.lower():
                    df[col] = pd.to_datetime(df[col], errors="coerce")

            date_cols = df.select_dtypes(include="datetime64[ns]").columns

            if len(date_cols) > 0:
                fecha_col = st.selectbox("Selecciona columna de fecha", date_cols)
                num_col = st.selectbox("Selecciona variable numérica", df.select_dtypes(include=np.number).columns)
                fig = px.line(df.sort_values(fecha_col), x=fecha_col, y=num_col,
                      title=f"Evolución temporal de {num_col}")
                st.plotly_chart(fig)
            else:
                st.info("Este dataset no contiene columnas de fecha reconocidas.")

        # --- Insights ---
        with tab6:
            st.write("Hallazgos clave:")
            if "Teen Mental Health" in df.columns or "anxiety_level" in df.columns:
                st.write("- Mayor uso de redes sociales tiende a asociarse con menos horas de sueño.")
                st.write("- La actividad física parece estar relacionada con menores niveles de estrés.")
                st.write("- Ansiedad, estrés y adicción muestran correlaciones fuertes entre sí.")
            if "Superstore" in df.columns or "Profit" in df.columns:
                st.write("- Las categorías de productos muestran diferencias claras en ventas y utilidad.")
                st.write("- Los descuentos altos tienden a reducir la utilidad.")
                st.write("- Las regiones presentan variaciones significativas en rentabilidad.")
            if "risk_label" in df.columns:
                st.write("- Los métodos de pago y tipo de dispositivo influyen en el riesgo de fraude.")
                st.write("- Las devoluciones y entregas tardías se asocian con mayor riesgo operativo.")
            if "AI_Replacement_Risk" in df.columns:
                st.write("- Industrias con alto riesgo de reemplazo por IA muestran menor satisfacción laboral.")
                st.write("- La necesidad de actualización profesional es mayor en sectores con alta automatización.")
    else:
        st.warning("Primero carga un dataset en la sección anterior.")
