# Using the AddressBook framework on MacOS X
#
# I didn't add a single line of C code for this!
import AddressBook

book = AddressBook.ABAddressBook.sharedAddressBook()
me = book.me()

propNames = me.properties()
d = {}
for i in range(len(propNames)):
	d[propNames[i]] = me.valueForProperty_(propNames[i])

keys = d.keys()
keys.sort()
print "Information about me"
print "--------------------"
for k in keys:
	if d[k] == None: continue
	print '%s: %s'%(k, d[k])

