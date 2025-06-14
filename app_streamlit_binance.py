import streamlit as st
import pandas as pd
from scanner_tecnico_conservador import scanner_conservador, analisar_par_individual
from scanner_tecnico_binance import scanner_tecnico

st.set_page_config(page_title="Binance TA Scanner", layout="wide")

st.title("📈 Binance Technical Scanner")

modo = st.selectbox("Escolhe o modo de análise:", ["Scanner Técnico Normal", "Scanner Conservador com Confiança", "Análise Individual"])

intervalo = st.selectbox("Escolhe o timeframe:", ["1h", "4h", "1d"])

if modo == "Análise Individual":
    simbolo = st.text_input("Insere o par (ex: BTCUSDT):", value="BTCUSDT")
    if st.button("🔍 Analisar Par Individual"):
        resultado = analisar_par_individual(simbolo.upper(), intervalo)
        if not resultado.empty:
            st.success("Análise concluída com sucesso!")
            st.dataframe(resultado, use_container_width=True)
        else:
            st.warning("Não foi possível analisar o par ou nenhum sinal foi gerado.")
else:
    if st.button("🚀 Executar Scanner"):
        if modo == "Scanner Técnico Normal":
            resultado = scanner_tecnico(intervalo)
        else:
            resultado = scanner_conservador(intervalo)

        if not resultado.empty:
            st.success(f"{len(resultado)} oportunidades encontradas!")
            st.dataframe(resultado, use_container_width=True)
            csv = resultado.to_csv(index=False).encode('utf-8')
            st.download_button("💾 Download CSV", csv, "resultado_scanner.csv", "text/csv")
        else:
            st.warning("Nenhuma moeda cumpre os critérios neste momento.")