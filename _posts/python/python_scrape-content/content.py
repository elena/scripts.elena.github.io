import os

p = "/home/elena/websites/_wp-turner/product/"
for r,d,f in os.walk(p):
    print f

u = Unit.objects.all()[0]

for x in f:
    r = open(os.path.join(p, x), 'r')
    text = r.read()
    srt = text.find('<div id="contents"')
    end = text.find("<!--footer-->")
    u.id = None
    u.slug = x
    u.content = text[srt:end]
    u.save()