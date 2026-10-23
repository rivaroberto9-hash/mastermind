# Mastermind (Python / Flask)

- `game.py`  logica: codice segreto e suggerimenti
- `app.py`   web app Flask con API `/api/new` e `/api/guess`
- `static/index.html`  interfaccia (IT/EN, 4-5 pezzi, 6-8 forme, tentativi, ripetizioni)
- `tests/`   test (`pip install pytest` poi `pytest`)

Il codice segreto resta sul server: il browser riceve solo un token cifrato e
vede il codice a partita finita. Le statistiche sono salvate nel browser.

## Provarlo sul PC
Doppio clic su `avvia.bat` (apre http://localhost:8080).

## Pubblicarlo online
Firebase Hosting serve solo file statici, quindi per un'app Python serve un host con
container. Il piu semplice e gratuito per iniziare e Render:

1. Metti questa cartella su un repository GitHub.
2. render.com > New > Web Service > scegli il repository, Runtime: Docker.
3. Environment: aggiungi `SECRET_KEY` con una stringa lunga casuale.
4. Deploy: ottieni un indirizzo `https://...onrender.com`.

Alternative con lo stesso Dockerfile: Fly.io (`fly launch`) oppure Google Cloud Run
(`gcloud run deploy --source .`, utile se vuoi restare nel progetto Google di Firebase).

Senza `SECRET_KEY` ogni riavvio del server invalida le partite in corso.
