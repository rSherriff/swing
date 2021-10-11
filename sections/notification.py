from sections.section import Section
from actions.actions import Action
from ui.notification_ui import NotificationUI


class Notification(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        super().__init__(engine, x, y, width, height, "notification_dialog.xp")

        self.text = ""
        self.ui = NotificationUI(self, x, y, self.tiles["graphic"])

    def setup(self, text):
        self.text = text

    def render(self, console):
        super().render(console)
        console.print(self.x + 4, self.y + 2, self.text, (255, 255, 255))
