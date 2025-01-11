# HoYoLogin
 
Automatically check in HoYoLab

## Target
- [Genshin Impact](https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481)
- [Honkai Impact 3rd](https://act.hoyolab.com/bbs/event/signin-bh3/index.html?act_id=e202110291205111)
- [Honkai: Star Rail](https://act.hoyolab.com/bbs/event/signin/hkrpg/e202303301540311.html?act_id=e202303301540311)
- [Tears of Themis](https://act.hoyolab.com/bbs/event/signin/nxx/index.html?act_id=e202202281857121)
- [Zenless Zone Zero](https://act.hoyolab.com/bbs/event/signin/zzz/e202406031448091.html?act_id=e202406031448091)

## Usage
1. Fork this repo.
2. Add secrets.
   - cookies for hoyolab as `HOYOLAB_COOKIE` (`NAME=VALUE; NAME2=VALUE2;~`)
   - discord webhook url as `WEBHOOK_URL` (`https://discord.com/api/webhooks/~`)
3. try manually to check! (the workflow has `workflow_dispatch` trigger)

## How do I get the cookie?
1. Open the check in page (any [target](#Target) page is fine) and open developer tools.
2. Open `Network` tab and select the top request which should be `~.html`.
3. See request headers, then you can find the cookie!  

__note: the order of cookies does NOT matter.__

## Example
![image](https://github.com/user-attachments/assets/0e9629f3-7ac9-4b67-a8ad-4e674daee80a)
