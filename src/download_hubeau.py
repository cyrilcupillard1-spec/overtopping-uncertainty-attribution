"""Télécharge les débits moyens journaliers (QmJ) d'une station ou d'un site Hub'Eau.

Usage (depuis la racine du dépôt) :
    python src/download_hubeau.py H0203020 --debut 1970-01-01 --fin 2025-12-31

Écrit data/raw/hubeau_<code>_QmJ.csv (data/raw/ n'est pas versionné : le script suffit
à reproduire les données). Vérifier l'unité sur les premières valeurs : Hub'Eau renvoie
en principe les débits en l/s.
"""
import argparse
import time
from pathlib import Path

import pandas as pd
import requests

BASE = "https://hubeau.eaufrance.fr/api/v1/hydrometrie/obs_elab"  # si 404 : vérifier la version sur hubeau.eaufrance.fr


def fetch(code, debut, fin, taille=20000):
    """Toutes les observations élaborées QmJ entre deux dates, par tranches de 20 ans."""
    lignes = []
    d0, dfin = pd.Timestamp(debut), pd.Timestamp(fin)
    while d0 <= dfin:
        d1 = min(d0 + pd.DateOffset(years=20) - pd.Timedelta(days=1), dfin)
        url, params = BASE, {
            "code_entite": code,
            "grandeur_hydro_elab": "QmJ",
            "date_debut_obs_elab": d0.strftime("%Y-%m-%d"),
            "date_fin_obs_elab": d1.strftime("%Y-%m-%d"),
            "size": taille,
        }
        while url:  # suit les pages suivantes s'il y en a
            r = requests.get(url, params=params, timeout=60)
            r.raise_for_status()
            js = r.json()
            lignes += js.get("data", [])
            url, params = js.get("next"), None
            time.sleep(0.3)
        d0 = d1 + pd.Timedelta(days=1)
    return pd.DataFrame(lignes)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("code", help="code du site (8 caractères) ou de la station (10 caractères)")
    p.add_argument("--debut", default="1950-01-01")
    p.add_argument("--fin", default=pd.Timestamp.today().strftime("%Y-%m-%d"))
    a = p.parse_args()

    df = fetch(a.code, a.debut, a.fin)
    if df.empty:
        raise SystemExit(f"Aucune donnée pour {a.code} : vérifier le code et la période.")
    df["date"] = pd.to_datetime(df["date_obs_elab"])
    df = df.sort_values("date").drop_duplicates("date")

    out = Path("data/raw") / f"hubeau_{a.code}_QmJ.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

    jours = (df["date"].max() - df["date"].min()).days + 1
    print(f"{out} : {len(df)} jours de {df['date'].min():%Y-%m-%d} à {df['date'].max():%Y-%m-%d}, "
          f"{100 * (1 - len(df) / jours):.1f} % de jours manquants")
    print(df[["date", "resultat_obs_elab"]].describe(include="all").loc[["min", "max", "mean"]])


if __name__ == "__main__":
    main()