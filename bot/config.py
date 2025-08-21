import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

# Информация об автомобилях
CARS = {
    "chevy_57": {
        "name": "Chevrolet Bel Air (1957)",
        "info": """*Chevrolet Bel Air (1957)*
*Год выпуска:* 1957
*Мощность:* До 283 л.с.
*Максимальная скорость:* Около 180 км/ч
*Фан-факт:* Символ американской мечты 50-х. Ассоциируется с золотой эрой рок-н-ролла.""",
        "sticker": "CAACAgIAAxkBAAELVhNmAAE8Uv0M3QABm1YVU7_5Q2u8t9YAApUuAAJ4e-lJAAE8wvq7AAHp3jQE"
    },
    "mercedes_gullwing": {
        "name": "Mercedes-Benz 300 SL «Gullwing» (1954)",
        "info": """*Mercedes-Benz 300 SL «Gullwing» (1954)*
*Год выпуска:* 1954
*Мощность:* 215 л.с.
*Максимальная скорость:* До 250 км/ч
*Фан-факт:* Двери «крылья чайки» появились из-за жёсткой трубчатой рамы. Любимая машина звезд эпохи.""",
        "sticker": "CAACAgIAAxkBAAELVhVmAAE8U3bU2QAB1QABcG9pzQABASpLAAKXLgACeHvpSXkAAbPxAAE0-t4E"
    },
    "jaguar_etype": {
        "name": "Jaguar E-Type (1961)",
        "info": """*Jaguar E-Type (1961)*
*Год выпуска:* 1961
*Мощность:* 265 л.с.
*Максимальная скорость:* 241 км/ч
*Фан-факт:* Энцо Феррари назвал его «самым красивым автомобилем». Подарок Бриджит Бардо.""",
        "sticker": "CAACAgIAAxkBAAELVhdmAAE8U8vVtQABsQABcG9pzQABASpLAAKYLgACeHvpSXkAAbPxAAE0-t4E"
    },
    "ford_mustang": {
        "name": "Ford Mustang (1964½)",
        "info": """*Ford Mustang (1964½)*
*Год выпуска:* 1964
*Мощность:* До 271 л.с.
*Максимальная скорость:* Около 190 км/ч
*Фан-факт:* Породил класс «пони-кар». За 100 дней продано 100 000 машин. Автомобиль Стива Маккуина.""",
        "sticker": "CAACAgIAAxkBAAELVhlmAAE8U_6p1wABsQABcG9pzQABASpLAAKZLgACeHvpSXkAAbPxAAE0-t4E"
    },
    "cadillac_59": {
        "name": "Cadillac Series 62 (1959)",
        "info": """*Cadillac Series 62 (1959)*
*Год выпуска:* 1959
*Мощность:* 345 л.с.
*Максимальная скорость:* Около 175 км/ч
*Фан-факт:* Обладатель самых больших задних крыльев. Розовый кадиллак был любимой машиной Элвиса Пресли.""",
        "sticker": "CAACAgIAAxkBAAELVhtmAAE8VBJkUQABsQABcG9pzQABASpLAAKaLgACeHvpSXkAAbPxAAE0-t4E"
    }
}
