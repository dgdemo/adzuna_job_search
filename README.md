# Adzuna Job Search

## Quick start
1. Create a `.env` from `.env.example` and fill in `ADZUNA_APP_ID` / `ADZUNA_APP_KEY`  
2. Create venv & install requirements  
3. Run a search to CSV

```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt

cp .env.example .env
# edit .env with your keys

python src/main.py --what "Terraform" --days 7 --out results.csv
