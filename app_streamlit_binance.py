import streamlit as st
import pandas as pd
from scanner_tecnico_binance import scanner_tecnico

st.set_page_config(page_title="Scanner Técnico Binance", layout="centered")
st.title("🔍 Scanner Técnico de Criptomoedas na Binance")

password = st.text_input("🔐 Introduz a palavra-passe para aceder:", type="password")
if password != "minhaSenha123":
    st.warning("Acesso negado.")
    st.stop()

st.markdown("Este scanner identifica moedas com RSI < 30 e EMA20 acima da EMA50.")

if st.button("🔄 Executar Scanner Técnico"):
    with st.spinner("A analisar moedas na Binance..."):
        resultado = scanner_tecnico()
        if not resultado.empty:
            st.success(f"Foram encontradas {len(resultado)} moedas com as condições técnicas.")
            st.dataframe(resultado)
            st.download_button("📥 Download CSV", resultado.to_csv(index=False), "resultados.csv", "text/csv")
        else:
            st.warning("Nenhuma moeda cumpre as condições neste momento.")
