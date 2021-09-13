from sections.section import Section
from actions.actions import Action
from ui.confirmation_ui import ConfirmationUI


class Confirmation(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int):
        super().__init__(engine, x, y, width, height)

        self.text = ""
        self.ui = ConfirmationUI(self, x, y, self.tiles["graphic"])

    def setup(self, text, confirmation_action):
        self.text = text
        self.ui.reset(confirmation_action)

    def render(self, console):
        super().render(console)
        console.print(self.x + 4, self.y + 1, self.text, (0, 0, 0))
