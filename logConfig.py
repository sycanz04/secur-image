import logging

# Create log file if it doesn't exist
path = 'securImage.log'
with open (path, 'a') as  file:
    pass

# Log config
logging.basicConfig(
    filename='securImage.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(funcName)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create a function to get logger
def getLogger(name):
    return logging.getLogger(name)
