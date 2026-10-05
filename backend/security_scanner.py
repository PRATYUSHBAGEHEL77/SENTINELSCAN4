"""Inspectible SentinelScan security test catalog and CVSS 3.1 helper."""
import math
TEST_CATALOG = {
    'AUTH': 'Authentication/session controls', 'AUTHZ': 'Authorization/access control',
    'INPUT': 'Input validation/data handling', 'API': 'API security',
    'CLIENT': 'Client-side security', 'TLS': 'Transport security', 'DATA': 'Data protection'
}
MANUAL_CATALOG = {'TLS-001': 'TLS certificate/deployment review', 'TLS-002': 'HSTS deployment review'}

def _roundup(x): return math.ceil(x*10-1e-9)/10

def cvss_from_observation(o):
    av={'Network':0.85,'Adjacent':0.62,'Local':0.55,'Physical':0.2}.get(o.get('attack_vector'),0.85)
    ac={'Low':0.77,'High':0.44}.get(o.get('complexity','Low'),0.77)
    pr={'None':0.85,'Low':0.62,'High':0.27}.get(o.get('privileges','None'),0.85)
    ui={'None':0.85,'Required':0.62}.get(o.get('interaction','None'),0.85)
    scope='U'
    c={'None':0,'Low':0.22,'High':0.56}.get(o.get('confidentiality','None'),0)
    i={'None':0,'Low':0.22,'High':0.56}.get(o.get('integrity','None'),0)
    a={'None':0,'Low':0.22,'High':0.56}.get(o.get('availability','None'),0)
    impact=1-(1-c)*(1-i)*(1-a)
    if scope=='U':
        impact_score=6.42*impact
        exploit=8.22*av*ac*pr*ui
        score=_roundup(min(impact_score+exploit,10)) if impact>0 else 0.0
        vector=f"CVSS:3.1/AV:{'N' if o.get('attack_vector','Network')=='Network' else 'A' if o.get('attack_vector')=='Adjacent' else 'L'}/AC:{'L' if o.get('complexity','Low')=='Low' else 'H'}/PR:{'N' if o.get('privileges','None')=='None' else 'L' if o.get('privileges')=='Low' else 'H'}/UI:{'N' if o.get('interaction','None')=='None' else 'R'}/S:U/C:{'N' if c==0 else 'L' if c==0.22 else 'H'}/I:{'N' if i==0 else 'L' if i==0.22 else 'H'}/A:{'N' if a==0 else 'L' if a==0.22 else 'H'}"
    else:
        impact_score=7.52*(impact-0.029)-3.25*(impact-0.02)**15
        exploit=8.22*av*ac*pr*ui
        score=_roundup(min(1.08*(impact_score+exploit),10)) if impact>0 else 0.0
        vector='CVSS:3.1'
    return {'score':score,'vector':vector,'attack_vector':o.get('attack_vector','Network'),'complexity':o.get('complexity','Low'),'privileges':o.get('privileges','None'),'interaction':o.get('interaction','None'),'scope':scope,'confidentiality':o.get('confidentiality','None'),'integrity':o.get('integrity','None'),'availability':o.get('availability','None'),'reason':'Score derived from observed impact/exploitability assumptions; verify against the final authorized deployment context.'}
