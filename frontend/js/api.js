/** Cliente HTTP/JSON desacoplado hacia el Gateway :8000 (que delega por gRPC :50051). */

const DEFAULT_TIMEOUT_MS = 15000;
let activeController = null;

function cleanBaseUrl(url) {
  return String(url || "http://127.0.0.1:8000").trim().replace(/\/+$/, "");
}

async function fetchJsonWithTimeout(url, options = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timer = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(url, { ...options, signal: controller.signal });
    const text = await resp.text();
    let payload = null;
    try {
      payload = text ? JSON.parse(text) : null;
    } catch {
      payload = { detail: text };
    }
    if (!resp.ok) {
      const detail = payload && payload.detail ? String(payload.detail) : `HTTP ${resp.status}`;
      const err = new Error(detail);
      err.status = resp.status;
      throw err;
    }
    return payload;
  } catch (err) {
    if (err && err.name === "AbortError") {
      throw new Error("Tiempo de espera agotado al contactar el Gateway gRPC.");
    }
    throw err;
  } finally {
    window.clearTimeout(timer);
  }
}

export async function checkHealth(gatewayUrl) {
  const base = cleanBaseUrl(gatewayUrl);
  return fetchJsonWithTimeout(`${base}/health`, { method: "GET" }, 5000);
}

export async function fetchModelInfo(gatewayUrl) {
  const base = cleanBaseUrl(gatewayUrl);
  return fetchJsonWithTimeout(`${base}/api/v1/model`, { method: "GET" }, 5000);
}

export async function inspectImage(gatewayUrl, { file, confThreshold, applyClahe }) {
  if (activeController) {
    activeController.abort();
  }
  activeController = new AbortController();
  const controller = activeController;
  const timer = window.setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

  const base = cleanBaseUrl(gatewayUrl);
  const form = new FormData();
  form.append("file", file, file.name || "sample.png");
  form.append("conf_threshold", String(confThreshold));
  form.append("apply_clahe", applyClahe ? "true" : "false");

  try {
    const resp = await fetch(`${base}/api/v1/inspect`, {
      method: "POST",
      body: form,
      signal: controller.signal,
    });
    const text = await resp.text();
    const payload = text ? JSON.parse(text) : {};
    if (!resp.ok) {
      throw new Error(payload.detail ? String(payload.detail) : `Error HTTP ${resp.status}`);
    }
    return payload;
  } catch (err) {
    if (err && err.name === "AbortError") {
      throw new Error("Solicitud cancelada o timeout de 15s superado.");
    }
    throw err;
  } finally {
    window.clearTimeout(timer);
    if (activeController === controller) {
      activeController = null;
    }
  }
}
