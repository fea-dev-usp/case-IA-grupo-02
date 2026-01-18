import os
from pysus import SIM
#Vamos listar todos os estados e o distrito federal
# Ordem: Norte -> Nordeste -> Centro-Oeste -> Sudeste -> Sul
ESTADOS = [
    # Norte
    'AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO',
    # Nordeste
    'AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE',
    # Centro-Oeste
    'DF', 'GO', 'MT', 'MS',
    # Sudeste
    'ES', 'MG', 'RJ', 'SP',
    # Sul
    'PR', 'RS', 'SC'
]
ANOS = [2020]
caminho_base = './data/raw/sim/'

def baixar_sim():
    sim = SIM().load()
    for uf in ESTADOS:
        for ano in ANOS:
            print(f'Baixando dados do SIM - {uf} - {ano}')
            try: 
                files = sim.get_files("CID10", uf=uf, year=ano)
                sim.download(files, local_dir=f"{caminho_base}/sim")
            except Exception as e:
                print(f'Erro ao baixar dados do SIM para {uf} - {ano}: {e}')

if __name__ == "__main__":
    baixar_sim()
    print("Download concluído.")


