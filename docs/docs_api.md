# docClassifier: API de Classificação de Documentos

Este projeto é uma API RESTful construída em Python usando [FastAPI](https://fastapi.tiangolo.com/) e [TensorFlow/Keras](https://www.tensorflow.org/?hl=pt-br), projetada para classificar imagens de documentos (como CNH, RG e Passaporte).


## Modelo de Machine Learning

O núcleo desta API é um modelo de Visão Computacional baseado em Redes Neurais Convolucionais (CNN). Seu objetivo é realizar a **classificação** de imagens de documentos em múltiplas categorias pré-definidas.

* **Tecnologia**: TensorFlow (Keras)
* **Tipo do Modelo**: Classificação de Imagens (Multiclasse)

Classes-Alvo: 
| Tipo de Documento | Descrição |
| :--- | :--- |
| **RG (Registro Geral)** | Documento de Identidade padrão brasileiro. |
| **CNH (Carteira Nacional de Habilitação)** | Documento de Habilitação. |
| **Passaporte** | Documento de viagem internacional. |
| **Outros** | **Classe de rejeição** contendo diversas fotos (selfies, paisagens, outros documentos, etc.) para ensinar o modelo a diferenciar e rejeitar o que não é um documento conhecido. |

O modelo é treinado antes de rodar a API, usando a estrutura de diretórios padrão do Keras (`flow_from_directory`). Cada subpasta dentro de `api/src/infra/datasets/train/` é tratada como uma classe (label). Os dados são divididos automaticamente durante o carregamento em dois conjuntos: **treinamento (80%)** e **validação (20%)**.

O modelo é compilado com **otimizador `Adam`** e a função de perda `categorical_crossentropy` (função padrão para classificação multiclasse). O modelo conta também com **Callbacks** para um "treino inteligente", utilizando os parâmetros:
* `EarlyStopping`: Monitora a perda no conjunto de validação e para o treinamento automaticamente se o modelo não apresentar melhorias por um número definido de épocas, salvando sempre os melhores pesos.
* `ReduceLROnPlateau`: Reduz a taxa de aprendizado se o modelo parar de melhorar, permitindo um ajuste fino dos pesos.

Após o treino, o modelo é avaliado no conjunto de validação para gerar as métricas finais: `accuracy` e `classification_report`. 

### Processamento das imagens
As imagens são carregadas usando `ImageDataGenerator`, onde passam por **Data Augmentation**: são modificadas aleatoriamente (rotação, zoom, deslocamento horizontal e vertical) em tempo real. Isso cria novas imagens sintéticas que ajudam o modelo a generalizar melhor.

### Arquitetura do Modelo

* **Tipo**: Rede Neural Convolucional (CNN) Sequencial.

* **Input**: O modelo espera um tensor no formato (altura, largura, canais de cor),

* **Normalização**: O modelo espera que os valores dos pixels estejam normalizados no intervalo `[0, 1]`, ou seja, `valor_pixel / 255.0`.

* **Camadas Convolucionais**: O modelo é composto por uma pilha de blocos **Conv2D** e **MaxPooling2D**.
    * **Conv2D** (Convolução): Atua como um "extrator de características", aprendendo a identificar padrões visuais (bordas, texturas, formas).
    * **MaxPooling2D** (Agrupamento): Reduz o tamanho espacial da imagem, ajudando o modelo a focar nas características mais importantes e a ser mais eficiente.

* **Camadas Densas**: Após as convoluções, os dados são "achatados" (`Flatten`) e passam por camadas totalmente conectadas (`Dense`).

* **Dropout**: Uma técnica de regularização é aplicada (desativando neurônios aleatoriamente) para evitar overfitting (quando o modelo "decora" os dados de treino e falha em generalizar).

* **Output**  A última camada é `Dense` com ativação `softmax`. O número de neurônios nesta camada é igual ao número de classes (ex: 4). A função softmax garante que a saída seja um vetor de probabilidades, ex: {`[0.98, 0.01, 0.005, 0.005]`}, onde a soma de todas as probabilidades é 1.


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
