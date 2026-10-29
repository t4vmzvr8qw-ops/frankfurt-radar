#!/usr/bin/env python3
"""Fetch dated Frankfurt events from public structured feeds, not news article dates."""
import datetime as dt, json, re, urllib.request, urllib.parse, html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/events.json'
TZ=dt.timezone(dt.timedelta(hours=1))
now=dt.datetime.now(dt.timezone.utc)
results={}
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'FrankfurtRadar/2.0 (personal event explorer; contact via repository)','Accept':'application/json, application/ld+json'})
 with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
def clean(s):return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]*>',' ',str(s or '')))).strip()[:950]
def add(title,start,end,place,desc,url,category,source,lat=None,lng=None):
 if not title or not start:return
 try:
  start_dt=dt.datetime.fromisoformat(str(start).replace('Z','+00:00'))
  if start_dt.tzinfo is None:start_dt=start_dt.replace(tzinfo=TZ)
  end_dt=dt.datetime.fromisoformat(str(end).replace('Z','+00:00')) if end else start_dt
  if end_dt.tzinfo is None:end_dt=end_dt.replace(tzinfo=TZ)
  if end_dt<now-dt.timedelta(days=1) or start_dt>now+dt.timedelta(days=100):return
 except (ValueError,TypeError):return
 key=(clean(title).lower(),start_dt.date().isoformat())
 if key in results:return
 results[key]={'id':f'{source}-{len(results)+1}','title':clean(title)[:180],'start':start_dt.isoformat(),'end':end_dt.isoformat(),'location':clean(place)[:180],'description':clean(desc),'url':url if str(url).startswith('https://') else '', 'category':clean(category)[:40] or 'Sonstiges','source':source,'lat':lat,'lng':lng}
try:
 data=fetch('https://www.evensos.de/api/map/events?'+urllib.parse.urlencode({'city':'frankfurt-am-main','date':'month'}))
 for f in data.get('features',[]):
  p=f.get('properties') or {}; g=f.get('geometry') or {}; co=g.get('coordinates') or []
  add(p.get('name') or p.get('title'),p.get('startDate') or p.get('start') or p.get('date'),p.get('endDate') or p.get('end'),p.get('location') or p.get('venue'),p.get('description'),p.get('url'),p.get('category'),'evensos',co[1] if len(co)>=2 else None,co[0] if len(co)>=2 else None)
 print('Evensos geo feed:',len(results))
except Exception as e:print('Evensos geo feed unavailable:',e)
try:
 data=fetch('https://www.evensos.de/events/frankfurt-am-main.json')
 for element in data.get('dataFeedElement',[]):
  e=element.get('item') or element
  loc=e.get('location') or {};loc=loc if isinstance(loc,dict) else {'name':str(loc)}
  address=loc.get('address') or {};address=address if isinstance(address,dict) else {}
  geo=loc.get('geo') or {}
  add(e.get('name'),e.get('startDate'),e.get('endDate'),loc.get('name') or address.get('streetAddress'),e.get('description'),e.get('url'),e.get('category') or 'Event','evensos',geo.get('latitude'),geo.get('longitude'))
 print('Evensos list:',len(results))
except Exception as e:print('Evensos list unavailable:',e)
try:
 url='https://aktuelles.uni-frankfurt.de/wp-json/tribe/events/v1/events/?'+urllib.parse.urlencode({'per_page':50,'start_date':now.date().isoformat(),'end_date':(now+dt.timedelta(days=90)).date().isoformat()})
 data=fetch(url)
 for e in data.get('events',[]):
  venue=e.get('venue') or {};venue=venue if isinstance(venue,dict) else {}
  cats=e.get('categories') or []
  add(e.get('title'),e.get('start_date'),e.get('end_date'),venue.get('venue') or venue.get('address'),e.get('description'),e.get('url'),cats[0].get('name') if cats else 'Universität','Goethe-Uni')
 print('University events:',len(results))
except Exception as e:print('University feed unavailable:',e)
items=sorted(results.values(),key=lambda e:e['start'])[:400]
if items:
 OUT.write_text(json.dumps({'updated_at':now.isoformat(),'items':items},ensure_ascii=False,indent=2),encoding='utf8')
 print('Saved',len(items),'dated events')
else:
 print('No verified dated events retrieved; retaining previous feed')
 if not OUT.exists():OUT.write_text(json.dumps({'updated_at':None,'items':[]}),encoding='utf8')
