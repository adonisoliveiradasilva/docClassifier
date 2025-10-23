# docClassifier: API de Classificação de Documentos

**docClassifier** é um sistema inteligente baseado em Visão Computacional e Deep Learning (Redes Neurais Convolucionais - CNN) para a **classificação e validação de documentos** de identificação.

O objetivo principal é predizer o tipo de documento enviado (RG, CNH, Passaporte) e comparar essa previsão com a classificação esperada pelo usuário.

---
## Visão Geral do Projeto

Este projeto demonstra a construção de uma solução de IA robusta e escalável, combinando o poder do **Deep Learning** com princípios avançados de **Engenharia de Software** (Clean Architecture e Atomic Design).

A arquitetura modular garante que o processamento de imagem, a lógica do modelo e a interface do usuário sejam independentes, facilitando a manutenção, testes e futuras expansões.


### Modelo de Machine Learning

O modelo central é uma **Rede Neural Convolucional (CNN)** treinada para categorizar imagens nos seguintes tipos: `cnh`, `rg` e `passporte`

### Fluxo de Classificação e Validação

1.  **Envio:** O usuário interage com o Frontend e submete uma imagem de documento, informando também o tipo de documento esperado (ex: "CNH").
2.  **Pré-processamento:** O Backend recebe a imagem, aplica validações de segurança e otimiza a imagem (redimensionamento e normalização) para o modelo.
3.  **Predição (CNN):** O modelo CNN processa a imagem pré-processada e retorna o tipo de documento previsto (ex: "CNH").
4.  **Validação:** O sistema compara o tipo previsto pelo modelo ("CNH") com o tipo informado pelo usuário ("CNH").
5.  **Resultado:** A resposta é retornada ao usuário, indicando se houve **correspondência** (classificação bem-sucedida) ou falha.

---
## Tecnologias e Metodologias

### Backend (Python)

* **Python 3.10+**
* **TensorFlow / Keras**
* **FastAPI**
* **Pillow**
* **Clean Architecture**
* **Testes Unitários (pytest + mock)**

### Frontend (Web)

* **TypeScript / Angular**
* **SCSS e HTML5**
* **RxJS**
* **Atomic Design**

---
## Como Executar o Projeto

#### Backend (API Python)

1.  **Clonar o repositório:**
    ```bash
    git clone [link-do-seu-repo]
    cd docClassifier
    ```
2.  **Criar e Ativar o ambiente virtual**
    ```bash
    # Cria o ambiente
    python -m venv venv

    # Ativa o ambiente (Windows PowerShell)
    .\venv\Scripts\Activate.ps1

    # Ou para Linux/macOS
    source venv/bin/activate
    ```
3.  **Instalar dependências**
    ```bash
    # Recomenda-se atualizar o pip primeiro
    python -m pip install --upgrade pip

    # Instala as dependências do projeto
    pip install -r requirements.txt  
    ```
4.  **Rodar a API**
    ```bash
    python -m api.app
    ```
    *A documentação interativa da API estará disponível em `http://localhost:8000/docs`*


### Frontend (Angular)

1.  **Instalar Node.js e Angular CLI** (se ainda não tiver).
2.  **Navegar para a pasta do Frontend:**
    ```bash
    cd ui/
    ```
3.  **Instalar dependências do Node:**
    ```bash
    npm install
    ```
4.  **Executar o servidor de desenvolvimento:**
    ```bash
    npm start
    ```
    *A interface será aberta em `http://localhost:4200`.*

---

## Documentação Completa

Para detalhes técnicos sobre a arquitetura do modelo, estrutura de pastas, _endpoints_ da API, acesse:

[**/docs**](docs/)
