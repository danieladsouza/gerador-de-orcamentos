import csv
import os
from colorama import Fore

# Arquivo de parcelas
arquivo_orcamento = 'parcelas.csv'

# Pausar e limpar tela
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    print()
    input(f'{Fore.GREEN}Pressione ENTER para continuar!')


# Arquivo
def carregar_orcamento():
    try:
        with open(arquivo_orcamento, 'r', newline='') as arquivo:
            reader = csv.reader(arquivo)
            return list(reader)
    except FileNotFoundError:
        return[]

def salvar_orcamento(parcelas):
    with open('parcelas.csv', 'w', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerows(parcelas)


# Interface
def exibir_imoveis():
    print(f'{Fore.YELLOW}-- TIPOS DE IMÓVEIS --')
    print(f'{Fore.BLUE}1. Casa')
    print(f'{Fore.BLUE}2. Apartamento')
    print(f'{Fore.BLUE}3. Estúdio')

def selecionar_imovel():
    tipo = input(f'{Fore.YELLOW} Digite o número do tipo de imóvel desejado: ').strip()
    return tipo

def selecionar_quartos():
    limpar_terminal()
    quartos = input(f'{Fore.YELLOW} Gostaria de 1 ou 2 quartos?: ').strip()
    return quartos

def selecionar_garagem():
    limpar_terminal()
    garagem = input(f'{Fore.YELLOW} Gostaria de adicionar vaga de garagem? (s/n): ').strip()
    return garagem

# Regra de negócio
class Imovel():
    def __init__(self, tipo, quartos=1, garagem=False, criancas=True, estudio=0):
        self.tipo = tipo
        self.quartos = quartos
        self.garagem = garagem
        self.criancas = criancas
        self.vaga_estudio = estudio
        self.valor = 0

    def valor_tipo(self):
        if self.tipo == 'estudio':
            self.valor += 1200
        elif self.tipo == 'apartamento':
            self.valor += 700
        elif self.tipo == 'casa':
            self.valor += 900
    
    def qtde_quartos(self):
        if self.tipo == 'apartamento' and self.quartos == 2:
            self.valor += 200
        elif self.tipo == 'casa' and self.quartos == 2:
            self.valor += 250

    def vaga_garagem(self):
        if (self.tipo == 'casa' or self.tipo == 'apartamento') and self.garagem:
            self.valor += 300
        elif self.tipo == 'estudio':
            if self.vaga_estudio >= 2:
                self.valor += 250
                if self.vaga_estudio > 2:
                    self.valor += (self.vaga_estudio - 2) * 60

    def tem_filhos(self):
        if self.tipo == 'apartamento' and not self.criancas:
            self.valor *= 0.95

    def calcular_valor(self):
        self.valor = 0
        self.valor_tipo()
        self.qtde_quartos()
        self.vaga_garagem()
        self.tem_filhos()
        return self.valor
    
# Contrato / financeiro
def parcelar_contrato(valor_contrato=2000):
    limpar_terminal()
    escolha = input(f'{Fore.RED} Nosso contrato imobiliário é no valor de R$2000,00. Gostaria de parcelar? (s/n): ').strip()

    if escolha != 's':
       print()
       return 1
    limpar_terminal()
    print(f'''{Fore.CYAN}Opções de parcelamento:
1x
2x
3x
4x
5x''')
        
    while True:
        escolha = input(f'{Fore.GREEN}Em quantas vezes gostaria de parcelar o valor do contrato? (1-5): ').strip()
        limpar_terminal()    
        if escolha in ('1', '2', '3', '4', '5'):
            return int(escolha)
        else:
            print(f'{Fore.RED}Opção inválida. Digite apenas números de 1 a 5.')

def gerar_parcelas(aluguel, contrato, parcelas_contrato):
    parcelas = []
    
    valor_parcela_contrato = contrato / parcelas_contrato

    total = aluguel * 12 + contrato

    parcelas.append([f'Aluguel mensal: R${aluguel:.2f}'])
    parcelas.append([f'Valor do contrato: R${contrato:.2f} em {parcelas_contrato}x'])
    parcelas.append([f'Total anual: R${total:.2f}'])
    parcelas.append([])

    for mes in range(1, 13):
        valor_mes = aluguel
        if mes <= parcelas_contrato:
            valor_mes += valor_parcela_contrato
            parcelas.append([f'Mes {mes}: R${valor_mes:.2f} (valor do aluguel + parcela do contrato)'])
        else:
            parcelas.append([f'Mes {mes}: R${valor_mes:.2f} (valor do aluguel)'])

    return parcelas

# Loop principal
while True:
    limpar_terminal()
    print(f'''{Fore.BLUE}======= GERADOR DE ORÇAMENTOS =======
    ======= R.M IMOVEIS =======''')
    exibir_imoveis()
    tipo_escolhido = selecionar_imovel()

    if tipo_escolhido == '1':
        tipo = 'casa'
    elif tipo_escolhido == '2':
        tipo = 'apartamento'
    elif tipo_escolhido == '3':
        tipo = 'estudio'
    else:
        print(f'{Fore.RED} Opção inválida. Por favor, selecione um tipo disponível.')
        pausar()
        continue

    if tipo != 'estudio': 
        quartos = int(selecionar_quartos())
        if quartos not in (1,2):
            print(f'{Fore.RED} Opção inválida. Por favor, selecione uma quantidade aceitável.')
            pausar()
            continue 
    else:
        quartos = 1

    escolha = selecionar_garagem().lower()

    if escolha == 's':
        if tipo == 'estudio':
           vagas = int(input(f'{Fore.RED} Quantas vagas deseja para o estúdio?: '))
           garagem = False
        else:
           garagem = True 
           vagas = 0
    else:
        garagem = False
        vagas = 0

    if tipo == 'apartamento':
        filhos = input(f'{Fore.RED} Possui filhos? (s/n): ').lower()
        criancas = True if filhos == 's' else False
        if filhos not in ('s','n').strip():
            print(f'{Fore.RED}Resposta inválida. Por favor, tente novamente.')
        pausar()
        continue
    else:
        criancas = True

    novo_imovel = Imovel(tipo=tipo, quartos=quartos, garagem=garagem,criancas=criancas,estudio=vagas)
    
    valor_final = novo_imovel.calcular_valor()

    print(f'{Fore.GREEN}Valor do aluguel: R${valor_final:.2f}')
    
    contrato = 2000

    parcelas_contrato = parcelar_contrato(contrato)
    total = valor_final * 12 + contrato

    print(f'{Fore.YELLOW}Contrato em {parcelas_contrato}x de R${contrato/parcelas_contrato:.2f}')
    print(f'{Fore.YELLOW}Total anual: R${total:.2f}')
    print(f'{Fore.GREEN}Arquivo de parcelas gerado!')

    parcelas = gerar_parcelas(valor_final, contrato, parcelas_contrato)
    salvar_orcamento(parcelas)

    pausar()
