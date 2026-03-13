import logging
import os

LOG_DIR = "artifacts/logs" # lets make this exist
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "pipeline.log") # create a logger file for the pipeline in the log directory

logging.basicConfig(
    filemode=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# this allows every module to share the same logger