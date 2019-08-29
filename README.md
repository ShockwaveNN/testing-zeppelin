# Project for QA for zeppelin Project

## Steps to setup

1. Install zeppelin according to [instruction](https://zeppelin.apache.org/docs/latest/quickstart/install.html)
2. [Download](http://chromedriver.chromium.org/downloads) chromedriver and install to `/usr/bin/chromedriver`
3. Install requirements `pip install -r requirements.txt`
4. Run `pytest test`

### Allure reports

If you wanna get allure result run  
`pytest --alluredir=/allure tests`  
`allure serve allure`

Reports:
![Screenshot_20190829_185053](https://user-images.githubusercontent.com/668524/63956661-890d6000-ca8f-11e9-8388-0a187852d274.png)
![Screenshot_20190829_185035](https://user-images.githubusercontent.com/668524/63956662-890d6000-ca8f-11e9-8be3-e77d74d188db.png)
