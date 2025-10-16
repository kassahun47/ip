from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.get('/')
async def get_ip(request: Request):
    ip = request.headers.get('X-Forwarded-For', request.client.host)

    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    return {'ip': ip}

@app.get('/info')
async def get_ipinfo(request: Request):
    '''Try to get the real IP address from common headers, fallback to client.host.'''
    #ip = request.headers.get('X-Forwarded-For', request.client.host)
    ip = request.headers.get('x-forwarded-for')

    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://ipinfo.io/{ip}/json')
        if response.status_code != 200:
            return {'error': 'Could not get info from ipinfo.io'}
        data = response.json()

    return {
        #'ip': data.get('ip', ip),
        'ip': ip,
        #'coordinates': data.get('loc'),
        'coordinates': [float(coord) for coord in data.get('loc').split(',')],
        'country': data.get('country'),
        'city': data.get('city'),
        'timezone': data.get('timezone'),
        #'isp' : data.get('org'),
        'isp' : ' '.join(data.get('org').split()[1:])
    }
