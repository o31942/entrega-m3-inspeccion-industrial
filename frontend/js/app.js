/** Bootstrap inicial de cliente desacoplado enlazado con Gateway HTTP->gRPC. */

import { checkHealth, fetchModelInfo } from "./api.js";
import { createStore } from "./state.js";

const store = createStore();

export async function initTelemetry() {
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

void initTelemetry();
