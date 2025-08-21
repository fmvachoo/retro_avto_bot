from bot.config import CARS

class StickerManager:
    @staticmethod
    def get_car_info(qr_data: str):
        """Получить информацию об автомобиле по данным QR-кода"""
        return CARS.get(qr_data)
    
    @staticmethod
    def get_all_cars_count():
        """Получить общее количество автомобилей"""
        return len(CARS)

# Глобальный экземпляр менеджера стикеров
sticker_manager = StickerManager()
