# Cloud Run: Manual scaling is now GA

## Resumo Técnico
O Cloud Run agora suporta escalonamento manual (General Availability). Isso permite definir o número mínimo/máximo de instâncias, oferecendo controle mais preciso sobre cold starts e custos.

## Por que importa para a Aurora
- Reduz cold starts em endpoints críticos.
- Permite otimizar custos de agentes e serviços event-driven.
- Facilita previsibilidade de performance.

## Passos sugeridos
- Identificar endpoints sensíveis a cold start.
- Configurar escalonamento manual para esses serviços.
- Monitorar impacto em custo e latência.

## Referências
- [Cloud Run Manual Scaling](https://cloud.google.com/run/docs/configuring/manual-scaling)
