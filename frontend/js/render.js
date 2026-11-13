/** Renderizador DOM seguro (sin innerHTML inseguro) para resultados, XAI e historial. */

import { UI_STATES } from "./state.js";

export function renderHealth(state) {
  const pill = document.getElementById("health-badge");
  const text = document.getElementById("health-text");
  const modelIdEl = document.getElementById("meta-model-id");
  const modelRevEl = document.getElementById("meta-model-rev");
  const runtimeEl = document.getElementById("meta-runtime");

  if (!pill || !text) return;

  pill.classList.remove("health-online", "health-offline", "health-unknown");
  if (state.health && state.health.status === "SERVING") {
    pill.classList.add("health-online");
    text.textContent = `Online · gRPC ${state.health.runtime} (uptime ${state.health.uptime_seconds}s)`;
    if (modelIdEl) modelIdEl.textContent = state.health.model_id;
    if (modelRevEl) modelRevEl.textContent = String(state.health.model_revision).slice(0, 10);
    if (runtimeEl && state.modelInfo) {
      runtimeEl.textContent = `${state.modelInfo.license} · ${state.health.runtime}`;
    }
  } else {
    pill.classList.add("health-offline");
    text.textContent = "Backend desconectado · Inicia make backend (:50051 / :8000)";
  }
}

export function renderScoresBars(scores) {
  const container = document.getElementById("scores-bars");
  if (!container) return;
  container.replaceChildren();

  scores.forEach((score, idx) => {
    const row = document.createElement("div");
    row.className = idx === 0 ? "score-row score-row-top" : "score-row";

    const label = document.createElement("span");
    label.textContent = score.label_es || score.class_name;

    const track = document.createElement("div");
    track.className = "score-track";

    const fill = document.createElement("div");
    fill.className = "score-fill";
    const pct = Math.max(0, Math.min(100, Number(score.probability || 0) * 100));
    fill.style.width = `${pct.toFixed(1)}%`;
    track.appendChild(fill);

    const pctText = document.createElement("span");
    pctText.className = "score-pct";
    pctText.textContent = `${pct.toFixed(1)}%`;

    row.append(label, track, pctText);
    container.appendChild(row);
  });
}

export function renderHistory(history, onSelectEntry) {
  const tbody = document.getElementById("history-tbody");
  const countEl = document.getElementById("history-count");
  if (!tbody) return;
  if (countEl) {
    countEl.textContent = `${history.length} registro${history.length === 1 ? "" : "s"}`;
  }
  tbody.replaceChildren();

  if (history.length === 0) {
    const emptyRow = document.createElement("tr");
    emptyRow.className = "history-empty-row";
    const cell = document.createElement("td");
    cell.colSpan = 7;
    cell.textContent = "Aún no se han ejecutado inspecciones en esta sesión.";
    emptyRow.appendChild(cell);
    tbody.appendChild(emptyRow);
    return;
  }

  for (const item of history) {
    const tr = document.createElement("tr");
    const r = item.result;

    const cells = [
      item.timestamp,
      item.filename,
      r.predicted_label_es || r.predicted_class,
      `${(Number(r.confidence) * 100).toFixed(1)}%`,
      r.requires_human_review ? "Revisión HITL" : "Detectado",
      `${r.latency_ms} ms`,
    ];

    for (const val of cells) {
      const td = document.createElement("td");
      td.textContent = val;
      tr.appendChild(td);
    }

    const actionTd = document.createElement("td");
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn btn-secondary";
    btn.textContent = "Ver";
    btn.addEventListener("click", () => onSelectEntry(item));
    actionTd.appendChild(btn);
    tr.appendChild(actionTd);
    tbody.appendChild(tr);
  }
}

export function renderApp(state, onSelectHistory) {
  renderHealth(state);
  renderHistory(state.history, onSelectHistory);

  const chip = document.getElementById("ui-state-pill");
  const emptyEl = document.getElementById("empty-state");
  const loadingEl = document.getElementById("loading-state");
  const successEl = document.getElementById("success-state");
  const errorEl = document.getElementById("error-banner");
  const errorMsg = document.getElementById("error-message");
  const inspectBtn = document.getElementById("btn-inspect");
  const announcer = document.getElementById("sr-announcer");

  if (chip) {
    chip.className = `state-chip state-${state.status}`;
    chip.textContent = state.status.toUpperCase();
  }

  if (inspectBtn) {
    inspectBtn.disabled = !state.selectedFile || state.status === UI_STATES.LOADING;
  }

  emptyEl?.classList.toggle("hidden", state.status !== UI_STATES.IDLE && state.status !== UI_STATES.ERROR);
  loadingEl?.classList.toggle("hidden", state.status !== UI_STATES.LOADING);
  successEl?.classList.toggle("hidden", state.status !== UI_STATES.SUCCESS);
  errorEl?.classList.toggle("hidden", state.status !== UI_STATES.ERROR);

  if (state.status === UI_STATES.ERROR && errorMsg) {
    errorMsg.textContent = state.errorMessage;
  }

  if (state.status === UI_STATES.SUCCESS && state.result) {
    const r = state.result;
    const hitlBadge = document.getElementById("hitl-badge");
    if (hitlBadge) {
      hitlBadge.textContent = r.requires_human_review
        ? "LOW_CONFIDENCE_REVIEW · REVISIÓN HUMANA"
        : "DEFECT_DETECTED · ALTA CONFIANZA";
      hitlBadge.className = `hitl-badge ${r.requires_human_review ? "hitl-review" : "hitl-ok"}`;
    }

    document.getElementById("predicted-label").textContent = r.predicted_label_es;
    document.getElementById("predicted-code").textContent = r.predicted_class;
    document.getElementById("confidence-value").textContent = `${(Number(r.confidence) * 100).toFixed(1)}%`;
    document.getElementById("res-request-id").textContent = r.request_id;
    document.getElementById("res-latency").textContent = `${r.latency_ms} ms`;
    document.getElementById("res-clahe").textContent = r.applied_clahe ? "Activo" : "Desactivado";
    document.getElementById("res-threshold").textContent = Number(r.conf_threshold).toFixed(2);
    document.getElementById("res-roi").textContent = `[${r.roi_bbox.x1}, ${r.roi_bbox.y1}, ${r.roi_bbox.x2}, ${r.roi_bbox.y2}]`;
    document.getElementById("res-transport-label").textContent = r.transport || "HTTP->gRPC";

    const origImg = document.getElementById("img-original");
    if (origImg && state.previewUrl) {
      origImg.src = state.previewUrl;
    }
    const overlayImg = document.getElementById("img-overlay");
    if (overlayImg && r.overlay_png_base64) {
      overlayImg.src = `data:image/png;base64,${r.overlay_png_base64}`;
    }

    renderScoresBars(r.scores || []);
    if (announcer) {
      announcer.textContent = `Inspección completada: ${r.predicted_label_es}, confianza ${(Number(r.confidence) * 100).toFixed(1)}%.`;
    }
  }
}
