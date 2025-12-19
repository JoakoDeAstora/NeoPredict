import requests
from bs4 import BeautifulSoup
import pdfplumber
import io
import os

class CmfScraperService:
    def __init__(self, download_dir: str = "temp_pdfs"):
        self.base_url = "https://www.cmfchile.cl"
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)

    def visit_investor_site(self, company_name: str, url: str) -> str:
        """
        [Phase 1: Step 2 & 3] Visits the site, verifies links, and extracts content.
        This represents the 'Robot' logic.
        """
        print(f"[ROBOT] Visiting {company_name} at {url}...")
        try:
            # 1. Download Source
            headers = {"User-Agent": "NeoPredictBot/1.0"}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"[ROBOT] Failed to access {url} (Status: {response.status_code})")
                return ""
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 2. Extract Links (Reports/News)
            # Heuristic: Look for 'href' containing keywords like 'pdf', 'report', 'memoria'
            valid_content = ""
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                
                # Check relevance in Link Text (Phase 1, Step 3: Verificación de Contenido - Basic)
                keywords = ["Report", "Annual", "Memoria", "Results", "Resultados", "Trimestral"]
                if not any(k.lower() in text.lower() for k in keywords):
                    continue
                    
                full_url = href if href.startswith('http') else os.path.join(url, href)
                
                # Phase 1, Step 3: Verificación de Existencia (HEAD Request)
                if self.verify_link_existence(full_url):
                    print(f"  [ROBOT] Valid Verified Link Found: {text} -> {full_url}")
                    # Phase 1, Step 4: Limpieza/Extraction (Mocking content extraction from listing)
                    valid_content += f"{text}: {full_url}\n"
            
            return valid_content

        except Exception as e:
            print(f"[ROBOT] Error visiting {url}: {e}")
            return ""

    def verify_link_existence(self, url: str) -> bool:
        """
        Phase 1, Step 3: Sends a HEAD request to verify link exists without downloading.
        """
        try:
            head_resp = requests.head(url, timeout=5, allow_redirects=True, headers={"User-Agent": "NeoPredictBot/1.0"})
            return head_resp.status_code < 400
        except:
            return False

    def clean_text(self, text: str) -> str:
        """
        Phase 1, Step 4: Basic cleaning.
        """
        return " ".join([line.strip() for line in text.split('\n') if line.strip()])
