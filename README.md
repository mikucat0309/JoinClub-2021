# JoinClub-2021
Hackersir 8th Join Club System 

Derived from [this](https://github.com/ch3n97w/JoinClub-2020)

## 使用 .env
部份功能需要先設定 .env 才可以使得此系統運行
```shell
# Django secret key
# 請進入 Django shell 運行:
# from django.core.management.utils import get_random_secret_key
# get_random_secret_key()
# 產生新的 secret key
SECRET_KEY='' 

# 收據傳送 Mail
# 下面兩項可以設定使用的 Mail 以及密碼
# 以便使用裡面的 SMTP 服務
EMAIL_SENDER=''
EMAIL_SENDER_PASSWD=''
```

## Changelog
### Added
- join
  - search
    - 更新search功能
    - 新增search給社員查詢繳費情形
    - 新增search 刷條碼機確認有無填寫保密協議
  - Form
    - 新增保密協議表單
    - 更新入社表單
  - Model
    - 新增secret,receipt
  - Functions
    - 產生電子收據並寄送到o365信箱
