import polars as pl
import glob
import os

# 1. Definir caminhos e variáveis
input_path = './data/raw/sim/sim/'
output_file = './data/processed/sim_2020_unificado.parquet'

# Garante que a pasta de saída existe
os.makedirs(os.path.dirname(output_file), exist_ok=True)

variaveis_sim = [
    "TIPOBITO", "DTOBITO", "IDADE", "SEXO", 
    "RACACOR", "ESC2010", "CODMUNRES", 
    "CIRCOBITO", "CAUSABAS"
]

# 2. Listar arquivos
arquivos = glob.glob(os.path.join(input_path, "*.parquet"))

print(f"Encontrados {len(arquivos)} arquivos. Iniciando processamento...")

# 3. Processamento Lazy com Streaming
# scan_parquet cria um plano de execução, não lê os dados ainda
q = (
    pl.scan_parquet(arquivos)
    .select(variaveis_sim) # Seleciona apenas as colunas desejadas
)

# 4. Gravar no disco (sink_parquet usa streaming para não estourar a RAM)
q.sink_parquet(output_file)

print(f"Processo finalizado! Arquivo salvo em: {output_file}")