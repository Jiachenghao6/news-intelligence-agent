import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse
import logging
from sqlalchemy.orm import Session
from .database import Article, get_db, SessionLocal
from .config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self):
        self.headers = {'User-Agent': config.USER_AGENT}
        self.db: Session = SessionLocal()

    def fetch_page(self, url):
        """Fetches a single page and returns the soup object."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def is_new_url(self, url):
        """Checks if the URL already exists in the database."""
        return self.db.query(Article).filter(Article.url == url).first() is None

    def save_article(self, url, title, content):
        """Saves a new article to the database."""
        if not title or not content:
            logger.warning(f"Skipping {url}: Missing title or content")
            return

        try:
            article = Article(
                url=url,
                title=title,
                content=content,
                fetched_at=datetime.utcnow()
            )
            self.db.add(article)
            self.db.commit()
            logger.info(f"Saved article: {title}")
        except Exception as e:
            logger.error(f"Error saving article {url}: {e}")
            self.db.rollback()

    def parse_article(self, url, soup):
        """
        Extracts title and content from a soup object.
        This is a heuristic-based extractor. For specific sites, 
        subclasses or specific rules would be better.
        """
        if not soup:
            return None, None

        # Heuristic for title
        title = None
        if soup.title:
            title = soup.title.string
        if not title:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text(strip=True)
        
        # Heuristic for content (very basic)
        # 1. Look for <article> tag
        article_body = soup.find('article')
        if article_body:
            content = article_body.get_text(separator='\n', strip=True)
        else:
            # 2. Fallback: find the div with the most p tags
            paragraphs = soup.find_all('p')
            content = "\n".join([p.get_text(strip=True) for p in paragraphs])
            
        return title, content

    def get_links(self, url, soup):
        """Extracts relevant article links from the page."""
        links = set()
        if not soup:
            return links
            
        domain = urlparse(url).netloc
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            parsed_url = urlparse(full_url)
            
            # Basic filtering: must be same domain
            if parsed_url.netloc == domain:
                # Heuristic: Article URLs often have dates or specific paths
                # For now, we'll just avoid obviously non-article links
                if any(x in full_url for x in ['/xwdt/', '/gzdt/', '/art/', 'content', 'detail']):
                     links.add(full_url)
                # Fallback for government sites: they often use /xxgk/ or similar. 
                # Let's be permissive for the provided sites but avoid root/index
                elif len(parsed_url.path) > 10 and not parsed_url.path.endswith(('index.html', 'index.htm', '/')):
                    links.add(full_url)
                    
        return links

    def crawl_site(self, seed_url):
        """Crawls the seed URL for links and processes them."""
        logger.info(f"Crawling seed: {seed_url}")
        soup = self.fetch_page(seed_url)
        if not soup:
            return

        links = self.get_links(seed_url, soup)
        logger.info(f"Found {len(links)} potential links on {seed_url}")
        
        count = 0
        for link in links:
            if count >= 5: # Limit to 5 articles per run for testing
                break
            if self.is_new_url(link):
                self.process_url(link)
                count += 1

    def process_url(self, url):
        """Main entry point to process a single article URL."""
        if not self.is_new_url(url):
            logger.info(f"URL already exists: {url}")
            return

        logger.info(f"Processing: {url}")
        soup = self.fetch_page(url)
        if soup:
            title, content = self.parse_article(url, soup)
            # Only save if it looks like a real article (has substantial content)
            if title and content and len(content) > 100:
                self.save_article(url, title, content)
            else:
                logger.info(f"Skipped {url}: Content too short or no title")

    def close(self):
        self.db.close()

if __name__ == "__main__":
    # Test run
    crawler = Crawler()
    test_url = "https://www.ndrc.gov.cn/xwdt/" # News section of NDRC
    crawler.crawl_site(test_url)
    crawler.close()
