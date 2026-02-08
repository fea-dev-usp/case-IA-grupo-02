import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# Configuração da página
st.set_page_config(page_title="Dashboard Municipal 360º", layout="wide", page_icon="fea_dev_logo.jpg")

# --- CUSTOM CSS (Fundo + Sidebar Preta) ---
def set_custom_style(bg_image_file):
    '''
    Define o background da página principal com uma imagem
    e pinta a sidebar de preto absoluto.
    '''
    # Tenta ler a imagem de fundo. Se não existir, define apenas a cor preta.
    try:
        with open(bg_image_file, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        bg_css = f"""background-image: url("data:image/png;base64,{bin_str}");
                     background-size: cover;"""
    except FileNotFoundError:
        # Se não achar o fundo.png, usa um fundo preto padrão
        bg_css = "background-color: #000000;"

    style = f"""
    <style>
    /* 1. Fundo da Aplicação Principal */
    .stApp {{
        {bg_css}
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* 2. Estilização da Sidebar (Fundo Preto) */
    [data-testid="stSidebar"] {{
        background-color: #000000 !important;
        border-right: 1px solid #333333; /* Divisória sutil */
    }}

    /* 3. Forçar cor do texto da Sidebar para Branco */
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}
    
    /* Ajuste para inputs ficarem visíveis no fundo preto */
    [data-testid="stSidebar"] .stTextInput > div > div {{
        background-color: #1E1E1E;
        color: white;
    }}
    [data-testid="stSidebar"] .stSelectbox > div > div {{
        background-color: #1E1E1E;
        color: white;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Aplica o estilo (tenta ler fundo.png, se não tiver, fica preto)
set_custom_style('fundo3.png')

# --- 1. CARREGAMENTO DOS DADOS ---
@st.cache_data
def load_data():
    df = pd.read_csv("DATASET_MESTRE_FINAL.csv")
    
    # Tratamento de UF
    if 'cod' in df.columns:
        df['cod'] = df['cod'].astype(str)
        codigos_uf = {
            '11': 'RO', '12': 'AC', '13': 'AM', '14': 'RR', '15': 'PA', '16': 'AP', '17': 'TO',
            '21': 'MA', '22': 'PI', '23': 'CE', '24': 'RN', '25': 'PB', '26': 'PE', '27': 'AL', '28': 'SE',
            '29': 'BA', '31': 'MG', '32': 'ES', '33': 'RJ', '35': 'SP', '41': 'PR', '42': 'SC', '43': 'RS',
            '50': 'MS', '51': 'MT', '52': 'GO', '53': 'DF'
        }
        df['UF_Cod'] = df['cod'].str[:2]
        df['UF'] = df['UF_Cod'].map(codigos_uf)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Arquivo 'DATASET_MESTRE_FINAL.csv' não encontrado.")
    st.stop()

# --- 2. SIDEBAR (FILTROS) ---
st.sidebar.header("🔍 Filtros")

# Como o fundo é preto, vamos garantir que o slider e multiselect funcionem
estados = sorted(df['UF'].dropna().unique())
ufs_selecionadas = st.sidebar.multiselect("Selecione Estados", estados, default=['SP', 'RJ', 'MG'])

pop_min, pop_max = int(df['populacao'].min()), int(df['populacao'].max())
pop_range = st.sidebar.slider("Faixa de População", pop_min, pop_max, (pop_min, pop_max))

df_filtered = df[
    (df['UF'].isin(ufs_selecionadas)) & 
    (df['populacao'].between(pop_range[0], pop_range[1]))
]

# --- 3. HEADER COM LOGO E BANNER ---
# Layout ajustado: Logo na esquerda, Título na direita
col_logo, col_title = st.columns([0.15, 0.85])

with col_logo:
    # Usando o arquivo JPG que você enviou
    try:
        st.image("fea_dev_logo.jpg", width=100)
    except:
        st.warning("Logo não encontrado")

with col_title:
    st.markdown("## Projeto Grupo 02 - Mapeando o Brasil")
    st.markdown("**FEA.dev** | Análise de Dados Públicos")


st.markdown("---")

st.title(f"🇧🇷 Panorama Municipal ({len(df_filtered)} filtrados)")

# --- 4. KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("População Coberta", f"{df_filtered['populacao'].sum():,.0f}")
col2.metric("Média Mortalidade Infantil", f"{df_filtered['taxa_mortalidade_infantil'].mean():.2f}")
col3.metric("Cobertura Pré-Natal Média", f"{df_filtered['pct_prenatal'].mean():.1f}%")
col4.metric("PIB per Capita Médio", f"R$ {df_filtered['pib_per_capita'].mean():,.2f}")

st.markdown("---")

# --- 5. VISUALIZAÇÕES ---
tab1, tab2, tab3 = st.tabs(["💰 Economia vs Saúde", "🏥 Eficiência Hospitalar", "📋 Dados Brutos"])

with tab1:
    st.subheader("O Dinheiro traz Saúde?")
    fig_corr = px.scatter(
        df_filtered, 
        x='pib_per_capita', 
        y='taxa_mortalidade_infantil',
        color='UF',
        size='populacao',
        hover_name='mun',
        hover_data=['obitos_infantil', 'prenatal_ok'],
        log_x=True, 
        title="PIB per Capita (Log) vs Taxa de Mortalidade Infantil"
    )
    # Ajuste para tema escuro no gráfico também, se quiser
    fig_corr.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_corr, use_container_width=True)

with tab2:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Internações Sensíveis (ICSAP)")
        top_icsap = df_filtered.nlargest(10, 'pct_icsap').sort_values('pct_icsap', ascending=True)
        fig_bar = px.bar(
            top_icsap, 
            x='pct_icsap', 
            y='mun', 
            orientation='h',
            color='UF',
            title="Top 10 Municípios com maior % de Internações Evitáveis"
        )
        fig_bar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_g2:
        st.subheader("Custo Médio da Internação")
        fig_hist = px.histogram(
            df_filtered, 
            x="custo_medio", 
            nbins=50, 
            title="Distribuição do Custo Médio Hospitalar",
            color_discrete_sequence=['green']
        )
        fig_hist.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_hist, use_container_width=True)

with tab3:
    st.dataframe(
        df_filtered[['cod', 'mun', 'UF', 'populacao', 'pib_per_capita', 'taxa_mortalidade_infantil', 'pct_prenatal']],
        use_container_width=True,
        hide_index=True
    )