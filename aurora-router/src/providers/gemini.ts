import fetch from "node-fetch";
import { cfg } from "../config.js";
import { withTrace, logJSON } from "../observability.js";

export async function callGemini({
  prompt,
  traceId,
}: {
  prompt: string;
  traceId: string;
}): Promise<{ ok: boolean; text?: string; raw?: any }> {
  const body = {
    contents: [
      {
        role: "user",
        parts: [{ text: `Complete apenas o trecho em falta: ${prompt}` }],
      },
    ],
    generationConfig: {
      maxOutputTokens: cfg.gemini.maxOutputTokens,
      temperature: cfg.gemini.temperature,
      topP: cfg.gemini.topP,
    },
  };

  const started = Date.now();
  const resp = await fetch(`${cfg.gemini.url}?key=${cfg.gemini.apiKey}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const raw: any = await resp.json();
  const latency = Date.now() - started;

  const text =
    raw?.candidates?.[0]?.content?.parts?.map((p: any) => p.text).join("") ??
    "";
  const ok = !!text;

  logJSON(
    withTrace(traceId, {
      service: cfg.service.name,
      event: "fallback_gemini",
      fallback_reason: "timeout_or_invalid",
      latency_ms: latency,
      input_tokens: undefined, // se disponível via response.metadata
      output_tokens: undefined, // se disponível via response.metadata
      status: resp.status,
    }),
  );

  return { ok, text, raw };
}
