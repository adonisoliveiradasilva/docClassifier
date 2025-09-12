import traceback
from api.src.errors.handle_errors import handle_errors
from typing import Any, Dict

def log_and_handle_exception(exc: Exception) -> Dict[str, Any]:
    """
    Função para log detalhado de exceções e retorno de resposta padrão.
    """
    # Log detalhado no terminal
    print(f"Erro detalhado: {type(exc).__name__}: {str(exc)}")
    traceback.print_exc()
    
    # Gera a resposta padronizada usando handle_errors
    response = handle_errors(type(exc))
    print(f"Resposta gerada pelo handle_errors: {response}")
    
    return response
