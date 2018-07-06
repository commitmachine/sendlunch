from __future__ import unicode_literals, print_function
import sys

#import from command line
for i in sys.argv[1:]:
    __import__("places." + i)
    r = sys.modules["places."+i].restaurant()
    print('Running', r.get_name())
    r.get_lunches()
