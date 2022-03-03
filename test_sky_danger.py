from check_danger import check_text_is_danger, check_image_is_danger


def test_check_text_is_danger():
    not_danger_text1 = """Шановні жителі Славутича! Тероборона міста ще раз звертається до вас! Не виходьте в 
    навколишній ліс! Не пересувайтесь по ґрунтових дорогах! Це небезпечно для вашого життя!! ❗️Територія 
    замінована!!! Будьте відповідальними! """
    not_danger_text2 = """Графік роботи аптек Славутича 02.03.2022:
    1. Аптека оптових цін (навпроти Сільпо) з 9-00 до 14-00
    2. Аптека Біла Ромашка (Фора) з 9-00 до 16-00
    3. Аптека Медсервіс з 08-00 до 17-00
    4. АНЦ (Люкс) з 9-00 до 16-00
    5. Аптека Бам з 9-00 до 16-00"""
    assert not check_text_is_danger(not_danger_text1)
    assert not check_text_is_danger(not_danger_text2)
    assert check_text_is_danger("УВАГА! ПОВІТРЯНА тривога. Всі в укриття!")
    assert not check_text_is_danger("ВІДБІЙ ПОВІТРЯНОЇ тривоги")


def test_check_image_is_danger():
    assert check_image_is_danger("static/danger.jpg")
    assert not check_image_is_danger("static/not_danger.jpg")
    assert not check_image_is_danger("static/not_danger_at_all.jpg")
