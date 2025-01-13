from services import database_connection_group_8 as dbc
import httpx
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Optional
from services.dcr_active_repository_group_8 import (
    check_login_from_dcr,
    DcrActiveRepository,
    DcrUser,
    EventsFilter,
)


class HelloWorld(toga.App):
    graph_id: str = (
        "1986676"  # https://dcrgraphs.net/tool/main/Graph?id=e3d0ef56-e918-4804-bcff-6bd7e8493f33
    )
    dcr_ar = None
    option_container = None
    all_instances_box = None
    instance_box = None
    data_event_box = None
    current_instance_id = None
    instances: dict = {}
    user: DcrUser = None
    connected: bool = False

    def startup(self):
        name_label = toga.Label(
            text="Your name: ",
            style=Pack(padding=(0, 5)),
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        login_box = self.login_box_widget()
        all_instances_box = self.all_instances_widget()
        instance_box = self.instance_box()
        data_event_box = self.data_event_box()

        logout_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        logout_button = toga.Button(
            text="Logout",
            on_press=self.logout,  # Handler til logout-knappen
            style=Pack(padding=10),
        )
        logout_box.add(logout_button)

        self.login_item = toga.OptionItem("Login", login_box)
        self.all_instances_item = toga.OptionItem("All instances", all_instances_box)
        self.instance_run_item = toga.OptionItem("Instance run", instance_box)
        self.logout_item = toga.OptionItem("Logout", logout_box)
        self.data_event_item = toga.OptionItem("Data Event", self.data_event_box)
        

        self.option_container = toga.OptionContainer(
            content=[self.login_item],  # Only show login initially, this sucks
            on_select=self.option_item_changed,
            style=Pack(direction=COLUMN),
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.option_container
        self.main_window.show()




    def login_box_widget(self) -> toga.Box:
        login_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        username_label = toga.Label(text="Username:", style=Pack(padding=(5)))
        password_label = toga.Label(text="Password:", style=Pack(padding=(5)))
        self.username_input = toga.TextInput(style=Pack(flex=1))
        self.password_input = toga.PasswordInput(style=Pack(flex=1))
        login_button = toga.Button(
            text="Login", on_press=self.login_handler, style=Pack(padding=5)
        )

        login_box.add(username_label)
        login_box.add(self.username_input)
        login_box.add(password_label)
        login_box.add(self.password_input)
        login_box.add(login_button)
        return login_box

    def all_instances_widget(self) -> toga.Box:
        self.all_instances_box = toga.Box(style=Pack(direction=COLUMN, flex=1))

        label = toga.Label("Log in to see instances")
        self.all_instances_box.add(label)

        return self.all_instances_box

    def instance_box(self) -> toga.Box:
        self.instance_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        label = toga.Label(
            "Select an instance from the All instances tab or create a new!"
        )
        self.instance_box.add(label)

        return self.instance_box

    events_with_data = ['Activity7']

    def data_event_box(self) -> toga.Box:
        self.data_event_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        label = toga.Label(
            "Special action needs to be taken for this event!"
        )
        self.data_event_box.add(label)

        return self.data_event_box

    def display_data_event(self, event_id):
        match event_id:
            case 'Activity7':
                self.option_container.content.append(self.data_event_item)
                self.option_container.current_tab = "Data Event"
                self.option_container.content.remove("Logout")
                self.option_container.content.remove("All instances")
                self.option_container.content.remove("Instance run")
                self.display_meds_needs_form()

    def display_meds_needs_form(self):
        self.data_event_box.clear()

        form_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        instruction_label = toga.Label(
            text="Do you feel you need medication, or can you live without it?",
            style=Pack(padding=(0, 10)),
        )

        self.choice_selection = toga.Selection(
            items=["Needs medication", "Can live without it"],
            style=Pack(padding=(5, 10)),
        )

        submit_button = toga.Button(
            text="Submit Choice",
            on_press=self.submit_meds_needs,
            style=Pack(padding=5),
        )

        form_box.add(instruction_label)
        form_box.add(self.choice_selection)
        form_box.add(submit_button)

        self.data_event_box.add(form_box)
        self.data_event_box.refresh()

    async def submit_meds_needs(self, widget):
        choice = self.choice_selection.value
        choice_id = None

        if choice == "Needs medication":
            choice_id = 1
        elif choice == "Can live without it":
            choice_id = 2
        else:
            print("[x] No valid choice selected.")
            return

        if choice_id:
            await self.dcr_ar.execute_data_event(self.graph_id, self.current_instance_id, "Activity7", choice_id)
            dbc.insert_or_update_choice(self.current_instance_id, "Activity7", choice_id)
            self.option_container.content.append(self.all_instances_item)
            self.option_container.content.append(self.instance_run_item)
            self.option_container.content.append(self.logout_item)
            self.option_container.current_tab = "Instance run"
            self.option_container.content.remove("Data Event")
            await self.after_execute_event()

    async def option_item_changed(self, widget):
        if widget.current_tab.text == "All instances":
            await self.show_instances_box()

    async def role_changed(self, widget):
        self.user.role = self.role_selection.value
        dbc.update_dcr_role(self.user.email, self.user.role)
        await self.show_instance_box()

    async def logout(self, widget):
        self.option_container.content.append(
            self.login_item
        )  # this doesn't seem right, but what was being told to do in the feed back doesn't work.
        self.option_container.current_tab = "Login"

        self.option_container.content["Login"].enabled = True
        self.option_container.content["All instances"].enabled = False
        self.option_container.content["Instance run"].enabled = False
        self.option_container.content["Logout"].enabled = False
        self.option_container.current_tab = "Login"

        self.user = None
        self.dcr_ar = None
        self.current_instance_id = None
        self.username_input.value = ""
        self.password_input.value = ""
        self.instances = {}
        self.option_container.content.remove("All instances")
        self.option_container.content.remove("Instance run")
        self.option_container.content.remove("Logout")

    async def execute_event(self, widget): 
        print(f'[i] You want to execute event: {widget.id}')
        event_id = widget.id
        if event_id in self.events_with_data:
            self.display_data_event(event_id)
        else:
            executed = await self.dcr_ar.execute_event(self.graph_id, self.current_instance_id, widget.id)
            print(f'[i] executed: {executed}')
            await self.after_execute_event()

    async def after_execute_event(self):
        pending_events = await self.dcr_ar.get_events(self.graph_id, self.current_instance_id, EventsFilter.PENDING)
        valid = True
        if len(pending_events)>0:
            valid = False
        dbc.update_instance(self.current_instance_id, valid)
        await self.show_instance_box()

    async def show_instances_box(self):
        if self.connected:
            self.all_instances_box.clear()
            self.instances.clear()

            dcr_ar_instances = await self.dcr_ar.get_instances(self.graph_id)
            db_instances = dbc.get_all_instances()
            my_instances = dbc.get_instances_for_user(self.user.email)
            my_instance_ids = (
                [instance_id for instance_id, _ in my_instances] if my_instances else []
            )

            if len(dcr_ar_instances) > 0 and db_instances:
                db_instance_ids = [instance_id for instance_id, _ in db_instances]
                self.instances = {
                    int(instance_id): name
                    for instance_id, name in dcr_ar_instances.items()
                    if int(instance_id) in db_instance_ids
                }

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

            self.all_instances_box.add(label)
            self.all_instances_box.add(new_instance_btn)
            self.all_instances_box.add(delete_all_instances_btn)

            instances_box = toga.Box(style=Pack(direction=COLUMN))
            for instance_id, instance_name in self.instances.items():
                buttons_box = toga.Box(style=Pack(direction=ROW))

                instance_button = toga.Button(
                    instance_name,
                    on_press=self.show_instance,
                    style=Pack(padding=5),
                    id=instance_id,
                    enabled=instance_id in my_instance_ids,
                )
                del_button = toga.Button(
                    "x",
                    on_press=self.delete_instance_by_id,
                    style=Pack(padding=5, color="red"),
                    id=f"x{instance_id}",
                    enabled=instance_id in my_instance_ids,
                )

                buttons_box.add(instance_button)
                buttons_box.add(del_button)
                instances_box.add(buttons_box)

            self.all_instances_box.add(instances_box)
            self.all_instances_box.refresh()
        else:
            print("Login first to see this tab")

    async def show_instance(self, widget):
        self.current_instance_id = widget.id
        self.option_container.current_tab = "Instance run"
        await self.show_instance_box()

    async def show_instance_box(self):
        self.instance_box.clear()

        events = await self.dcr_ar.get_events(
            self.graph_id, self.current_instance_id, EventsFilter.ALL
        )

        role_items = []
        if self.user.role:
            role_items.append(self.user.role)

        for event in events:
            event_role = event.role
            if event_role and event_role not in role_items:
                role_items.append(event_role)

        self.role_selection = toga.Selection(
            items=role_items,
            value=role_items[0] if len(role_items) > 0 else None,
            on_change=self.role_changed,
            style=Pack(padding=5),
        )

        if len(role_items) > 0:
            self.role_selection.value = role_items[0]
            self.user.role = self.role_selection.value

        current_instance_box = toga.Box(style=Pack(direction=ROW, flex=1))

        other_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        current_role = toga.Label("Current role")
        selected_role_label = toga.Label("Select other role")
        other_box.add(current_role)
        other_box.add(selected_role_label)
        other_box.add(self.role_selection)
        current_instance_box.add(other_box)

        current_instance_label = toga.Label("Current instance")
        current_instance_box.add(current_instance_label)

        self.instance_box.add(current_instance_box)
        events_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        for event in events:
            color = None
            btn_enabled = True
            text = event.label

            if event.enabled:
                color = "green"
            if event.pending:
                color = "blue"
                text = text + " !"

            if len(event.role) > 0:
                if event.role != self.user.role:
                    btn_enabled = False
                text = text + f" (role: {event.role})"

            if event.enabled:
                event_button = toga.Button(
                    text=text,
                    style=Pack(padding=5, color=color),
                    id=event.id,
                    on_press=self.execute_event,
                    enabled=btn_enabled,
                )
                events_box.add(event_button)

        self.instance_box.add(events_box)


        self.instance_box.refresh()

    async def delete_instance_by_id(self, widget):
        instance_id = widget.id[1:]
        await self.dcr_ar.delete_instance(self.graph_id, instance_id)

        dbc.delete_instance(instance_id)
        if instance_id == self.current_instance_id:
            self.instance_box.clear()
            self.instance_box.add(
                toga.Label(
                    "Select an instance from the All instances tab or create a new!"
                )
            )
            self.instance_box.refresh()

        await self.show_instances_box()

    async def create_new_instance(self, widget):
        self.current_instance_id = await self.dcr_ar.create_new_instance(self.graph_id)
        events = await self.dcr_ar.get_events(
            self.graph_id, self.current_instance_id, EventsFilter.ALL
        )
        has_pending = any(event.pending for event in events)
        dbc.insert_instance(
            self.current_instance_id,
            not has_pending,  # valid is True if there are no pending events
            self.user.email,
        )

        self.option_container.current_tab = "Instance run"
        await self.show_instances_box()
        await self.show_instance_box()

    async def delete_all_instances(self, widget):
        user_instances = dbc.get_instances_for_user(self.user.email)
        if user_instances:
            for (
                instance_id,
                _,
            ) in user_instances:
                dbc.delete_instance(instance_id)
            self.instance_box.clear()
            self.instance_box.add(
                toga.Label(
                    "Select an instance from the All instances tab or create a new!"
                )
            )
            self.instance_box.refresh()
            await self.show_instances_box()

    async def login_handler(self, widget):
        self.connected = await check_login_from_dcr(
            self.username_input.value, self.password_input.value
        )
        if self.connected:
            self.user = DcrUser(self.username_input.value, self.password_input.value)
            self.dcr_ar = DcrActiveRepository(self.user)

            self.user.role = dbc.get_dcr_role(email=self.user.email)
            print(f"[i] Role: {self.user.role}")

            self.option_container.content.append(self.all_instances_item)
            self.option_container.current_tab = "All instances"
            self.option_container.content.remove("Login")
            self.option_container.content.append(self.instance_run_item)
            self.option_container.content.append(self.logout_item)

        else:
            print("Login failed, try again.")


def main():
    return HelloWorld()
