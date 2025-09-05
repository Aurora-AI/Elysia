export const cfg = {
  primaryTimeoutMs: parseInt(
    process.env.PRIMARY_MODEL_TIMEOUT_MS ?? "6000",
    10,
  ),
  gemini: {
    url:
      process.env.GEMINI_API_URL ??
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-latest:generateContent",
    apiKey: process.env.GEMINI_API_KEY ?? "",
    maxOutputTokens: parseInt(process.env.GEMINI_MAX_TOKENS ?? "256", 10),
    temperature: parseFloat(process.env.GEMINI_TEMPERATURE ?? "0.7"),
    topP: parseFloat(process.env.GEMINI_TOP_P ?? "0.95"),
  },
  service: {
    name: process.env.SERVICE_NAME ?? "aurora-router",
  },
};
