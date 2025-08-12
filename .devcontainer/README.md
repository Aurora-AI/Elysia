# Aurora Dev Container

Este Dev Container permite desenvolver a Aurora Platform em um ambiente isolado e consistente.

## Configuração

### Plano A: Docker Outside-of-Docker (Padrão)
O container usa o daemon Docker do host através do socket `/var/run/docker.sock`.

### Plano B: Docker-in-Docker (Fallback)
Se o Plano A não funcionar, edite o `devcontainer.json` e substitua:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": false,
      "upgradePackages": true
    }
  },
  "runArgs": ["--privileged"],
  "mounts": [],
  "containerEnv": {},
  "postCreateCommand": "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y curl jq dos2unix && echo 'postCreate OK';"
}
```

## Uso

1. Abra o projeto no VS Code
2. Execute: `> Dev Containers: Rebuild Container Without Cache`
3. Aguarde a construção do container
4. Valide o Docker:
   ```bash
   docker version
   docker compose version
   ```

## Scripts Disponíveis

### Verificar Qdrant
```bash
# Normalizar e executar o script
dos2unix scripts/check_qdrant.sh || true
chmod +x scripts/check_qdrant.sh
bash -x scripts/check_qdrant.sh
```

### Executar testes
```bash
# Dentro do Dev Container
python -m pytest
```

## Troubleshooting

- Se `docker version` falhar, tente o Plano B (DinD)
- Se houver problemas de permissão, verifique se o usuário está no grupo `dockhost`
- Para rebuild completo: `> Dev Containers: Rebuild Container Without Cache`
