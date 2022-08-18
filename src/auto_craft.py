import pyautogui as keyboard
from time import sleep


class ItemStack:

    def __init__(self, name: str, count: int):
        self.__name: str = name
        self.__count: int = count
    
    def get_name(self) -> str:
        return self.__name
    
    def get_count(self) -> int:
        return self.__count

key_actions: dict[str, str] = {
    "w": "w",
    "a": "a",
    "s": "s",
    "d": "d",
    "e": "e",
    "left-click": "x",
    "right-click": "c",
    "shift": "shift",
    "esc": "esc"
}
single_item_photos: dict[str, str] = {
    "block_of_iron": "resource/items/single/block_of_iron.png",
    "error_block_of_iron": "resource/items/single/error_block_of_iron.png"
}
fullstack_item_photos: dict[str, str] = {
    "iron_ingot": "resource/items/fullstack/iron_ingot.png",
    "error_iron_ingot": "resource/items/fullstack/error_iron_ingot.png"
}
recipes: dict[str, list[ItemStack]] = {
    "block_of_iron": [
        ItemStack("iron_ingot", 9)
    ]
}

def inventory_has_space() -> bool:
    slot_location: keyboard.Point = keyboard.locateCenterOnScreen("resource/inventory_slot.png", confidence=0.8, region=(600, 600, 700, 360))
    return slot_location != None

def move_to_target(target_pic_path: str, region: tuple[int] = None, confidence: float = None):
    keyboard.moveTo(keyboard.locateCenterOnScreen(target_pic_path, confidence=confidence, region=region))

class ItemNameAdjuster:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(ItemNameAdjuster, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def adjust(self, name: str) -> str:
        raise NotImplementedError()

class CraftItemNameAdjuster(ItemNameAdjuster):

    def adjust(self, name: str) -> str:
        return name.replace("_", " ")

class ErrorNameMaker(ItemNameAdjuster):

    def adjust(self, name: str) -> str:
        return "error_" + name

class ItemNameAdjusterFactory:

    def create(type: str) -> ItemNameAdjuster:
        if type == "craft":
            return CraftItemNameAdjuster()
        elif type == "error":
            return ErrorNameMaker()
        else:
            return None

class ItemTakerData:

    def __init__(
        self,
        item_name: str = None,
        region: tuple[int] = None,
        recipe: list[ItemStack] = None
    ):
        self.__item_name: str = item_name
        self.__region: tuple[int] = region
        self.__recipe: list[ItemStack] = recipe
    
    def get_item_name(self) -> str:
        return self.__item_name
    
    def get_region(self) -> tuple[int]:
        return self.__region
    
    def get_recipe(self) -> list[ItemStack]:
        return self.__recipe

class ItemTaker(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(ItemTaker, cls).__new__(cls)
        return cls._instance
    
    def take(self, item_taker_data: ItemTakerData):
        raise NotImplementedError()

class AllItemTaker(ItemTaker):

    def take(self, item_taker_data: ItemTakerData):
        x: int = 670
        y: int = 194
        for i in range(6):
            keyboard.moveTo(x, y)
            for j in range(9):
                with keyboard.hold(key_actions["shift"]):
                    keyboard.click()
                keyboard.moveRel(75, 0)
            y += 70

class AllItemTakerUsingScan(ItemTaker):

    def take(self, item_taker_data: ItemTakerData):
        item_location: keyboard.Point = None
        item_pic_path: str = ""
        recipe_item_name: str = ""
        recipe_item_count: int = 0
        while inventory_has_space():
            for recipe_item in item_taker_data.get_recipe():
                recipe_item_name = recipe_item.get_name()
                recipe_item_count = recipe_item.get_count()
                item_pic_path = fullstack_item_photos[recipe_item_name]
                for i in range(recipe_item_count):
                    item_location = keyboard.locateCenterOnScreen(item_pic_path, confidence=.7, region=item_taker_data.get_region())
                    if not inventory_has_space:
                        return
                    if item_location == None:
                        return
                    keyboard.moveTo(item_location)
                    with keyboard.hold(key_actions["shift"]):
                        keyboard.click()

class ItemTakerUsingScan(ItemTaker):

    def take(self, item_taker_data: ItemTakerData):
        item_location: keyboard.Point = None
        item_name: str = item_taker_data.get_item_name()
        item_pic_path: str = fullstack_item_photos[item_name]
        region: tuple[int] = item_taker_data.get_region()
        if item_name == None or region == None:
            return
        item_location: keyboard.Point = keyboard.locateCenterOnScreen(item_pic_path, confidence=.7, region=region)
        if item_location == None:
            return
        keyboard.moveTo(item_location)
        with keyboard.hold(key_actions["shift"]):
            keyboard.click()

class ItemTakerFactory:

    def create(item_taker_type: str) -> ItemTaker:
        if item_taker_type == "all":
            return AllItemTaker()
        elif item_taker_type == "scan_all":
            return AllItemTakerUsingScan()
        elif item_taker_type == "scan_single":
            return ItemTakerUsingScan()
        else:
            None

class Crafter(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Crafter, cls).__new__(cls)
        return cls._instance

    def craft(self, craft_item_name: str):
        raise NotImplementedError()

class DefaultCrafter(Crafter):

    def craft(self, craft_item_name: str):
        keyboard.moveTo(670, 373)
        keyboard.click()
        keyboard.moveTo(450, 270)
        keyboard.click()
        keyboard.write(ItemNameAdjusterFactory.create("craft").adjust(craft_item_name))
        keyboard.moveTo(980, 369)
        keyboard.click()

class CrafterUsingScan(Crafter):

    def craft(self, craft_item_name: str):
        crafting_menu_area: tuple[int] = 330, 198, 570, 656
        crafting_table_area: tuple[int] = 922, 197, 690, 282
        can_craft: bool = True
        item_name_adjuster: ItemNameAdjuster = ItemNameAdjusterFactory.create("craft")
        move_to_target("resource/craft_supporter_icon.png", confidence=.9)
        keyboard.click()
        while can_craft:
            move_to_target("resource/item_search_icon.png", confidence=.9)
            keyboard.click()
            keyboard.write(item_name_adjuster.adjust(craft_item_name))
            move_to_target(single_item_photos[craft_item_name], crafting_menu_area, .5)
            with keyboard.hold(key_actions["shift"]):
                keyboard.click()
            move_to_target(single_item_photos[craft_item_name], crafting_table_area, .6)
            with keyboard.hold(key_actions["shift"]):
                keyboard.click()
            can_craft = keyboard.locateCenterOnScreen("resource/inventory_slot.png", confidence=.8, region=crafting_table_area) != None

class CrafterFactory:

    def create(crafter_type: str) -> Crafter:
        if crafter_type == "default":
            return DefaultCrafter()
        elif crafter_type == "scan":
            return CrafterUsingScan()
        else:
            None

class Bot:

    def __init__(
        self,
        item_taker: ItemTaker,
        crafter: Crafter
    ):
        self.__item_taker: ItemTaker = item_taker
        self.__crafter: Crafter = crafter
    
    def craft(self, item_name: str):
        inventory_region: tuple[int] = 612, 85, 689, 498
        craft_recipe: list[ItemStack] = recipes[item_name]
        item_taker_data: ItemTakerData = ItemTakerData(region=inventory_region, recipe=craft_recipe)
        keyboard.keyDown(key_actions["a"])
        sleep(0.3)
        keyboard.keyUp(key_actions["a"])
        keyboard.press(key_actions["right-click"])
        self.__item_taker.take(item_taker_data)
        keyboard.press(key_actions["esc"])
        keyboard.keyDown(key_actions["d"])
        sleep(0.3)
        keyboard.keyUp(key_actions["d"])
        keyboard.press(key_actions["right-click"])
        self.__crafter.craft(item_name)

if __name__ == "__main__":
    sleep(3)
    item_taker: ItemTaker = ItemTakerFactory.create("scan_all")
    crafter: Crafter = CrafterFactory.create("scan")
    bot: Bot = Bot(item_taker, crafter)
    # bot.craft("block_of_iron")
    crafter.craft("block_of_iron")









