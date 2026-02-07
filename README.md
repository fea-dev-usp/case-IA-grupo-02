# Mapeando a Saúde Pública no Brasil com Inteligência Artificial

> **"O Brasil não é dividido apenas por fronteiras estaduais, mas por perfis de eficiência e vulnerabilidade invisíveis a olho nu."**

## Sobre o Projeto
Este projeto aplica técnicas de **Data Science, Machine Learning (K-Means)** e **Deep Learning (Autoencoders)** para mapear a qualidade da saúde pública nos 5.570 municípios brasileiros.

Ao cruzar dados de mortalidade, economia (PIB), saneamento e gestão hospitalar, o sistema ignora as divisões geográficas tradicionais para encontrar "Brasis" semelhantes baseados em dados, além de identificar anomalias estatísticas.

---

## Principais Descobertas (Insights)

### 1. O Fenômeno da "Riqueza Desequilibrada"
O algoritmo de Clustering identificou um grupo de cidades com **PIB per capita altíssimo**, mas que falham em converter essa riqueza em bem-estar social, apresentando índices de violência elevados e gestão de saúde mediana. Isso prova que **PIB não é sinônimo de saúde**.

### 2. A "Crise de Gestão" (ICSAP Alto)
Identificamos um cluster onde a mortalidade não é causada apenas por pobreza, mas pela ineficiência da Atenção Básica. O alto índice de **Internações por Condições Sensíveis à Atenção Primária (ICSAP)** mostra que os hospitais estão lotados de pacientes que poderiam ter sido tratados no posto de saúde.

### 3. Anomalias com Deep Learning
Utilizando uma Rede Neural (Autoencoder) para aprender o "padrão Brasil", detectamos cidades anômalas.
* **Caso de Estudo:** *Lagoa Santa (GO)* foi apontada pela IA como uma anomalia estatística (Erro de Reconstrução no Top 1%). A cidade combina porte populacional minúsculo com infraestrutura de saneamento muito boa e economia atípica (turismo), um perfil que a IA considerou "matematicamente improvável" comparado ao resto do país.

---

## Metodologia e Pipeline

O projeto foi dividido em dois notebooks:

### `note0_dataset.ipynb`
* **Extração:** Coleta automatizada de dados do **DATASUS** (SIH, SIM, SINASC) e **IBGE** via API (`pysus`, `sidrapy`).
* **Tratamento:** Limpeza de nulos, normalização de nomes de municípios e cálculo de indicadores (ex: Taxa de Mortalidade por 1.000 nascidos).
* **Output:** Gera o dataset limpo `DATASET_MESTRE_FINAL.csv`.

### `note1_IA.ipynb` (Modelagem)
* **Fase 1: Clustering (Não-Supervisionado)**
    * Algoritmo: **K-Means**.
    * Otimização: Método do Cotovelo (Elbow Method).
    * Visualização: Redução de dimensionalidade com **PCA** (2D).
* **Fase 2: Análise Espacial**
    * Mapeamento dos clusters usando a biblioteca `geobr`.
* **Fase 3: Detecção de Anomalias (Deep Learning)**
    * Arquitetura: **Autoencoder** (Rede Neural Simétrica).
    * Lógica: o modelo aprende a comprimir e reconstruir os dados. Cidades com alto "Erro de Reconstrução" (MSE) são flagradas como anomalias.

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3.11+
* **Manipulação de Dados:** Pandas, NumPy
* **Machine Learning:** Scikit-learn (KMeans, PCA, Scalers)
* **Deep Learning:** TensorFlow / Keras (Autoencoders)
* **Geoprocessamento:** Geobr, Geopandas
* **Visualização:** Matplotlib, Seaborn

---

## Como Executar o Projeto

### 1. Pré-requisitos

* **Python 3.10 ou 3.11**.
* **VS Code** (com extensão Jupyter) ou **Jupyter Lab**.

### 2. Configuração do Ambiente (Virtual Environment)

É **altamente recomendado** usar um ambiente virtual para isolar as versões das bibliotecas e evitar conflitos.

**No Windows (PowerShell/CMD):**

* Cria o ambiente virtual chamado .venv
python -m venv .venv

* Ativa o ambiente
.venv\Scripts\activate

**No Linux ou Mac:**

* Cria o ambiente
python3 -m venv .venv

* Ativa o ambiente
source .venv/bin/activate

### 3. Instalação das Dependências

Com o ambiente ativado (você verá `(.venv)` no terminal), instale as bibliotecas listadas:

pip install -r requirements.txt

### 4. Executando o Pipeline

O projeto segue um fluxo lógico. Não inverta a ordem.

1. Abra o notebook `note0_dataset.ipynb`.
2. Certifique-se de que o Kernel do Jupyter está apontando para o seu ambiente `.venv`.
3. Execute todas as células (`Run All`).
4. **Verificação:** Ao final, confira se o arquivo `DATASET_MESTRE_FINAL.csv` foi criado com sucesso.
5. Abra o notebook `note1_IA.ipynb`.
6. Este notebook lerá o CSV gerado no passo anterior.
7. Execute as células sequencialmente para:
* Gerar os Clusters (K-Means).
* Visualizar os Mapas.
* Treinar a Rede Neural (Autoencoder).
* Gerar o relatório de Anomalias.

---

### ⚠️ Problemas Comuns ⚠️

* **Erro de "Module not found":** Certifique-se de que você instalou o `requirements.txt` **dentro** do ambiente virtual ativado e que o seu Jupyter Notebook está usando o kernel desse mesmo ambiente.
* Se você está tentando instalar a biblioteca pysus no **Windows** usando o Python 3.13 (que é muito novo). A pysus depende de uma biblioteca chamada pyreaddbc (para ler arquivos do governo), que é escrita em C. Como o **Windows** não tem um "Compilador de C" instalado e não existem versões prontas para o Python 3.13 ainda, a instalação "explode". Solução: Usar **Google Colab** para gerar o DATASET_FINAL_LIMPO.csv.
