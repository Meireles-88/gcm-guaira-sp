from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import json

router = APIRouter()

class BotaoPanicoRequest(BaseModel):
    """Schema para requisição do botão de pânico"""
    agente_id: str
    localizacao: str
    timestamp: datetime = None

@router.post("/botao-panico")
async def acionar_botao(dados: BotaoPanicoRequest):
    """
    Endpoint para receber alertas de emergência dos agentes
    
    - **agente_id**: Identificação do agente
    - **localizacao**: Coordenadas geográficas
    """
    dados.timestamp = datetime.now()
    
    # Simulação: Salvar em log (futuro: Redis/WebSocket)
    with open("emergencia_log.json", "a") as log:
        log.write(json.dumps(dados.dict()) + "\n")
    
    return {
        "status": "alerta_recebido",
        "detalhes": dados.dict()
    }
