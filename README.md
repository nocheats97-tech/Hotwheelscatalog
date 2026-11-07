# Diecast Collector

Independent static catalog. No checkout, accounts or payment processing.

## Setup

1. Install Python 3 and run `pip install requests`.
2. Run `python sync.py` to fetch publicly accessible product information. If the Mattel endpoint rejects requests, the script leaves the existing catalog unchanged. The category handles are illustrative and may need updating.
3. Run `python -m http.server 8000`, then visit http://localhost:8000.
4. Click **Управление** to set your EUR prices. Download `prices.json` and replace the site's file to publish prices for all visitors. Browser-only edits are not visible to other visitors.
5. Publish the directory with GitHub Pages or another static host. GitHub Actions workflow attempts a daily sync (subject to public endpoint availability and access rules).

Note: The importer has not been live-tested in this environment. Ensure that your use of Mattel's content and images is authorized. Do not present this independent catalog as an official Mattel store.
