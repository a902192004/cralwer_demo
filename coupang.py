import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

def checkConnect(url, headers):
    try:
        response = requests.get(url, headers=headers, verify=True, timeout=15)
        checkSuccess = True
        return response, checkSuccess
    except Exception as e:
        print('下載失敗!')
        response = None
        checkSuccess = False
        return response, checkSuccess

def detail_img_handler(detail_url, headers):
    response, checkSuccess = checkConnect(detail_url, headers=headers)
    res_json = response.json()
    content_list = []
    print("res_json : " + str(res_json["details"]))
    for item in res_json['details']:
        descriptions = item.get('vendorItemContentDescriptions', [])
        for description in descriptions:
            img_url = description.get('content')
            if description.get('imageType') and img_url:
                content_list.append(f'https:{img_url}')
    return content_list, checkSuccess

# 搜尋條件
search_keyword = 'food'
# 搜尋最大頁數
maxPage = 5
# 迴圈搜尋結果頁數
outputDf = pd.DataFrame()
for page in range(1, maxPage+1):

    # header
    headers = {
        "authority": "www.coupang.com",
        "method": "GET",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36",
        "sec-ch-ua-platform": "macOS",
        "cookie": "sid=4fef195e74e24a0f907f211a139c81147c4525f9; PCID=50456808547313760358517; MARKETID=50456808547313760358517; delivery_toggle=false; searchKeyword=food%7Cair%7Cairpods; searchKeywordType=%7B%22food%22%3A0%7D%7C%7B%22air%22%3A0%7D%7C%7B%22airpods%22%3A0%7D; x-coupang-accept-language=ko-KR; x-coupang-target-market=KR; bm_so=8C7B7991006592BB5921434A3A21AFEA7BFE098216214BC35E5F618B2E7203F6~YAAQN4pFy8V4PCGRAQAAV/UiTQBlAacQR4txEOqN0u08TS0KJyaieCLx9NwZEJRc5d2MvHdeu3N/y0LqCWsu2XkhT0OwvH1vNjIdbaNAOADQ08QXNkOIcLwa2mm0Mmb+mLX+XHc5E7sOtKRrT1JUv7hG1LU7WaQQTs6QE2HeoKAF/JdcB3Rqd3ldRs1VP/8d2e0XwoaAFLRkMOXju7BHWyUZfLglzi3rYT/alIpUSlFtNgp4FwIBHGgfbFJwUlxggFfbVw8GnuFw5Qzw5GRGr5zoz+lFazatkaGXDgSFeWOM8b3Qd7pKID07qtm6YSHfsYT2hSS2aWwWESP3kYJGc+EJSaasSVGnw6ZTi9F+qW5c7zW73K/MwKyOEF02CMsuTjWyboIKnsffLh1/5nEpRKCjWopryD/s4Boi4yrNifo7VbRNEW83NBZ7JG6BBdgfuG8jbgi1WHMuYAexVPjRD3SRAA1vxFZTskIjEFUC1wbRgmYwslt8W4MKPeVWO79OYSx2QonYnzBx3eDiLWoQn9rPAL+QxW8A1INoaSFRaIpFaGqUAh5rmUk+qL+AjJK4xcQ5Q0M363aYYZK0jEBWxw==; bm_s=YAAQN4pFy814PCGRAQAAbfwiTQEQbk8hJCmtrejWWv4tGV9vXik7rKPg3qmQ8uTYPoQ/m9nguHGGKUJsTRAfW9xiwtY53nkCC4v0rCbo9YBXk7/3Kt+hf/A6HNHRjwPoD52U2M++hL4WOn+NTvi/sVylC7QwmJkJAHeRn+8ZUghybiNf5skJeGkeyeGoRP+/v3yJdDnYywDR5LrsbjY34XnTVtI8ysSldfWMAXXIw90iYovuUYqFpUZDuYXIi2HL1nXzcEQ2peQUeSUhhJnUp7d028d6XOzXvFz8UHNmcTGXYK5Wh7/RWmOIeqQZCD1ax0nek0m3j0AnelV8b1iktmPxl5ZY; bm_lso=8C7B7991006592BB5921434A3A21AFEA7BFE098216214BC35E5F618B2E7203F6~YAAQN4pFy8V4PCGRAQAAV/UiTQBlAacQR4txEOqN0u08TS0KJyaieCLx9NwZEJRc5d2MvHdeu3N/y0LqCWsu2XkhT0OwvH1vNjIdbaNAOADQ08QXNkOIcLwa2mm0Mmb+mLX+XHc5E7sOtKRrT1JUv7hG1LU7WaQQTs6QE2HeoKAF/JdcB3Rqd3ldRs1VP/8d2e0XwoaAFLRkMOXju7BHWyUZfLglzi3rYT/alIpUSlFtNgp4FwIBHGgfbFJwUlxggFfbVw8GnuFw5Qzw5GRGr5zoz+lFazatkaGXDgSFeWOM8b3Qd7pKID07qtm6YSHfsYT2hSS2aWwWESP3kYJGc+EJSaasSVGnw6ZTi9F+qW5c7zW73K/MwKyOEF02CMsuTjWyboIKnsffLh1/5nEpRKCjWopryD/s4Boi4yrNifo7VbRNEW83NBZ7JG6BBdgfuG8jbgi1WHMuYAexVPjRD3SRAA1vxFZTskIjEFUC1wbRgmYwslt8W4MKPeVWO79OYSx2QonYnzBx3eDiLWoQn9rPAL+QxW8A1INoaSFRaIpFaGqUAh5rmUk+qL+AjJK4xcQ5Q0M363aYYZK0jEBWxw==^1723576024672; bm_sv=B9862A4664BD751C4EB5B0F094A6ED91~YAAQJYpFy4DajzaRAQAARXJTUBg+1u+K153dvhIHY6XUoV6k4tTWqxsgO4DkxfZANTy1tfQCwRazTdA+QiVr1FuLX4hjfshmhc1AjxZOTU/Oc0QtJbbIagEwRv8aLfDYPjQRi9GsTvVagKGI31pRH2DhlMej+6PKT4KhGuvVE8xljHInHtJXwjeJOaAW0M3hLTnCuti+BFVnwgYeTMVicLmjK64Mdpq+ihW07xmKA7tOnWMA1SvU32jDVupUpIRC+jI=~1; overrideAbTestGroup=%5B%5D; baby-isWide=small; bm_sz=2DD6FF417A4865C6D07F2D0ADC849B6D~YAAQJYpFy5BpkDaRAQAAL8+jUBgWjhWZ2n0LjxiVcE/tj+7/8pMl5l+n7+xXOQN7TuOs+ZbaW81xrAfB7YehXvKYYKBdWQLyWXQ1o5abFDXQjf4JJejclrdY/b0TZ9Kf/jwWxkG8UNMwYxm3quxd4Iufb6S8WG12ktAzwWvUp+BO4/yjSygQbnyq9IdlRtALjms91iL2NzTIRoa3378q5/EjGVl9oQtzZYalTHLLoDU7n77iD9RJlxa5tXcv+6+2Gg8azxFwoabclMordRCcqq0pCD4IVu/fCUFdVyO9h0O+h3CdwaYTFfJbUlgV/KWPl3WdYHXhOipph4HQoqT4mVk3CDQHdXrZWmtQyg+NpTKo9KAeLRt3Wg25tacuo+N9PkFnLMacM0B9CNY8hqtcerE77MK/F1zZtGuYVlp3CXrzav1DotXfD13cQoTNcYYFfDbOCdTvNWntojS5bZHntLZdGg4rIDyV5SCGtIg6fbYQrLCxhrBIt20GxK42f+T3Z+DdsAUlxvs0qxfQ9RiATXZDuSvQmqRGuwdpw2iiyHg4vS6jKo1HKHo=~3223859~3686982; _abck=89A6180874CC42427ED7A030BDD5AFF7~0~YAAQJYpFyxBqkDaRAQAAgkekUAwTPNUY+piuc3At30m46Ohm72SzhZbBBGWKZTgh6ro/dEcAXbX2KDHXX2+7kQcHromi4riRnuMYvV5kPvS+f7hXt5FVW2AicYplmIdYRPdydconFmCCNssmgIGEhMXzl12V+Y4VtZp3a+qjv0tq1PDmhIllO+f3QRXWfij9bBcJw5b356PYG7fVjLtzYdjhpmL2fwCEzNc5FM/bgvPVfcz0up88zD923orF1bGwB0UOZRuBQ965YElfqd/5DVKKkGu6Inz3zoqKutuJjDYOVJ8ia/qPjX0NTQJQsi2yVeP9WCOeWyinpQ6vhqmXN2GXIDLbYdBpCO2n5pXjw3zQ9NEX3vSXkbXtEMVw57F9TYIK2VfzTiynk/RLKkXq4heW9hbpX9eKADEg8fKp+We4/UaAaVi2~-1~||0||~-1"
    }


    # 網址
    # search_keyword: 搜尋關鍵字
    # page: 搜尋結果第N頁
    url = f'https://www.coupang.com/np/search?q={search_keyword}' + \
          f'&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={str(page)}' \
         + '&rocketAll=false&searchIndexingToken=&backgroundColor='

    # 取得網頁資料
    checkSuccess = False
    tryNums = 0
    while not checkSuccess:
        response, checkSuccess = checkConnect(url, headers)
        if not checkSuccess:
            if tryNums == 3:
                break
            tryNums += 1
            print('失敗,暫停10秒')
            time.sleep(10)

    # 防呆
    if tryNums == 3:
        print('下載失敗3次 結束程式')
        break

    # 轉為soup格式
    soup = BeautifulSoup(response.text, 'html.parser')

    # 搜尋商品列表結果
    productList = soup.select('ul.search-product-list li')
    for product in productList:
        # 商品id
        product_tag = product.select_one('a')
        product_id = product_tag.get('data-product-id')
        data_item_id = product_tag.get('data-item-id')
        data_vendor_item_id = product_tag.get('data-vendor-item-id')
        # 商品圖片
        product_img_url = product.select_one('img.search-product-wrap-img').get('src')
        if 'blank1x1.gif' in product_img_url:
            product_img_url = product.select_one('img.search-product-wrap-img').get('data-img-src')
        # 商品描述
        product_descriptions = product.select_one('div.descriptions-inner')
        # 商品名稱
        product_name = product_descriptions.select_one('div.name').get_text().strip()
        # 商品價格
        product_price = product_descriptions.select_one('strong.price-value').get_text().strip()
        # 商品詳情圖片
        detail_url = f'https://www.coupang.com/vp/products/{product_id}/items/{data_item_id}/vendoritems/{data_vendor_item_id}'
        detail_img, checkSuccess = detail_img_handler(detail_url, headers)
        print("product_name : " + product_name)
        print("product_price : " + product_price)
        print("product_img_url : " + "https:" + product_img_url)
        print("detail_img : " + str(detail_img) + '\n')
        # 避免請求過多
        time.sleep(4)
