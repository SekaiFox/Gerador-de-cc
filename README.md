# 🏦 Gerador de Contas Correntes para Testes

Uma aplicação web (Python + Streamlit) que gera números de agência e conta corrente sinteticamente válidos para os principais bancos brasileiros, destinados a ambientes de teste.

---
### ⚠️ AVISO IMPORTANTE: USO EXCLUSIVO PARA TESTES
**Este projeto foi desenvolvido para fins acadêmicos e de teste de software (sandbox).**

As contas geradas são **100% fictícias** e aleatórias. Elas **não** possuem fundos nem estão ativas. O objetivo é apenas testar formulários que validam o dígito verificador da conta.
---

![Gerador_de_Contas_Bancarias_xgmEf49rhP](https://github.com/user-attachments/assets/6975fb3a-9b56-4a50-a503-d53b6d5659f6)


## 🎯 O Problema (Contexto de Desenvolvimento)

Testar sistemas de pagamento (PIX, TED) ou formulários de cadastro de banco exige números de agência e conta que passem na validação. Diferente do CPF, **não existe um padrão único**: cada banco (Itaú, Bradesco, Caixa, etc.) usa seu próprio algoritmo proprietário (variações de Módulo 10 ou Módulo 11) para calcular o dígito verificador (DV).

## 💡 A Solução (Habilidade Técnica)

Este projeto é um gerador multi-banco que **implementa a lógica de cálculo de DV específica** para os principais bancos tradicionais do Brasil:
* Banco do Brasil (Módulo 11)
* Itaú Unibanco (Módulo 10)
* Bradesco (Módulo 11, regras próprias)
* Caixa Econômica (Módulo 11, formato de operação)
* Santander (Módulo 10, regras próprias)

Para fintechs (Nubank, Inter, etc.), cujos algoritmos não são públicos, a ferramenta gera um *placeholder* aleatório. Isso demonstra conhecimento em algoritmos de validação e desenvolvimento modular.

## 🛠️ Tecnologias Utilizadas
* **Python**
* **Streamlit**
* **Pandas** (para exportação para Excel)

## 🏁 Como Executar o Projeto

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/SekaiFox/Gerador-de-cc.git](https://github.com/SekaiFox/Gerador-de-cc.git)
    cd Gerador-de-cc
    ```
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```
3.  Instale as dependências (crie um arquivo `requirements.txt`):
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute o app Streamlit:
    ```bash
    streamlit run gerador_conta.py
    ```

**Arquivo `requirements.txt`:**
