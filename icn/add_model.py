#!/usr/bin/python

import getopt
import sys

from icn_lib import ModelDB

def main(argv):

  inputfile = ''

  try:
    opts, args = getopt.getopt(argv,"hf:",["ifile="])
  
  except getopt.GetoptError:
    print('add_model.py -f <inputfile>')
    sys.exit(2)
 
  for opt, arg in opts:
    
    if opt == '-h':
      
      print('usage: python add_model.py -f <inputfile>')
      sys.exit()

    elif opt in ("-f"):
      
      inputfile = arg

      # DB access
      db = ModelDB('mongodb://localhost:27017', 'models', '/flowers')
      db.configure_database_fs()

      # save to DB
      with io.FileIO(inputfile, 'r') as f:
        db.put_model(inputfile, f)
        print('Model saved to MongoDB')

      sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])