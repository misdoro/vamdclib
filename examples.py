from nodes import *
from database import *

nl=Nodelist()

for node in nl:
   print "ivoaid"+node.identifier+" nn"+node.name+" nu"+node.url+"\n"

db = Database()

for node in nl:
  try:
    db.check_for_new_species(node)
  except Exception, e:
    print node.identifier+"\n"
    print e
    