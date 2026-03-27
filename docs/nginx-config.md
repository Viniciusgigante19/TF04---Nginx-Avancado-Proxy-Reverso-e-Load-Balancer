# Configuração do Nginx

## Estrutura de Arquivos

A configuração do Nginx está organizada no diretório `nginx/`, separada por responsabilidade:

```
nginx/
├── nginx.conf              # Configurações globais
├── conf.d/
│   ├── load-balancer.conf  # Virtual hosts HTTP e roteamento
│   └── ssl.conf            # Virtual host HTTPS
└── ssl/
    ├── cert.pem            # Certificado self-signed
    └── key.pem             # Chave privada
```

## nginx.conf

Arquivo principal responsável pelas configurações globais do servidor. Define limites de conexão, compressão, logging, rate limiting e o cluster de backends. Os arquivos de `conf.d/` são carregados automaticamente pelo `include` no final do bloco `http`.

### Conexões

```nginx
events {
    worker_connections 1024;
}
```

Define o número máximo de conexões simultâneas que cada worker process do Nginx pode manter. Com o valor de 1024, o servidor suporta alto volume de requisições concorrentes sem degradação.

### Compressão Gzip

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

Ativa compressão automática nas respostas para os tipos de conteúdo listados, reduzindo o tamanho do tráfego de rede entre servidor e cliente.

### Logging

```nginx
log_format upstreamlog '$remote_addr - $host [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$upstream_addr"';
access_log /var/log/nginx/access.log upstreamlog;
```

Formato de log personalizado que inclui `$upstream_addr` — o IP da instância de backend que respondeu cada requisição. Isso permite rastrear exatamente qual instância da API atendeu cada chamada.

### Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
```

Define uma zona de rate limiting por IP do cliente, com capacidade de 10MB de memória para armazenar o estado. Limita cada IP a no máximo 10 requisições por segundo, protegendo o sistema contra abuso e ataques de força bruta.

### Upstream — Cluster de Backend

```nginx
upstream backend_cluster {
    least_conn;
    server api-1:8000;
    server api-2:8000;
    server api-3:8000;
}
```

Define o grupo de servidores de backend disponíveis para receber requisições. As três instâncias são réplicas da mesma API Python (FastAPI), rodando cada uma em seu próprio container Docker na porta 8000. O algoritmo `least_conn` é detalhado no documento de load balancing.

### Include

```nginx
include /etc/nginx/conf.d/*.conf;
```

Carrega automaticamente todos os arquivos de configuração do diretório `conf.d/`, mantendo o `nginx.conf` limpo e cada responsabilidade em seu próprio arquivo.