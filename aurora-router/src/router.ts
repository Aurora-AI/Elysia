import { cfg } from "./config.js";
import {
  newTraceId,
  traceIdHeader,
  withTrace,
  logJSON,
} from "./observability.js";
import { callPrimaryModel, isValid } from "./providers/primary.js";
import { callGemini } from "./providers/gemini.js";
import http from "http";
import { setTimeout as sleep } from "timers/promises";

function timeoutReject(ms: number, traceId: string) {
  return new Promise((_, rej) =>
    setTimeout(() => rej(new Error(`PRIMARY_TIMEOUT_${ms}ms`)), ms),
  );
}

async function handleLLM(prompt: string, traceId: string) {
  const ac = new AbortController();
  const primary = callPrimaryModel(prompt, ac.signal);
  try {
    const result: any = await Promise.race([
      primary,
      timeoutReject(cfg.primaryTimeoutMs, traceId),
    ]);
    if (isValid(result)) {
      logJSON(
        withTrace(traceId, { service: cfg.service.name, event: "primary_ok" }),
      );
      return result.text!;
    }
    throw new Error("PRIMARY_INVALID_RESPONSE");
  } catch (err: any) {
    // fallback Gemini
    const g = await callGemini({ prompt, traceId });
    if (!g.ok) throw new Error("FALLBACK_FAILED");
    return g.text!;
  } finally {
    ac.abort(); // evita gastos desnecessários após fallback
  }
}

const server = http.createServer(async (req, res) => {
  if (req.method !== "POST" || req.url !== "/v1/complete") {
    res.writeHead(404);
    return res.end();
  }
  let body = "";
  for await (const chunk of req) body += chunk;
  const { prompt } = JSON.parse(body || "{}");
  const traceId = req.headers[traceIdHeader()]?.toString() || newTraceId();
  res.setHeader(traceIdHeader(), traceId);

  try {
    const text = await handleLLM(prompt, traceId);
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ trace_id: traceId, text }));
  } catch (e: any) {
    logJSON(
      withTrace(traceId, {
        service: cfg.service.name,
        event: "error",
        error: e?.message,
      }),
    );
    res.writeHead(502, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ trace_id: traceId, error: "fallback_failed" }));
  }
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () =>
  logJSON({ service: cfg.service.name, event: "listening", port: PORT }),
);
