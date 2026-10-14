import urllib.parse
import ipaddress
import socket
from bs4 import BeautifulSoup

class SafeWebCrawler:
    """
    Second Syllabus Unit V: Web Retrieval and Crawling.
    Safe, local-first crawler designed to respect:
    1. SSRF Prevention (blocks localhost, 127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, link-local, cloud metadata 169.254.169.254).
    2. Strict domain allowlist.
    3. Crawl depth and page limits.
    4. Local HTML file parsing fallback for offline execution.
    """
    
    ALLOWED_DOMAINS = {"example.com", "python.org", "en.wikipedia.org"}
    MAX_PAGES = 5
    MAX_DEPTH = 2
    
    @staticmethod
    def is_safe_url(url: str, allowed_domains: set = None) -> bool:
        """Validates that URL is well-formed, uses http/https, and does not target internal IP spaces."""
        if allowed_domains is None:
            allowed_domains = SafeWebCrawler.ALLOWED_DOMAINS
            
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
            
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # Check domain allowlist
        if not any(hostname == d or hostname.endswith("." + d) for d in allowed_domains):
            return False
            
        # SSRF checks: resolve hostname and ensure not private/loopback/link-local
        try:
            ip_str = socket.gethostbyname(hostname)
            ip = ipaddress.ip_address(ip_str)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                return False
        except Exception:
            return False
            
        return True

    @staticmethod
    def parse_local_html(html_content: str, source_url: str = "local_file") -> dict:
        """Parses local or safe HTML using BeautifulSoup4 to extract title, text, and outgoing links."""
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove script and style elements
        for element in soup(["script", "style", "noscript"]):
            element.decompose()
            
        title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled Document"
        text = soup.get_text(separator=" ", strip=True)
        
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http") or href.startswith("/"):
                links.append(href)
                
        return {
            "source": source_url,
            "title": title,
            "text": text,
            "links": links[:10],
            "word_count": len(text.split())
        }
