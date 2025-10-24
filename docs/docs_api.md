# docClassifier: API de Classificação de Documentos

Este projeto é uma API RESTful construída em Python usando [FastAPI](https://fastapi.tiangolo.com/) e [TensorFlow/Keras](https://www.tensorflow.org/?hl=pt-br), projetada para classificar imagens de documentos (como CNH, RG e Passaporte).

## Arquitetura do Projeto

A arquitetura da API segue os principios da **Clean Aechitectute** para garantir que o código seja desacoplado, testável, independente de frameworks e fácil de manter.

A regra de Dependência é estritamente seguinda: **as camadas externas dependem das internasm nunca o contrário**.

`(Mundo Externo) -> main -> infra -> use_cases -> domain`

### As camadas e suas responsabilidades

* `api/ml_training`: É um *mini-projeto* independente responsável apenas por treinar o modelo. Ele lê os dados brutos de `api/src/infra/datasets/`, treina a CNN e salva o modelo e as métricas em `api/src/infra/models/`. 

* `api/src/domain/` - *Camada de domínio*: contém as regras de negócio mais puras e centrais da aplicação. **Não depende de nenhuma outra camada**.
    * `enuns/`: Define as entidades de negócios (ex: `DocumentTypeEnum`).
    * `entities/`: Define as estruturas de dados puras (ex: `PredictionResult`).

* `api/src/use_cases/` - *Camada de caso de uso*: contém a **lógica de negócio** principal do projeto.
    * `contracts/`: Define as **interfaces** que o caso de uso precisa (define o que deve fazer, mas não como faz).

* `api/src/infra/` - *Camada de infraestutura*: contém as ferramentas **externas**, onde *implementa* a interface do caso de uso. 
    * `logs/`: Configuração do sistema de logging.
    * `dataset/`: Asrmazena os dados de treinamento do modelo.
    * `models`: Armazena o modelo treinado e as métricas do modelo.

* `api/src/main/` - *Camada principal*: é a camada que faz a conexão e expõe a aplicação via HTTP. Nesta camada, é criada a instância do FastAPI, são registrados os handlers de exceção, é feita a conexão com a interface e a injeção do caso de uso, são definidos os endpoints e validados os inputs da API.

## Endpoints

A API possui um endpoint principal para classificação:
```bash
POST /model/classify_docs
```

Classifica a imagem enviada e valida se o tipo identificado pelo modelo corresponde ao tipo informado pelo usuário.

### Requisição

A requisição deve ser do tipo `multipart/form-data` e conter os seguintes campos:

* `documentType`: O tipo de documento que o usuário deseja carregar na aplicação, sendo os permitidos: `cnh`, `rg`, e `passaporte`.

* `file`: O arquivo de imagem a ser classificado, sendo os permitidos: `png`, `jpeg`, e `jpg`.

E a resposta de sucesso é a seguinte:

```json
{
    "status_code": 200,
    "message": "Classificação realizada com sucesso.",
    "data": {
        "user_expected_type": "cnh",
        "model_predicted_type": "cnh",
        "confidence_score": 0.9987,
        "is_match": true
    }
}
```
**Respostas de Erro**:

* `422 Unprocessable Entity`: A requisição falhou na validação (ex: `image` não é uma imagem válida ou `expected_type` não é um dos valores permitidos).

* `500 Internal Server Error`: Ocorreu um erro inesperado durante a predição do modelo.