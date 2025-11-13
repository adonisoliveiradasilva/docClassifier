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

* `api/tests/` - *Camadas de testes*: testes unitários e de integração responsáveis por validar o comportamento da camada principal da aplicação e garantir a estabilidade da API.

## Endpoints

A API possui um endpoint principal para classificação:
```bash
POST /model/classify_docs
```

Classifica a imagem enviada e valida se o tipo identificado pelo modelo corresponde ao tipo informado pelo usuário.

### Requisição

A requisição deve ser do tipo `multipart/form-data` e conter os seguintes campos:

* `document_type` - *obrigatório*: tipo de documento que o usuário deseja carregar na aplicação, sendo os permitidos: `cnh`, `rg`, e `passaporte`.

* `file` - *obrigatório*: arquivo de imagem a ser classificado, sendo os permitidos: `png`, `jpeg`, e `jpg`.


### Resposta de sucesso — Documento confere

Indica que o tipo de documento enviado **corresponde ao tipo informado** pelo usuário.
```json
{
	"status_code": 200,
	"message": "Imagem confere com o tipo informado.",
	"data": {
		"user_expected_type": "cnh",
		"model_predicted_type": "cnh",
		"confidence_score": 0.62,
		"is_match": true
	}
}
```

### Resposta de sucesso — Documento não confere

Indica que o documento enviado **não corresponde ao tipo informado** pelo usuário, mesmo que a imagem tenha sido processada corretamente.
```json
{
	"status_code": 422,
	"message": "Não foi possível identificar RG na imagem enviada.",
	"data": {
		"user_expected_type": "rg",
		"model_predicted_type": "cnh",
		"confidence_score": 0.62,
		"is_match": false
	}
}
```

### Resposta de erro - 422
```json
{
  "detail": "Tipo de documento inválido: conta."
}
```
```json
{
  "detail": "Tipo de documento não fornecido."
}
```
```json
{
  "detail": "Imagem não fornecida ou formato inválido."
}
```

### Resposta de erro - 500

Ocorreu um erro inesperado durante a predição do modelo.
```json
{
  "detail": "Erro interno no servidor durante a classificação."
}
```
