import sys
import os
import errno
import time
import json
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ImgScraper:

    def __init__(self):
        self.searchWord = []
        self.linkList = []
        self.outPath = ''

    def main(self):
        # timeout
        import socket
        socket.setdefaulttimeout(10)

        # 파일 실행시 검색어를 하나이상 넘겨줬는지 판단
        # 아규먼트를 넘겨주지 않았을 때 len(sys.argv)의 값은 1 이다 (sys.argv[0] == ImgScraper.py)
        if len(sys.argv) < 2:
            print('Usage: python3 ImgScraper.py searchWord_0 ... searchWord_N')
            print('end...')
            sys.exit()
        else:
            for i in range(len(sys.argv) - 1):

                # 넘겨준 아규먼트값을 searchWord에 append
                self.searchWord.append(sys.argv[i + 1])

                # 파일 저장경로
                self.outPath = '/Project/03_Src/python/imgClassification/resources/images/' + self.searchWord[i]

                try:
                    # 저장경로에 디렉터리가 없으면 생성
                    if not (os.path.isdir(self.outPath)):
                        os.mkdir(self.outPath)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        print("Failed to create directory!!!!!")
                        raise

                # get_img_link 함수를 실행해 소스링크 리스트를 받음
                self.linkList = ImgScraper.get_img_link(self.searchWord[i])

                # Img Download
                for j in range(len(self.linkList)):
                    try:
                        opener = urllib.request.build_opener()
                        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                        urllib.request.install_opener(opener)

                        urllib.request.urlretrieve(self.linkList[j], self.outPath + '/' + str(j))
                        print('downloading....' + str(len(self.linkList) - j))

                    # 주소에 한글이 포함 or 403 Error => PASS
                    except Exception:
                        print('failed ' + self.linkList[j])
                        continue

                print('Download ' + str(len(self.linkList)) + ' ' + self.searchWord[i] + ' images')

    @staticmethod
    def get_img_link(search_word):
        # 링크 주소를 담을 list 생성
        _linkList = []
        # headless chrome 실행을 위한 옵션 설정
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        # selenium,  크롬 드라이버 실행 (headless)
        # bing 이미지 검색 페이지 get
        driver = webdriver.Chrome(executable_path='/Project/03_Src/python/imgClassification/drivers/chromedriver',
                                  chrome_options=options)
        driver.get('https://www.bing.com/images/search?q=' + search_word + '&qft=+filterui:face-face&FORM=IRFLTR')
        time.sleep(1)

        # 페이지 스크롤링
        elem = driver.find_element_by_tag_name("body")
        _pageDown_cnt = 200
        while _pageDown_cnt:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            print('scrolling...' + str(_pageDown_cnt))
            _pageDown_cnt -= 1

        time.sleep(2)

        # beautifulSoup으로 처리하기위해 페이지 소스를 받음
        _pageSrc = driver.page_source
        soup = BeautifulSoup(_pageSrc, 'lxml')

        # class가 iusc인 모든 a태그를 리스트로 받고
        # for문을 돌려  m 속성값을 dict로 할당, _linkList에 append시킴
        _aTags = soup.body.find_all('a', {'class': 'iusc'})
        for _aTag in _aTags:
            _aTag = _aTag['m']
            a_dict = json.loads(_aTag)

            # {'murl' : 'imgLink'}
            if a_dict['murl'][:4] == 'http':
                _linkList.append(a_dict['murl'])

        driver.close()

        return _linkList


if __name__ == '__main__':
    print('start...')
    ImgScraper().main()
    print('end...')
