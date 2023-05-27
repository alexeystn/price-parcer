#!/bin/bash
cd ~/price-parser/output
python3 -m http.server 80
