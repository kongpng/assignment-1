import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Optional


class HelloWorld(toga.App):

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
        instance_box = self.instance_box()

        logout_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        logout_button = toga.Button(
            text="Logout",
            on_press=self.logout,  # Handler til logout-knappen
            style=Pack(padding=10)
        )
        logout_box.add(logout_button)


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

    def instance_box(self) -> toga.Box:
        instance_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        role_items = list([' ', 'Doctor', 'Nurse', 'Patient'])
        selected_role_item = 'Doctor'
        events = [{'id':'Diagnose', 'label':'Diagnose', 'role':'Doctor'},
                  {'id':'Operate', 'label':'Operate', 'role':'Doctor'},
                  {'id':'Give treatment', 'label':'Give treatment', 'role':'Nurse'},
                  {'id':'Take treatment', 'label':'Take treatment', 'role':'Patient'}]

        label = toga.Label("Each instance will appear here")
        instance_box.add(label)

        ### Currentbox
        current_instance_box = toga.Box(style=Pack(direction=ROW, flex=1))
        
        ### other box
        other_instance_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        current_role = toga.Label("Current role")
        selected_role_label = toga.Label("Select other role")
        self.role_selection = toga.Selection(
            items=role_items,
            value=role_items[0],
            on_change=self.role_changed
        )

        other_instance_box.add(current_role)
        other_instance_box.add(selected_role_label)
        other_instance_box.add(self.role_selection)
        current_instance_box.add(other_instance_box)
        ### End other box

        ### Not added box
        not_added_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        current_instance_label = toga.Label("Current instance")
        not_yet_added_label = toga.Label("Not added yet!")

        not_added_box.add(current_instance_label)
        not_added_box.add(not_yet_added_label)
        current_instance_box.add(not_added_box)
        ### End not added box

        ### End Currentbox

        ### Scrollcontainer
        scroll_container = toga.ScrollContainer(style=Pack(flex=1))
        event_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        for event in events:
            event_button = toga.Button(
                text=f"{event['label']} (role: {event['role']})",
                id=event['id'],
                on_press=self.execute_event
            )
            event_box.add(event_button)

        scroll_container.content = event_box
        
        ### End Scrollcontainer
        
        instance_box.add(current_instance_box)
        instance_box.add(scroll_container)


        return instance_box

    async def option_item_changed(self, widget):
        print("[i] You have selected another Option Item!")

    async def role_changed(self, widget):
        print(f'[i] You changed the role to {self.role_selection.value}!')

    async def logout(self, widget):
        print("You want to logout!")

    async def execute_event(self, widget):
        print(f'[i] You want to execute event: {widget.id}')

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