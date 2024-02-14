from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# import pyperclip

def getBreedpower():

  # 创建 Chrome 无头浏览器选项
  chrome_options = Options()
  chrome_options.add_argument('--headless')  # 设置无头模式

  # 初始化 Chrome 浏览器对象
  # browser = webdriver.Chrome(options=chrome_options, service=Service(executable_path='/Users/cjmac/Downloads/chromedriver-mac-x64/chromedriver'))
  browser = webdriver.Chrome(options=chrome_options)

  # 打开网页
  browser.get('https://palworldgg.com/zh/pals/')

  # 获取页面标题并打印
  print(browser.title)

  # 复制源码
  # print(browser.page_source)
  # pyperclip.copy(browser.page_source)


  petsList = browser.find_element(By.CSS_SELECTOR, '.el-scrollbar__view')
  pets = petsList.find_elements(By.CSS_SELECTOR, '.data-card')

  list = []
  for pet in pets:
    obj = {
      'href': pet.get_attribute('href'),
      'name': pet.find_element(By.CSS_SELECTOR, '.font-bold').text,
      'no': pet.find_element(By.CSS_SELECTOR, '.text-gray-500').text.split('.')[1],
    }
    list.append(obj)


  def getBreedpower(href):
    browser.get(href)
    breedInfo = browser.find_elements(By.CSS_SELECTOR, '.data-card-no-bg.mt-4[data-astro-cid-jk3orfdl]')[4]
    breedItem = breedInfo.find_element(By.CSS_SELECTOR, '.stats-item')
    # print(breedItem.find_element(By.CSS_SELECTOR, '.stats-name').text, breedItem.find_element(By.CSS_SELECTOR, '.stats-value').text)
    return breedItem.find_element(By.CSS_SELECTOR, '.stats-value').text


  # getBreedpower('https://palworldgg.com/zh/pals/suzaku/')

  for pet in list:
    pet['breedpower'] = getBreedpower(pet['href'])

  # for pet in list:
  #   print(pet)

  # 关闭浏览器
  browser.quit()
  return list
