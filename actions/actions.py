from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

from entities.entity import Entity

if TYPE_CHECKING:
    from engine import Engine


class Action:
    def __init__(self, engine) -> None:
        super().__init__()
        self.engine = engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        self.engine.quit()
        
class CloseMenu(Action):
    def perform(self) -> None:
        self.engine.close_menu()

class OpenMenu(Action):
    def perform(self) -> None:
        self.engine.open_menu()

class ShowTooltip(Action):
    def __init__(self, engine, tooltip_key: str) -> None:
        super().__init__(engine)
        self.tooltip_key = tooltip_key

    def perform(self):
        self.engine.show_tooltip(self.tooltip_key)

class HideTooltip(Action):
    def __init__(self, engine, tooltip_key: str) -> None:
        super().__init__(engine)
        self.tooltip_key = tooltip_key

    def perform(self):
        self.engine.hide_tooltip(self.tooltip_key)

class GameOver(Action):
    def perform(self) -> None:
        self.engine.game_over()
        
class DeleteEntity(Action):
    def __init__(self, engine, entity):
        super().__init__(engine)
        self.entity = entity

    def perform(self):
        self.engine.remove_entity(self.entity)

class SelectCounty(Action):
    def __init__(self, engine, county):
        super().__init__(engine)
        self.county = county

    def perform(self):
        self.engine.county_manager.selected_county = self.county

class PerformActivity(Action):
    def __init__(self, engine, type):
        super().__init__(engine)
        self.type = type

    def perform(self):
        self.engine.process_activity(self.type)

class UnlockCounty(Action):
    def __init__(self, engine):
        super().__init__(engine)

    def perform(self):
        self.engine.unlock_selected_county()

class AdvanceTurn(Action):
    def __init__(self, engine):
        super().__init__(engine)

    def perform(self):
        self.engine.advance_turn()

class AddActivity(Action):
    def __init__(self, engine, type) -> None:
        super().__init__(engine)
        self.type = type
    
    def perform(self) -> None:
        return self.engine.add_activity(self.type)

class RemoveActivity(Action):
    def __init__(self, engine, type) -> None:
        super().__init__(engine)
        self.type = type
    
    def perform(self) -> None:
        return self.engine.remove_activity(self.type)

class EnactPolicy(Action):
    def __init__(self, engine, type) -> None:
        super().__init__(engine)
        self.type = type
    
    def perform(self) -> None:
        return self.engine.enact_policy(self.type)

class DisableSection(Action):
    def __init__(self, engine, section) -> None:
        super().__init__(engine)
        self.section = section
    
    def perform(self) -> None:
        return self.engine.disable_section(self.section)

class CloseTurnSummary(Action):
    def __init__(self, engine) -> None:
        super().__init__(engine)
    
    def perform(self) -> None:
        return self.engine.close_turn_summary()

