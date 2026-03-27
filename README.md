# TF04 - Nginx Avançado: Proxy Reverso e Load Balancer

## Aluno
- **Nome:** Vinícius Gigante
- **Curso:** Análise e Desenvolvimento de Sistemas — UniFAAT
- **RA:** 6324558

## Arquitetura

- **Nginx:** Proxy reverso, load balancer, SSL e rate limiting
- **Frontend:** Loja virtual estática servida via http-server
- **Backend:** 3 instâncias da API FastAPI para alta disponibilidade
- **Admin:** Painel administrativo Node.js/Express

## Funcionalidades Implementadas

- ✅ Load balancing com algoritmo `least_conn`
- ✅ 3 instâncias de backend com failover automático
- ✅ Distribuição de carga visível em tempo real
- ✅ Health checks automáticos nas instâncias da API
- ✅ SSL/TLS com certificado self-signed
- ✅ Rate limiting por IP (10 req/s, burst de 5)
- ✅ Logs detalhados com upstream info (`$upstream_addr`)
- ✅ Compressão Gzip
- ✅ Virtual hosts (`localhost` e `admin.localhost`)
- ✅ Proxy headers com informações de conexão

## Pré-requisitos

- Docker Desktop
- Git

## Como Executar

Clone o repositório:

```bash
git clone https://github.com/Viniciusgigante19/TF04---Nginx-Avancado-Proxy-Reverso-e-Load-Balancer.git
cd TF04---Nginx-Avancado-Proxy-Reverso-e-Load-Balancer
```

Gere os certificados SSL:

Escolha o comando ideal para o seu terminal, somente um deles é necessário:


```POWERSHELL
docker run --rm -v "${PWD}/nginx/ssl:/ssl" alpine/openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /ssl/key.pem -out /ssl/cert.pem -subj "/CN=localhost"
```

    OU

```BASH
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/nginx/ssl://ssl" alpine/openssl \
  req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /ssl/key.pem -out /ssl/cert.pem \
  -subj "//CN=localhost"
```


Suba todos os serviços:

```bash
docker compose up --build
```

## Endpoints

| Serviço | URL |
|---------|-----|
| Loja Virtual (HTTP) | http://localhost:8080 |
| Loja Virtual (HTTPS) | https://localhost:8443 |
| Admin Dashboard | http://admin.localhost:8080 |
| Health Check | http://localhost:8080/health |
| API | http://localhost:8080/api/ |


## Teste de Load Balancing

Acesse http://localhost:8080 e clique em **Atualizar** repetidamente — o hostname e IP do servidor mudam a cada requisição, mostrando o balanceamento entre as instâncias.

## Teste de Failover

```bash
# Parar uma instância
docker stop tf04---nginx-avancado-proxy-reverso-e-load-balancer-api-1-1

# O Nginx redireciona automaticamente para api-2 e api-3
# Restaurar a instância
docker start tf04---nginx-avancado-proxy-reverso-e-load-balancer-api-1-1
```

## Estrutura do Projeto

```
TF04/
├── README.md
├── docker-compose.yml
├── nginx/
│   ├── nginx.conf
│   ├── conf.d/
│   │   ├── load-balancer.conf
│   │   └── ssl.conf
│   └── ssl/
│       ├── cert.pem        # gerado localmente, não versionado
│       └── key.pem         # gerado localmente, não versionado
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── produtos.html
│   ├── carrinho.html
│   └── css/style.css
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── admin/
│   ├── Dockerfile
│   ├── index.js
│   ├── dashboard.html
│   └── css/admin.css
└── docs/
    ├── nginx-config.md
    └── load-balancing.md
```