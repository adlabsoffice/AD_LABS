# 💰 Guia de Caça aos Créditos AWS ($100)

Para ganhar os **US$ 100 (R$ 600,00)** em créditos, precisamos completar estas 5 tarefas no console da AWS.

> [!IMPORTANT]
> **MUDE A REGIÃO PARA "Norte da Virgínia" (us-east-1)**
> No canto superior direito, ao lado do seu nome, certifique-se que está escrito **"Norte da Virgínia"** ou **"us-east-1"**.
> *Por que?* O Bedrock e outros serviços muitas vezes NÃO funcionam na região São Paulo (e são mais caros lá).

## Status Geral
- [x] **Tarefa 1: EC2** (Ligar uma máquina virtual) - $20
- [ ] **Tarefa 2: Bedrock** (Testar uma IA no chat) - $20
- [ ] **Tarefa 3: Billing** (Criar alerta de custo) - $20
- [ ] **Tarefa 4: Lambda** (Criar uma função simples) - $20
- [ ] **Tarefa 5: RDS** (Criar um banco de dados) - $20

---

## 🚀 O Jeito Mais Fácil (Pelo Painel)

**Olhe para a sua tela inicial (aquela do print que você mandou).**
Tem um quadrado chamado **"Explore a AWS"** com a lista das 5 tarefas.

**CLIQUE NOS LINKS DESSA LISTA!**
Eles te levam direto para a tela certa, sem precisar pesquisar nada.

### 1. Tarefa EC2 (Ligar Máquina)
1.  No quadrado "Explore a AWS", clique em **"Iniciar uma instância utilizando o EC2"**.
2.  Vai abrir uma tela cheia de opções.
3.  Procure o botão laranja **"Executar instância"** (Launch instance).
4.  **Nome:** Escreva "Teste".
5.  **Desça tudo** e clique no botão laranja **"Executar instância"**.
    *   *Não precisa mudar nada, o padrão já é grátis.*
6.  Espere ficar "Em execução".
7.  Depois, selecione ela, clique em **Estado da instância** -> **Encerrar instância** (Terminate).

### 2. Tarefa Bedrock (IA)
1.  No quadrado "Explore a AWS", clique em **"Utilizar um modelo de base..."**.
2.  Se ele pedir para "Solicitar acesso" (Request access):
    *   Clique no botão laranja.
    *   Marque "Titan Text G1 - Lite".
    *   Clique em "Next" e "Submit".
3.  Se já estiver no Chat:
    *   Escreva "Oi" e envie.

### 3. Tarefa Billing (Orçamento)
1.  No quadrado, clique em **"Configurar um orçamento..."**.
2.  Siga os passos da tela (Geralmente é só dar um nome e um valor, tipo $10).

### 4. Tarefa Lambda (App Web)
1.  No quadrado, clique em **"Criar uma aplicação web..."**.
2.  Escolha "Hello World" ou "Python".
3.  Crie.

### 5. Tarefa RDS (Banco de Dados)
1.  No quadrado, clique em **"Criar uma base de dados..."**.
2.  **CUIDADO AQUI:** Certifique-se de escolher a opção **"Nível Gratuito" (Free Tier)**.
3.  Crie e **DELETE** logo em seguida.

### 3. Tarefa Billing (Alerta de Custo)
1.  Pesquise por **"Budgets"** (ou Orçamentos).
2.  Clique em **"Criar orçamento"**.
3.  Selecione **"Orçamento de custo zero"** (Zero spend budget).
4.  Digite um e-mail para receber alertas.
5.  Clique em **"Criar orçamento"**.
6.  **Pronto!**

### 4. Tarefa Lambda (Função)
1.  Pesquise por **"Lambda"**.
2.  Clique em **"Criar função"**.
3.  Selecione **"Usar um esquema"** (Use a blueprint).
4.  Pesquise por "hello-world" e selecione a opção simples (Python ou Node).
5.  Dê o nome "MinhaFuncao".
6.  Clique em **"Criar função"**.
7.  **Pronto!**

### 5. Tarefa RDS (Banco de Dados)
1.  Pesquise por **"RDS"**.
2.  Clique em **"Criar banco de dados"**.
3.  Escolha **"Criação padrão"** e **"MySQL"**.
4.  Em **Modelos** (Templates), escolha **"Nível gratuito"** (Free tier) - **MUITO IMPORTANTE!**
5.  Defina uma senha qualquer.
6.  Clique em **"Criar banco de dados"**.
7.  Espere criar (pode demorar).
8.  Depois, selecione e vá em **"Ações"** -> **"Excluir"**.
    *   Desmarque "Criar snapshot final".
    *   Marque "Eu confirmo...".
    *   Digite "delete me" (ou o que pedir) para confirmar.
9.  **Pronto!**
