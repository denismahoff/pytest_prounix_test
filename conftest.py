import uuid
import pytest
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
# from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
# from unicodedata import decimal

# from unicodedata import decimal

supported_browsers = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox
}

supported_languages = {
    'العربيّة': 'ar',
    'català': 'ca',
    'česky': 'cs',
    'dansk': 'da',
    'Deutsch': 'de',
    'British English': 'en-gb',
    'Ελληνικά': 'el',
    'español': 'es',
    'suomi': 'fi',
    'français': 'fr',
    'italiano': 'it',
    '한국어': 'ko',
    'Nederlands': 'nl',
    'polski': 'pl',
    'Português': 'pt',
    'Português Brasileiro': 'pt-br',
    'Română': 'ro',
    'Русский': 'ru',
    'Slovensky': 'sk',
    'Українська': 'uk',
    '简体中文': 'zh-hans'
}


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='ru',
                     help=f"""Choose language: {', '.join(supported_languages.keys())}""")


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    language = request.config.getoption("language")
    browser = None
    if browser_name not in supported_browsers:
        joined_browsers = ', '.join(supported_browsers.keys())
        raise pytest.UsageError(f"--browser_name is invalid, supported browsers: {joined_browsers}")

    if language in supported_languages.values():
        if browser_name == 'chrome':
            options = Options()
            options.add_experimental_option('prefs', {'intl.accept_languages': language})
            browser = webdriver.Chrome(options=options)
        elif browser_name == 'firefox':
            fp = webdriver.FirefoxProfile()
            fp.set_preference("intl.accept_languages", language)
            browser = webdriver.Firefox(firefox_profile=fp)
    else:
        joined_languages = ', '.join(supported_languages.keys())
        raise pytest.UsageError(f"--language is invalid, supported languages: {joined_languages}")
    # options
    browser.maximize_window()
    browser.implicitly_wait(15)

    yield browser
    random_filename = str(uuid.uuid4()) + ".png"
    screen_path = f'C:\\Users\\Admin\\Desktop\\{random_filename}'
    browser.save_screenshot(screen_path)
    print(f"Скриншот сохранен по пути: {screen_path}")
    print("\nquit browser..")
    browser.quit()


def passing_basic_auth(browser):
    url_auth = 'https://proandi-easy:W53W8tIe@easy-stage.wirfoerdern.net'
    browser.get(url_auth)
    try:
        browser.find_element(By.CSS_SELECTOR, '#login_box_header')
    except NoSuchElementException:
        raise AssertionError('Не пройдена basic auth!')


def login_to_web_personal_account(browser):
    url_login = 'https://easy-stage.wirfoerdern.net/'
    login = 'testantragsteller.Denis.am@example.com'
    password = 'EasyStage2023Test'
    browser.get(url_login)
    browser.find_element(By.ID, 'username').send_keys(login)
    browser.find_element(By.ID, 'password').send_keys(password)
    browser.find_element(By.ID, 'login').click()
    try:
        browser.find_element(By.CSS_SELECTOR, '.box.info.no-editable')
    except NoSuchElementException:
        raise AssertionError('Не удалось залогиниться!')


def select_draft_offer(browser):
    browser.find_element(By.CSS_SELECTOR,
                         '.box.text-center.d-block.edit-box.test_dashboard_neuen_antrag_anlegen').click()
    ar_url = browser.current_url
    er_url = 'https://easy-stage.wirfoerdern.net/foerderantrag-erstellen/'
    try:
        assert ar_url == er_url
    except AssertionError:
        print(f"Ожидаемый URL: {er_url}, текущий URL: {ar_url}")
        raise


def open_easy_funding_offer(browser):
    browser.find_element(By.ID, 'FoerderfinderFoerderangeboteTable_action_0').click()


def open_easy_automation_funding_offer(browser):
    browser.find_element(By.ID, 'FoerderfinderFoerderangeboteTable_action_1').click()
    ar_span_offer = browser.find_element(By.CSS_SELECTOR, '.page_main_h2.text-break').text
    er_span_offer = 'EASY - Testautomatisierung'
    try:
        assert ar_span_offer == er_span_offer
    except AssertionError:
        print(f"Ожидался текст: '{er_span_offer}', фактический текст: '{ar_span_offer.text}'")
        raise


def open_free_space2023_offer(browser):
    browser.find_element(By.ID, 'FoerderfinderFoerderangeboteTable_action_2').click()


def open_spending_and_financing_plan(browser):
    browser.find_element(By.ID, 'step_finanz_panel_header').click()
    try:
        browser.find_element(By.CSS_SELECTOR, '.p-0.table-scrollable.kf-box')
    except NoSuchElementException:
        raise AssertionError('Поле №3 "План расходов и финансирования" не найдено!')


# def my_func(sum:int, cent:int) -> str:
#     sum = f"{sum:,}".replace(",", ".")
#     return f"{sum},{cent} €"


def add_material_costs(browser, required_value):
    btn_new_pos_mat_costs_add = browser.find_element(By.ID, '1005_add')
    btn_new_pos_mat_costs_add.click()
    browser.find_element(By.ID, '1005_new_position_bezeichnung').send_keys('test_example_1')
    browser.find_element(By.ID, '1005_new_position_bezeichnung').send_keys(Keys.TAB)
    input_element = browser.find_element(By.ID, '1005_new_position_wert')
    input_element.send_keys(required_value)
    btn_new_pos_mat_costs_save = browser.find_element(By.ID, '1005_new_position_save')
    btn_new_pos_mat_costs_save.click()
    time.sleep(3)
    text_input = browser.find_element(By.XPATH, '//*[@id="1005"]/div/div/div[1]/div[3]/span').text  # 10.000,00 €
    text_input = text_input.replace(" €", "", 1)  # 10.000,00
    text_input = text_input.replace(".", "")  # 10000,00

    assert text_input == required_value, \
        'Введённое значение не соответствует значению в mat costs'
