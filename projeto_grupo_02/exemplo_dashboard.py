import streamlit as st
import duckdb
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Dashboard TMI Brasil", layout="wide")

st.title("📊 Monitoramento da Mortalidade Infantil (TMI)")
st.markdown("Dashboard analítico processando arquivo único consolidado (2022-2024)")

# --- 1. CONEXÃO E LEITURA DOS DADOS ---
@st.cache_data
def load_data():
    """
    Lê o arquivo 'Largo' e transforma em 'Longo' (linhas por ano)
    para permitir filtros dinâmicos.
    """
    # Query ajustada para as colunas exatas que você passou
    query = """
    SELECT Codigo_IBGE, Nascidos_2022 AS Nascidos, Obitos_Infantis_2022 AS Obitos_Infantis, 2022 AS Ano 
    FROM 'dados_resumidos/tmi_municipios_agg_2022_2024.parquet'
    
    UNION ALL
    
    SELECT Codigo_IBGE, Nascidos_2023 AS Nascidos, Obitos_Infantis_2023 AS Obitos_Infantis, 2023 AS Ano 
    FROM 'dados_resumidos/tmi_municipios_agg_2022_2024.parquet'
    
    UNION ALL
    
    SELECT Codigo_IBGE, Nascidos_2024 AS Nascidos, Obitos_Infantis_2024 AS Obitos_Infantis, 2024 AS Ano 
    FROM 'dados_resumidos/tmi_municipios_agg_2022_2024.parquet'
    
    UNION ALL
    
    SELECT Codigo_IBGE, Nascidos_22_24 AS Nascidos, Obitos_Infantis_22_24 AS Obitos_Infantis, '22-24 (Total)' AS Ano
    FROM 'dados_resumidos/tmi_municipios_agg_2022_2024.parquet'
    """
    return duckdb.query(query).to_df()

try:
    df = load_data()
except Exception as e:
    st.error(f"Erro ao carregar os dados. Verifique se o caminho do arquivo parquet está correto. Detalhe: {e}")
    st.stop()

# --- 2. SIDEBAR E FILTROS ---
st.sidebar.header("Filtros")

# Filtro de Ano
# Forçamos a conversão para string para evitar erros de ordenação entre int (2022) e string (Total)
df['Ano_Str'] = df['Ano'].astype(str)
anos_disponiveis = sorted(df['Ano_Str'].unique())
ano_selecionado = st.sidebar.selectbox("Selecione o Período", anos_disponiveis, index=0)

municipio_input = st.sidebar.text_input("Buscar por Código IBGE (Opcional)")

# Aplica filtros
df_filtered = df[df['Ano_Str'] == ano_selecionado].copy()

if municipio_input:
    df_filtered = df_filtered[df_filtered['Codigo_IBGE'].astype(str).str.contains(municipio_input)]

# --- 3. CÁLCULO DE MÉTRICAS ---
total_nascidos = df_filtered['Nascidos'].sum()
total_obitos = df_filtered['Obitos_Infantis'].sum()

# Evita divisão por zero no agregado
tmi_calculada = (total_obitos / total_nascidos * 1000) if total_nascidos > 0 else 0

# Calcula TMI por linha (município) para os gráficos
# fillna(0) garante que não quebre se tiver Nascidos=0
df_filtered['TMI'] = (df_filtered['Obitos_Infantis'] / df_filtered['Nascidos'] * 1000).fillna(0)

# --- 4. EXIBIÇÃO ---

col1, col2, col3 = st.columns(3)
col1.metric("Nascidos Vivos", f"{total_nascidos:,.0f}".replace(",", "."))
col2.metric("Óbitos Infantis", f"{total_obitos:,.0f}".replace(",", "."))
col3.metric("Taxa (TMI) do Período", f"{tmi_calculada:.2f}")

st.divider()

col_chart, col_data = st.columns([2, 1])

with col_chart:
    st.subheader(f"Distribuição da TMI - {ano_selecionado}")
    # Gráfico simples
    st.bar_chart(df_filtered.set_index('Codigo_IBGE')['TMI'].head(50))
    st.caption("A mostrar os primeiros 50 registros.")

with col_data:
    st.subheader("Top 10 Maiores Taxas")
    
    # Lógica do Top 10
    top_10 = df_filtered.nlargest(10, 'TMI')[['Codigo_IBGE', 'Nascidos', 'Obitos_Infantis', 'TMI']]
    
    # Formatação (Styler) para ficar bonito
    # IMPORTANTE: Removi o parâmetro 'width' que estava causando o erro.
    # Usamos 'use_container_width=True' que é o padrão seguro.
    st.dataframe(
        top_10.style.format({'TMI': '{:.2f}', 'Nascidos': '{:.0f}', 'Obitos_Infantis': '{:.0f}'}),
        hide_index=True,
        use_container_width=True
    )

with st.expander("Ver dados brutos (Amostra 100 linhas)"):
    st.dataframe(df_filtered.head(100), use_container_width=True)