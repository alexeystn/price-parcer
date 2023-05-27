#!/bin/bash
sudo cp my_server.service /etc/systemd/system/my_server.service
sudo systemctl daemon-reload 
sudo systemctl enable my_server.service 
sudo systemctl start my_server.service 
sudo systemctl status my_server.service