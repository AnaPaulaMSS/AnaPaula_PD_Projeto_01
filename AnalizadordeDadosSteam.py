import csv

class Jogo:
    """  Uma classe para carregar e analisar dados de jogos da Steam. """

    def __init__(self, nome, ano, preco):

        self.nome = nome 

        try:
            # Tenta a lógica para o formato "Mês dia, Ano" (ex: "Oct 21, 2008")
            self.ano = int(ano.split(',')[-1].strip())
        except (ValueError, IndexError):
            # tenta a lógica para o formato "Mês Ano" (ex: "May 2020")
            try:
                self.ano = int(ano.split()[-1].strip())
            except (ValueError, IndexError):
                print(f"Aviso: Não foi possível extrair o ano da data '{ano}'.")

        self.preco = float(preco)
    
class AnalisadordeDados:

    """ Carrega os dados de um arquivo CSV e retorna uma lista de objetos Jogo."""

    def __init__(self, arquivo):
        self.jogos = self.Carregar_dados(arquivo)

    def Carregar_dados(self, arquivo):
        """
        Carrega os dados de um arquivo CSV de jogos e os retorna como uma lista de objetos.

        Args:
            arquivo (str): O caminho para o arquivo CSV.

        Returns:
            list: Uma lista de objetos Jogo se o carregamento for bem-sucedido.
            None: Retorna None se o arquivo não for encontrado.

        """
        jogos_carregados = []
        try:
            with open(arquivo, mode='r', encoding='utf-8') as arquivo_csv:
                leitor_csv = csv.DictReader(arquivo_csv)
                #(csv.DictReader) é uma classe do módulo csv de Python que permite ler um arquivo CSV e transformar cada linha do arquivo num dicionário
                
                for linha in leitor_csv:

                    nome = linha['Name']
                    ano = linha['Release date']
                    preco = linha['Price']
                    
                    jogos_carregados.append(
                        Jogo(nome, ano, preco)
                    )               
        except FileNotFoundError:  # Se o arquivo não estiver lá, o Python avisa com um erro.
        
            print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
            return None
                
        # Se tudo deu certo, iremos retornar uma lista cheia de jogos. 
        return jogos_carregados

    def Porcentagem_Jogos_Gratuitos(self):
        
        """ Calcula o percentual de jogos gratuitos e pagos na plataforma. """

        if not self.jogos:
            return 0.0, 0.0, "Nenhum jogo encontrado para análise."

        total_jogos = len(self.jogos)
        jogos_gratuitos = 0
        
        for jogo in self.jogos:
            if jogo.preco == 0:
                jogos_gratuitos += 1
        
        percentual_gratuitos = (jogos_gratuitos / total_jogos) * 100
        percentual_pagos = 100 - percentual_gratuitos
        
        return percentual_gratuitos, percentual_pagos

    def Ano_Jogos_Novos(self):

        """ Encontra o ano com o maior número de lançamentos de jogos. """

        if not self.jogos:
            return None, "Nenhum jogo encontrado para análise."

        contagem_por_ano = {}

        for jogo in self.jogos:
            if jogo.ano > 0:
                if jogo.ano in contagem_por_ano:
                    contagem_por_ano[jogo.ano] += 1
                else:
                    contagem_por_ano[jogo.ano] = 1

        if not contagem_por_ano: 
            return None, "Não foi possível extrair anos válidos dos dados."

        ano_jogos_novos = None
        maior_contagem = 0
        
        
        for ano, contagem in contagem_por_ano.items():
            if contagem > maior_contagem:
                maior_contagem = contagem
                ano_jogos_novos = ano
        
        return ano_jogos_novos, maior_contagem

    def Jogo_Caro(self):

        """ Encontra o jogo mais caro de cada ano. """

        if not self.jogos:
            return None
    
        jogo_mais_caro = max(self.jogos, key=lambda jogo: jogo.preco)
        
        return jogo_mais_caro



#-----------------------------------------------------------------------------------------------------------------------------
# R E S U L T A D O S
#-----------------------------------------------------------------------------------------------------------------------------

analisador = AnalisadordeDados('steam_games.csv')

# Pergunta 1

gratuitos, pagos = analisador.Porcentagem_Jogos_Gratuitos()
print('\n--- Pergunta 1: Qual o percentual de jogos gratuitos e pagos? ---')
print(f'Jogos Gratuitos: {gratuitos:.2f}%')
print(f'Jogos Pagos: {pagos:.2f}%')

# Pergunta 2

ano, contagem = analisador.Ano_Jogos_Novos()
print('\n--- Pergunta 2: Qual o ano com o maior número de novos jogos? ---')
print(f'O ano com o maior número de lançamentos foi {ano}, com {contagem} jogos.')

# Pergunta 3 

jogo_mais_caro = analisador.Jogo_Caro()
print('\n--- Pergunta 3: Qual o Jogo mais caro da tabela inteira?---')
print(f'O jogo mais caro é {jogo_mais_caro.nome} com o preço de ${jogo_mais_caro.preco:.2f}.\n')