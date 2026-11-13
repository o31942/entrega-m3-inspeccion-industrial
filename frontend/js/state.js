/** Máquina de estados explícita para el cliente desacoplado SteelSight M3. */

export const UI_STATES = Object.freeze({
  IDLE: "idle",
  LOADING: "loading",
  SUCCESS: "success",
  ERROR: "error",
});

export function createStore() {
  let state = {
    status: UI_STATES.IDLE,
    gatewayUrl: "http://127.0.0.1:8000",
    health: null,
    modelInfo: null,
    selectedFile: null,
    previewUrl: null,
    confThreshold: 0.70,
    applyClahe: true,
    result: null,
    errorMessage: "",
    history: [],
  };

  const listeners = new Set();

  function getState() {
    return { ...state, history: [...state.history] };
  }

  function subscribe(listener) {
    listeners.add(listener);
    listener(getState());
    return () => listeners.delete(listener);
  }

  function patch(partial) {
    state = { ...state, ...partial };
    const snap = getState();
    for (const fn of listeners) {
      fn(snap);
    }
    return snap;
  }

  function setLoading() {
    return patch({ status: UI_STATES.LOADING, errorMessage: "" });
  }

  function setSuccess(result) {
    const entry = {
      id: result.request_id,
      timestamp: new Date().toLocaleTimeString(),
      filename: state.selectedFile ? state.selectedFile.name : "muestra.png",
      result,
      previewUrl: state.previewUrl,
    };
    const nextHistory = [entry, ...state.history].slice(0, 8);
    return patch({
      status: UI_STATES.SUCCESS,
      result,
      errorMessage: "",
      history: nextHistory,
    });
  }

  function setError(message) {
    return patch({
      status: UI_STATES.ERROR,
      errorMessage: message || "Error inesperado comunicando con el backend.",
    });
  }

  function reset() {
    return patch({
      status: UI_STATES.IDLE,
      selectedFile: null,
      result: null,
      errorMessage: "",
    });
  }

  return {
    getState,
    subscribe,
    patch,
    setLoading,
    setSuccess,
    setError,
    reset,
  };
}
