from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from urllib.parse import quote
from time import sleep
import sys

if len(sys.argv) <= 3:
    print(sys.argv[0], '[Username] [Password] [曜日] ([号館])')
    # TODO:[Day:today,tommorow,mon,thu,wed,...]'
    exit(-1)

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
YOUBI = sys.argv[3]
GOUKAN = '2号館'
if len(sys.argv) > 4:
    GOUKAN = sys.argv[4]

LIBAREA = '図書館エリア'
CAMPUS = '千住'

try:
    assert(YOUBI[0] in '月火水木金土')
    assert(YOUBI.endswith('曜日'))
    assert(len(YOUBI) == 3)
except AssertionError:
    print('"月曜日"のように入力してください')
    exit(-1)

KENSUU = '//*[@id="opac_print_target_384catdbl"]/div[3]/div[3]/select'

YOYAKU_AREA_UNFORMATTED = r'//*[@id="opac_print_target_384catdbl"]/div[3]/div[5]/table/tbody/tr[{}]/td[9]'

YOYAKU_BUTTON_UNFORMATTED = r'//*[@id="orderRSV_ButtonBB200838%02d_384catdbl{}"]'
# YOYAKU_BUTTON_UNFORMATTED = r'//*[@id="orderRSV_ButtonBB20083858_384catdbl{}"]'
#                               //*[@id="orderRSV_ButtonBB20083856_384catdbl0"]
#                               //*[@id="orderRSV_ButtonBB20083854_384catdbl0"]

LOGIN_USER = '/html/body/div/div/div/div[2]/form/table/tbody/tr[1]/td/input'
LOGIN_PASS = '/html/body/div/div/div/div[2]/form/table/tbody/tr[2]/td/input'

LOGIN_BUTTON = '/html/body/div/div/div/div[2]/form/div/a[1]/input'

ANOTHER_WINDOW_OK = '//*[@id="popup"]/table/tr[2]/td[1]/input'

MOUSIKOMI = '/html/body/div/div/table/tbody/tr[1]/td/table/tbody/tr[6]/td/div/div'

KETTEI = '/html/body/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/form/table/tbody/tr[10]/td/div/div/a[1]/img'

IRAIBANGOU = '/html/body/div/div/table/tbody/tr/td/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[3]/div/div/span/strong'

# EEYOUBI=r'%25E7%2581%2p5AB%25E6%259B%259C%25E6%2597%25A5'
# QUERY=r'=%25E5%259B%25B3%25E6%259B%25B8%25E9%25A4%25A8%25E3%2582%25A8%25E3%2583%25AA%25E3%2582%25A2%25205%25E5%258F%25B7%25E9%25A4%25A8'+EEYOUBI

QUERY = quote(quote(LIBAREA+' '+GOUKAN+' '+YOUBI+' '+CAMPUS))

LIB_URL = r'https://tdu-lib.mrcl.dendai.ac.jp/index.php?action=pages_view_main&active_action=v3search_view_main_init&op_param=words='+QUERY + \
    '%26sortkey%3D%26sorttype%3D%26listcnt%3D%26startpos%3D%26fromDsp%3Dcatsre%26searchDsp%3Dcatsre%26initFlg%3D_RESULT_SET%26hitcnt%3D%26searchsql%3D%26searchhis%3D%26akey%3D%26fct_gcattp%3D%26fct_auth%3D%26fct_pub%3D%26fct_year%3D%26fct_cls%3D%26fct_sh%3D%26fct_lang%3D%26fct_holar%3D%26fct_tag%3D%26fct_campus%3D%26fct_range_year%3D%26fct_user1%3D%26fct_user2%3D%26fct_user3%3D%26fct_user4%3D%26fct_user5%3D&block_id=384&tab_num=0&search_mode=simple#search_list-0'

driver = webdriver.Chrome()

driver.maximize_window()

driver.get(LIB_URL)

sleep(3)

# https://yuki.world/selenium-select/
kensuu = driver.find_element_by_xpath(KENSUU)
select = Select(kensuu)
select.select_by_index(len(select.options)-1)

sleep(5)

print('Searching Vacant...')
for i in range(100):
    e = driver.find_element_by_xpath(
        YOYAKU_AREA_UNFORMATTED.format(str(2+i)))
    print(i, e.text)
    if e.text != '0件':
        continue
    print('found at', i)

    # Brute BUTTON XPATH
    for j in range(100):
        try:
            driver.find_element_by_xpath(
                (YOYAKU_BUTTON_UNFORMATTED % (j)).format(str(i))).click()
            break
        except NoSuchElementException:
            pass
    else:
        print('Error')
        exit(-1)
    break
else:
    print('Full')
    # TODO:GO NEXT PAGE
    exit(-1)

driver.find_element_by_xpath(LOGIN_USER).send_keys(USERNAME)  # username
driver.find_element_by_xpath(LOGIN_PASS).send_keys(PASSWORD)  # password

driver.find_element_by_xpath(LOGIN_BUTTON).click()

sleep(8)

driver.find_element_by_xpath(ANOTHER_WINDOW_OK).click()

sleep(8)

driver.switch_to_window(driver.window_handles[-1])

# https://qiita.com/DNA1980/items/528ff6269986b262acdc
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

sleep(1)

driver.find_element_by_xpath(MOUSIKOMI).click()


driver.find_element_by_xpath(KETTEI).click()

print('依頼番号', driver.find_element_by_xpath(IRAIBANGOU).text)


# MEMO

# YOYAKU AREA
# 1
# //*[@id="opac_print_target_384catdbl"]/div[3]/div[5]/table/tbody/tr[2]/td[9]
# //*[@id="opac_print_target_384catdbl"]/div[3]/div[4]/table/tbody/tr[2]/td[9]
# //*[@id="opac_print_target_384catdbl"]/div[3]/div[5]/table/tbody/tr[2]/td[9]
# //*[@id="opac_print_target_384catdbl"]/div[3]/div[5]/table/tbody/tr[2]/td[9]
# 2
# //*[@id="opac_print_target_384catdbl"]/div[3]/div[5]/table/tbody/tr[3]/td[9]
# //*[@id="opac_print_target_384catdbl"]/div[3]/div[5]/table/tbody/tr[3]/td[9]

# YOYAKU BUTTON
# 1 //*[@id="orderRSV_ButtonBB20083858_384catdbl0"]
# 2 //*[@id="orderRSV_ButtonBB20083858_384catdbl1"]
# 4 //*[@id="orderRSV_ButtonBB20083858_384catdbl4"]


'''
<a href="JavaScript:chkvalidate()" onclick="if(!checkSubmit()){return false};document.svcrsvform.action='/webopac/rsvchk.do';

								" class="btn opac_imgbtn" onmouseover="imgChange2On(this)" onmouseout="imgChange2Off(this)">
<img src="https://lib.mrcl.dendai.ac.jp/webopac/image/default/ja/btn_dg_moudhikomi_off_140-30.png" title="申込" alt="申込"></a>
'''
# body > div > div > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(7) > td > div > div > a

'''
<div class="opac_footer_btn_area">
					<a href="JavaScript:chkvalidate()" onclick="if(!checkSubmit()){return false};document.svcrsvform.action='/webopac/rsvchk.do';

								" class="btn opac_imgbtn" onmouseover="imgChange2On(this)" onmouseout="imgChange2Off(this)">
<img src="https://lib.mrcl.dendai.ac.jp/webopac/image/default/ja/btn_dg_moudhikomi_off_140-30.png" title="申込" alt="申込"></a>
					&nbsp;&nbsp;&nbsp;&nbsp;
					</div>
'''
# mousikomi

# '/html/body/div/div/table/tbody/tr[1]/td/table/tbody/tr[6]/td/div/div/a/img'
# /html/body/div/div/table/tbody/tr[1]/td/table/tbody/tr[6]/td/div/div/a

# driver.find_element_by_xpath(MOUSIKOMI).click()
# driver.find_element_by_name('申込').click()
# driver.find_elements_by_css_selector
# driver.findElement(By.linkText('申込')).click()
# opac_imgbtns = driver.find_elements_by_class_name('opac_imgbtn')
# print(opac_imgbtns)
# opac_imgbtns[0].click()
# driver.find_element_by_link_text('申込').click()
