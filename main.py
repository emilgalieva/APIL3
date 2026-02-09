import arcade.gui
import requests

MAP_FILE = "current_map.png"


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__()
        self.geocoder_params = {}
        self.static_map_params = {"apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13", "ll": "0.01,0.01",
                                  "spn": "10.0,10.0", "size": "640,360"}
        self.organization_search_params = {}
        self.current_map_texture = None
        self.update_image()

    def update_image(self):
        response = requests.get("https://static-maps.yandex.ru/v1?", self.static_map_params)
        print(response)
        with open(MAP_FILE, "wb") as file:
            file.write(response.content)
        self.current_map_texture = arcade.load_texture(MAP_FILE)

    def on_draw(self):
        self.clear(arcade.color.BLACK)
        if self.current_map_texture is not None:
            arcade.draw_texture_rect(self.current_map_texture, arcade.LBWH(0, 0, self.width, self.height))


if __name__ == "__main__":
    main_window = MainWindow()
    arcade.run()