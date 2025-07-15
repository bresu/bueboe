from sqlmodel import create_engine, Session
from app.core.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Initializing database connection with URL type: {settings.db_url.split('://')[0]}")
engine = create_engine(settings.db_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session