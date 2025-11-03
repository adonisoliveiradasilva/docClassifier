# Caminhos dos dados e onde salvar o modelo
PATH_DATASET_TRAIN = "api/src/infra/datasets/train"
PATH_SALVE_MODEL = "api/src/infra/models/classify_documents/"

# Hiperpâremtros para o treinamento do modelo
IMAGE_SIZE = (128, 128)
INPUT_SHAPE = (128, 128, 3)

# Parâmetros para o treinamento do modelo
EPOCHS = 50
BATCH_SIZE = 32
LEARNING_RATE = 0.001
SEED = 42
VALIDATION_SPLIT = 0.2

# Nomes dos arquivos para salvar o modelo e as métricas
MODEL_NAME = "model_classify_documents.h5"
METRICS_NAME = "model_classify_documents_metrics.json"
