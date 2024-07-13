# coingecko.com currencies scraper
Scrapy parser for extracting most important information about currency from coingecko.com

## Usage:

Clone with git:
```sh
git clone https://github.com/selforg-level/coingecko-scraper.git
```

Cd into project:
```sh
cd coingecko-scraper
```

Create venv and install requirements:
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run coins scraper:
```sh
scrapy crawl coins -o output.json
```

