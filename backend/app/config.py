CLUSTERS_CONFIG = {
    "SQM-B": {
        "name": "Sociedad Química y Minera de Chile",
        "sector": "Minería",
        # FUENTE 1: Variación/Movimiento (Usaremos Yahoo Finance o API de Bolsa)
        "yahoo_ticker": "SQM-B.SN", 
        # FUENTE 2: Análisis de Sentimiento (Sitio oficial de reportes)
        "investor_url": "https://ir.sqm.com/English/financial-results/default.aspx",
        # Palabras clave para validar que encontramos info relevante
        "keywords": ["Earnings", "Resultados", "Quarterly", "Trimestral"]
    },
    "CHILE": {
        "name": "Banco de Chile",
        "sector": "Financiero",
        "yahoo_ticker": "CHILE.SN",
        "investor_url": "https://ww3.bancochile.cl/wps/wcm/connect/investor-relations/home/financial-information/quarterly-results",
        "keywords": ["Financial Report", "Memoria", "Estados Financieros"]
    },
    "CENCOSUD": {
        "name": "Cencosud S.A.",
        "sector": "Retail",
        "yahoo_ticker": "CENCOSUD.SN",
        "investor_url": "https://investors.cencosud.com/English/financial-information/quarterly-results/default.aspx",
        "keywords": ["Resultados", "Earnings Release", "Presentación"]
    },
    "COPEC": {
        "name": "Empresas Copec",
        "sector": "Energía",
        "yahoo_ticker": "COPEC.SN",
        "investor_url": "https://investors.empresascopec.cl/financial-information/results-center",
        "keywords": ["Earnings", "Results", "Memoria Anual"]
    },
    "ENELAM": {
        "name": "Enel Américas",
        "sector": "Utilities",
        "yahoo_ticker": "ENELAM.SN",
        "investor_url": "https://www.enelamericas.com/en/investors/financial_information/newsletter.html",
        "keywords": ["Newsletter", "Report", "Press Release"]
    },
    "LTM": {
        "name": "Latam Airlines Group",
        "sector": "Transporte",
        "yahoo_ticker": "LTM.SN", 
        "investor_url": "https://www.latamairlinesgroup.net/financial-information/quarterly-results",
        "keywords": ["Operational", "Results", "Traffic"]
    }
}