
cd /home/ghost/BitcoinResearch/

git pull --rebase origin main

source /home/ghost/dev-env/bin/activate
python block_size.py && python supplybtc.py

git add -A
git commit -m 'actualización semanal'
git push origin main
