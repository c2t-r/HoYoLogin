import os
import json
from http.cookies import SimpleCookie
from datetime import datetime, timezone
from req import get, post, parse_resp
from webhook import send

cookie = os.environ['cookie']
webhook_url = os.environ['webhook']

def main():
    with open("payloads.json", "r") as f:
        payloads = json.load(f)

    global cookie
    _cookie = SimpleCookie()
    _cookie.load(cookie)
    cookies = {k: v.value for k, v in _cookie.items()}
    print("cookie loaded.")

    lang = cookies["mi18nLang"]
    print(f'language: {lang}')

    token = {
        "content-type": "application/json;charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "x-rpc-platform": "4",
        "x-rpc-language": lang,
        "x-rpc-client_type": "5",
        "cookie": cookie
    }

    # verify token
    response = get("https://api-account-os.hoyolab.com/auth/api/getUserAccountInfoByLToken", token)
    verify_resp = parse_resp(response)
    if not verify_resp["retcode"] == 0 or not verify_resp["message"] == "OK":
        print("invalid token provided. please check it.")
        send(webhook_url, { "content": "invalid token provided. please check it." })
        return
    uid = verify_resp["data"]["account_id"]

    # get user game
    response = get(f'https://bbs-api-os.hoyolab.com/game_record/card/wapi/getGameRecordCard?uid={uid}', token)
    card_obj = parse_resp(response)
    print(f'target games: {", ".join([i["game_name"] for i in card_obj["data"]["list"]])}\n')

    for card in card_obj["data"]["list"]:
        payload = [i for i in payloads if i["game_id"] == card["game_id"]][0]
        print(card["game_name"])

        info_url = f'{payload["url"]}info?lang={lang}&act_id={payload["act_id"]}'
        sign_url = f'{payload["url"]}sign?lang={lang}'
        home_url = f'{payload["url"]}home?lang={lang}&act_id={payload["act_id"]}'

        response = get(info_url, {**token, "x-rpc-signgame": payload["id"]})
        info_resp = parse_resp(response)
        
        data = {
            "username": "HoYoLab-AutoCkeckin",
            "content": "",
            "embeds": []
        }
        embed = {
            "title": card["game_name"],
            "description": f'{card["nickname"]} (UID:{card["game_role_id"]}) {card["region_name"]}({card["region"]}) Lv.{card["level"]}',
            "fields": [{
                "name": i["name"],
                "value": i["value"],
                "inline": True
            } for i in card["data"]],
            "thumbnail": { "url": card["logo"] },
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%zZ").replace("+", "")
        }

        if info_resp["data"]["is_sign"] == False:
            response = post(sign_url, {**token, "x-rpc-signgame": payload["id"]}, json.dumps({"act_id": payload["act_id"], "lang": lang}))
            sign_resp = parse_resp(response)
            print(f'response: {sign_resp["message"]}')
            if sign_resp["message"] == "OK":
                print("successfully signed in!")
                data["content"] = "successfully signed in!"
                embed["color"] = 0x38f4af

                response = get(info_url, {**token, "x-rpc-signgame": payload["id"]})
                info_resp = parse_resp(response)

                response = get(home_url, {**token, "x-rpc-signgame": payload["id"]})
                home_resp = parse_resp(response)
                reward = home_resp["data"]["awards"][info_resp["data"]["total_sign_day"]]
                print(f'reward: {reward["name"]}x{reward["cnt"]}')
                embed["description"] += f'\n```\n{reward["name"]} x{reward["cnt"]}\n```'
        else:
            print("already signed in today...")
            data["content"] = "already signed in today..."
            embed["color"] = 0x0000FF

        print(f'total_sign_day: {info_resp["data"]["total_sign_day"]}')
        embed["title"] += f' (total: {info_resp["data"]["total_sign_day"]})'
        
        data["embeds"] = [embed]
        send(webhook_url, data)
        print()

if __name__ == "__main__":
    main()