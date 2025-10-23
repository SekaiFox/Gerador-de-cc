#PASSO A PASSO PARA UTILIZAÇÃO
# 1. Instale as bibliotecas:
#    pip install streamlit pandas
# 2. Salve este código (por exemplo, `gerador_contas_multibanco.py`).
# 3. Execute o aplicativo:
#    streamlit run gerador_contas_multibanco.py
# 4. IMPORTANTE: Use esses dados apenas para ambientes de teste.
#    Apenas os 5 grandes bancos tradicionais geram DVs válidos.
#    Os demais são placeholders (números aleatórios).

import streamlit as st
import pandas as pd
import random
from io import BytesIO

# --- LÓGICAS GENÉRICAS DE CÁLCULO ---

def _calcular_dv_modulo10(base_str, pesos):
    """Calcula DV pelo Módulo 10."""
    soma_produtos = 0
    
    # Itera de trás para frente
    for i in range(len(base_str) - 1, -1, -1):
        digito = int(base_str[i])
        
        # Pega o peso correspondente (cíclico)
        peso = pesos[(len(base_str) - 1 - i) % len(pesos)]
        
        produto = digito * peso
        # Se produto >= 10, soma os dígitos (ex: 16 -> 1+6=7)
        soma_produtos += (produto // 10) + (produto % 10)
        
    resto = soma_produtos % 10
    dv = 0 if resto == 0 else (10 - resto)
    return str(dv)

def _calcular_dv_modulo11(base_str, pesos, dv_map={}):
    """Calcula DV pelo Módulo 11 (usado por BB, Bradesco, Caixa)."""
    soma = 0
    # Ajusta os pesos para o tamanho da string (da direita para a esquerda)
    pesos_a_usar = pesos[len(pesos) - len(base_str):]
    
    for i, num in enumerate(base_str):
        soma += int(num) * pesos_a_usar[i]
        
    resto = soma % 11
    
    # Mapeamento de DV (ex: 10 pode virar 'X', 'P', '0', etc.)
    dv_calculado = 11 - resto
    
    if dv_calculado in dv_map:
        return dv_map[dv_calculado]
    
    return str(dv_calculado)

# --- IMPLEMENTAÇÕES POR BANCO ---

def _gerar_conta_bb(): # 001
    agencia_base = str(random.randint(1000, 9999))
    conta_base = str(random.randint(1000000, 9999999)) # 7 dígitos
    
    pesos = [9, 8, 7, 6, 5, 4, 3, 2]
    mapa_dv = {10: 'X', 11: '0', 0: '0'}
    
    dv_agencia = _calcular_dv_modulo11(agencia_base, pesos, mapa_dv)
    dv_conta = _calcular_dv_modulo11(conta_base, pesos, mapa_dv)
    
    return f"{agencia_base}-{dv_agencia}", f"{conta_base}-{dv_conta}", "Banco do Brasil"

def _gerar_conta_itau(): # 341
    agencia = str(random.randint(1000, 9999))
    conta = str(random.randint(10000, 99999)) # 5 dígitos
    
    # Itaú usa Módulo 10 com pesos 2,1 (cíclico)
    pesos_itau = [2, 1]
    dv_conta = _calcular_dv_modulo10(agencia + conta, pesos_itau)
    
    return f"{agencia}", f"{conta}-{dv_conta}", "Itaú Unibanco"

def _gerar_conta_bradesco(): # 237
    agencia_base = str(random.randint(1000, 9999))
    conta_base = str(random.randint(100000, 9999999)) # 7 dígitos
    
    # Bradesco usa Módulo 11 com pesos de 2 a 7 (para conta) e 2 a 5 (agência)
    pesos_ag = [5, 4, 3, 2]
    pesos_cta = [7, 6, 5, 4, 3, 2] # Para 7 dígitos, [7,6,5,4,3,2,7]
    pesos_cta = [2, 3, 4, 5, 6, 7][::-1][:len(conta_base)] # Ajuste de pesos 2-7
    pesos_cta.reverse()
    
    mapa_dv = {10: 'P', 11: '0', 0: '0'}
    
    dv_agencia = _calcular_dv_modulo11(agencia_base, pesos_ag, mapa_dv)
    dv_conta = _calcular_dv_modulo11(conta_base, [7,6,5,4,3,2,7,6,5,4,3,2][:len(conta_base)][::-1], mapa_dv)
    
    return f"{agencia_base}-{dv_agencia}", f"{conta_base}-{dv_conta}", "Bradesco"

def _gerar_conta_caixa(): # 104
    agencia_base = str(random.randint(1000, 9999))
    # Formato: 001 00012345-6 (Op 3 dig + Conta 8 dig + DV)
    op = "001" # Operação (001=CC, 013=Poupança)
    conta_base = str(random.randint(10000000, 99999999)) # 8 dígitos
    
    base_calculo = agencia_base + op + conta_base
    pesos = [8, 7, 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    soma = 0
    for i, num in enumerate(base_calculo):
        soma += int(num) * pesos[i]
    
    resto = (soma * 10) % 11
    dv = 0 if resto == 10 or resto == 0 else resto
    
    return f"{agencia_base}", f"{op}.{conta_base}-{dv}", "Caixa Econômica"
    
def _gerar_conta_santander(): # 033
    agencia = str(random.randint(1000, 9999))
    conta = str(random.randint(1000000, 9999999)) # 7 dígitos
    
    # Santander usa Módulo 10 com pesos 9,7,3,1,9,7,1,3,1,9,7,3 (Ag+Conta)
    pesos_santander = [9, 7, 3, 1, 9, 7, 1, 3, 1, 9, 7, 3]
    base = "00" + agencia + "0" + conta # Variações de zeros
    base = agencia + "00" + conta # 4 + 2 + 7 = 13 dígitos?
    
    # A lógica do Santander é notoriamente complexa e varia.
    # Vamos usar um placeholder por enquanto, pois a regra não é clara.
    # return f"{agencia}", f"{conta}-{random.randint(0,9)}", "Santander (Placeholder)"
    
    # Tentativa com lógica Módulo 10 (baseada em docs de boleto)
    # Agencia(4) + "01" (fixo) + Conta(7)
    base = agencia + "01" + conta
    pesos = [9,7,3,1,9,7,3,1,9,7,3,1][::-1] # 12 pesos
    pesos_a_usar = pesos[:len(base)]
    pesos_a_usar.reverse()

    soma_produtos = 0
    for i, digito_str in enumerate(base):
        produto = int(digito_str) * pesos_a_usar[i]
        soma_produtos += (produto % 10) # Santander só pega a unidade
        
    unidade_soma = soma_produtos % 10
    dv = 0 if unidade_soma == 0 else (10 - unidade_soma)
    
    return f"{agencia}", f"01{conta}-{dv}", "Santander"

# --- PLACEHOLDER (Para outros bancos) ---
def _gerar_conta_placeholder(bank_name):
    """Gera números aleatórios (NÃO VÁLIDOS) como exemplo."""
    ag = f"{random.randint(100, 9999)}"
    cta = f"{random.randint(100000, 9999999)}-{random.randint(0,9)}"
    return ag, cta, f"{bank_name} (Placeholder)"

# --- FUNÇÃO PRINCIPAL DE GERAÇÃO ---

def gerar_conta_bancaria(banco_id, banco_nome):
    """Chama a função de geração correta com base no ID do banco."""
    
    if banco_id == "001":
        return _gerar_conta_bb()
    elif banco_id == "341":
        return _gerar_conta_itau()
    elif banco_id == "237":
        return _gerar_conta_bradesco()
    elif banco_id == "104":
        return _gerar_conta_caixa()
    elif banco_id == "033":
        return _gerar_conta_santander()
    
    # --- Ponto de parada ---
    # Daqui para baixo, a lógica não é pública
    
    else:
        # Se a lógica não existe, usa o placeholder
        return _gerar_conta_placeholder(banco_nome)

# --- INTERFACE STREAMLIT ---

st.set_page_config(page_title="Gerador de Contas", layout="centered")
st.title("🏦 Gerador de Contas Correntes (para Testes)")
st.warning("Use estes dados apenas para ambientes de teste e desenvolvimento.")

# Lista de bancos (baseada em dados públicos de número de clientes)
LISTA_BANCOS = {
    # Lógica Real Implementada
    "001": "Banco do Brasil (Lógica Real)",
    "341": "Itaú Unibanco (Lógica Real)",
    "237": "Bradesco (Lógica Real)",
    "104": "Caixa Econômica (Lógica Real)",
    "033": "Santander (Lógica Real)",
    
    # Fintechs / Bancos Digitais (Lógica Proprietária - NÃO PÚBLICA)
    "260": "Nubank (Nu Pagamentos)",
    "380": "PicPay",
    "323": "Mercado Pago",
    "077": "Banco Inter",
    "336": "C6 Bank",
    "212": "PagBank (BancoSeguro)",
    "745": "BTG Pactual",
    "102": "XP Investimentos",
    "735": "Banco Neon",
    
    # Outros Bancos (Lógica não implementada)
    "746": "Sicoob",
    "756": "Sicredi",
    "655": "Banco Votorantim (BV)",
    "637": "Banco Sofisa",
    "121": "Banco Agibank",
    "070": "Banco de Brasília (BRB)"
}

opcoes_bancos = list(LISTA_BANCOS.items())

banco_selecionado = st.selectbox(
    "Para qual banco deseja gerar contas?",
    options=opcoes_bancos,
    format_func=lambda x: f"({x[0]}) {x[1]}"
)

quantidade = st.number_input("Quantas contas deseja gerar?", min_value=1, max_value=1000, value=10)

if st.button("Gerar Contas"):
    
    banco_id, banco_nome = banco_selecionado
    
    # IDs com lógica real
    ids_validos = ["001", "341", "237", "104", "033"]
    
    if banco_id not in ids_validos:
        st.error(f"Atenção: A lógica de DV para '{banco_nome}' é proprietária (secreta) ou não foi implementada. Serão gerados números aleatórios (placeholders) que **NÃO SÃO VÁLIDOS**.")
    
    contas_geradas = []
    for _ in range(quantidade):
        contas_geradas.append(gerar_conta_bancaria(banco_id, banco_nome))
    
    df = pd.DataFrame(contas_geradas, columns=["Agência", "Conta", "Banco"])

    st.success(f"{quantidade} contas para '{banco_nome}' geradas com sucesso!")
    st.dataframe(df)

    output = BytesIO()
    df.to_excel(output, index=False)
    st.download_button(
        label="📥 Baixar Contas em Excel",
        data=output.getvalue(),
        file_name=f"contas_teste_{banco_id}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )