import sys
import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app as fastapi_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        path = scope.get("path", "")
        # Vercel rewrites /api/index.py ga yo'naltirganda pathni to'g'rilash
        if path == "/api/index.py" or path == "/api/index":
            # Asl manzilni tekshirish
            # headers dan x-matched-path ni olish
            headers = dict(scope.get("headers", []))
            matched = headers.get(b"x-matched-path", b"").decode("utf-8")
            if matched:
                scope["path"] = matched
            else:
                scope["path"] = "/"
        elif path.startswith("/api/index.py"):
            scope["path"] = path.replace("/api/index.py", "") or "/"

        if scope.get("path") == "/debug":
            body = json.dumps({
                "original_path": path,
                "scope_path": scope.get("path"),
                "headers": {k.decode('latin1', 'ignore'): v.decode('latin1', 'ignore') for k, v in scope.get("headers", [])}
            }).encode("utf-8")
            
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"content-length", str(len(body)).encode("latin1")),
                ],
            })
            await send({
                "type": "http.response.body",
                "body": body,
            })
            return

    await fastapi_app(scope, receive, send)
