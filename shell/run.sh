#!/bin/bash
cd ~/price-parser/python
python3 download_prices.py -w
python3 plot_favourites.py
python3 print_report.py
cp ../database/database.db ../output/database.db
