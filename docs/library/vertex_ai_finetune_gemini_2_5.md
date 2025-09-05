# Vertex AI: Supervised fine-tuning for Gemini 2.5 Pro & Flash-Lite

## Resumo Técnico

O Vertex AI agora permite fine-tuning supervisionado dos modelos Gemini 2.5 Pro e Flash-Lite. Isso possibilita adaptar os modelos aos dados internos da Aurora, reduzindo a necessidade de prompts extensos e otimizando a performance para domínios específicos.

## Por que importa para a Aurora

- Reduz o tamanho do prompt e a latência das respostas.
- Diminui custos operacionais com tokens.
- Permite maior personalização e controle sobre o comportamento dos LLMs.

## Passos sugeridos

- Avaliar datasets internos para fine-tune.
- Planejar experimento controlado de fine-tuning.
- Medir impacto em latência e custo.

## Referências

- [Documentação Vertex AI](https://cloud.google.com/vertex-ai/docs/generative-ai/model-tuning)
