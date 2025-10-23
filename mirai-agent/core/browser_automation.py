"""
Browser Automation with CDP (Chrome DevTools Protocol)
Lightweight browser automation without Playwright overhead
"""

import json
import logging
import subprocess
import time
from typing import Any, Dict, List, Optional
from urllib.parse import quote

logger = logging.getLogger(__name__)


class BrowserAutomation:
    """
    Browser automation using Chrome/Chromium with CDP
    
    Features:
    - Navigate to URLs
    - Execute JavaScript
    - Extract page content
    - Take screenshots
    - Handle downloads
    """

    def __init__(
        self,
        headless: bool = True,
        timeout: int = 30,
        user_agent: Optional[str] = None,
    ):
        """
        Initialize browser automation

        Args:
            headless: Run in headless mode
            timeout: Default timeout for operations
            user_agent: Custom user agent
        """
        self.headless = headless
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        self.chrome_available = self._check_chrome()
        
        # Stats
        self.stats = {
            "pages_visited": 0,
            "scripts_executed": 0,
            "errors": 0,
        }

    def _check_chrome(self) -> bool:
        """Check if Chrome/Chromium is available"""
        try:
            result = subprocess.run(
                ["which", "chromium-browser"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                logger.info("✅ Chromium found")
                return True

            result = subprocess.run(
                ["which", "google-chrome"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                logger.info("✅ Chrome found")
                return True

            logger.warning("⚠️ Chrome/Chromium not found")
            return False

        except Exception as e:
            logger.warning(f"⚠️ Chrome check failed: {e}")
            return False

    def fetch_url(self, url: str, wait_time: int = 2) -> Optional[str]:
        """
        Fetch URL and return page content

        Args:
            url: URL to fetch
            wait_time: Time to wait for page load (seconds)

        Returns:
            Page HTML content or None if failed
        """
        if not self.chrome_available:
            logger.error("Chrome/Chromium not available")
            return None

        self.stats["pages_visited"] += 1

        try:
            # Use Chrome in headless mode with --dump-dom
            cmd = [
                "chromium-browser" if self._check_chromium() else "google-chrome",
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                f"--user-agent={self.user_agent}",
                "--dump-dom",
                url,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=self.timeout,
                text=True,
            )

            if result.returncode == 0:
                return result.stdout
            else:
                logger.error(f"Chrome returned error: {result.stderr}")
                self.stats["errors"] += 1
                return None

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout fetching {url}")
            self.stats["errors"] += 1
            return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            self.stats["errors"] += 1
            return None

    def _check_chromium(self) -> bool:
        """Check if chromium-browser command exists"""
        try:
            result = subprocess.run(
                ["which", "chromium-browser"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except:
            return False

    def screenshot(self, url: str, output_path: str) -> bool:
        """
        Take screenshot of URL

        Args:
            url: URL to screenshot
            output_path: Path to save screenshot

        Returns:
            True if successful
        """
        if not self.chrome_available:
            logger.error("Chrome/Chromium not available")
            return False

        try:
            cmd = [
                "chromium-browser" if self._check_chromium() else "google-chrome",
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                f"--user-agent={self.user_agent}",
                "--screenshot=" + output_path,
                "--window-size=1920,1080",
                url,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=self.timeout,
            )

            if result.returncode == 0:
                logger.info(f"📸 Screenshot saved: {output_path}")
                return True
            else:
                logger.error(f"Screenshot failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return False

    def get_page_text(self, url: str) -> Optional[str]:
        """
        Get text content from page (without HTML tags)

        Args:
            url: URL to fetch

        Returns:
            Page text or None
        """
        html = self.fetch_url(url)
        if not html:
            return None

        # Extract text from HTML
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

            return text

        except ImportError:
            logger.warning("BeautifulSoup not available, returning raw HTML")
            return html
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None

    def get_links(self, url: str) -> List[str]:
        """
        Extract all links from page

        Args:
            url: URL to fetch

        Returns:
            List of URLs found on page
        """
        html = self.fetch_url(url)
        if not html:
            return []

        try:
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin

            soup = BeautifulSoup(html, "html.parser")
            links = []

            for link in soup.find_all("a", href=True):
                href = link["href"]
                absolute_url = urljoin(url, href)
                links.append(absolute_url)

            return links

        except ImportError:
            logger.warning("BeautifulSoup not available")
            return []
        except Exception as e:
            logger.error(f"Error extracting links: {e}")
            return []

    def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """
        Search Google and return results

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of dicts with 'title', 'url', 'snippet'
        """
        # Simple Google search using URL
        search_url = f"https://www.google.com/search?q={quote(query)}&num={num_results}"
        
        html = self.fetch_url(search_url)
        if not html:
            return []

        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html, "html.parser")
            results = []

            # Parse search results (this is fragile and may need updates)
            for g in soup.find_all("div", class_="g")[:num_results]:
                try:
                    title_elem = g.find("h3")
                    title = title_elem.get_text() if title_elem else ""

                    link_elem = g.find("a")
                    url = link_elem["href"] if link_elem and "href" in link_elem.attrs else ""

                    snippet_elem = g.find("div", class_="VwiC3b")
                    snippet = snippet_elem.get_text() if snippet_elem else ""

                    if title and url:
                        results.append({
                            "title": title,
                            "url": url,
                            "snippet": snippet,
                        })
                except Exception as e:
                    logger.debug(f"Error parsing search result: {e}")
                    continue

            return results

        except ImportError:
            logger.warning("BeautifulSoup not available")
            return []
        except Exception as e:
            logger.error(f"Error parsing search results: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get browser automation statistics"""
        return self.stats


class PDFParser:
    """Simple PDF parser"""

    @staticmethod
    def extract_text(pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text or None
        """
        try:
            import pypdf

            with open(pdf_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text

        except ImportError:
            logger.warning("pypdf not available")
            return None
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return None


class HTMLParser:
    """Simple HTML parser"""

    @staticmethod
    def extract_text(html: str) -> Optional[str]:
        """
        Extract text from HTML

        Args:
            html: HTML content

        Returns:
            Extracted text or None
        """
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

            return text

        except ImportError:
            logger.warning("BeautifulSoup not available")
            return None
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None


if __name__ == "__main__":
    # Test browser automation
    print("🧪 Testing Browser Automation...")

    browser = BrowserAutomation()

    if browser.chrome_available:
        print("\n1. Testing URL fetch:")
        content = browser.fetch_url("https://example.com")
        if content:
            print(f"   ✅ Fetched {len(content)} chars")

        print("\n2. Testing text extraction:")
        text = browser.get_page_text("https://example.com")
        if text:
            print(f"   ✅ Extracted {len(text)} chars")
            print(f"   Preview: {text[:200]}...")

        print(f"\n✅ Stats: {browser.get_stats()}")
    else:
        print("⚠️ Chrome/Chromium not available, skipping tests")
