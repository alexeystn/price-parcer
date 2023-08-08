### How to install:

1. Install git: <br>
`apt-get update` <br>
`sudo apt install git`

2. Clone this repository: <br>
`git clone https://github.com/alexeystn/price-parser`

3. Install modules: <br>
`apt install python3-pip` <br>
`pip3 install numpy` <br>
`pip3 install matplotlib` <br>

4. Configure daily run at 10:00: <br>
`crontab -e` <br>
Add following line: <br>
`00 10 * * * ~/price-parser/shell/run.sh` <br>

5. Reboot cron: <br>
`sudo service cron reload`

6. Make script executable: <br>
`chmod +x ~/price-parser/shell/run.sh`

7. Configure autorun http-server: <br>
`cd ~/price-parser/shell/` <br>
`source install_server.sh`

### Other commands:

Pull latest changes: <br>
`git pull`

Download prices and update database right now: <br>
`python3 download_prices.py -w`
