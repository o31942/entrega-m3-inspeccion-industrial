# Model Card — NEU Steel Surface Defect Inspector (ResNet-18 ONNX)

> **Trazabilidad M3 (Grupo 9 · Omar David Sánchez Jiménez · UAO 2026-2S)**  
> Este documento describe el modelo preentrenado **MaaS (Model as a Service)** cargado en tiempo de ejecución por el servidor gRPC (`protos/defect_inspection.proto`) y registrado en **MLflow Model Registry** (`neu-steel-defect-resnet18`).

---

## 1. Modelo Base (MaaS)

| Campo | Especificación verificada |
| --- | --- |
| **Nombre / Identificador Hub** | `senanurcetin/neu-steel-defect-resnet18` |
| **Revisión fijada (commit SHA)** | `ad13c70618a8a28a50309456dd40d9a45b2869d1` |
| **Autoría original** | `senanurcetin` (Hugging Face Hub & [visual-qc-project](https://github.com/senanurcetin/visual-qc-project)) |
| **Enlace oficial Hugging Face** | https://huggingface.co/senanurcetin/neu-steel-defect-resnet18 |
| **Arquitectura** | ResNet-18 (preentrenada en ImageNet, ajustada sobre NEU-CLS para 6 clases) |
| **Tarea** | Clasificación multiclase de defectos superficiales en acero laminado (`image-classification`) |
| **Formato de pesos y runtime** | `neu_resnet18.onnx` (44.79 MB, FP32) ejecutado sobre **ONNX Runtime CPU** |
| **Tensor de entrada** | `(1, 3, 224, 224)` `float32`, normalizado con `mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]` |
| **Clases soportadas (6)** | `0: crazing`, `1: inclusion`, `2: patches`, `3: pitted_surface`, `4: rolled-in_scale`, `5: scratches` |

---

## 2. Dataset de Origen y Preprocesamiento

* **Dataset base:** **NEU Surface Defect Database (NEU-CLS / NEU-DET)** — K. Song y Y. Yan (*Northeastern University*).
* **Volumen y balanceo:** `1,800` imágenes en escala de grises (`200 × 200 px` nativos), `300` muestras por cada una de las `6` clases de defectos en bandas de acero laminado en caliente.
* **Idioma / Dominio:** Dominio de visión artificial industrial siderúrgica (independiente de idioma textual; etiquetas técnicas en inglés mapeadas al español en la UI de operador).
* **Limitaciones de representatividad del dataset:** Las capturas provienen de recortes de tiras de acero tomadas bajo iluminación halógena controlada de laboratorio. Imágenes consecutivas pueden compartir alta similitud estructural sobre la misma bobina.
* **Preprocesamiento en servicio (`M3`):** Ingesta agnóstica con validación de formato, ecualización adaptativa opcional **CLAHE** (`clipLimit=2.0`, `tileGridSize=(8,8)`), conversión a RGB de 3 canales, redimensionamiento a `224 × 224` y normalización estándar ImageNet.

---

## 3. Métricas de Desempeño y Rendimiento

### 3.1. Métricas reportadas por el modelo base (Hub Model Card / `results.json`)

| Split / Evaluación | Accuracy | Macro F1-Score | Muestras (`n_test`) |
| --- | --- | --- | --- |
| Split aleatorio 80/20 (seed 42) | `1.000` (360/360) | `1.000` | `360` |
| Split por bloques (índices `241–300` retenidos) | `1.000` (360/360) | `1.000` | `360` |
| Latencia de referencia ONNX CPU FP32 (batch=1) | — | — | `47.779 ms` mediana (benchmark publicado del Hub) |

### 3.2. Degradación documentada ante perturbaciones en línea (Hub Model Card)

| Condición degradada en inferencia | Accuracy reportado |
| --- | --- |
| Imagen limpia / iluminación más oscura (`x0.5`) | `1.000` |
| Bajo contraste (`x0.5`) | `0.947 – 0.967` |
| Iluminación excesiva (`x1.6`) | `0.822 – 0.828` |
| Ruido de sensor (`sd=0.05`) / Compresión JPEG Q=15 | `0.678 – 0.808` |
| Mitad / cuarto de resolución | `0.514 – 0.661` |
| Desenfoque fuerte (`radius=3`) / ruido (`sd=0.12`) | `0.344 – 0.386` |

### 3.3. Mediciones del equipo en MLflow (`http://127.0.0.1:5050`)

Las corridas comparables registradas en `scripts/evaluar.py` documentan para nuestra configuración local CPU (`ONNXRuntime CPUExecutionProvider`):
* Calidad multiclase (`accuracy`, `precision_macro`, `recall_macro`, `f1_macro`, `roc_auc_ovr`).
* Desempeño de servicio (`latency_mean_ms`, `latency_p95_ms`, `throughput_img_s`) comparando umbral de confianza y activación de CLAHE.

---

## 4. Limitaciones, Sesgos y Supervisión Humana (HITL)

1. **Saturación del benchmark NEU:** Un `100%` en `NEU-CLS` limpio **no implica generalización garantizada en planta real**. Cambios de iluminación, desenfoque por velocidad de línea o aleaciones distintas (acero inoxidable espejo, aluminio) degradan drásticamente la precisión.
2. **Riesgo de falsos negativos y sesgo de automatización:** Confiar ciegamente en una predicción con baja certeza puede aprobar lotes defectuosos. Por diseño de la capa de servicio (`DefectInspectionService`), toda predicción con probabilidad inferior al umbral configurable (`conf_threshold`, default `0.70`) dispara el estado **`LOW_CONFIDENCE_REVIEW`** para revisión obligatoria por inspector (**Human-in-the-Loop**).
3. **Explicabilidad espacial auxiliar:** ResNet-18 ONNX entrega logits globales de clasificación; el mapa térmico de saliencia (`overlay_png_base64`) y la caja ROI provienen de análisis de gradiente estructural posprocesado como apoyo visual al operario y no constituyen segmentación semántica pixel-a-pixel certificada.
4. **Uso no previsto:** Prohibido utilizar como único sistema de certificación de seguridad estructural aeroespacial/nuclear sin validación metrológica en línea y calibración sobre el acero objetivo.

---

## 5. Licencia y Condiciones de Uso

* **Licencia del modelo MaaS:** **MIT License** (`senanurcetin/neu-steel-defect-resnet18`, verificada en Hub).
* **Licencia del código del repositorio M3:** **MIT License** ([`LICENSE`](../LICENSE)).
* **Condición de atribución y pesos:** Los binarios (`.onnx`) **no** se almacenan en Git; se descargan de manera reproducible desde Hugging Face Hub fijando exactamente `senanurcetin/neu-steel-defect-resnet18@ad13c70618a8a28a50309456dd40d9a45b2869d1` mediante `uv run python scripts/descargar_modelo.py`.
