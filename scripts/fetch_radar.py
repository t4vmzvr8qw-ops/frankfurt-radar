#!/usr/bin/env python3
"""Build a news-link feed about Frankfurt. Not a confirmed event-calendar feed."""
import datetime as dt, email.utils, hashlib, html, json, re, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
queries=[('Events','(Frankfurt Veranstaltung OR Festival OR Event) when:7d'),('Kultur','(Frankfurt Ausstellung OR Museum) when:7d'),('Food','(Frankfurt Restaurant Eröffnung OR Gastronomie) when:7d'),('Outdoor','(Frankfurt Outdoor OR GrünGürtel OR Natur) when:7d'),('Märkte','(Frankfurt Markt OR Flohmarkt OR Food Festival) when:7d')]
items={}
for category,q in queries:
 try:
  url='https://news.google.com/rss/search?'+urllib.parse.urlencode({'q':q,'hl':'de','gl':'DE','ceid':'DE:de'})
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; FrankfurtRadar/1.0)'})
  with urllib.request.urlopen(req,timeout=20) as res: body=res.read(2_000_000)
  tree=ET.fromstring(body)
  for it in tree.findall('.//channel/item')[:28]:
   title=html.unescape(re.sub('<[^>]+>','',it.findtext('title',''))).strip();link=it.findtext('link','');source=it.findtext('source','')
   try: date=email.utils.parsedate_to_datetime(it.findtext('pubDate','')).astimezone(dt.timezone.utc)
   except: continue
   if not title or not link or date<dt.datetime.now(dt.timezone.utc)-dt.timedelta(days=10):continue
   dedup=re.sub(r'\W+','',title.lower().split(' - ')[0])[:120]
   if dedup not in items:items[dedup]={'id':hashlib.sha256(link.encode()).hexdigest()[:16],'title':title,'url':link,'source':source,'published':date.isoformat(),'category':category}
  print('Fetched',category)
 except Exception as exc:print('Warning: RSS failed',category,exc)
p=ROOT/'data/radar.json'
if items:p.write_text(json.dumps({'updated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'items':sorted(items.values(),key=lambda x:x['published'],reverse=True)[:100]},indent=2,ensure_ascii=False),encoding='utf8')
else:
 print('Retaining previous feed')
 if not p.exists():p.write_text('{"updated_at":null,"items":[]}')
