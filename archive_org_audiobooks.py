
# thanks ChatGPT!

import re
import requests
from xml.sax.saxutils import escape

ITEM = 'the-secret-of-chimneys-by-agatha-christie'
DLOD = f'https://archive.org/download/{ITEM}'
META = re.sub('download', 'metadata', DLOD)
DETL = re.sub('download', 'details',  DLOD)

data = requests.get(META).json()

mp3s = [
    f for f in data['files']
    if f['name'].lower().endswith('.mp3')
]

# assume they are sorted same as in the DLOD page

def rss_item(n, f):
    title = f'Chapter {n}'
    url = f"{DLOD}/{f['name']}"
    length = f.get('size', '0')
    return f"""
    <item>
      <title>{escape(title)}</title>
      <enclosure  url="{escape(url)}"
                  length="{length}"
                  type="audio/mpeg"/>
      <guid>{escape(url)}</guid>
    </item>
"""

items = ''.join(rss_item(i+1, f) for i,f in enumerate(mp3s))

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>The Secret of Chimneys</title>
  <link>{DETL}</link>
  <description>Audiobook chapters</description>
  {items}
</channel>
</rss>
"""

open('chimneys.xml', 'w').write(rss)