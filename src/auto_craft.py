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
item_photos: dict[str, str] = {
    "iron_block": "resource/iron_block.png",
    "iron_ingot": "resource/iron_ingot.png"
}
recipes: dict[str, list[ItemStack]] = {
    "iron_block": [
        ItemStack("iron_ingot", 9)
    ]
}

def inventory_has_space() -> bool:
    slot_location: keyboard.Point = keyboard.locateCenterOnScreen("resource/inventory_slot.png", confidence=0.7, region=(600, 600, 700, 360))
    return slot_location != None

class ItemTaker:

    def take(self, recipe: list[ItemStack]):
        raise NotImplementedError()

class AllItemTaker(ItemTaker):

    def take(self, recipe: list[ItemStack]):
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

    def take(self, recipe: list[ItemStack]):
        item_location: keyboard.Point = None
        recipe_item_name: str = ""
        recipe_item_count: int = 0
        while inventory_has_space():
            for recipe_item in recipe:
                recipe_item_name = recipe_item.get_name()
                recipe_item_count = recipe_item.get_count()
                for i in range(recipe_item_count):
                    item_location = keyboard.locateCenterOnScreen(item_photos[recipe_item_name], confidence=.7, region=(611, 85, 692, 502))
                    if not inventory_has_space:
                        return
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
        else:
            None

class Crafter:

    def craft(self, craft_item_name: str):
        raise NotImplementedError()

class DefaultCrafter(Crafter):

    def craft(self, craft_item_name: str):
        keyboard.moveTo(670, 373)
        keyboard.click()
        keyboard.moveTo(450, 270)
        keyboard.click()
        keyboard.write(craft_item_name)
        keyboard.moveTo(980, 369)
        keyboard.click()

class CrafterFactory:

    def create(crafter_type: str) -> Crafter:
        if crafter_type == "default":
            return DefaultCrafter()
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
        keyboard.keyDown(key_actions["a"])
        sleep(0.3)
        keyboard.keyUp(key_actions["a"])
        keyboard.press(key_actions["right-click"])
        self.__item_taker.take(recipes[item_name])
        keyboard.press(key_actions["esc"])
        keyboard.keyDown(key_actions["d"])
        sleep(0.3)
        keyboard.keyUp(key_actions["d"])
        keyboard.press(key_actions["right-click"])
        self.__crafter.craft(item_name)

if __name__ == "__main__":
    sleep(3)
    item_taker: ItemTaker = ItemTakerFactory.create("scan_all")
    crafter: Crafter = CrafterFactory.create("default")
    bot: Bot = Bot(item_taker, crafter)
    # bot.craft("iron_block")
    item_taker.take(recipes["iron_block"])








