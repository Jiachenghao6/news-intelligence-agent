import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    is_high_value = Column(Boolean, default=False)
    
    # Analysis results
    summary = Column(Text, nullable=True)
    analysis_report = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Article(title='{self.title}', url='{self.url}')>"

class Source(Base):
    __tablename__ = 'sources'
    
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

class Settings(Base):
    __tablename__ = 'settings'
    
    key = Column(String, primary_key=True)
    value = Column(Text, nullable=True)

# Database Setup
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'info_system.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database tables."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at {DB_PATH}")

def get_db():
    """Dependency for getting DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_setting(key: str, default_value: str = ""):
    """Gets a setting value."""
    db = SessionLocal()
    try:
        setting = db.query(Settings).filter(Settings.key == key).first()
        return setting.value if setting else default_value
    finally:
        db.close()

def set_setting(key: str, value: str):
    """Sets a setting value."""
    db = SessionLocal()
    try:
        setting = db.query(Settings).filter(Settings.key == key).first()
        if setting:
            setting.value = value
        else:
            setting = Settings(key=key, value=value)
            db.add(setting)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error setting value: {e}")
        return False
    finally:
        db.close()

def delete_article(article_id: int):
    """Deletes an article by ID."""
    db = SessionLocal()
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        if article:
            db.delete(article)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"Error deleting article: {e}")
        return False
    finally:
        db.close()

def add_source(url: str):
    """Adds a new source URL."""
    db = SessionLocal()
    try:
        if db.query(Source).filter(Source.url == url).first():
            return False # Already exists
        source = Source(url=url)
        db.add(source)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error adding source: {e}")
        return False
    finally:
        db.close()

def delete_source(source_id: int):
    """Deletes a source by ID."""
    db = SessionLocal()
    try:
        source = db.query(Source).filter(Source.id == source_id).first()
        if source:
            db.delete(source)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"Error deleting source: {e}")
        return False
    finally:
        db.close()

def get_sources():
    """Returns all sources."""
    db = SessionLocal()
    try:
        return db.query(Source).all()
    finally:
        db.close()

def get_all_articles():
    """Returns all articles for developer view."""
    db = SessionLocal()
    try:
        return db.query(Article).order_by(Article.id.desc()).all()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
