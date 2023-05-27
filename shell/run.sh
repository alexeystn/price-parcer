#!/bin/bash
cd ~/price-parser/python
python3 download_prices.py -w
python3 plot_favourites.py
cp ../database/database.db ../output/database.db
