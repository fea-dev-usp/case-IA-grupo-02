# case-IA-grupo-02
Repositório do grupo 2 para o case de IA da capacitação 2025/2.


## Obtendo taxa de mortalidade infantil (TMI)

###  Dicionário de Dados Selecionados (SIM)

| Variável (Coluna) | Descrição | Valores / Regras |
| :--- | :--- | :--- |
| **`CODMUNRES`** | **Município de Residência** | Código IBGE (Chave primária para agrupar). |
| **`CAUSABAS`** | **Causa Básica do Óbito** | Código CID-10 da doença ou violência que causou a morte. |
| **`TIPOBITO`** | **Tipo do Óbito** | `1`: Fetal (Natimorto)<br>`2`: Não Fetal (Usar este para mortalidade geral). |
| **`DTOBITO`** | **Data do Óbito** | Formato: `DDMMAAAA`. |
| **`IDADE`** | **Idade Codificada** | **Dígito 1 (Unidade):**<br>`0`=Minutos, `1`=Horas, `2`=Dias, `3`=Meses,<br>`4`=Anos, `5`=Anos (+100).<br>**Dígitos 2-3:** Quantidade. |
| **`SEXO`** | **Sexo** | `1`: Masculino<br>`2`: Feminino<br>`9`: Ignorado. |
| **`RACACOR`** | **Raça / Cor** | `1`: Branca<br>`2`: Preta<br>`3`: Amarela<br>`4`: Parda<br>`5`: Indígena. |
| **`ESC2010`** | **Escolaridade (Nível)** | `0`: Sem escolaridade<br>`1`: Fund. I (1ª-4ª)<br>`2`: Fund. II (5ª-8ª)<br>`3`: Médio<br>`4`: Sup. Incompleto<br>`5`: Sup. Completo. |
| **`CIRCOBITO`** | **Circunstância (Violência)** | `1`: Acidente<br>`2`: Suicídio<br>`3`: Homicídio<br>`4`: Outros<br>`9`: Ignorado. |