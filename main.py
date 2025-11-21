import time
import logging
import argparse
from apscheduler.schedulers.background import BackgroundScheduler
from src.crawler import Crawler
from src.processor import Processor
from src.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline(urls):
    logger.info("Starting pipeline run...")
    
    # 1. Crawl
    crawler = Crawler()
    for url in urls:
        crawler.crawl_site(url)
    crawler.close()
    
    # 2. Process & Analyze
    processor = Processor()
    processor.process_pending_articles()
    processor.close()
    
    logger.info("Pipeline run complete.")

def main():
    parser = argparse.ArgumentParser(description="Information Processing System")
    parser.add_argument("--urls", nargs="+", help="List of URLs to crawl", default=["https://news.ycombinator.com"]) # Default example
    parser.add_argument("--loop", action="store_true", help="Run in a loop (every hour)")
    
    args = parser.parse_args()
    
    if args.loop:
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_pipeline, 'interval', hours=1, args=[args.urls])
        scheduler.start()
        logger.info("Scheduler started. Press Ctrl+C to exit.")
        try:
            # Run once immediately
            run_pipeline(args.urls)
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            scheduler.shutdown()
    else:
        run_pipeline(args.urls)

if __name__ == "__main__":
    main()
