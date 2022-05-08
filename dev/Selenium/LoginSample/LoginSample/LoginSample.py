#import traceback
#from selenium import webdriver



#try:
#    # Create webdriver instance uisng chrome
#    driver = webdriver.Chrome( "C:/selenium/chromedriver" )
    
#    # Load Kinnouke login page
#    driver.get( "https://www.e4628.jp/" )
    
#    # Fill login form
#    company_id_element =driver.find_element_by_name("y_companycd")
#    company_id_element.send_keys("company")

#    login_id_element =driver.find_element_by_name("y_logincd")
#    login_id_element.send_keys("name")

#    password_element = driver.find_element_by_name("password")
#    password_element.send_keys("pass")

#    #driver.save_screenshot("c:/login.png")

#    # Push "Login" button
#    element = driver.find_element_by_id("id_passlogin")
#    element.click()
    

#    elm = driver.find_element_by_link_text("ログイン情報を保存する")

#    #driver.save_screenshot("c:/main.png")


#    # Find and Click "Clock out" button
#    #clockout_element = driver.find_element_by_name("_stampButton")
#	#clockout_element.click()
    
#    # Close web browser
#    driver.quit()

#except:
#    traceback.print_exc()



from selenium import webdriver
 
#ChrmoeDriverサーバーのパスを引数に指定しChromeを起動
driver = webdriver.Chrome("C:/selenium/chromedriver")
#指定したURLに遷移する
driver.get("https://www.google.co.jp/webhp?hl=ja&sa=X&ved=0ahUKEwiOioXq2ZPZAhVKoZQKHa9zD3IQPAgD")
#リンクテキスト名が"Gmail"の要素を取得
element = driver.find_element_by_xpath("//*[@id=\"gbw\"]/div/div/div[1]/div[2]/a")
#Gmailのリンクをクリック
element.click()