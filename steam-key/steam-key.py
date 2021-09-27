# coding=utf-8
"""
Module Summary Here.
Get free steam-key from vxgzh and post to steam.
Authors: gorgeousdays@outlook.com
Create time:2021.9.11
"""

import re
import requests
import yaml
import datetime
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def logger(txt):
    print("{}:{}".format(datetime.datetime.now(),txt))

def getHTMLText(url):
     try:
          kv = {'user-agent':'Mozilla/5.0'}
          r = requests.get(url, timeout = 30, headers = kv) 
          r.raise_for_status()   
          r.encoding = r.apparent_encoding   
          return r.text   
     except:
          return 'error'

#get the atricle link
def get_link_from_vx(url):
    with open("config.yaml", "r") as file:
        file_data = file.read()
    config = yaml.safe_load(file_data)
    headers = {
        "Cookie": config['wechat-cookie'],
        "User-Agent": config['user-agent'] 
    }
    data=requests.get(url, headers=headers, verify=False).json()
    link=data['app_msg_list'][0]['link']
    return link

#get the steam key from atricle link
def get_key_from_atricle(link):
    html_text=getHTMLText(link)

    #get steam keys form link
    temp_keys=re.findall(r'<p style="box-sizing: border-box;">(.*?)</p>',html_text,re.I|re.M|re.S)
    steam_keys=[]
    for key in temp_keys:
        if len(key)==17:
            steam_keys.append(key)
    logger("Get keys successfully:{}".format(steam_keys))

    #generate true keys
    steam_keys_list=[]
    for index,key in enumerate(steam_keys):
        steam_keys_list.append([])
        for i in range(7):
            tempkey=key.replace("?",str(i))
            steam_keys_list[index].append(tempkey)
   
    return steam_keys_list
    
#post keys to steam
def post_key_to_steam(steam_keys_list):
    with open("config.yaml", "r") as file:
        file_data = file.read()
    config = yaml.safe_load(file_data)
    post_url = "https://store.steampowered.com/account/ajaxregisterkey/"
    data = {"product_key":None,"sessionid": config['steam-sessionid']}
    headers = {
        "Cookie":config['steam-cookie'],
        "User-Agent": config['user-agent']
    }
    for j in range(len(steam_keys_list[0])):
        data['product_key']=steam_keys_list[-1][j]
        logger("Now key:{}".format(steam_keys_list[-1][j]))
        res = requests.post(url=post_url,data=data,headers=headers).json()
        checked=check_res(res)
        time.sleep(0.1)
        if checked==True:
            break
    for i in range(len(steam_keys_list)):
        for j in range(len(steam_keys_list[0])):
            data['product_key']=steam_keys_list[i][j]
            logger("Now key:{}".format(steam_keys_list[i][j]))
            res = requests.post(url=post_url,data=data,headers=headers).json()
            checked=check_res(res)
            time.sleep(0.1)
            if checked==True:
                break

#judge the json result returned by steam
def check_res(res):
    #Success
    if res["success"] == 1:
        for item in res["purchase_receipt_info"]["line_items"]:
            logger("Success:{}".format(item["line_item_description"]))
        return True
    # Error codes from https://steamstore-a.akamaihd.net/public/javascript/registerkey.js?v=qQS85n3B1_Bi&l=english
    else:
        errorCode = res["purchase_result_details"]
        sErrorMessage = ""
        if errorCode == 14:
            sErrorMessage = 'The product code you\'ve entered is not valid. Please double check to see if you\'ve mistyped your key. I, L, and 1 can look alike, as can V and Y, and 0 and O.'
        elif errorCode == 15:
            sErrorMessage = 'The product code you\'ve entered has already been activated by a different Steam account. This code cannot be used again. Please contact the retailer or online seller where the code was purchased for assistance.'
        elif errorCode == 53:
            sErrorMessage = 'The product code you\'ve entered is not valid. Please double check to see if you\'ve mistyped your key. I, L, and 1 can look alike, as can V and Y, and 0 and O.'
        elif errorCode == 13:
            sErrorMessage = 'Sorry, but this product is not available for purchase in this country. Your product key has not been redeemed.'
        elif errorCode == 9:
            sErrorMessage = 'This Steam account already owns the product(s) contained in this offer. To access them, visit your library in the Steam client.'
        elif errorCode == 24:
            sErrorMessage = 'The product code you\'ve entered requires ownership of another product before activation.\n\nIf you are trying to activate an expansion pack or downloadable content, please first activate the original game, then activate this additional content.'
        elif errorCode == 36:
            sErrorMessage = 'The product code you have entered requires that you first play this game on the PlayStation®3 system before it can be registered.\n\nPlease:\n\n- Start this game on your PlayStation®3 system\n\n- Link your Steam account to your PlayStation®3 Network account\n\n- Connect to Steam while playing this game on the PlayStation®3 system\n\n- Register this product code through Steam.'
        elif errorCode == 50: 
            sErrorMessage = 'The code you have entered is from a Steam Gift Card or Steam Wallet Code. Browse here: https://store.steampowered.com/account/redeemwalletcode to redeem it.'
        else:
            sErrorMessage = 'An unexpected error has occurred.  Your product code has not been redeemed.  Please wait 30 minutes and try redeeming the code again.  If the problem persists, please contact <a href="https://help.steampowered.com/en/wizard/HelpWithCDKey">Steam Support</a> for further assistance.';
        logger("Error key:{}".format(sErrorMessage))
        return False

def main():
    with open("config.yaml", "r") as file:
        file_data = file.read()
    config = yaml.safe_load(file_data)
    url = config['wechat-article-get-api']
    temp_link=get_link_from_vx(url)
    flag = True
    while flag:
        link=get_link_from_vx(url)
        if(link!=temp_link):
            logger("Article link:{}".format(link))
            steam_keys_list=get_key_from_atricle(link)
            post_key_to_steam(steam_keys_list)
            flag=False
        else:
            logger("Article not update.")
            time.sleep(60)

if __name__ == '__main__':
    main()
    #link=""
    #steam_keys_list=get_key_from_atricle(link)
    #post_key_to_steam(steam_keys_list)