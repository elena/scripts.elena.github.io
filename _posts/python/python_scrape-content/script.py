import os, requests

#URL = "http://www.turnerengineering.com.au/product-catalogue.asp?iCategoryID=%s"
URL = "http://www.turnerengineering.com.au/product-details.asp?iCategoryID=%s"
N = 500

test = "<p>No information to display at this time...</p>"
good = []

for x in range(1,N):
    r = requests.get(URL % x)
    print("  ... {}".format(x))
    if test not in r.content:
        print("** is good! {}".format(x))
        good.append(x)
        f = open("/home/elena/websites/_wp-turner/product/{}.html".format(x), 'w+')
        f.write(r.content)
        f.close()

"""
"<p>No information to display at this time...</p>"
"""
