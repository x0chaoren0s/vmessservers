from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class ScrollableTextInput(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollableTextInput, self).__init__(**kwargs)
        self.text_input = TextInput(
            multiline=True,
        )
        self.add_widget(self.text_input)

    def on_size(self, *args):
        self.text_input.height = self.height


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.scrollable_text_input = ScrollableTextInput()
        self.add_widget(self.scrollable_text_input)


class MyApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == '__main__':
    MyApp().run()