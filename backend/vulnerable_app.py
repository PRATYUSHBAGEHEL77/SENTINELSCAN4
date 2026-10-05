"""SentinelScan controlled assessment lab.
Localhost-only synthetic vulnerabilities. No production data or outbound fetching.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import json, os
from pathlib import Path

DATA=Path(os.environ.get('SENTINELSCAN_DATA', str(Path.home()/'AppData'/'Local'/'SentinelScan'))); DATA.mkdir(parents=True,exist_ok=True)
STATE=DATA/'security_state.json'

def fixed():
    try:return bool(json.loads(STATE.read_text()).get('lab_fixed'))
    except Exception:return False

class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, obj):
        body=json.dumps(obj).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        p=urlparse(self.path); q=parse_qs(p.query); isfixed=fixed()
        if p.path=='/health': self.send_json(200,{'status':'ok','lab':'synthetic','scope':'localhost-only'}); return
        if p.path=='/admin': self.send_json(403 if isfixed else 200, {'error':'admin authorization required','lab':'synthetic'} if isfixed else {'admin_marker':'DEMO-ONLY','lab':'synthetic'}); return
        if p.path.startswith('/idor'): self.send_json(403 if isfixed else 200, {'error':'object authorization required'} if isfixed else {'object_id':q.get('object_id',['2'])[0],'owner':'synthetic-user-2','lab':'synthetic'}); return
        if p.path.startswith('/xss'): self.send_json(200, {'html':'&lt;script&gt;','encoded':True,'lab':'synthetic'} if isfixed else {'html':q.get('q',[''])[0],'encoded':False,'lab':'synthetic'}); return
        if p.path.startswith('/jwt'): self.send_json(401 if isfixed else 200, {'error':'signature required'} if isfixed else {'role':'admin','alg':'none','lab':'synthetic'}); return
        if p.path.startswith('/ssrf'): self.send_json(400 if isfixed else 200, {'error':'destination blocked'} if isfixed else {'accepted_destination':q.get('url',[''])[0],'lab':'synthetic'}); return
        self.send_json(404,{'error':'not found','lab':'synthetic'})
    def log_message(self,*args): pass

if __name__=='__main__':
    print('SentinelScan controlled lab: http://127.0.0.1:8100/health')
    ThreadingHTTPServer(('127.0.0.1',8100),Handler).serve_forever()
