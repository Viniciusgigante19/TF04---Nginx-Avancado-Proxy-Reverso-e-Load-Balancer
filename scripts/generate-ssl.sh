#!/bin/bash

# Define o caminho absoluto baseado no diretório de execução
# No Bash, $(pwd) é a forma padrão e mais segura
CERT_DIR="$(pwd)/nginx/ssl"

# Garante que a pasta de destino exista antes do Docker tentar montá-la
mkdir -p "$CERT_DIR"

echo "Iniciando geração de certificados em: $CERT_DIR"

# MSYS_NO_PATHCONV=1 é a 'rédea' necessária para o Git Bash/MINGW64
# O uso de //ssl e //CN impede que o terminal crie pastas fantasmas como /ssl;C
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$CERT_DIR://ssl" \
  alpine/openssl \
  req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout //ssl/key.pem \
  -out //ssl/cert.pem \
  -subj "//CN=localhost"

echo "Certificados gerados com sucesso."