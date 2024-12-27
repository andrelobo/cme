# CME - Sistema de Controle de Materiais e Estoque

## Tecnologias Utilizadas

### Backend
- **Python**: Linguagem principal do backend.
- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **SQLAlchemy**: ORM utilizado para interação com o banco de dados.
- **PostgreSQL**: Banco de dados relacional.

### Frontend
- **React.js**: Biblioteca para construção de interfaces de usuário.
- **Shadcn/UI**: Conjunto de componentes UI integrados com TailwindCSS.
- **TailwindCSS**: Framework CSS para estilização.

### Infraestrutura
- **Docker**: Contêinerização de serviços (backend, frontend e banco de dados).
- **Docker Compose**: Orquestração dos contêineres.

---

## Como Rodar o Projeto

### Pré-requisitos
- [Docker](https://www.docker.com/) instalado na máquina.
- [Docker Compose](https://docs.docker.com/compose/) instalado.
- Clonar este repositório:
  ```bash
  git clone https://github.com/seu-usuario/cme.git
  cd cme
  ```

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Banco de dados
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=cme_db

# URL do banco de dados
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}

# URL da API (usada no frontend)
VITE_API_URL=http://localhost:8000
```

### Iniciar a Aplicação
1. **Subir os contêineres com Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Acessar a aplicação:**
   - **Frontend**: [http://localhost:5173](http://localhost:5173)
   - **Backend (documentação da API)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Estrutura do Projeto

```
CME
├── backend
│   ├── app
│   │   ├── main.py        # Ponto de entrada do backend
│   │   ├── models.py      # Definições das tabelas e ORM
│   │   ├── routers        # Endpoints divididos por funcionalidade
│   │   └── ...
│   └── Dockerfile         # Configuração do contêiner do backend
├── frontend
│   ├── src
│   │   ├── components     # Componentes React reutilizáveis
│   │   ├── pages          # Páginas da aplicação
│   │   └── ...
│   └── Dockerfile         # Configuração do contêiner do frontend
├── .env                   # Variáveis de ambiente
├── docker-compose.yml     # Orquestração dos serviços
└── README.md              # Documentação do projeto
```

---

## Funcionalidades
- **Cadastro de usuários**: Cadastro de usuários e seus níveis de acesso (admin, tecnico, enfermagem)
- **Cadastro de materiais**: Inserção de materiais com dados relevantes.
- **Listagem**: Exibição de materiais cadastrados e seus detalhes.
- **Rastreamento**: Registro de etapas e falhas associadas a materiais.


## Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
