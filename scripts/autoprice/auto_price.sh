cd /home/ghost/BitcoinResearch/scripts/bins

git pull origin main
git add -A
git commit -m "auto price $(date +'%Y-%m-%d')"
git push origin main
