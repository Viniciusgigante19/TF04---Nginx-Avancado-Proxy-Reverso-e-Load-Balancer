# Load Balancing e Roteamento

## Como Funciona

O load balancer opera exclusivamente no momento da requisição. Quando o cliente faz uma chamada HTTP, o Nginx lê o domínio e o caminho da URL e decide para qual servidor interno encaminhar — sem estado, sem sessão, puramente baseado em regras declaradas nos blocos `server{}`.

Cada `server{}` representa um virtual host — um domínio diferente atendido pelo mesmo Nginx. Dentro de cada servidor, os blocos `location` definem o roteamento por caminho: dada uma URL, o Nginx encontra o `location` correspondente e encaminha a requisição para o destino configurado no `proxy_pass`.

## Virtual Hosts

### localhost — Loja Virtual

```nginx
server {
    listen 80;
    server_name localhost;
    ...
}
```

Atende requisições para `localhost`. Roteia o tráfego para o frontend estático e para o cluster de backend dependendo do caminho acessado.

### admin.localhost — Painel Administrativo

```nginx
server {
    listen 80;
    server_name admin.localhost;
    ...
}
```

Virtual host separado para o painel admin. Apesar de usar a mesma porta 80, o Nginx diferencia os dois servidores pelo header `Host` da requisição — é isso que torna possível dois sites distintos no mesmo servidor e mesma porta.

## Locations

### Roteamento do Frontend

```nginx
location / {
    proxy_pass http://frontend:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ...
}
```

Encaminha toda requisição para a raiz ao container `frontend` na porta 3000. Os headers `Upgrade` e `Connection` habilitam suporte a WebSocket caso necessário.

### Roteamento da API com Load Balancing

```nginx
location /api/ {
    proxy_pass http://backend_cluster;
    ...
    limit_req zone=one burst=5 nodelay;
}
```

Requisições para `/api/` são encaminhadas para o `upstream backend_cluster` definido no `nginx.conf`, que distribui entre as 3 instâncias da API usando o algoritmo `least_conn` — a instância com menos conexões ativas no momento recebe a próxima requisição. O `limit_req` aplica o rate limiting definido globalmente, permitindo rajadas de até 5 requisições além do limite antes de rejeitar.

### Health Check do Load Balancer

```nginx
location /health {
    access_log off;
    default_type text/plain;
    return 200 "Load Balancer OK\n";
}
```

Endpoint interno que responde diretamente do Nginx sem passar por nenhum backend. Usado para verificar se o proxy está operacional. O `access_log off` evita poluição nos logs com chamadas de monitoramento.

## Headers de Proxy

Todos os blocos de roteamento enviam informações do cliente e do servidor através de headers HTTP:

| Header | Valor | Finalidade |
|--------|-------|------------|
| `Host` | `$host` | Domínio original da requisição |
| `X-Real-IP` | `$remote_addr` | IP real do cliente |
| `X-Forwarded-For` | `$proxy_add_x_forwarded_for` | Cadeia de IPs em proxies encadeados |
| `X-Instance-IP` | `$upstream_addr` | IP da instância de backend que respondeu |
| `X-Server-Name` | `$hostname` | Nome do container Nginx |

Esses headers permitem que os backends identifiquem o cliente real mesmo estando atrás do proxy, e permitem ao frontend exibir em tempo real qual instância da API atendeu cada requisição.

## SSL — ssl.conf

```nginx
server {
    listen 443 ssl;
    server_name localhost;

    ssl_certificate     /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ...
}
```

Bloco separado que habilita HTTPS na porta 443. O certificado é self-signed, gerado para uso local e de demonstração. O roteamento interno é idêntico ao do servidor HTTP — os mesmos `location` para frontend e API — com a diferença que toda a comunicação entre cliente e Nginx é criptografada. A terminação SSL ocorre no Nginx, e o tráfego interno entre Nginx e os containers continua em HTTP simples.