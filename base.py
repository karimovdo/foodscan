import os
from PIL import Image
import pytesseract
import re
import pandas as pd
import cv2
import numpy as np

#  обработка изображения, наклон

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    rect = cv2.minAreaRect(coords)
    angle = rect[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    if abs(angle) < 1 or abs(angle) > 45:
        return image

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    corrected_img = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return corrected_img

def preprocess_image(image_path):
    # изменение размера 
    img = cv2.imread(image_path)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # в градации серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # бинаризация
    binarized = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
    
    # удалениие шума
    kernel = np.ones((1, 1), np.uint8)
    denoised = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    
    #  наклон
    deskewed = deskew(denoised)
    
    # сохранение 
    processed_image_path = 'processed_' + os.path.basename(image_path)
    cv2.imwrite(processed_image_path, deskewed)
    
    return processed_image_path


# рабочая папка
os.chdir('c:/Users/Денис/Desktop/python/foodscan/')
folder_path = '1'

# расширения 
extensions = ('.png', '.tiff', '.jpeg', '.jpg')

all_text_rus = ""
# в начале на рурском смотрим
for filename in os.listdir(folder_path):
    if filename.endswith(extensions):
        image_path = os.path.join(folder_path, filename)
        try:
            processed_image_path = preprocess_image(image_path)
            text = pytesseract.image_to_string(Image.open(processed_image_path), lang='rus')
            
            all_text_rus += text + "\n"  
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")

all_text_eng = ""
# потом на англ
for filename in os.listdir(folder_path):
    if filename.endswith(extensions):
        image_path = os.path.join(folder_path, filename)
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='eng')
            all_text_eng += text + "\n"  
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")

# переаодим в нижний регистр
all_text_rus = all_text_rus.lower()  
all_text_eng = all_text_eng.lower()  
# подгружаем бренды для поиска
brands_df = pd.read_csv('brand.csv')
brands = brands_df['brand'].tolist()

results_df = pd.DataFrame(columns=['Brand'])
found_brand = None

for brand in brands:
    brand_lower = brand.lower()
    if brand_lower in all_text_rus or brand_lower in all_text_eng:
        found_brand = brand  
        break

temp_df = pd.DataFrame([{'Brand': found_brand if found_brand else 'бренд не определен'}])
results_df = pd.concat([results_df, temp_df], ignore_index=True)


# словарь категорий с ключевыми словами
# categories = {
#     1: "каши|каша|сухие каши|мюсли|рис для детского питания|сухие макаронные изделия",
#     2: "молочный продукт|овсяная каша|рисовый пудинг",
#     3.1: "фруктовое пюре|фруктовый коктейль|фруктовый десерт",
#     3.2: "овощное пюре|пюре овощное|картофельное пюре",
#     4.1: "овощи|бобовые|каши|крахмалистые продукты",
#     4.2: "сыр",
#     4.3: "источник белка",
#     5.1: "сушёные фрукты|сушеные фрукты",
#     6: "ингредиенты|оливковое масло|бульонные кубики",
#     7: "кондитерские изделия|шоколад|конфеты|лакрица",
#     8: "напитки|фруктовый сок"
# }

categories = {
    1: "сухие каши|крахмалистые продукты|кашка|мюсли|бибикаша|рис|каша|каши",
    2: "молочные продукты|йогурт|кефир|ряженка|йогурт питьевой|молоко|молочный коктейль|молочная смесь|молочко|смесь|молочный пудинг|молочная|кисломолочный продукт|биолакт|бифидокефир|творог",
    3.1: "фруктовое пюре|фруктовый коктейль|фруктовый десерт|пудинг|фруктовый пудинг|фруктовое желе|фруктово-ягодное пюре|фруктово-овощное пюре|фруктовое пюре яблоко|фруктовое пюре груша|фруктовое пюре яблоко-груша-персик|фруктовое пюре яблоко-черная смородина-ежевика|фруктовое пюре яблоко-клубника-земляника-клюква|фруктовое пюре яблоко-малина-шиповник|фруктовое пюре яблоко-ежевика-малина|фруктовое пюре яблоко-персик|фруктовое пюре яблоко-груша-банан-манго|со злаками яблоко-черника-земляника|фруктово-овощное пюре яблоко-тыква-персик-банан|фруктовое пюре яблоко-творог со вкусом печенья|фруктово-ягодное пюре яблоко-клубника-малина|мультифрукт|пюре яблоко-банан-печенье|пюре яблоко-банан-клубника-киви|пюре банан|фруктовый батончик|пюре со сливками|фруктовый салатик|пюре яблоко и голубика|фруктовое пюре чернослив|фруктовые пюре пауч|фруктово-ягодный микс",
    3.2: "овощное пюре|картофельное пюре|овощное пюре морковь|овощное пюре цветная капуста|овощное пюре брокколи|овощное пюре тыква|овощное пюре кабачок|пюре овощной микс|крем-суп овощной",
    4.1: "овощи|бобовые|специализированное лечебное питание для детей от 1 года до 10 лет|полноценная сбалансированная сухая питательная смесь|питание|продукт|низкоаллергенные|овощные|цельнозерновые|лакомые|специализированный продукт детского диетического лечебного питания|мини-хлебцы мультизлаковые банан-груша-яблоко|мини-хлебцы рисовые|мини-хлебцы рисовые с грушей|снек|экструдированные|экструдированные звездочки|батончик|",
    4.2: "сыр агуша",
    4.3: "макарошки с говядинкой|растительно-мясное пюре|консервы растительно-мясные|фрикадельки|суп-пюре с фрикадельками|картофель и морковь с цыплёнком|картофель с овощами и индейкой|овощное рагу с цыплёнком|овощной суп с цыплёнком|овощной суп с индейкой|пюре рис с курочкой|сочное рагу с говядиной|сливочная курочка с овощами|нежное соте из индеечки|овощи с фрикадельками из говядины|паста с овощами и говядиной|рагу из свинины и говядины с овощами|рагу из индейки с рисом|овощи с фрикадельками из говядины|лакомство по-итальянски",
    4.4: "кролик с картофелем|рагу из говядины|мясное рагу|пюре из цыпленка с телятиной|пюре из говядины|пюре из телятины|пюре из курицы|пюре из индейки|пюре из кролика|говядина по-домашнему с морковью",
    4.5: "кролик|ягнёнок|мясное пюре цыпленок-говядина|мясное пюре|говядина|индейка|цыпленок|монопюре из кролика|монопюре из семги|монопюре из хека|монопюре из цыпленка|монопюре из говядины|монопюре из индейки",
    5.1: "сушёные фрукты|чернослив|яблочные кусочки|яблочно-абрикосовая пастила|яблочно-персиковая пастила|яблочные чипсы|яблочня пастила",
    5.2: "печенье|детское печеньице|сашет|мультизлаковые хлебцы|с железом|с кальцием",
    6: "ингpедиенты",
    7: "шоколад|молочный шоколад|детский шоколад",
    8: "напитки|фруктовый сок|сок груша|сок зелёное яблоко|сок яблоко прямого отжима|нектар морковь с мякотью|сок яблоко-абрикос|сок яблоко-вишня|сок|нектар|сок яблоко-банан|с мякотью|сок яблоко-виноград|осветлённый|сок яблоко-ежевика|сок яблоко-клюква|вода детская|смузи фруктовый микс|смузи"
}
# ищем категорию
def categorize_text(text, categories):
    for cat, keywords in categories.items():
        if re.search(keywords, text.lower()):
            return cat
    return "Категория не определена"

results_df['Category'] = categorize_text(all_text_rus, categories)

import pandas as pd

# словарь для соответствиякатегорий 
category_descriptions = {
    "1": "Сухие каши и крахмалистые продукты",
    "2": "Молочные продукты",
    "3.1": "Фруктовые пюре/коктейли и фруктовые десерты",
    "3.2": "Овощные пюре",
    "4.1": "Поликомпонентные продукты/блюда: сочетания крахмалистых (крупяных) продуктов, овощей, молочных продуктов и/или белка",
    "4.2": "Сыр",
    "4.3": "Поликомпонентные продукты/блюда: сочетания крахмалистых (крупяных) продуктов, овощей, молочных продуктов и/или белка",
    "4.4": "Поликомпонентные продукты/блюда: сочетания крахмалистых (крупяных) продуктов, овощей, молочных продуктов и/или белка",
    "4.5": "Поликомпонентные продукты/блюда: сочетания крахмалистых (крупяных) продуктов, овощей, молочных продуктов и/или белка",
    "5.1": "Сухие закуски и перекусы",
    "5.2": "Печенье",
    "6": "Ингредиенты",
    "7": "Кондитерские изделия",
    "8": "Напитки"
}

results_df['Category Description'] = results_df['Category'].apply(lambda x: category_descriptions.get(str(x), "Неизвестная категория"))

# ищем калории
def find_kcal(text):
    kcal_match = re.search(r"(\d+)\s*ккал", text)
    if kcal_match:
        return int(kcal_match.group(1))
    
    kj_kcal_match = re.search(r"(\d+)(?:/(\d+))?\s*(?:кдж/ккал|кджккал)", text, re.IGNORECASE)
    if kj_kcal_match:
        return int(kj_kcal_match.group(1))
    
    kj_match = re.search(r"(\d+)\s*кдж", text, re.IGNORECASE)
    if kj_match:
        return int(kj_match.group(1)) / 4.184

    return None

def find_kcal_eng(text):
    kcal_match = re.search(r"(\d+)\s*kcal", text, re.IGNORECASE)
    if not kcal_match:
        kj_match = re.search(r"(\d+)\s*kj", text, re.IGNORECASE)
        if kj_match:
            return int(kj_match.group(1)) / 4.184
        return None
    return int(kcal_match.group(1))

kcal_value = find_kcal(all_text_rus)

if kcal_value is None:
    kcal_value = find_kcal_eng(all_text_eng)

results_df['kcal'] = [kcal_value if kcal_value is not None else 'значение не найдено']
# натрий
def find_sodium(text_rus, text_eng):
    sodium_rus = re.search(r"натрий\D*(\d+)", text_rus, re.IGNORECASE)
    if sodium_rus:
        return int(sodium_rus.group(1))
    
    sodium_eng = re.search(r"sodium\D*(\d+)", text_eng, re.IGNORECASE)
    if sodium_eng:
        return int(sodium_eng.group(1))
    
    return 'не указано'

sodium_value = find_sodium(all_text_rus, all_text_eng)
results_df['Sodium'] = [sodium_value]
# белок
def find_protein(text_rus, text_eng):
    protein_rus = re.search(r"бел(ок|ки)\D*(\d+)", text_rus, re.IGNORECASE)
    if protein_rus:
        return int(protein_rus.group(2))
    
    protein_eng = re.search(r"protein\D*(\d+)", text_eng, re.IGNORECASE)
    if protein_eng:
        return int(protein_eng.group(1))
    
    return 'не указано'

protein_value = find_protein(all_text_rus, all_text_eng)
results_df['Protein'] = [protein_value]

# угли
def find_carbohydrates(text_rus, text_eng):
    carbs_rus = re.search(r"углевод\D*(\d+)", text_rus, re.IGNORECASE)
    if carbs_rus:
        return int(carbs_rus.group(1))
    
    carbs_eng = re.search(r"carbo\D*(\d+)", text_eng, re.IGNORECASE)
    if carbs_eng:
        return int(carbs_eng.group(1))
    
    return 'не указано'

carbohydrate_value = find_carbohydrates(all_text_rus, all_text_eng)
results_df['Carbohydrate'] = [carbohydrate_value]
# сахар и подсл
def find_sugar(text_rus, text_eng):
    sugar_rus = re.search(r"(сахар|подсластитель|e950|e951|e952|e953|e954|e955|e956|e957|e958|e959|e960|e961|e962|e965|e966|e967|e968|e969|e999)\D*(\d+)", text_rus, re.IGNORECASE)
    if sugar_rus:
        return int(sugar_rus.group(2))
                
    sugar_eng = re.search(r"(sucrose|sugar|e950|e951|e952|e953|e954|e955|e956|e957|e958|e959|e960|e961|e962|e965|e966|e967|e968|e969|e999)\D*(\d+)", text_eng, re.IGNORECASE)
    if sugar_eng:
        return int(sugar_eng.group(2))
    
    return 'не указано'


sugar_value = find_sugar(all_text_rus, all_text_eng)
results_df['Sugar'] = [sugar_value]
# жир
def find_fat(text_rus, text_eng):
    fat_rus = re.search(r"жир\D*(\d+)", text_rus, re.IGNORECASE)
    if fat_rus:
        return int(fat_rus.group(1))
    
    fat_eng = re.search(r"fat\D*(\d+)", text_eng, re.IGNORECASE)
    if fat_eng:
        return int(fat_eng.group(1))
    return 'не указано'



fat_value = find_fat(all_text_rus, all_text_eng)
results_df['Fat'] = [fat_value]
# фрукты
def find_fruits_with_value(text_rus, text_eng):
    fruits_rus = "(яблок|персик|абрикос|ананас)"
    fruits_eng = "(apple|peach|apricot|pineapple)"
    
    match_rus = re.search(fr"{fruits_rus}\D*(\d+)", text_rus, re.IGNORECASE)
    if match_rus:
        return match_rus.group(2)
    
    match_eng = re.search(fr"{fruits_eng}\D*(\d+)", text_eng, re.IGNORECASE)
    if match_eng:
        return match_eng.group(2)
    
    return "Не обнаружено"

fruits_value = find_fruits_with_value(all_text_rus, all_text_eng)
results_df['Fruits'] = [fruits_value]
# проверяем все проверки из таблицы
def check_energy(row):
    try:
        kcal = float(row['kcal'])  
    except ValueError:
        return "Данные отсутствуют или некорректны"
    
    category = int(row['Category'])
    if category == 1 and kcal >= 80:
        return "Соответствует"
    elif category == 2 and kcal >= 60:
        return "Соответствует"
    elif category == 3.1 and kcal >= 60:
        return "Соответствует"
    elif category == 3.2 and kcal >= 60:
        return "Соответствует"
    elif category == 4.1 and kcal >= 60:
        return "Соответствует"
    elif category == 4.2 and kcal >= 60:
        return "Соответствует"
    elif category == 4.3 and kcal >= 60:
        return "Соответствует"
    elif category == 4.4 and kcal >= 60:
        return "Соответствует"
    elif category == 4.5 and kcal >= 60:
        return "Соответствует"
    elif category == 5.1 and kcal <= 50:
        return "Соответствует"
    elif category == 5.2 and kcal <= 50:
        return "Соответствует"
    elif category == 6 and kcal >= 0:
        return "Соответствует"
    elif category == 7 and kcal >= 0:
        return "Соответствует"
    elif category == 8 and kcal >= 0:
        return "Соответствует"
    else:
        return "Не соответствует"
# натрий
def check_sodium(row):
    if row['Sodium'] == 'не указано':
        return "Данные отсутствуют"
    
    try:
        sodium = float(row['Sodium'])
    except ValueError:
        return "Данные отсутствуют или некорректны"
    
    category = row['Category']
    sodium_rules = {
        '1': 50, '2': 50, '3.1': 50, '3.2': 50,
        '4.1': 50, '4.2': 100, '4.3': 50, '4.4': 50, '4.5': 50,
        '5.1': 50, '5.2': 50, '6': 50
    }
    
    if category in sodium_rules:
        if sodium <= sodium_rules[category]:
            return "Соответствует"
        else:
            return "Не соответствует"
    else:
        return "Категория не определена или отсутствуют правила"
# угли
def check_carbohydrates(row):
    if row['Carbohydrate'] in ['/', 'не указано']:
        return "Не применимо"
    
    try:
        carbohydrates = float(row['Carbohydrate'])
    except ValueError:
        return "Данные отсутствуют или некорректны"
    
    category = row['Category']
    carb_rules = {
        '4.1': 15, '4.2': 15, '4.3': 15, '4.4': 15, '4.5': 15, '5.2': 15
    }
    
    if category in carb_rules:
        if carbohydrates <= carb_rules[category]:
            return "Соответствует"
        else:
            return "Не соответствует"
    else:
        return "Не применимо"
# сахар
def check_sugar_absence(row):
    if row['Category'] in ['7', '8']:
        return "Не применимо"
    
    if row['Sugar'] == "не указано":
        return "Соответствует"
    
    try:
        sugar = float(row['Sugar'])
        return "Содержит добавленный сахар или подсластители"
    except ValueError:
        return "Данные отсутствуют или некорректны"
# белок
def check_protein(row):
    if row['Protein'] == 'не указано':
        return "Данные отсутствуют"
    
    try:
        protein = float(row['Protein'])
    except ValueError:
        return "Данные отсутствуют или некорректны"
    
    category = row['Category']
    protein_rules = {
        '1': (None, 5.5),  # (минимальное значение, максимальное значение)
        '4.1': (3, None),
        '4.2': (3, None),
        '4.3': (3, None),
        '4.4': (4, None),
        '4.5': (7, None),
        '5.2': (None, 5.5)
    }
    
    if category in protein_rules:
        min_protein, max_protein = protein_rules[category]
        if (min_protein is None or protein >= min_protein) and (max_protein is None or protein <= max_protein):
            return "Соответствует"
        else:
            return "Не соответствует"
    else:
        return "Не применимо"
# жир
def check_fat(row):
    if row['Fat'] == 'не указано':
        return "Данные отсутствуют"
    
    try:
        fat = float(row['Fat'])
    except ValueError:
        return "Данные отсутствуют или некорректны"
    
    category = row['Category']
    fat_rules = {
        '1': 4.5, '2': 4.5, '3.1': 4.5, '3.2': 4.5,
        '4.1': 4.5, '4.2': 6, '4.3': 4.5, '4.4': 6, '4.5': 6,
        '5.1': 4.5, '5.2': 4.5
    }
    
    if category in fat_rules and fat <= fat_rules[category]:
        return "Соответствует"
    elif category not in fat_rules:
        return "Не применимо"  
    else:
        return "Не соответствует"

def check_fruits(row):
    if row['Fruits'] in ['Не обнаружено', 'не указано', '/']:
        if row['Category'] in ['3.1', '5.2', '6']:
            return "Не применимо"
        else:
            return "Данные отсутствуют или требования не определены"
    
    try:
        if isinstance(row['Fruits'], str):
            fruits = float(row['Fruits'].rstrip('%'))
        else:
            fruits = float(row['Fruits'])
    except ValueError:
        return "Данные отсутствуют или некорректны"
    
    category = row['Category']
    fruits_rules = {
        '1': (None, 10), '2': (None, 5), '4.1': (None, 5), '4.2': (None, 5),
        '4.3': (None, 5), '4.4': (None, 5), '4.5': (None, 5), '5.1': (100, 100), '5.2': (None, None)
    }
    
    if category in fruits_rules:
        min_fruits, max_fruits = fruits_rules[category]
        if (min_fruits is None or fruits >= min_fruits) and (max_fruits is None or fruits <= max_fruits):
            return "Соответствует"
        else:
            return "Не соответствует"
    else:
        return "Не применимо"

results_df['Energy_Compliance'] = results_df.apply(check_energy, axis=1)
results_df['Sodium_Compliance'] = results_df.apply(check_sodium, axis=1)
results_df['Carbohydrates_Compliance'] = results_df.apply(check_carbohydrates, axis=1)
results_df['Sugar_Absence Compliance'] = results_df.apply(check_sugar_absence, axis=1)
results_df['Protein_Compliance'] = results_df.apply(check_protein, axis=1)
results_df['Fat_Compliance'] = results_df.apply(check_fat, axis=1)
results_df['Fruits_Compliance'] = results_df.apply(check_fruits, axis=1)

# проверка про грудное молоко
def check_breastfeeding_support(text):
    if "грудного" in text:
        return "Поддержка и защита грудного вскармливания есть"
    else:
        return "Нет поддержки и защиты грудного вскармливания"

results_df['Breastfeeding_Support'] = [check_breastfeeding_support(all_text_rus)]
# всякие маркетинговые штуки
def check_health_claims(text):
    keywords = [
        "без добавления", "низким содержанием", "гмо", "нездоровых", 
        "натуральные продукты", "обеспечивает", "содержит три вида овощей",
        "содержит овощи", "органические", "фермерские", "натуральные",
        "свежие", "сбалансированное", "идеальный", "уникальный",
        "идеальные", "надлежащее", "источником"
    ]
    
    found_keywords = [keyword for keyword in keywords if keyword in text]
    
    if found_keywords:
        claim_status = "Применяются недопустимые заявления о составе продукции, ее пользе для здоровья и маркетинговых тезисов в рекламных материалах"
        found_keywords_str = ', '.join(found_keywords)
    else:
        claim_status = "Нет недопустимых заявлений о составе продукции, ее пользе для здоровья и маркетинговых тезисов в рекламных материалах"
        found_keywords_str = "Нет"

    return claim_status, found_keywords_str

claim_status, found_keywords_str = check_health_claims(all_text_rus.lower())
results_df['Health_Claims_Compliance'] = [claim_status]
results_df['Found_Health_Claims'] = [found_keywords_str]
# в принципе еще штуки
def check_taste_claims(text):
    taste_keywords = [
        "Восторг", "вкусовых", "рецепторов", "вкусный", "вкуснятина",
        "вкуснейший", "привередливых", "любит", "гамма", "экзотические",
        "вкус", "аромат"
    ]
    
    found_keywords = [keyword for keyword in taste_keywords if keyword in text]
    
    if found_keywords:
        taste_claim_status = "Есть заявления, касающиеся идеального вкуса"
        found_keywords_str = ', '.join(found_keywords)
    else:
        taste_claim_status = "Нет заявления, касающиеся идеального вкуса"
        found_keywords_str = "Нет"

    return taste_claim_status, found_keywords_str



taste_claim_status, found_keywords_str = check_taste_claims(all_text_rus.lower())
results_df['Taste_Claims_Compliance'] = [taste_claim_status]
results_df['Found_Taste_Claims'] = [found_keywords_str]
# иаркетинговые тезисы
def check_quality_claims(text):
    quality_keywords = [
        "спелости", "наполненные пользой и вкусом", "индивидуально", "нежная", "комочков",
        "идеально", "текстурой", "аппетитные", "удобно", "вдохновленный", "правильный выбор",
        "исследования", "экспертами", "фермерами", "доверяем", "лишнего", "нездоровой",
        "невкусного", "самостоятельного", "гарантируем", "совершенный", "идеальный",
        "оптимальный", "Завтрак", "Мы гарантируем"
    ]
    
    found_keywords = [keyword for keyword in quality_keywords if keyword in text]
    
    if found_keywords:
        quality_claim_status = "Есть маркетинговые тезисы"
        found_keywords_str = ', '.join(found_keywords)
    else:
        quality_claim_status = "Нет маркетинговых тезисов"
        found_keywords_str = "Нет"

    return quality_claim_status, found_keywords_str

quality_claim_status, found_keywords_str = check_quality_claims(all_text_rus.lower())
results_df['Quality_Claims_Compliance'] = [quality_claim_status]
results_df['Found_Quality_Claims'] = [found_keywords_str]
# советы экспертов
def check_expert_support(text):
    expert_keywords = ["экспертами", "педиатрами"]
    
    found_keywords = [keyword for keyword in expert_keywords if keyword in text]
    
    if found_keywords:
        expert_claim_status = "Есть заявления/маркировки, подразумевающие поддержку продукта или бренда со стороны экспертов и заслуживающих доверия"
    else:
        expert_claim_status = "Нет заявления/маркировки, подразумевающие поддержку продукта или бренда со стороны экспертов и заслуживающих доверия"

    return expert_claim_status

results_df['Expert_Support_Compliance'] = [check_expert_support(all_text_rus.lower())]


# загрузка компонентов
comp_df = pd.read_excel('comp.xlsx')

def find_number_for_component(text, component):
    # ищем число, за которым следует %
    match = re.search(r'\b' + re.escape(component) + r'\b\D*(\d+(?:\.\d+)?)\s*%', text)
    if match:
        return float(match.group(1))
    else:
        return 0

# добавляем столбцы для каждого компонента и процентн
for component in comp_df['Компонент'].tolist():
    results_df[component] = find_number_for_component(all_text_rus, component)

component_columns = comp_df['Компонент'].tolist()

# добавляем столбцы для нутриентов
nutrients = ['Белки', 'Жиры', 'Углеводы', 'Клетчатка', 'Vit_A', 'Vit_B1', 'Vit_B2', 'Vit_B6', 'Vit_B12', 'Vit_C', 'Vit_D', 'Vit_PP', 'Натрий', 'Калий', 'калорийность']
for nutrient in nutrients:
    results_df[nutrient] = 0

# расчет содержания нутриентов 
for _, comp_row in comp_df.iterrows():
    component = comp_row['Компонент']
    component_percentage = results_df[component] / 100  
    for nutrient in nutrients:
        results_df[nutrient] += comp_row[nutrient] * component_percentage

# есть ли вообще проценты
def check_percentage_presence(row):
    for component in component_columns:
        if component in row.index and row[component] > 0:
            return "Есть процентное соотношение компонентов"
    return "Нет процентного соотношения компонентов"

results_df['Percentage_Presence'] = results_df.apply(check_percentage_presence, axis=1)

#тут посчитаем общий балл
def calculate_score(row):
    ball = 10.0  
    
    # всго 10 
    one_point_deductions = [
        'Energy_Compliance', 'Sodium_Compliance', 'Carbohydrates_Compliance', 
        'Sugar_Absence Compliance', 'Percentage_Presence', 'Protein_Compliance', 
        'Fat_Compliance'
    ]
    
    half_point_deductions = [
        'Fruits_Compliance', 'Breastfeeding_Support', 'Health_Claims_Compliance', 
        'Taste_Claims_Compliance', 'Quality_Claims_Compliance', 'Expert_Support_Compliance'
    ]
    
    for column in one_point_deductions:
        if row[column] == "Не соответствует" or row[column] == "Содержит добавленный сахар или подсластители":
            ball -= 1
    
    for column in half_point_deductions:
        if row[column] in ["Не соответствует", "Применяются недопустимые заявления о составе продукции, ее пользе для здоровья и маркетинговых тезисов в рекламных материалах", "Есть заявления, касающиеся идеального вкуса", "Есть маркетинговые тезисы", "Есть заявления/маркировки, подразумевающие поддержку продукта или бренда со стороны экспертов и заслуживающих доверия"]:
            ball -= 0.5
    
    return ball

results_df['Final Score'] = results_df.iloc[:1].apply(calculate_score, axis=1)
print(results_df)
# сохранямсмя
results_df.to_json('results_data.json', orient='records', force_ascii=False, lines=True)
results_df.to_excel('results_df.xlsx')
json_data = results_df.to_json(orient='records', force_ascii=False)


