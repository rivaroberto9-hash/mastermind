"""Web app Mastermind (Flask).

Il codice segreto non lascia mai il server in chiaro: viaggia nel browser dentro un
token cifrato (Fernet), quindi il server resta senza stato e funziona anche con più
istanze. Il codice viene rivelato solo a partita finita.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os

from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, jsonify, request, send_from_directory

from game import Config, gen_code, score, valid_guess

app = Flask(__name__, static_folder="static", static_url_path="/static")

# In produzione impostare SECRET_KEY: senza, ogni riavvio invalida le partite in corso.
_secret = os.environ.get("SECRET_KEY") or os.urandom(32).hex()
_fernet = Fernet(base64.urlsafe_b64encode(hashlib.sha256(_secret.encode()).digest()))
TOKEN_TTL = 60 * 60 * 24  # una partita non finita scade dopo 24 ore


def seal(cfg: Config, code: list[int], used: int) -> str:
    payload = json.dumps({"c": cfg.to_dict(), "code": code, "n": used}).encode()
    return _fernet.encrypt(payload).decode()


def unseal(token) -> tuple[Config, list[int], int] | None:
    if not isinstance(token, str):
        return None
    try:
        d = json.loads(_fernet.decrypt(token.encode(), ttl=TOKEN_TTL))
        return Config.from_dict(d["c"]), d["code"], d["n"]
    except (InvalidToken, ValueError, KeyError, TypeError):
        return None


def err(msg: str, status: int = 400):
    return jsonify(error=msg), status


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/healthz")
def healthz():
    return "ok"


@app.post("/api/new")
def api_new():
    cfg = Config.from_dict(request.get_json(silent=True))
    return jsonify(token=seal(cfg, gen_code(cfg), 0))


@app.post("/api/guess")
def api_guess():
    data = request.get_json(silent=True) or {}
    opened = unseal(data.get("token"))
    if opened is None:
        return err("partita non valida o scaduta", 410)
    cfg, code, used = opened
    guess = data.get("guess")
    if not valid_guess(cfg, guess):
        return err("combinazione non valida")
    if used >= cfg.tries:
        return err("tentativi esauriti", 409)

    full, part = score(code, guess)
    used += 1
    won = full == cfg.length
    over = won or used >= cfg.tries
    out = {"full": full, "part": part, "won": won, "over": over, "n": used}
    if over:
        out["code"] = code
    else:
        out["token"] = seal(cfg, code, used)
    return jsonify(out)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=False)
