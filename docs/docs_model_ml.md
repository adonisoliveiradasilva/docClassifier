# docClassifier: Modelo de Machine Learning

O núcleo do projeto é um modelo de Visão Computacional baseado em **Redes Neurais Convolucionais (CNN)**. Seu objetivo é realizar a **classificação** de imagens de documentos em múltiplas categorias pré-definidas.

* **Tecnologia**: TensorFlow (Keras)
* **Tipo do Modelo**: Classificação de Imagens (Multiclasse)

**Classes-Alvo** 
| Tipo de Documento | Descrição |
| :--- | :--- |
| **RG (Registro Geral)** | Documento de Identidade padrão brasileiro. |
| **CNH (Carteira Nacional de Habilitação)** | Documento de Habilitação. |
| **Passaporte** | Documento de viagem internacional. |
| **Outros** | **Classe de rejeição** contendo diversas fotos (selfies, paisagens, outros documentos, etc.) para ensinar o modelo a diferenciar e rejeitar o que não é um documento conhecido. |


## Coleta e Preparação dos Dados

A base de dados para este projeto foi **coletada manualmente**. Esta abordagem foi necessária devido à dificuldade de encontrar bases de dados públicas adequadas que contivessem os documentos de identificação brasileiros (RG, CNH e PASSAPORTE) com qualidade e variedade suficientes para o treinamento.


## Organização e Processamento

O carregamento e pré-processamento das imagens são realizadas pela classe `ImageDatasetLoader`, que utiliza a função `image_dataset_from_directory` do TensorFlow. Cada subpasta dentro de `api/src/infra/datasets/train/` representa uma classe (label) correspondente a um tipo de documento. As imagens são divididos automaticamente em dois conjuntos: 
* **Treinamento (que corresponde 80% das imagens)**
* **Validação (que corresponde 20% das imagens)**

Durante o carregamento, as iamgens pssam por duas etapas principais:
* **Normalização**: todas as imagens são normalizadas para o intervalo de `[0,1]` usando `layers.Rescaling(1.0 / 255)`.
* **Data Augmentation**: aplicado apenas no conjunto de treinamento, é utilizado a classe `Sequential` do Keras com as seguintes transformações aleatórias:
    * **RandomRotation** - pequenas rotações aleatórias;
    * **RandomTranslation** - deslocamento horizontal e vertical;
    * **RandomZoom** - zom aleatório;
    * **RandomShear** - cisalhamento (sher) - efeito de inclinação.

Essas transformações aumentam a diversidade das imagens e ajudam o modelo a generalizar melhor.
Os conjuntos de dados são pré-carregados com `prefetch(buffer_size=tf.data.AUTOTUNE)` para melhorar o desempenho no treinamento.


## Arquitetura do Modelo

A classe `ArchitectureModel` define a arquitetura da CNN utilizada na classificação de documentos. O modelo é construído de forma sequencial, combinando camadas convolucionais e densas com normalização em lote e dropout para regularização.

#### Estrutura da Rede

| Camadas | Descrição |
| :--- | :--- |
| Conv2D (32 filtros) | Kernel (3x3), padding="same"
| BatchNormalization  |	Normaliza a ativação da camada anterior
| ReLU Activation | Função de ativação não linear
| MaxPooling2D | Pooling (2x2)
| Conv2D (64 filtros) | Kernel (3x3), padding="same"
| BatchNormalization + ReLU + MaxPooling2D | —
| Conv2D (128 filtros) | Kernel (3x3), padding="same"
| BatchNormalization + ReLU + MaxPooling2D | —
| Flatten | Transforma os mapas de ativação em um vetor
| Dense (256) | Camada totalmente conectada
| BatchNormalization + ReLU + Dropout(0.3) | Regularização
| Dense (128) | Camada intermediária com ativação ReLU
| Dense (num_classes, softmax) | Saída com probabilidade para cada classe


## Treinamento do Modelo

O modelo é compilado com:
* **Otimizador**: `Adam`.
* **Função de Perda**: `categorical_crossentropy` (função padrão para classificação multiclasse).
* **Métricas**: `accuracy`

Durante o treinamento, são utilizados **callbacks** para otimização dinâmica:
* `EarlyStopping`: interrompe o treino se não houver melhora na validação por determinado número de épocas, salvando os melhores pesos.
* `ReduceLROnPlateau`: reduz a taxa de aprendizado quando a performance estabiliza, permitindo ajustes finos nos pesos.

Após o treino, o modelo é avaliado no conjunto de validação para gerar as métricas finais: `accuracy` e `classification_report`. 
