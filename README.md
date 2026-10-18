# Attributing uncertainty in a dike overtopping probability

**Question.** For a given dike, how much of the uncertainty on its annual overtopping probability comes from extreme-rainfall statistics, and how much from the rainfall–runoff model? Is this attribution sensitive to the stationarity assumption?

**Data.** E-OBS daily precipitation; Hub'Eau daily discharge for unregulated catchments in Île-de-France.

**Layout.** `src/` code · `notebooks/` exploration · `report/` notes and report · `data/raw/` downloaded data (not versioned) · `data/processed/` · `tests/`

**Reproduce.**
    conda env create -f environment.yml
    conda activate hydro_env
    python src/download_hubeau.py <station code>
    