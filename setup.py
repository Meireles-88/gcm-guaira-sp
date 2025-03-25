import os
import sys
from pathlib import Path
import platform

class GCMPProjectCreator:
    def __init__(self):
        self.base_structure = {
            "backend": {
                "core": ["settings.py", "security.py", "celery.py"],
                "apps": {
                    "ocorrencias": ["models.py", "api.py", "admin.py"],
                    "pessoal": ["models.py", "admin.py"],
                    "armamento": ["models.py", "admin.py"],
                    "atendimento": ["models.py"],
                    "inteligencia": ["models.py"]
                },
                "services": ["sinesp_client.py"],
                "manage.py": None,
                "requirements.txt": None
            },
            "api_fastapi": {
                "emergencia": ["schemas.py", "endpoints.py"],
                "inteligencia": ["schemas.py", "endpoints.py"],
                "Dockerfile": None
            },
            "frontend": {
                "admin": [],
                "portal_cidadao": []
            },
            "mobile": {
                "lib": [],
                "api_client": []
            },
            "docs": {
                "ADRs": ["001-mvc-to-fastapi.md"],
                "guia_migracao.md": None
            },
            "docker-compose.yml": None,
            ".env": None,
            "README.md": None,
            "scripts": {
                "deploy": [],
                "backup": []
            }
        }
        self.os_type = platform.system()
        self.project_path = Path.cwd()

    def create_project_structure(self):
        """Cria toda a estrutura do projeto"""
        print(f"\n🛠️ Criando estrutura do projeto em: {self.project_path}")
        print(f"🔍 Sistema operacional detectado: {self.os_type}\n")

        try:
            for item, content in self.base_structure.items():
                current_path = self.project_path / item
                
                if isinstance(content, dict):
                    self._create_directory(current_path)
                    self._process_directory_content(current_path, content)
                elif isinstance(content, list):
                    self._create_directory(current_path)
                    for file in content:
                        self._create_file(current_path / file)
                else:
                    self._create_file(current_path)

            self._add_initial_content()
            print("\n✅ Projeto criado com sucesso!")
            self._print_post_installation_instructions()

        except Exception as e:
            print(f"\n⛔ Erro crítico durante a criação do projeto: {str(e)}")
            sys.exit(1)

    def _create_directory(self, path):
        """Cria um diretório com verificação de existência"""
        try:
            path.mkdir(exist_ok=True)
            print(f"📁 Diretório criado: {path}")
        except PermissionError:
            print(f"⛔ Permissão negada para criar diretório: {path}")
            raise
        except Exception as e:
            print(f"⛔ Erro ao criar diretório {path}: {str(e)}")
            raise

    def _create_file(self, file_path):
        """Cria um arquivo vazio"""
        try:
            file_path.touch()
            print(f"📄 Arquivo criado: {file_path}")
        except PermissionError:
            print(f"⛔ Permissão negada para criar arquivo: {file_path}")
            raise
        except Exception as e:
            print(f"⛔ Erro ao criar arquivo {file_path}: {str(e)}")
            raise

    def _process_directory_content(self, base_path, content_dict):
        """Processa recursivamente o conteúdo de um diretório"""
        for item, content in content_dict.items():
            current_path = base_path / item
            
            if isinstance(content, dict):
                self._create_directory(current_path)
                self._process_directory_content(current_path, content)
            elif isinstance(content, list):
                self._create_directory(current_path)
                for file in content:
                    self._create_file(current_path / file)
            else:
                self._create_file(current_path)

    def _add_initial_content(self):
        """Adiciona conteúdo inicial aos arquivos importantes"""
        print("\n📝 Adicionando conteúdo inicial aos arquivos...")
        
        # Configurações Django
        self._create_django_settings()
        
        # Requirements
        self._create_requirements_file()
        
        # Docker
        self._create_docker_files()
        
        # Modelos e Schemas
        self._create_models_and_schemas()
        
        # Documentação
        self._create_documentation()

    def _create_django_settings(self):
        """Cria o arquivo de configurações do Django"""
        settings_path = self.project_path / "backend" / "core" / "settings.py"
        with settings_path.open("w", encoding='utf-8') as f:
            f.write("""# Configurações Django
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'sua-chave-secreta-aqui')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend.apps.ocorrencias',
    'backend.apps.pessoal',
    'backend.apps.armamento',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.core.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'gcm_db'),
        'USER': os.getenv('DB_USER', 'gcm_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'senha_segura'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Configurações adicionais...
""")

    def _create_requirements_file(self):
        """Cria o arquivo requirements.txt"""
        requirements_path = self.project_path / "backend" / "requirements.txt"
        with requirements_path.open("w", encoding='utf-8') as f:
            f.write("""django==4.2
psycopg2-binary
python-dotenv
celery
redis
djangorestframework
""")

    def _create_docker_files(self):
        """Cria os arquivos Dockerfile e docker-compose.yml"""
        # Dockerfile para FastAPI
        dockerfile_path = self.project_path / "api_fastapi" / "Dockerfile"
        with dockerfile_path.open("w", encoding='utf-8') as f:
            f.write("""FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn python-multipart psycopg2-binary
CMD ["uvicorn", "emergencia.endpoints:app", "--host", "0.0.0.0", "--port", "8000"]
""")

        # Docker Compose
        compose_path = self.project_path / "docker-compose.yml"
        with compose_path.open("w", encoding='utf-8') as f:
            f.write("""version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: ${DB_USER:-gcm_user}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-senha_segura}
      POSTGRES_DB: ${DB_NAME:-gcm_db}
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    ports:
      - "6379:6379"

  web:
    build: ./api_fastapi
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

volumes:
  pg_data:
""")

        # Arquivo .env
        env_path = self.project_path / ".env"
        with env_path.open("w", encoding='utf-8') as f:
            f.write("""# Configurações Django
DJANGO_SECRET_KEY=sua-chave-secreta

# Banco de dados
DB_NAME=gcm_db
DB_USER=gcm_user
DB_PASSWORD=senha_segura
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0
""")

    def _create_models_and_schemas(self):
        """Cria os modelos Django e schemas FastAPI"""
        # Modelo de Ocorrência
        ocorrencias_model_path = self.project_path / "backend" / "apps" / "ocorrencias" / "models.py"
        with ocorrencias_model_path.open("w", encoding='utf-8') as f:
            f.write("""from django.db import models
from backend.apps.pessoal.models import Agente

class Ocorrencia(models.Model):
    \"\"\"Modelo para registro de ocorrências policiais\"\"\"
    TIPOS_CRIME = [
        ('1456', 'Roubo de Veículo'),  # Código alinhado ao INFOCRIM
        ('7890', 'Porte Ilegal de Arma'),
        ('3456', 'Violência Doméstica'),
    ]
    
    tipo = models.CharField(max_length=4, choices=TIPOS_CRIME)
    data_registro = models.DateTimeField(auto_now_add=True)
    localizacao = models.CharField(max_length=100)
    agente_responsavel = models.ForeignKey(Agente, on_delete=models.PROTECT)
    descricao = models.TextField()
    fotos = models.JSONField(default=list)
    
    def __str__(self):
        return f"Ocorrência {self.id} - {self.get_tipo_display()}"

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"
""")

        # Admin para Ocorrências
        ocorrencias_admin_path = self.project_path / "backend" / "apps" / "ocorrencias" / "admin.py"
        with ocorrencias_admin_path.open("w", encoding='utf-8') as f:
            f.write("""from django.contrib import admin
from .models import Ocorrencia

@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    \"\"\"Configuração do admin para ocorrências\"\"\"
    list_display = ('id', 'tipo', 'data_registro', 'agente_responsavel')
    list_filter = ('tipo',)
    search_fields = ('descricao', 'localizacao')
""")

        # Modelo de Agente
        pessoal_model_path = self.project_path / "backend" / "apps" / "pessoal" / "models.py"
        with pessoal_model_path.open("w", encoding='utf-8') as f:
            f.write("""from django.db import models

class Agente(models.Model):
    \"\"\"Modelo para agentes da GCM\"\"\"
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    lotacao = models.CharField(max_length=50)
    data_ingresso = models.DateField()
    
    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    class Meta:
        verbose_name = "Agente"
        verbose_name_plural = "Agentes"
""")

        # Endpoint de Emergência (FastAPI)
        emergencia_endpoint_path = self.project_path / "api_fastapi" / "emergencia" / "endpoints.py"
        with emergencia_endpoint_path.open("w", encoding='utf-8') as f:
            f.write("""from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import json

router = APIRouter()

class BotaoPanicoRequest(BaseModel):
    \"\"\"Schema para requisição do botão de pânico\"\"\"
    agente_id: str
    localizacao: str
    timestamp: datetime = None

@router.post("/botao-panico")
async def acionar_botao(dados: BotaoPanicoRequest):
    \"\"\"
    Endpoint para receber alertas de emergência dos agentes
    
    - **agente_id**: Identificação do agente
    - **localizacao**: Coordenadas geográficas
    \"\"\"
    dados.timestamp = datetime.now()
    
    # Simulação: Salvar em log (futuro: Redis/WebSocket)
    with open("emergencia_log.json", "a") as log:
        log.write(json.dumps(dados.dict()) + "\\n")
    
    return {
        "status": "alerta_recebido",
        "detalhes": dados.dict()
    }
""")

    def _create_documentation(self):
        """Cria a documentação do projeto"""
        # README.md
        readme_path = self.project_path / "README.md"
        with readme_path.open("w", encoding='utf-8') as f:
            f.write("""# Controle Geral da GCM-Guaíra-SP

## Estrutura do Projeto

### Backend (Django)
- Apps principais:
  - `ocorrencias`: Registro de ocorrências policiais
  - `pessoal`: Gestão de agentes
  - `armamento`: Controle de armamento e viaturas

### API (FastAPI)
- Módulos:
  - `emergencia`: Botão de pânico e alertas
  - `inteligencia`: Análise preditiva

## Configuração Inicial

1. Crie/atualize o arquivo `.env` na raiz com as variáveis necessárias
2. Execute `docker-compose up -d` para iniciar os containers
3. Acesse a API em http://localhost:8000

## Documentação Técnica
Consulte os ADRs em `docs/ADRs` para decisões arquiteturais.
""")

        # ADR exemplo
        adr_dir = self.project_path / "docs" / "ADRs"
        adr_dir.mkdir(exist_ok=True, parents=True)
        adr_path = adr_dir / "001-mvc-to-fastapi.md"
        with adr_path.open("w", encoding='utf-8') as f:
            f.write("""# 1. Decisão Arquitetural: Django para FastAPI

## Status
Proposto

## Contexto
O módulo de emergência requer:
- Alta performance
- Suporte a WebSockets
- Integração com sistemas nacionais (SINESP/INFOCRIM)

## Decisão
Migrar o módulo de emergência para FastAPI na Fase 2.

## Consequências
- Vantagens:
  - Melhor performance
  - Suporte nativo a async/await
  - Integração mais simples com SINESP
- Desvantagens:
  - Dupla stack (Django + FastAPI)
  - Gerenciamento adicional de containers
""")

    def _print_post_installation_instructions(self):
        """Exibe instruções pós-instalação"""
        print("\n📌 Próximos passos:")
        print("1. Configure o ambiente:")
        print("   cd backend && pip install -r requirements.txt")
        print("2. Inicie os containers Docker:")
        print("   docker-compose up -d")
        print("3. Execute as migrações do Django:")
        print("   python manage.py migrate")
        print("4. Crie um superusuário:")
        print("   python manage.py createsuperuser")
        print("\n🌐 Acesse:")
        print("- Admin Django: http://localhost:8001/admin")
        print("- API FastAPI: http://localhost:8000/botao-panico")
        print("\n⚠️ Lembre-se de configurar o arquivo .env antes de iniciar!")

if __name__ == "__main__":
    print("🚀 Iniciando criação do projeto GCM-Guaíra-SP")
    creator = GCMPProjectCreator()
    creator.create_project_structure()