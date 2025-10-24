# docClassifier: Modelo de Machine Learning

O núcleo do projeto é um modelo de Visão Computacional baseado em **Redes Neurais Convolucionais (CNN)**. Seu objetivo é realizar a **classificação** de imagens de documentos em múltiplas categorias pré-definidas.

* **Tecnologia**: TensorFlow (Keras)
* **Tipo do Modelo**: Classificação de Imagens (Multiclasse)

Classes-Alvo: 
| Tipo de Documento | Descrição |
| :--- | :--- |
| **RG (Registro Geral)** | Documento de Identidade padrão brasileiro. |
| **CNH (Carteira Nacional de Habilitação)** | Documento de Habilitação. |
| **Passaporte** | Documento de viagem internacional. |
| **Outros** | **Classe de rejeição** contendo diversas fotos (selfies, paisagens, outros documentos, etc.) para ensinar o modelo a diferenciar e rejeitar o que não é um documento conhecido. |


## Coleta e Preparação dos Dados

A base de dados para este projeto foi **coletada manualmente**. Esta abordagem foi necessária devido à dificuldade de encontrar bases de dados públicas adequadas que contivessem os documentos de identificação brasileiros (RG, CNH e PASSAPORTE) com qualidade e variedade suficientes para o treinamento.


### Organização e Processamento

O modelo é treinado usando a estrutura de diretórios padrão do Keras (`flow_from_directory`). Cada subpasta dentro de `api/src/infra/datasets/train/` é tratada como uma classe (label). Os dados são divididos automaticamente durante o carregamento em dois conjuntos: 
* **Treinamento (80%)**
* **Validação (20%)**

As imagens são carregadas usando `ImageDataGenerator`, onde passam por **Data Augmentation**: são modificadas aleatoriamente (rotação, zoom, deslocamento horizontal e vertical) em tempo real. Isso cria novas imagens sintéticas que ajudam o modelo a generalizar melhor.


## Treinamento do Modelo

O modelo é compilado com **otimizador `Adam`** e a função de perda `categorical_crossentropy` (função padrão para classificação multiclasse). O modelo conta também com **Callbacks** para um "treino inteligente", utilizando os parâmetros:
* `EarlyStopping`: Monitora a perda no conjunto de validação e para o treinamento automaticamente se o modelo não apresentar melhorias por um número definido de épocas, salvando sempre os melhores pesos.
* `ReduceLROnPlateau`: Reduz a taxa de aprendizado se o modelo parar de melhorar, permitindo um ajuste fino dos pesos.

Após o treino, o modelo é avaliado no conjunto de validação para gerar as métricas finais: `accuracy` e `classification_report`. 


## Arquitetura do Modelo

* **Tipo**: Rede Neural Convolucional (CNN) Sequencial.

* **Input**: O modelo espera um tensor no formato (altura, largura, canais de cor),

* **Normalização**: O modelo espera que os valores dos pixels estejam normalizados no intervalo `[0, 1]`, ou seja, `valor_pixel / 255.0`.

* **Camadas Convolucionais**: O modelo é composto por uma pilha de blocos **Conv2D** e **MaxPooling2D**.
    * **Conv2D** (Convolução): Atua como um "extrator de características", aprendendo a identificar padrões visuais (bordas, texturas, formas).
    * **MaxPooling2D** (Agrupamento): Reduz o tamanho espacial da imagem, ajudando o modelo a focar nas características mais importantes e a ser mais eficiente.

* **Camadas Densas**: Após as convoluções, os dados são "achatados" (`Flatten`) e passam por camadas totalmente conectadas (`Dense`).

* **Dropout**: Uma técnica de regularização é aplicada (desativando neurônios aleatoriamente) para evitar overfitting (quando o modelo "decora" os dados de treino e falha em generalizar).

* **Output**  A última camada é `Dense` com ativação `softmax`. O número de neurônios nesta camada é igual ao número de classes (ex: 4). A função softmax garante que a saída seja um vetor de probabilidades, ex: {`[0.98, 0.01, 0.005, 0.005]`}, onde a soma de todas as probabilidades é 1.