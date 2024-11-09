import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from itertools import combinations

# Função para transformar os dados em uma matriz binária
def transformar_dados_para_matriz_binaria(file_path):
    # Ler os dados de cada linha como uma lista de produtos
    with open(file_path, 'r') as f:
        transactions = [line.strip().split(',') for line in f.readlines()]
    
    # Encontrar todos os produtos únicos
    all_products = set([item for sublist in transactions for item in sublist])
    
    # Criar um DataFrame com a matriz binária
    data = []
    for transaction in transactions:
        transaction_data = {product: (product in transaction) for product in all_products}
        data.append(transaction_data)
    
    df = pd.DataFrame(data)
    return df

# Função para calcular a frequência de cada produto
def calcular_frequencia_produto(df):
    # Contar o número de ocorrências de cada produto
    frequencias = df.sum()
    
    # Calcular o total de registros de vendas (número total de transações)
    total_registros = len(df)

    # Calcular a frequência de cada produto (ocorrências / total de vendas)
    frequencia_produto = frequencias / total_registros
    return frequencia_produto

# Função para aplicar o corte com base no suporte
def cortar_por_suporte(frequencia_produto, min_support):
    # Filtrar produtos que têm suporte maior ou igual ao min_support
    produtos_filtrados = frequencia_produto[frequencia_produto >= min_support]
    return produtos_filtrados

# Função para gerar combinações de 2 em 2 produtos
def gerar_combinacoes(produtos_filtrados):
    # Gerar combinações de 2 em 2 produtos
    combinacoes = list(combinations(produtos_filtrados.index, 2))
    return combinacoes

# Função para calcular as regras de associação e aplicar o corte de confiança
def calcular_regras_associacao(df, combinacoes, min_confidence):
    regras = []
    
    for combinacao in combinacoes:
        # Subconjunto de dados que inclui os produtos da combinação
        df_subconjunto = df[df[combinacao[0]] & df[combinacao[1]]]
        
        # Calcular o número de transações que incluem os dois produtos
        count_comb = len(df_subconjunto)

        # Calcular a confiança da combinação
        support_A = df[combinacao[0]].sum() / len(df)
        support_B = df[combinacao[1]].sum() / len(df)
        support_AB = count_comb / len(df)

        if support_A > 0 and support_B > 0:
            # Calcular a confiança
            confidence = support_AB / support_A
            if confidence >= min_confidence:
                regras.append((combinacao, support_AB, confidence))
    
    return regras

# Função principal para processar o CSV
def processar_csv(file_path, min_support=0.5, min_confidence=0.5):
    # Transformar os dados em uma matriz binária
    df = transformar_dados_para_matriz_binaria(file_path)

    # Calcular a frequência dos produtos
    frequencia_produto = calcular_frequencia_produto(df)
    print(f"Frequência de cada produto em {file_path}:")
    print(frequencia_produto)

    # Cortar os produtos com base no suporte mínimo
    produtos_filtrados = cortar_por_suporte(frequencia_produto, min_support)
    print(f"Produtos após o corte de suporte em {file_path}:")
    print(produtos_filtrados)

    # Gerar combinações de 2 em 2 produtos
    combinacoes = gerar_combinacoes(produtos_filtrados)
    print(f"Combinations de 2 produtos em {file_path}:")
    print(combinacoes)

    # Calcular as regras de associação e aplicar o corte de confiança
    regras = calcular_regras_associacao(df, combinacoes, min_confidence)
    print(f"Regras de associação em {file_path}:")
    for regra in regras:
        print(f"Produtos: {regra[0]}, Suporte: {regra[1]:.4f}, Confiança: {regra[2]:.4f}")

# Caminho do arquivo CSV
file_paths = ['C:/data/data2.csv', 'C:/data/data3.csv', 'C:/data/data6.csv']

# Processar cada arquivo CSV
for file_path in file_paths:
    processar_csv(file_path, min_support=0.5, min_confidence=0.5)
