"""Servidor estático desacoplado con MIME ES Modules correcto en Windows (:5173)."""

from __future__ import annotations

import argparse
import functools
import http.server
import mimetypes
from pathlib import Path

mimetypes.add_type("text/javascript; charset=utf-8", ".js")
mimetypes.add_type("text/css; charset=utf-8", ".css")
mimetypes.add_type("text/html; charset=utf-8", ".html")


class ModuleSafeHandler(http.server.SimpleHTTPRequestHandler):
    """Handler HTTP que garantiza Content-Type correcto para .js ES Modules."""

    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".html": "text/html; charset=utf-8",
    }


def serve_frontend(host: str = "127.0.0.1", port: int = 5173) -> None:
    """Inicia servidor estático apuntando al directorio frontend/."""
    root = Path(__file__).resolve().parent.parent / "frontend"
    handler = functools.partial(ModuleSafeHandler, directory=str(root))
    with http.server.ThreadingHTTPServer((host, port), handler) as httpd:
        print(
            f"Frontend desacoplado activo en http://{host}:{port} (dir={root})",
            flush=True,
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor frontend desacoplado M3")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5173)
    args = parser.parse_args()
    serve_frontend(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
