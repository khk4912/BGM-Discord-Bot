# 환영합니다!
BGM-Discord-Bot은 한국어를 지원하는 디스코드 봇입니다.


## 봇 초대하기
이 소스를 사용하고 있는 봇은 [이곳](https://discordapp.com/oauth2/authorize?client_id=351733476141170688&scope=bot&permissions=2146958847) 에서 초대가 가능합니다. 


# 개인 호스팅
이 소스 기반으로 다른 봇을 만드는 행위는 **권장하지 않습니다!**
소스가 개인이 사용하기 위한 목적으로 만들어져 편의성이 고려되지 않았으며, 제작자가 라이브러리에 익숙하지 않았을때부터 제작된 소스라 난잡한 부분이 많습니다.

## 파이썬 설치 및 필요한 모듈 설치하기
[이곳](https://www.python.org/downloads/)에서 파이썬을 설치하실 수 있습니다.
**__3.6.x__ 버전을 권장합니다!**

이제 다음의 모듈을 설치하세요.
```
discord-rewrite
lxml
beautifulsoup4
aiomysql
requests
```

## 필요한 소프트웨어 설치
[MariaDB](https://downloads.mariadb.org/) - 봇의 DB 프로그램입니다.
DB를 설치 하신 후에는 PW.py에 


## DB Import 하기
먼저, bot이라는 이름의 DB를 생성해주세요.
```sql
CREATE DATABASE bot;
```
이제, DB에 레포지토리에 업로드되어 있는 bot_schema.sql 을 적용시켜 주세요.

```
mysql -u[유저이름] -p bot < bot_schema.sql
```

## API 신청하기
봇 / BOT 의 기능 구현을 위해 많은 API 가 사용되었습니다.<br>
이 기능을 이용하기 위해선 사용자가 직접 API를 신청해야만 합니다.

TOKEN.py의 주석을 참조하여 API를 신청 후 TOKEN.py의 알맞은 곳에 넣어주세요!

- [디스코드 봇 계정 생성](https://discordapp.com/developers/applications/)
- [NMT 번역](https://developers.naver.com/docs/papago/papago-nmt-overview.md)
- [SMT 번역](https://developers.naver.com/docs/papago/papago-smt-overview.md)
- [언어 감지](https://developers.naver.com/docs/papago/papago-detectlangs-overview.md)
- [검색(백과사전)](https://developers.naver.com/docs/search/encyclopedia/)
- [링크 단축](https://developers.naver.com/docs/utils/shortenurl/)
- [날씨](https://openweathermap.org/api)
- [미세먼지](https://www.data.go.kr/dataset/15000581/openapi.do)
- [기상특보](https://www.data.go.kr/dataset/15000415/openapi.do)

## 끝!
이제 봇의 셀프 호스팅의 준비가 끝났습니다!