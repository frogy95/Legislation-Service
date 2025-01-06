import requests

def urlopen_hira():
    url = "https://biz.hira.or.kr/qya/bbs/selectComBbsList.ndo"

    # 개발자 도구에서 확인한 Content-Type, 인코딩 정보 등을 그대로 입력
    headers = {
        "Content-Type": "text/xml; charset=UTF-8",
        "Accept": "application/xml, text/xml, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache, no-store",
        "Connection": "keep-alive",
        "Content-Length": "927",
        "Cookie": "WT_FPC=id=2c74c0528e558c279011725513957868:lv=1735628207366:ss=1735628207366; WMONID=QFHiofJgkm0; BIZINTERSESSION=g5Ukf3GsE9b3ZhDkhfamL1mjt1ccVgqGF2cHCvSDASZmg0dWZ05d!-81161013; JSESSIONID=null; WT_FPC=id=2c74c0528e558c279011725513957868:lv=1735628207366:ss=1735628207366",
        "Expires": "-1",
        "Host": "biz.hira.or.kr",
        "If-Modified-Since": "Thu, 01 Jun 1970 00:00:00 GMT",
        "Origin": "https://biz.hira.or.kr",
        "Pragma": "no-cache",
        "Referer": "https://biz.hira.or.kr/popup.ndo?formname=qya_bizcom%3A%3AInfoBank.xfdl&framename=InfoBank",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    # 실제 Request Payload가 이런 식의 문자열 구조일 거야.
    # 여기서는 네트워크 탭에서 확인한 'SSV:utf-8' 이후 내용을 그대로 복붙하는 게 중요.
    payload = """SSV:utf-8JSESSIONID=nullBIZINTERSESSION=WT_FPC=id=2c74c0528e558c279011725513957868:lv=1735628207366:ss=1735628207366WMONID=QFHiofJgkm0browserType=ChromeosVersion=Windows 10navigatorName=ChromenavigatorVersion=131Dataset:dsParam_RowType_brdTyBltNo:STRING(256)bltNo:STRING(256)totCnt:STRING(256)currentPage:STRING(256)recordCountPerPage:STRING(256)firstIndex:STRING(256)lastIndex:STRING(256)bbsId:STRING(256)cbSearchCnd:STRING(256)edSearchWrd:STRING(256)nttId:STRING(256)atchFileId:STRING(256)codeId:STRING(256)catType01Val:STRING(256)catType02Val:STRING(256)catType03Val:STRING(256)N120020BBSMSTR_000000000675allDataset:gdsCurrentMenu_RowType_menuId:STRING(256)menuNm:STRING(256)urlDtlAddr:STRING(256)sysCd:STRING(256)scnId:STRING(256)locToDown:STRING(256)hiSysCd:STRING(256)bPopupYn:STRING(256)seAdtYn:STRING(256)formId:STRING(256)winId:STRING(256)params:STRING(256)"""

    response = requests.post(url, headers=headers, data=payload.encode("utf-8"), verify=False)

    return response.text