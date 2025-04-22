cd /home/ghost/BitcoinResearch/scripts/bins


git add -A
git commit -m "auto price $(date +'%Y-%m-%d')"
git pull -ff origin main
git push origin main
