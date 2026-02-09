from io import BytesIO
from PIL import Image
import arcade.gui
import requests

SCALE_SENSITIVITY = 2


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__()
        self.geocoder_params = {}
        self.static_map_params = {"apikey": "5292d178-4924-4e74-a7df-abc50271081b", "ll": "0.01,0.01",
                                  "spn": "10.0,10.0", "size": "160,90"}
        self.organization_search_params = {}
        self.current_map_texture = None
        self.image_changed = True
        self.keys_for_register = (arcade.key.PAGEUP, arcade.key.PAGEDOWN)
        self.keys_pressed = {el: False for el in self.keys_for_register}
        self.keys_for_register_click = (arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT)
        self.keys_clicked = {el: False for el in self.keys_for_register_click}

    def update_image(self):
        response = requests.get("https://static-maps.yandex.ru/v1?", self.static_map_params)
        print(response)
        self.current_map_texture = arcade.Texture(Image.open(BytesIO(response.content)).convert("RGBA"))

    def update_scale(self, is_positive, delta_time):
        scale = self.static_map_params["spn"].split(",")
        result = float(scale[0]) + SCALE_SENSITIVITY * delta_time * (1 if is_positive else -1)
        if 0.0 <= result <= 180.0:
            scale[0] = str(result)
        result = float(scale[1]) + SCALE_SENSITIVITY * delta_time * (1 if is_positive else -1)
        if 0.0 <= result <= 180.0:
            scale[1] = str(result)
        self.static_map_params["spn"] = ",".join(scale)
        self.image_changed = True

    def update_ll_pos(self, direction: int):
        spn = self.static_map_params["spn"].split(",")
        ll = self.static_map_params["ll"].split(",")
        if direction < 2:
            result = float(ll[0]) + float(spn[0]) * (1 if direction == 1 else -1)
            if -180.0 + float(spn[0]) / 2 <= result <= 180.0 - float(spn[0]) / 2:
                ll[0] = str(result)
        else:
            result = float(ll[1]) + float(spn[1]) * (1 if direction == 3 else -1)
            if -90.0 + float(spn[1]) / 2 <= result <= 90.0 - float(spn[1]) / 2:
                ll[1] = str(result)
        self.static_map_params["ll"] = ",".join(ll)
        self.image_changed = True

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        if self.current_map_texture is not None:
            arcade.draw_texture_rect(self.current_map_texture, arcade.LBWH(0, 0, self.width, self.height))

    def on_update(self, delta_time: float):
        if self.keys_pressed[arcade.key.PAGEUP]:
            self.update_scale(1, delta_time)
        if self.keys_pressed[arcade.key.PAGEDOWN]:
            self.update_scale(0, delta_time)
        if self.keys_clicked[arcade.key.UP]:
            self.update_ll_pos(3)
        if self.keys_clicked[arcade.key.DOWN]:
            self.update_ll_pos(2)
        if self.keys_clicked[arcade.key.LEFT]:
            self.update_ll_pos(0)
        if self.keys_clicked[arcade.key.RIGHT]:
            self.update_ll_pos(1)
        if self.image_changed:
            self.update_image()
            self.image_changed = False
        for el in self.keys_for_register_click:
            if self.keys_clicked[el]:
                self.keys_clicked[el] = False

    def on_key_press(self, symbol: int, modifiers: int):
        for el in self.keys_for_register:
            if symbol == el:
                self.keys_pressed[el] = True
                break
        else:
            for el in self.keys_for_register_click:
                if symbol == el:
                    self.keys_clicked[el] = True
                    break

    def on_key_release(self, symbol: int, modifiers: int):
        for el in self.keys_for_register:
            if symbol == el:
                self.keys_pressed[el] = False
                break


if __name__ == "__main__":
    main_window = MainWindow()
    arcade.run()
