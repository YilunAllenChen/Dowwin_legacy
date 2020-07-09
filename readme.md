# How to setup environment to run dowwin
1. install [MongoDB](https://docs.mongodb.com/manual/installation/)
2. Under Dowwin repo, do: 
    - `pip3 installl -r requirements.txt`
3. Find the installed package yfinance and its module base.py. On my computer it's:  
    - lib/python3.6/site_packages/yfinance/base.
    - Change line 286 to: 
        - self._institutional_holders = holders[0]
    - This allows the crawler to acquire info of stock even if there isn't any institutional holders.