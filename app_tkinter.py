import tkinter as tk
from tkinter import ttk
import random
import pandas as pd
from tkinter import messagebox
from ttkthemes import ThemedTk

# Keeping the core logic functions from the original app
def _calcular_dv_modulo10(base_str, pesos):
    soma_produtos = 0
    for i in range(len(base_str) - 1, -1, -1):
        digito = int(base_str[i])
        peso = pesos[(len(base_str) - 1 - i) % len(pesos)]
        produto = digito * peso
        soma_produtos += (produto // 10) + (produto % 10)
    resto = soma_produtos % 10
    dv = 0 if resto == 0 else (10 - resto)
    return str(dv)

def _calcular_dv_modulo11(base_str, pesos, dv_map={}):
    soma = 0
    pesos_a_usar = pesos[len(pesos) - len(base_str):]
    for i, num in enumerate(base_str):
        soma += int(num) * pesos_a_usar[i]
    resto = soma % 11
    dv_calculado = 11 - resto
    if dv_calculado in dv_map:
        return dv_map[dv_calculado]
    return str(dv_calculado)

# Bank account generation functions
def _gerar_conta_bb():
    agencia_base = str(random.randint(1000, 9999))
    conta_base = str(random.randint(1000000, 9999999))
    pesos = [9, 8, 7, 6, 5, 4, 3, 2]
    mapa_dv = {10: 'X', 11: '0', 0: '0'}
    dv_agencia = _calcular_dv_modulo11(agencia_base, pesos, mapa_dv)
    dv_conta = _calcular_dv_modulo11(conta_base, pesos, mapa_dv)
    return f"{agencia_base}-{dv_agencia}", f"{conta_base}-{dv_conta}", "Banco do Brasil"

def _gerar_conta_itau():
    agencia = str(random.randint(1000, 9999))
    conta = str(random.randint(10000, 99999))
    pesos_itau = [2, 1]
    dv_conta = _calcular_dv_modulo10(agencia + conta, pesos_itau)
    return f"{agencia}", f"{conta}-{dv_conta}", "Itaú Unibanco"

def _gerar_conta_bradesco():
    agencia_base = str(random.randint(1000, 9999))
    conta_base = str(random.randint(100000, 9999999))
    pesos_ag = [5, 4, 3, 2]
    pesos_cta = [2, 3, 4, 5, 6, 7][::-1][:len(conta_base)]
    pesos_cta.reverse()
    mapa_dv = {10: 'P', 11: '0', 0: '0'}
    dv_agencia = _calcular_dv_modulo11(agencia_base, pesos_ag, mapa_dv)
    dv_conta = _calcular_dv_modulo11(conta_base, [7,6,5,4,3,2,7,6,5,4,3,2][:len(conta_base)][::-1], mapa_dv)
    return f"{agencia_base}-{dv_agencia}", f"{conta_base}-{dv_conta}", "Bradesco"

def _gerar_conta_caixa():
    agencia_base = str(random.randint(1000, 9999))
    op = "001"
    conta_base = str(random.randint(10000000, 99999999))
    base_calculo = agencia_base + op + conta_base
    pesos = [8, 7, 6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = 0
    for i, num in enumerate(base_calculo):
        soma += int(num) * pesos[i]
    resto = (soma * 10) % 11
    dv = 0 if resto == 10 or resto == 0 else resto
    return f"{agencia_base}", f"{op}.{conta_base}-{dv}", "Caixa Econômica"

def _gerar_conta_santander():
    agencia = str(random.randint(1000, 9999))
    conta = str(random.randint(1000000, 9999999))
    base = agencia + "01" + conta
    pesos = [9,7,3,1,9,7,3,1,9,7,3,1][::-1]
    pesos_a_usar = pesos[:len(base)]
    pesos_a_usar.reverse()
    soma_produtos = 0
    for i, digito_str in enumerate(base):
        produto = int(digito_str) * pesos_a_usar[i]
        soma_produtos += (produto % 10)
    unidade_soma = soma_produtos % 10
    dv = 0 if unidade_soma == 0 else (10 - unidade_soma)
    return f"{agencia}", f"01{conta}-{dv}", "Santander"

def _gerar_conta_placeholder(bank_name):
    ag = f"{random.randint(100, 9999)}"
    cta = f"{random.randint(100000, 9999999)}-{random.randint(0,9)}"
    return ag, cta, f"{bank_name} (Placeholder)"

def gerar_conta_bancaria(banco_id, banco_nome):
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
    else:
        return _gerar_conta_placeholder(banco_nome)

class BankAccountGenerator:
    def __init__(self):
        self.root = ThemedTk(theme="equilux")
        self.root.title("Gerador de Contas Bancárias")
        self.root.geometry("800x600")
        
        # Configure style
        style = ttk.Style(self.root)
        style.configure("Treeview", background="#2e2e2e", 
                      fieldbackground="#2e2e2e", foreground="white")
        style.configure("TLabel", padding=5, font=('Segoe UI', 10))
        style.configure("TButton", padding=10, font=('Segoe UI', 10))
        style.configure("TCombobox", padding=5)
        
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="🏦 Gerador de Contas Correntes", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Warning message
        warning_label = ttk.Label(main_frame, 
                                text="⚠️ Use estes dados apenas para ambientes de teste", 
                                font=('Segoe UI', 10, 'italic'))
        warning_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Bank selection
        self.LISTA_BANCOS = {
            "001": "Banco do Brasil (Lógica Real)",
            "341": "Itaú Unibanco (Lógica Real)",
            "237": "Bradesco (Lógica Real)",
            "104": "Caixa Econômica (Lógica Real)",
            "033": "Santander (Lógica Real)",
            "260": "Nubank (Nu Pagamentos)",
            "380": "PicPay",
            "323": "Mercado Pago",
            "077": "Banco Inter",
            "336": "C6 Bank",
            "212": "PagBank (BancoSeguro)",
            "745": "BTG Pactual",
            "102": "XP Investimentos",
            "735": "Banco Neon"
        }

        bank_label = ttk.Label(main_frame, text="Selecione o banco:")
        bank_label.grid(row=2, column=0, pady=5, sticky=tk.W)

        self.bank_var = tk.StringVar()
        self.bank_combo = ttk.Combobox(main_frame, textvariable=self.bank_var, width=40)
        self.bank_combo['values'] = [f"({k}) {v}" for k, v in self.LISTA_BANCOS.items()]
        self.bank_combo.grid(row=2, column=1, pady=5, sticky=tk.W)
        self.bank_combo.set(self.bank_combo['values'][0])

        # Quantity selection
        quantity_label = ttk.Label(main_frame, text="Quantidade de contas:")
        quantity_label.grid(row=3, column=0, pady=5, sticky=tk.W)

        self.quantity_var = tk.StringVar(value="10")
        quantity_entry = ttk.Entry(main_frame, textvariable=self.quantity_var, width=10)
        quantity_entry.grid(row=3, column=1, pady=5, sticky=tk.W)

        # Generate button
        generate_btn = ttk.Button(main_frame, text="Gerar Contas", command=self.generate_accounts)
        generate_btn.grid(row=4, column=0, columnspan=2, pady=20)

        # Results treeview
        self.tree = ttk.Treeview(main_frame, columns=('Agência', 'Conta', 'Banco'), 
                                show='headings', height=10)
        self.tree.grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        # Configure treeview columns
        for col in ('Agência', 'Conta', 'Banco'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=5, column=2, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Export button
        export_btn = ttk.Button(main_frame, text="Exportar para Excel", 
                               command=self.export_to_excel)
        export_btn.grid(row=6, column=0, columnspan=2, pady=20)

    def generate_accounts(self):
        try:
            quantity = int(self.quantity_var.get())
            if quantity < 1 or quantity > 1000:
                messagebox.showerror("Erro", "A quantidade deve estar entre 1 e 1000")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido")
            return

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get selected bank
        bank_selection = self.bank_combo.get()
        banco_id = bank_selection[1:4]  # Extract bank ID from selection
        banco_nome = self.LISTA_BANCOS.get(banco_id, "Banco Desconhecido")

        # Generate accounts
        self.generated_accounts = []
        for _ in range(quantity):
            account = gerar_conta_bancaria(banco_id, banco_nome)
            self.generated_accounts.append(account)
            self.tree.insert('', 'end', values=account)

        messagebox.showinfo("Sucesso", f"{quantity} contas geradas com sucesso!")

    def export_to_excel(self):
        if not hasattr(self, 'generated_accounts') or not self.generated_accounts:
            messagebox.showwarning("Aviso", "Gere algumas contas primeiro!")
            return

        try:
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Salvar como..."
            )

            if filepath:
                df = pd.DataFrame(self.generated_accounts, 
                                columns=["Agência", "Conta", "Banco"])
                df.to_excel(filepath, index=False)
                messagebox.showinfo("Sucesso", "Arquivo Excel salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BankAccountGenerator()
    app.run()