from kivy.config import Config

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', True)
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.image import Image

from datetime import date
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class MainWidget(RelativeLayout):
    date_text = StringProperty("Date")
    total = StringProperty("$0")
    list_canvas = ObjectProperty()
    text_input_str1 = StringProperty("")
    text_input_str2 = StringProperty("0")
    item_count = 0
    item_dict = {} #key: cart image, value: list of everything else in that row
    total_cost = 0
    cart_original_image = Image(source='img/cart_original.png')
    date_today = date.today()
    date_formatted = date_today.strftime("%d/%m/%y")
    edit_mode = False
    elt_to_pass = None
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.date_text = "Date: " + str(self.date_formatted) + "        Total Cost: $" + str(self.total_cost)


    def on_text_validate(self, widget):
        if self.edit_mode == False:
            item_label = Label(text=str(self.ids.text_input1.text), text_size=(self.size[0], self.size[1]/2), halign='left', valign='middle', padding=[300, 0, 0, 0], color=(1, 1, 1))
            price_label = Label(text=str(self.ids.text_input2.text), text_size=(self.size[0], self.size[1]/2), halign='center', valign='middle', color=(1, 1, 1))
            cart_button = Image(source='img/cart_original.png', size_hint=(None, None), size=(50, 50), on_touch_down=self.button_press)
            delete_button = Image(source='img/trash_original.png', size_hint=(None, None), size=(50, 50))
            self.item_dict[cart_button] = [item_label, price_label, cart_button, delete_button]
            self.ids.grid_lay.add_widget(item_label)
            self.ids.grid_lay.add_widget(price_label)
            self.ids.grid_lay.add_widget(cart_button)
            self.ids.grid_lay.add_widget(delete_button)
            self.item_count += 1
            self.total_cost += float(self.ids.text_input2.text)
            self.date_text = "Date: " + str(self.date_formatted) + "        Total Cost: $" + str(self.total_cost)
        else:
            self.total_cost -= float(self.item_dict[self.elt_to_pass][1].text)
            self.item_dict[self.elt_to_pass][0].text = self.ids.text_input1.text
            self.item_dict[self.elt_to_pass][1].text = self.ids.text_input2.text
            self.edit_mode = False
            self.total_cost += float(self.ids.text_input2.text)
            self.ids.date_label.text = "Date: " + str(self.date_formatted) + "        Total Cost: $" + str(self.total_cost)

    def button_press(self, button, event):
        elt_to_del = None
        for elt in self.item_dict.keys():
            if elt.pos[0] <= event.pos[0] <= elt.pos[0] + elt.size[0] and elt.pos[1] <= event.pos[1] <= elt.pos[1] + elt.size[1]:
                self.item_dict[elt][0].color = (0, 0, 0)
            # if elt.pos[0] + elt.size[0] <= event.pos[0] <= elt.pos[0] + elt.size[0] * 2 and elt.pos[1] <= event.pos[1] <= elt.pos[1] + elt.size[1]:
            #     elt_to_del = elt
            if (self.item_dict[elt][3].pos[0] <= event.pos[0] <= self.item_dict[elt][3].pos[0] + self.item_dict[elt][3].size[0]
                    and self.item_dict[elt][3].pos[1] <= event.pos[1] <= self.item_dict[elt][3].pos[1] + self.item_dict[elt][3].size[1]):
                elt_to_del = elt
            if event.pos[0] < elt.pos[0] and elt.pos[1] <= event.pos[1] <= elt.pos[1] + elt.size[1]:
                self.edit_text(elt)
                print("EDIT")
        # self.item_dict[button].color = (0, 0, 0)
        # print("button: ", button, " event: ", event)
        # print("elt", elt_to_del)
        if elt_to_del is not None:
            print(self.item_dict)
            for i in self.item_dict[elt_to_del]:
                self.ids.grid_lay.remove_widget(i)
            self.total_cost -= float(self.item_dict[elt_to_del][1].text)
            self.ids.date_label.text = "Date: " + str(self.date_formatted) + "        Total Cost: $" + str(self.total_cost)
            self.item_dict.pop(elt_to_del)
            elt_to_del = None

    def edit_text(self, elt):
        self.edit_mode = True
        self.text_input_str1 = self.item_dict[elt][0].text
        self.text_input_str2 = self.item_dict[elt][1].text
        self.elt_to_pass = elt


class GroceryApp(App):
    pass

if __name__ == '__main__':
    GroceryApp().run()