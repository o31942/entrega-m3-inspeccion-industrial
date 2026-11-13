/** Carga drag-and-drop y validación previa cliente de imágenes superficiales. */

import { checkHealth, fetchModelInfo, inspectImage } from "./api.js";
import { createStore } from "./state.js";

const MAX_BYTES = 10 * 1024 * 1024;
const ALLOWED_TYPES = new Set(["image/png", "image/jpeg", "image/webp", "image/bmp"]);
const store = createStore();
let lastObjectUrl = null;

function setPreviewFile(file) {
  if (!ALLOWED_TYPES.has(file.type)) {
    store.setError("Formato no soportado. Usa PNG, JPG, WEBP o BMP.");
    return false;
  }
  if (file.size === 0 || file.size > MAX_BYTES) {
    store.setError("Archivo fuera de rango (1B–10MB).");
    return false;
  }
  if (lastObjectUrl) URL.revokeObjectURL(lastObjectUrl);
  lastObjectUrl = URL.createObjectURL(file);
  store.patch({ selectedFile: file, previewUrl: lastObjectUrl });
  return true;
}

function bindUploadEvents() {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  dropzone?.addEventListener("click", () => fileInput?.click());
  dropzone?.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("drag-over");
  });
  dropzone?.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("drag-over");
    const f = e.dataTransfer?.files?.[0];
    if (f) setPreviewFile(f);
  });
  fileInput?.addEventListener("change", () => {
    const f = fileInput.files?.[0];
    if (f) setPreviewFile(f);
  });
}

export { checkHealth, fetchModelInfo, inspectImage, setPreviewFile };
bindUploadEvents();
