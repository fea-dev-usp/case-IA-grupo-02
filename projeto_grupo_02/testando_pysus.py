import pandas as pd
from pysus import SIH

# 1. Carrega a API do SIH
sih = SIH().load()

# 2. Define os arquivos que você quer (Ex: SP, 2020, Jan/Fev/Mar)
files = sih.get_files("RD", uf="SP", year=2020, month=[1, 2, 3])
print(f"Arquivos encontrados: {len(files)}")

# 3. Baixa os arquivos (O download retorna uma lista de objetos Parquet)
# Nota: Isso pode demorar um pouco dependendo da internet
parquets = sih.download(files) 

# 4. Pega o PRIMEIRO arquivo baixado e converte para DataFrame Pandas
# (parquets[0] é o mês 1, parquets[1] é o mês 2, etc.)
df = parquets[0].to_dataframe()

# --- COMO VISUALIZAR NO PYTHON ---

# Opção A: Ver as 5 primeiras linhas (O padrão do dia a dia)
print(df.head())

# Opção B: Ver as colunas (Para confirmar se tem DIAG_PRINC e MUNIC_RES)
print("\nColunas disponíveis:")
print(df.columns)

# Opção C: Informações técnicas (Tipos de dados e memória)
# df.info()