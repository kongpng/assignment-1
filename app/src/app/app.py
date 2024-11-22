import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Optional


class HelloWorld(toga.App):

    def login_box_widget(self) -> toga.Box:
        login_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        username_label = toga.Label(text="Username:", style=Pack(padding=(5)))
        password_label = toga.Label(text="Password:", style=Pack(padding=(5)))
        self.username_input = toga.TextInput(style=Pack(flex=1))
        self.password_input = toga.PasswordInput(style=Pack(flex=1))
        login_button = toga.Button(
            text="Login", on_press=self.say_hello, style=Pack(padding=5)
        )

        login_box.add(username_label)
        login_box.add(self.username_input)
        login_box.add(password_label)
        login_box.add(self.password_input)
        login_box.add(login_button)
        return login_box

    def all_instances_widget(self) -> toga.Box:
        all_instances_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        all_instances_container = toga.ScrollContainer(
            horizontal=False,
            style=Pack(direction=COLUMN, flex=1),
        )
        instances = [
            {"id": 1, "name": "Instance 1"},
            {"id": 2, "name": "Instance 2"},
            {"id": 3, "name": "Instance 3"},
        ]

        label = toga.Label("All instances will be listed here")
        new_instance_btn = toga.Button(
            text="Create new instance",
            on_press=self.create_new_instance,
            style=Pack(padding=5),
        )
        delete_all_instances_btn = toga.Button(
            text="Delete all instances",
            on_press=self.delete_all_instances,
            style=Pack(padding=5),
        )

        all_instances_box.add(label)
        all_instances_box.add(new_instance_btn)
        all_instances_box.add(delete_all_instances_btn)

        instances_box = toga.Box(style=Pack(direction=COLUMN))

        for instance in instances:
            buttons_box = toga.Box(style=Pack(direction=ROW))

            instance_button = toga.Button(
                instance["name"],
                on_press=self.show_instance,
                style=Pack(padding=5),
                id=instance["id"],
            )
            del_button = toga.Button(
                "x",
                on_press=self.delete_instance_by_id,
                style=Pack(padding=5, color="red"),
                id=f"x{instance['id']}",
            )

            buttons_box.add(instance_button)
            buttons_box.add(del_button)
            instances_box.add(buttons_box)

        all_instances_box.add(instances_box)
        all_instances_container.content = all_instances_box

        return all_instances_box

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            text="Your name: ",
            style=Pack(padding=(0, 5)),
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            text="Say Hello!",
            on_press=self.say_hello,
            style=Pack(padding=5),
        )

        main_box.add(name_box)
        main_box.add(button)

        login_box = self.login_box_widget()
        all_instances_box = self.all_instances_widget()
        # TODO add Containers and Widgets to your all_instances_box
        instance_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        # TODO add Containers and Widgets to your instance_box
        logout_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        option_container = toga.OptionContainer(
            content=[
                toga.OptionItem("Main box", main_box),
                toga.OptionItem("Login", login_box),
                toga.OptionItem("All instances", all_instances_box),
                toga.OptionItem("Instance run", instance_box),
                toga.OptionItem("Logout", logout_box),
            ],
            on_select=self.option_item_changed,
            style=Pack(direction=COLUMN),
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = option_container
        self.main_window.show()

    async def option_item_changed(self, widget):
        print("[i] You have selected another Option Item!")

    async def say_hello(self, widget):
        async with httpx.AsyncClient() as client:
            response = await client.get("https://jsonplaceholder.typicode.com/posts/42")

        payload = response.json()

        self.main_window.info_dialog(
            greeting(self.name_input.value),
            payload["body"],
        )

    async def show_instance(self, widget):
        print(f"you want to show {widget.id}")

    async def delete_instance_by_id(self, widget):
        print(f"you want to delete {widget.id[1:]}")

    async def create_new_instance(self, widget):
        print("[i] Create new instance!")

    async def delete_all_instances(self, widget):
        print("[i] Delete all instances!")


def greeting(name):
    if name:
        return f"Hello, {name}"
    else:
        return "Hello, stranger"


def main():
    return HelloWorld()
