"""Logica del Mastermind: generazione del codice e calcolo dei suggerimenti."""
from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass

# Valori ammessi dalle impostazioni (identici alla versione originale)
LENGTHS = (4, 5)
COLORS = (6, 8)
TRIES = (8, 10, 12)


@dataclass(frozen=True)
class Config:
    length: int = 4
    colors: int = 6
    tries: int = 10
    dup: bool = True

    @classmethod
    def from_dict(cls, d: dict | None) -> "Config":
        """Costruisce una configurazione valida; i valori non ammessi tornano al default."""
        d = d or {}
        base = cls()

        def pick(key, allowed, default):
            v = d.get(key)
            return v if isinstance(v, int) and not isinstance(v, bool) and v in allowed else default

        return cls(
            length=pick("len", LENGTHS, base.length),
            colors=pick("colors", COLORS, base.colors),
            tries=pick("tries", TRIES, base.tries),
            dup=d.get("dup") is not False,
        )

    def to_dict(self) -> dict:
        return {"len": self.length, "colors": self.colors, "tries": self.tries, "dup": self.dup}


def gen_code(cfg: Config, rng: random.Random | None = None) -> list[int]:
    """Codice segreto: numeri da 1 a `colors`; senza ripetizioni se cfg.dup è False."""
    rng = rng or random.SystemRandom()
    if cfg.dup:
        return [rng.randint(1, cfg.colors) for _ in range(cfg.length)]
    return rng.sample(range(1, cfg.colors + 1), cfg.length)


def score(code: list[int], guess: list[int]) -> tuple[int, int]:
    """Restituisce (pezzi al posto giusto, pezzi giusti al posto sbagliato)."""
    full = sum(c == g for c, g in zip(code, guess))
    rest_code = Counter(c for c, g in zip(code, guess) if c != g)
    rest_guess = Counter(g for c, g in zip(code, guess) if c != g)
    part = sum(min(n, rest_code[k]) for k, n in rest_guess.items())
    return full, part


def valid_guess(cfg: Config, guess) -> bool:
    return (
        isinstance(guess, list)
        and len(guess) == cfg.length
        and all(isinstance(x, int) and not isinstance(x, bool) and 1 <= x <= cfg.colors for x in guess)
    )
