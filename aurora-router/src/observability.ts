import { randomUUID } from "crypto";

export function traceIdHeader() {
  return "x-aurora-trace-id";
}
export function newTraceId() {
  return randomUUID();
}

export function withTrace<T>(traceId: string, payload: T) {
  return { trace_id: traceId, ...payload };
}

export function logJSON(obj: any) {
  // eslint-disable-next-line no-console
  console.log(JSON.stringify(obj));
}
