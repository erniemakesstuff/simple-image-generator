import multiprocessing
import logging
import sys
import health_service

file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)
app = health_service.app # Flask run initializes server.

if __name__ ==  '__main__':
    app.run(port=5050, debug=True, host='0.0.0.0')
    print("starting")