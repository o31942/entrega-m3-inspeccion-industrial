/** Generador determinista en Canvas 2D de texturas metálicas tipo NEU-DET. */

function seededNoise(seed) {
  let s = seed >>> 0;
  return () => {
    s = (1664525 * s + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

export async function createSyntheticDefectFile(kind) {
  const size = 200;
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");

  const rng = seededNoise(kind.length * 919 + 42);
  ctx.fillStyle = "#6e747d";
  ctx.fillRect(0, 0, size, size);

  // Grano metálico laminado
  for (let i = 0; i < 1400; i += 1) {
    const v = Math.floor(85 + rng() * 65);
    ctx.fillStyle = `rgb(${v},${v},${v})`;
    ctx.fillRect(Math.floor(rng() * size), Math.floor(rng() * size), 2, 1);
  }

  if (kind === "scratches") {
    ctx.strokeStyle = "#f1f5f9";
    ctx.lineWidth = 3;
    for (let k = 0; k < 4; k += 1) {
      ctx.beginPath();
      const y = 35 + k * 34;
      ctx.moveTo(15, y);
      ctx.lineTo(185, y + (rng() - 0.5) * 18);
      ctx.stroke();
    }
  } else if (kind === "patches") {
    for (let k = 0; k < 5; k += 1) {
      ctx.fillStyle = k % 2 === 0 ? "rgba(30,30,30,0.75)" : "rgba(215,215,215,0.45)";
      ctx.beginPath();
      ctx.ellipse(
        40 + rng() * 120,
        40 + rng() * 120,
        24 + rng() * 18,
        14 + rng() * 12,
        rng(),
        0,
        Math.PI * 2
      );
      ctx.fill();
    }
  } else if (kind === "pitted_surface") {
    ctx.fillStyle = "#111827";
    for (let k = 0; k < 42; k += 1) {
      ctx.beginPath();
      ctx.arc(18 + rng() * 164, 18 + rng() * 164, 2 + rng() * 4.5, 0, Math.PI * 2);
      ctx.fill();
    }
  } else if (kind === "inclusion") {
    ctx.fillStyle = "#18181b";
    ctx.fillRect(88, 30, 14, 130);
    ctx.fillStyle = "#d4d4d8";
    ctx.fillRect(92, 42, 4, 110);
  } else if (kind === "crazing") {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 1.6;
    for (let k = 0; k < 18; k += 1) {
      ctx.beginPath();
      let x = 20 + rng() * 160;
      let y = 20 + rng() * 160;
      ctx.moveTo(x, y);
      for (let seg = 0; seg < 4; seg += 1) {
        x += (rng() - 0.5) * 35;
        y += (rng() - 0.5) * 35;
        ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
  } else {
    // rolled-in_scale
    for (let k = 0; k < 9; k += 1) {
      ctx.fillStyle = "rgba(25,25,28,0.82)";
      ctx.beginPath();
      ctx.ellipse(25 + rng() * 150, 25 + rng() * 150, 16, 6, 0.25, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (!blob) {
        reject(new Error("No se pudo generar la muestra Canvas."));
        return;
      }
      resolve(new File([blob], `sample_${kind}.png`, { type: "image/png" }));
    }, "image/png");
  });
}
