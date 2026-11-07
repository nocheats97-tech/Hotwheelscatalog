"""Best-effort importer of publicly accessible Shopify collection products.
Run: python -m pip install requests && python sync.py
The Mattel endpoint may be blocked, disabled or subject to usage restrictions.
"""
import json, pathlib, time, requests
BASE='https://creations.mattel.com'
COLLECTIONS={'hot-wheels-collectors':'Hot Wheels Collectors','hot-wheels-rlc':'RLC','hot-wheels-elite-64':'Elite 64'}
ROOT=pathlib.Path(__file__).parent
session=requests.Session();session.headers.update({'User-Agent':'DiecastCatalog/1.0 (personal catalog; contact site administrator)'})
all_items={}
for handle, category in COLLECTIONS.items():
    for page in range(1,21):
        url=f'{BASE}/collections/{handle}/products.json'
        try:
            r=session.get(url,params={'limit':250,'page':page},timeout=25)
            r.raise_for_status()
            data=r.json()['products']
            if not isinstance(data,list): raise ValueError('Unexpected response')
        except (requests.RequestException,ValueError,KeyError) as exc:
            print(f'Cannot read {handle} page {page}: {exc}')
            break
        for p in data:
            key=str(p['id']);imgs=p.get('images') or []
            all_items[key]={'id':key,'title':p.get('title','Untitled'),'sku':next((v.get('sku') for v in p.get('variants',[]) if v.get('sku')),''),'category':category,'image':imgs[0].get('src','') if imgs else '', 'url':f"{BASE}/products/{p.get('handle','')}"}
        print(handle,page,len(data))
        if len(data)<250:break
        time.sleep(1.5)
if all_items:
    (ROOT/'products.json').write_text(json.dumps(list(all_items.values()),ensure_ascii=False,indent=2),encoding='utf-8')
    print('Saved',len(all_items),'products')
else:
    print('No products fetched; keeping existing products.json unchanged.')
