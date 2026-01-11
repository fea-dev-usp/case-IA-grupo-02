import os
from pysus import SIM
ESTADOS = ['AC', 'RO']
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


