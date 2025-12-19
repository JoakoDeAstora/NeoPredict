
from enum import Enum
from typing import Dict, List

class ClusterType(Enum):
    DOMESTIC = "Domestico"
    COMMODITIES = "Commodities"
    IDIOSINCRATIC = "Idiosincratico"

class TickerConfig:
    def __init__(self, cluster: ClusterType, drivers: List[str], sentiment_keywords: Dict[str, str], investor_url: str):
        self.cluster = cluster
        self.drivers = drivers
        self.sentiment_keywords = sentiment_keywords
        self.investor_url = investor_url

CLUSTERS_CONFIG: Dict[str, TickerConfig] = {
    # Cluster 1: Ciclo Doméstico
    "CHILE": TickerConfig(
        cluster=ClusterType.DOMESTIC,
        drivers=["TPM", "Inflation_UF"],
        sentiment_keywords={
            "TPM": "negative_if_high", 
            "Recorte de Tasa": "positive",
            "Mora": "negative"
        },
        investor_url="https://portales.bancochile.cl/relacion-con-inversionistas"
    ),
    "ENELAM": TickerConfig(
        cluster=ClusterType.DOMESTIC,
        drivers=["Hydrology", "Regulation", "FX"],
        sentiment_keywords={
            "Hidrología": "positive",
            "Lluvia": "positive",
            "Sequía": "negative",
            "Subsidio Eléctrico": "negative"
        },
        investor_url="https://www.enelamericas.com/en/investors.html"
    ),
    "CENCOSUD": TickerConfig(
        cluster=ClusterType.DOMESTIC,
        drivers=["Consumption", "IAS29_Filtered"],
        sentiment_keywords={
            "Same Store Sales": "positive",
            "IPO": "positive",
            "Consumo Discrecional": "positive"
        },
        investor_url="https://www.cencosud.com/en/investors"
    ),

    # Cluster 2: Commodities
    "SQM-B": TickerConfig(
        cluster=ClusterType.COMMODITIES,
        drivers=["Lithium_Price", "China_Demand"],
        sentiment_keywords={
            "China": "positive",
            "Demanda": "positive",
            "Royalty": "negative",
            "Corfo": "negative"
        },
        investor_url="https://www.sqm.com/en/inversionistas/"
    ),
    "COPEC": TickerConfig(
        cluster=ClusterType.COMMODITIES,
        drivers=["Energy", "Forestry", "Inhibition_Neuron"], 
        sentiment_keywords={
            "Celulosa": "neutral", 
            "Pulp Prices": "neutral",
            "Sucuriú": "positive"
        },
        investor_url="https://investor.empresascopec.cl/"
    ),

    # Cluster 3: Idiosincratic
    "LTM": TickerConfig(
        cluster=ClusterType.IDIOSINCRATIC,
        drivers=["JetFuel_Price", "Traffic_ASK"],
        sentiment_keywords={
            "Jet Fuel": "negative",
            "Chapter 11": "positive", 
            "ASK": "positive"
        },
        investor_url="https://www.latamairlinesgroup.net/"
    ),
}
