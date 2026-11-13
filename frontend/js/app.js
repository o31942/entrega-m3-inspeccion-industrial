/** Orquestador principal de eventos UI del cliente desacoplado SteelSight M3. */

import { checkHealth, fetchModelInfo, inspectImage } from "./api.js";
import { renderApp } from "./render.js";
import { createSyntheticDefectFile } from "./samples.js";
import { createStore } from "./state.js";

const MAX_BYTES = 10 * 1024 * 1024;
const ALLOWED_TYPES = new Set(["image/png", "image/jpeg", "image/webp", "image/bmp"]);

const store = createStore();
let lastObjectUrl = null;

function setPreviewFile(file) {
  if (!ALLOWED_TYPES.has(file.type)) {
    store.setError(`Formato no soportado (${file.type || "desconocido"}). Usa PNG, JPG, WEBP o BMP.`);
    return false;
  }
  if (file.size === 0 || file.size > MAX_BYTES) {
    store.setError("La imagen debe pesar entre 1 byte y 10 MB.");
    return false;
  }
  if (lastObjectUrl) {
    URL.revokeObjectURL(lastObjectUrl);
  }
  lastObjectUrl = URL.createObjectURL(file);
  const meta = document.getElementById("file-meta");
  document.getElementById("file-name").textContent = file.name;
  document.getElementById("file-details").textContent = `${(file.size / 1024).toFixed(1)} KB · ${file.type}`;
  meta?.classList.remove("hidden");

  store.patch({ selectedFile: file, previewUrl: lastObjectUrl, errorMessage: "" });
  return true;
}

async function syncBackendTelemetry() {
  const { gatewayUrl } = store.getState();
  try {
    const [health, modelInfo] = await Promise.all([
      checkHealth(gatewayUrl),
      fetchModelInfo(gatewayUrl).catch(() => null),
    ]);
    store.patch({ health, modelInfo });
  } catch {
    store.patch({ health: null });
  }
}

async function runCurrentInspection() {
  const st = store.getState();
  if (!st.selectedFile) {
    store.setError("Selecciona primero una imagen o genera una muestra Canvas.");
    return;
  }
  store.setLoading();
  try {
    const res = await inspectImage(st.gatewayUrl, {
      file: st.selectedFile,
      confThreshold: st.confThreshold,
      applyClahe: st.applyClahe,
    });
    store.setSuccess(res);
  } catch (err) {
    store.setError(err instanceof Error ? err.message : String(err));
  }
}

function bindEvents() {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const gatewayInput = document.getElementById("gateway-url");
  const thresholdInput = document.getElementById("conf-threshold");
  const thresholdOutput = document.getElementById("conf-threshold-value");
  const claheInput = document.getElementById("apply-clahe");

  dropzone?.addEventListener("click", () => fileInput?.click());
  dropzone?.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter" || ev.key === " ") {
      ev.preventDefault();
      fileInput?.click();
    }
  });
  dropzone?.addEventListener("dragover", (ev) => {
    ev.preventDefault();
    dropzone.classList.add("drag-over");
  });
  dropzone?.addEventListener("dragleave", () => dropzone.classList.remove("drag-over"));
  dropzone?.addEventListener("drop", (ev) => {
    ev.preventDefault();
    dropzone.classList.remove("drag-over");
    const file = ev.dataTransfer?.files?.[0];
    if (file) setPreviewFile(file);
  });

  fileInput?.addEventListener("change", () => {
    const file = fileInput.files?.[0];
    if (file) setPreviewFile(file);
  });

  gatewayInput?.addEventListener("change", () => {
    store.patch({ gatewayUrl: gatewayInput.value });
    void syncBackendTelemetry();
  });

  thresholdInput?.addEventListener("input", () => {
    const val = Number(thresholdInput.value);
    if (thresholdOutput) thresholdOutput.textContent = val.toFixed(2);
    store.patch({ confThreshold: val });
  });

  claheInput?.addEventListener("change", () => {
    store.patch({ applyClahe: Boolean(claheInput.checked) });
  });

  document.getElementById("btn-inspect")?.addEventListener("click", () => {
    void runCurrentInspection();
  });
  document.getElementById("btn-retry")?.addEventListener("click", () => {
    void runCurrentInspection();
  });
  document.getElementById("btn-refresh-health")?.addEventListener("click", () => {
    void syncBackendTelemetry();
  });
  document.getElementById("btn-reset")?.addEventListener("click", () => {
    document.getElementById("file-meta")?.classList.add("hidden");
    store.reset();
  });

  document.querySelectorAll("[data-sample]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const kind = btn.getAttribute("data-sample") || "scratches";
      const file = await createSyntheticDefectFile(kind);
      if (setPreviewFile(file)) {
        await runCurrentInspection();
      }
    });
  });
}

store.subscribe((state) => {
  renderApp(state, (historyEntry) => {
    store.patch({
      status: "success",
      result: historyEntry.result,
      previewUrl: historyEntry.previewUrl,
    });
  });
});

bindEvents();
void syncBackendTelemetry();
window.setInterval(() => {
  void syncBackendTelemetry();
}, 15000);
