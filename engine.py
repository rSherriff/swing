from __future__ import annotations

import time
from enum import Enum, auto
from threading import Timer
from typing import TYPE_CHECKING

import numpy as np
import tcod
from playsound import playsound
from tcod.console import Console

import tile_types
from application_path import get_app_path
from effects.melt_effect import MeltWipeEffect, MeltWipeEffectType
from effects.horizontal_wipe_effect import HorizontalWipeDirection, HorizontalWipeEffect
from effects.vertical_wipe_effect import VerticalWipeDirection, VerticalWipeEffect
from entities.player import Player
from input_handlers import EventHandler, MainGameEventHandler
from sections.menu import Menu
from sections.pitch import Pitch
from sections.map import Map
from sections.activities_bar import ActivitiesBar
from sections.statbar import Statbar
from sections.county_info import CountyInfo
from sections.turn_summary import TurnSummary
from sections.confirmation import Confirmation
from sections.notification import Notification
from utils.delta_time import DeltaTime
from verbs.activities import Activities
from verbs.policies import policy_templates
from fonts.font_manager import FontManager

from counties.county_manager import CountyManager


class GameState(Enum):
    MENU = auto()
    IN_GAME = auto()
    TURN_SUMMARY = auto()
    GAME_OVER = auto()
    COMPLETE = auto()


class Engine:
    def __init__(self, teminal_width: int, terminal_height: int):

        self.screen_width = teminal_width
        self.screen_height = terminal_height
        self.delta_time = DeltaTime()

        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.mouse_location = (0, 0)

        self.setup_effects()
        self.setup_sections()

        self.music_timer = Timer(77, self.play_music)
        self.play_music()

        self.entities = []
        self.tick_length = 2
        self.time_since_last_tick = -2

        self.state = GameState.IN_GAME

        self.county_manager = CountyManager()

        self.activity_points = 5
        self.power = 0
        self.support = 0

        self.turn_number = 1
        self.turn_summary_text = list()

        self.fontmanager = FontManager()
        self.fontmanager.add_font("number_font")

    def render(self, root_console: Console) -> None:
        """ Renders the game to console """
        for section_key, section_value in self.get_active_sections():
            if section_key not in self.disabled_sections:
                section_value.render(root_console)

        if self.state == GameState.IN_GAME or self.state == GameState.GAME_OVER:
            for entity in self.entities:
                root_console.print(entity.x, entity.y,
                                   entity.char, fg=entity.color)

        if self.full_screen_effect.in_effect == True:
            self.full_screen_effect.render(root_console)
        else:
            self.full_screen_effect.set_tiles(root_console.tiles_rgb)

        if self.end_turn_effect.in_effect == True:
            self.end_turn_effect.render(root_console)
        else:
            self.end_turn_effect.set_tiles(root_console.tiles_rgb)

        # TEMP
        root_console.print(18, 1, str(self.mouse_location))
        root_console.print(3, 1, "Power:" + str(self.power))
        root_console.print(3, 2, "Support:" + str(self.support))
        root_console.print(3, 3, "Turn Number:" + str(self.turn_number))
        root_console.print(18, 2, "Activity Points:" +
                           str(self.activity_points))

    def update(self):
        """ Engine update tick """
        for _, section in self.get_active_sections():
            section.update()

        self.delta_time.update_delta_time()

        if self.state == GameState.IN_GAME:
            self.time_since_last_tick += self.get_delta_time()

            self.tick_length -= 0.0002
            if self.time_since_last_tick > self.tick_length and self.state == GameState.IN_GAME:
                self.time_since_last_tick = 0

            for entity in self.entities:
                entity.update()

    def handle_events(self, context: tcod.context.Context):
        self.event_handler.handle_events(
            context, discard_events=self.full_screen_effect.in_effect or self.state == GameState.GAME_OVER)

    def setup_game(self):
        self.player = Player(self, 7, 4)
        self.entities.clear()
        self.entities.append(self.player)
        self.tick_length = 2

    def setup_effects(self):
        self.full_screen_effect = MeltWipeEffect(
            self, 0, 0, self.screen_width, self.screen_height, MeltWipeEffectType.RANDOM, 40)
        self.end_turn_effect = HorizontalWipeEffect(
            self, 0, 0, self.screen_width, self.screen_height)

    def setup_sections(self):
        self.menu_sections = {}
        self.menu_sections["Menu"] = Menu(
            self, 0, 0, self.screen_width, self.screen_height)

        self.game_sections = {}
        self.game_sections["statbar"] = Statbar(
            self, 0, 0, self.screen_width, 5)
        self.game_sections["map"] = Map(self, 0, 5, 75, 49)
        self.game_sections["countyinfo"] = CountyInfo(self, 75, 5, 53, 49)
        self.game_sections["actionsbar"] = ActivitiesBar(
            self, 0, 54, self.screen_width, 10)
        self.game_sections["confirmationDialog"] = Confirmation(
            self, 35, 25, 60, 10)
        self.game_sections["notificationDialog"] = Notification(
            self, 35, 25, 60, 10)

        self.turn_summary_sections = {}
        self.turn_summary_sections["turnsummary"] = TurnSummary(
            self, 30, 9, 68, 46)

        self.completion_sections = {}

        self.disabled_sections = ["confirmationDialog", "notificationDialog"]
        self.solo_ui_section = ""

    def get_active_sections(self):
        if self.state == GameState.MENU:
            return self.menu_sections.items()
        elif self.state == GameState.IN_GAME:
            return self.game_sections.items()
        elif self.state == GameState.TURN_SUMMARY:
            return self.turn_summary_sections.items()
        elif self.state == GameState.COMPLETE:
            return self.completion_sections.items()

    def get_active_ui_sections(self):
        if self.state == GameState.MENU:
            return self.menu_sections.items()
        elif self.state == GameState.IN_GAME:
            if "confirmationDialog" not in self.disabled_sections:
                return {"confirmationDialog": self.game_sections["confirmationDialog"]}.items()
            if "notificationDialog" not in self.disabled_sections:
                return {"notificationDialog": self.game_sections["notificationDialog"]}.items()
            return self.game_sections.items()
        elif self.state == GameState.TURN_SUMMARY:
            return self.turn_summary_sections.items()
        elif self.state == GameState.COMPLETE:
            return self.completion_sections.items()

    def enable_section(self, section):
        self.disabled_sections.remove(section)

    def disable_section(self, section):
        self.disabled_sections.append(section)

    def close_menu(self):
        self.state = GameState.IN_GAME
        self.setup_game()
        self.full_screen_effect.start()

    def open_menu(self):
        self.state = GameState.MENU
        self.full_screen_effect.start()

    def game_over(self):
        self.state = GameState.GAME_OVER
        Timer(3, self.open_menu).start()

    def complete_game(self):
        self.state = GameState.COMPLETE
        self.full_screen_effect.start()

    def get_delta_time(self):
        return self.delta_time.get_delta_time()

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def play_music(self):
        return
        playsound(get_app_path() + "/sounds/music.wav", False)
        self.music_timer = Timer(77, self.play_music)
        self.music_timer.start()

    def quit(self):
        if self.music_timer.is_alive():
            self.music_timer.cancel()
        raise SystemExit()

    def unlock_selected_county(self):
        cost = self.county_manager.get_selected_county().unlock_cost

        if self.power >= cost:
            self.county_manager.unlock_selected_county()
            self.power -= cost

    def advance_turn(self):
        self.turn_summary_text.clear()

        # Process news article based on what activities are about to happen
        total_power, total_support = 0, 0
        for county, values in self.county_manager.process_all_activites().items():
            county_summary = [county, values[0],
                              values[1], values[2], values[3]]
            self.turn_summary_text.append(county_summary)
            self.power += values[0]
            total_power += values[0]

            self.support += values[1]
            total_support += values[1]

        self.turn_summary_text.append(["Total", total_power, total_support])
        self.turn_summary_text.append(["New Values", self.power, self.support])

        self.turn_number += 1
        self.activity_points = 5
        self.state = GameState.TURN_SUMMARY
        self.end_turn_effect.start(HorizontalWipeDirection.RIGHT)

    def close_turn_summary(self):
        self.state = GameState.IN_GAME
        self.end_turn_effect.start(HorizontalWipeDirection.RIGHT)

    def add_activity(self, type):
        if self.activity_points > 0:
            self.county_manager.add_activity(type)
            self.activity_points -= 1
        else:
            print("Not enough activity points to add activity " + str(type) +
                  " to " + self.county_manager.get_selected_county().name)

    def remove_activity(self, type):
        if self.county_manager.remove_activity(type):
            self.activity_points += 1

    def enact_policy(self, type):
        if self.can_enact_policy(type):
            self.county_manager.enact_policy(type)
            self.support -= policy_templates[type].cost
        else:
            print("Not enough support to enact " + str(type) + " in " +
                  self.county_manager.get_selected_county().name)

    def can_enact_policy(self, type):
        return self.support >= policy_templates[type].cost

    def can_unlock_selected_county(self):
        return self.power >= self.county_manager.get_selected_county().unlock_cost

    def is_ui_paused(self):
        return self.full_screen_effect.in_effect or self.end_turn_effect.in_effect

    def open_confirmation_dialog(self, text, confirmation_action):
        self.game_sections["confirmationDialog"].setup(
            text, confirmation_action)
        self.enable_section("confirmationDialog")

    def close_confirmation_dialog(self):
        self.disable_section("confirmationDialog")

    def open_notification_dialog(self, text):
        self.game_sections["notificationDialog"].setup(text)
        self.enable_section("notificationDialog")

    def close_notification_dialog(self):
        self.disable_section("notificationDialog")
