import getopt
import io
import sys

import icn_lib.logger
from icn_lib.model_db_service import ModelDB

def main(argv):

  inputfile = ''

  try:
    opts, args = getopt.getopt(argv,"hf:",["ifile="])
  
  except getopt.GetoptError:
    logger.error('Usage error. Should be: add_model.py -f <inputfile>')
    sys.exit(2)
 
  for opt, arg in opts:
    
    if opt == '-h':
      
      logger.info('usage: python add_model.py -f <inputfile>')
      sys.exit()

    elif opt in ("-f"):
      
      inputfile = arg

      # DB access
      db = ModelDB('mongodb://localhost:27017', 'models', '/flowers')
      db.configure_database_fs()

      # save to DB
      with io.FileIO(inputfile, 'r') as f:
        db.put_model(inputfile, f)
        logger.debug('Model saved to MongoDB')

      sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
