# SentinelScan — Security Assessment Platform

SentinelScan is a local-first security assessment dashboard with a controlled synthetic Assessment Lab. It demonstrates an evidence-driven workflow: **Test → Prove → Understand → Fix → Retest**.

## What is actually assessed?
- **Assessed system:** SentinelScan Local Development Server
- **Test environment:** SentinelScan Controlled Assessment Lab
- **Real production World Monitor:** **Not assessed / no vulnerability claim**

`SS-*` findings refer to the SentinelScan local development server. `LAB-*` findings refer only to the synthetic localhost Assessment Lab. A `LAB-*` result is not evidence that World Monitor production is vulnerable.

## Judge demo
1. Run `START_SENTINELSCAN.bat`.
2. Open **Security Center**.
3. Click **CHECK LOCAL APP**.
4. Show the **Security Score**, severity graph, security-area graph, and plain-language findings.
5. Open a finding to show technical evidence and CVSS.
6. Use **FIX LAB → RETEST** only on `LAB-AUTHZ-001` to demonstrate the remediation lifecycle.
7. Explain that the same evidence check is replayed and the lifecycle changes to resolved when the synthetic fix is applied.

## Report design
The report is intentionally judge-friendly:
- Security Score /100
- Findings and priority counts
- Risk severity bars
- Security-area coverage bars
- Before → After remediation view
- Plain-language issue explanations
- Technical evidence, CVSS, reproduction and lifecycle

## Security boundaries
The scanner accepts **localhost targets only**. It does not scan arbitrary Internet hosts. The Assessment Lab is synthetic and intended for local demonstration. Do not expose the vulnerable lab publicly.

## Run manually
```text
python backend/server.py
```
Then open `http://127.0.0.1:8000/`.

For Render, use `python backend/server.py` as the Start Command. The server honors the platform `PORT` environment variable. The intentionally vulnerable synthetic lab should not be exposed publicly.

## Windows launcher note
- Use `START_SENTINELSCAN.bat`; do not double-click `frontend/index.html`.
- The launcher does not require a local `.venv` and does not use `findstr`, so Windows permission/quoting issues with `.venv` cannot block startup.
- It waits for `http://127.0.0.1:8000/health` before opening the dashboard.
