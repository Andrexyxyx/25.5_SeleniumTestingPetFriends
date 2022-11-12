import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.Selenium_Settings import valid_email, valid_password


@pytest.fixture(autouse=True)
def testing():
    driver = webdriver.Chrome('C:\Documents\chromedriver.exe')
    # Переходим на страницу авторизации
    driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    yield driver
    driver.quit()


def test_show_my_pets(testing):
    driver = testing
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, "h1").text == "PetFriends"

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-title')
    print(len(names))
    print(type(names))
    descriptions = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-text')
    for i in range(len(names)): #Можно взять любой элемент для перебора, т.к. количество имен равно количеству описаний и фото
        assert images[i].get_attribute('src') != '' # Ищем во всех фото атбритут src, который должен быть при прикреплении фото
        assert names[i].text != '' # Проверяем, что поле с именем у всех не пустое
        assert descriptions[i].text != '' # Проверяем, что поле с описанием у всех не пустое
        assert ', ' in descriptions[i] # Находим разделяющую запятую в описаниях
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0 # Проверяем что во всех карточках питомцев есть и возраст и тип животного
        assert len(parts[1]) > 0


def test1_amount_my_pets(testing):
    '''Проверка, что на странице со списком питомцев пользователя присутствуют все питомцы'''
    driver = testing
    # Кликаем на ссылку "Мои питомцы"
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()
    # Ожидаем в течение 5 секунд драйвером driver появления элемента с локатором '#all_my_pets table tbody tr'
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#all_my_pets table tbody tr')))

    # Узнаем количество питомцев по количеству строк с питомцами в таблице
    my_pets_table = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets table tbody tr')
    # Узнаем количество питомцев, которое отображается напротив слова "Питомцев: "
    my_pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(":")[1]
    # Проверяем, что количество строк с питомцами равно числу питомцев, указанному напротив слова "Питомцев: "
    assert len(my_pets_table) == int(my_pets_number)


def test2_half_card_with_photo(testing):
    '''Проверка, что на странице со списком питомцев пользователя хотя бы у половины питомцев есть фото'''
    driver = testing
    # Кликаем на ссылку "Мои питомцы"
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()

    # Узнаем количество фотографий возможных питомцев, обращаясь к тегу фотографий
    images_potential = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    # Подсчитываем количество питомцев, у которых реально есть фотография (по заполнению атрибута "src")
    images_fact = 0
    for i in range(len(images_potential)):
        if images_potential[i].get_attribute('src') != "":
            images_fact = images_fact + 1
    assert int(images_fact) >= (len(images_potential))/2


def test3_name_age_type_of_pets(testing):
    '''Проверка, что на странице со списком питомцев у всех питомцев есть имя, возраст и порода'''
    driver = testing
    # Кликаем на ссылку "Мои питомцы"
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()
    driver.implicitly_wait(5)

    # Выбираем списки имен, типов и возрастов животных
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    type_of_animal = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    age_of_animal = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    # Проверяем, что в списках нет пустых значений
    for i in range(len(names)):
        assert names[i].text != ''
        assert type_of_animal[i].text != ''
        assert age_of_animal[i].text != ''


def test4_different_names_of_pets(testing):
    '''Проверка, что на странице со списком питомцев у всех питомцев разные имена'''
    driver = testing
    # Кликаем на ссылку "Мои питомцы"
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()

    # Выбираем список имен животных
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    # Собираем имена животных в список
    names_list = [] # Пустой список для сборки имен животных
    for i in range(len(names)):
        names_list.append(names[i].text)
    assert len(names_list) == len(set(names_list))


def test5_recurring_pets(testing):
    '''Проверка, что на странице со списком питомцев в списке нет повторяющихся питомцев'''
    driver = testing
    # Кликаем на ссылку "Мои питомцы"
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()

    # Выбираем список имен животных
    data_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Собираем данные о питомцах в список
    data_pets_list = [] # Пустой список для сборки данных о животных
    for i in range(len(data_pets)):
        data_pets_list.append(data_pets[i].text)
    assert len(data_pets_list) == len(set(data_pets_list))




