type LLMResult = { ok: boolean; text?: string; raw?: any };

export async function callPrimaryModel(
  prompt: string,
  signal?: AbortSignal,
): Promise<LLMResult> {
  // TODO: implemente a chamada real (fetch/axios) ao seu endpoint local/free tier
  // Exemplo placeholder (sempre demora 10s p/ simular timeout):
  await new Promise((r) => setTimeout(r, 10_000));
  return { ok: false };
}

export function isValid(result: LLMResult): boolean {
  // Critérios mínimos de completude (ajuste conforme seu domínio)
  return !!(result.ok && result.text && result.text.trim().length > 2);
}
