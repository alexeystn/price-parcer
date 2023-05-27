#!/bin/bash
cd /root/price-parser/python
python3 download_prices.py -w
cp ../database/database.db ../output/database.db
