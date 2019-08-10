import time

from bot import DNSExitBot
from crack_captcha import CrackCaptcha
import mapping

if __name__ == '__main__':
    b = DNSExitBot()
    cc = CrackCaptcha()
    b.open_page('https://www.dnsexit.com/Direct.sv?cmd=signup')
    b.type_text(mapping.register_page['first_name'], 'asdasdasd')
    b.type_text(mapping.register_page['last_name'], 'asdasdasd')
    b.type_text(mapping.register_page['organization'], 'asdasdasd')
    b.type_text(mapping.register_page['address'], 'asdasdasd')
    b.type_text(mapping.register_page['city'], 'asdasdasd')
    b.type_text(mapping.register_page['state'], 'asdasdasd')
    b.select(mapping.register_page['country'], 'United States')
    b.type_text(mapping.register_page['zip'], '123456')
    b.type_text(mapping.register_page['email'], 'asdasdasd@asdasd.co')
    b.type_text(mapping.register_page['email_again'], 'asdasdasd@asdasd.co')
    b.type_text(mapping.register_page['phone'], '+1 123 123 12 12')
    b.type_text(mapping.register_page['fax'], '+1 123 123 12 12')
    b.type_text(mapping.register_page['userid'], 'lkjlkjlkjfff')
    b.type_text(mapping.register_page['password'], 'lkjlkjlkjfff')
    b.type_text(mapping.register_page['password_again'], 'lkjlkjlkjfff')
    b.select(mapping.register_page['secret_question'], 'City of Birth')
    
    b.type_text(mapping.register_page['secrect_answer'], 'secrect_answer')
    
    while True:
        try:
            temp_img = str(time.time()) + '.png'
            b.elem_screenshot(mapping.register_page['authidimg'], temp_img)
            authcode = cc.crack_it(temp_img)
            break
        except:
            b.driver.refresh()
    b.type_text(mapping.register_page['vfy'], authcode)
    b.click(mapping.register_page['Submit'])
    time.sleep(99999)

    
    
    

    
    
