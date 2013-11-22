import os, requests
from bs4 import BeautifulSoup

URL = 'http://www.turnerengineering.com.au/'
PATH = '/home/elena/websites/_wp-turner/wp-images'
content = '<div class="thumbnails-inline"><span>click on image to enlarge</span> <a class="thickbox" href="/Uploads/Images/cs-s9nkr.jpg"><img src="/Uploads/Images/thm_cs-s9nkr.jpg" alt="Inverter Wall Split - S9" width="190" height="71" /></a> <a class="thickbox" href="/Uploads/Images/cu-s9nkr-outdoor-unit.jpg"><img src="/Uploads/Images/thm_cu-s9nkr-outdoor-unit.jpg" alt="Inverter Wall Split - S9" width="149" height="120" /></a> <a class="thickbox" href="/Uploads/Images/cs-s9nkr-remote-control.jpg"><img src="/Uploads/Images/thm_cs-s9nkr-remote-control.jpg" alt="Inverter Wall Split - S9" width="57" height="120" /></a></div>'
soup = BeautifulSoup(content)

for img in soup.find_all('img'):
    src =  img.get('src')
    if not img.get('src')[:4] == "http":
        src = URL+src

    name = src.split('/')[-1]
    path = os.path.join(PATH, name)
    r = requests.get(src, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)


