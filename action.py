from __future__ import annotations

import time

import gspread
from dataclasses import dataclass, field
from typing import Optional, ClassVar

SHEET_NAME = ''
PAGE_NAME = ''


def get_sheet():
    client = gspread.oauth(credentials_filename='conf/google_credentials.json')
    page = client.open(SHEET_NAME).worksheet(PAGE_NAME)
    return page


@dataclass
class Action:
    user: str  # alias, not player
    noise: bool
    mt: Optional[int]
    desc: str
    priority: str
    effect: str
    target: str
    success: Optional[bool]
    cells: dict[str, gspread.Cell]
    sheet: ClassVar[gspread.Worksheet] = get_sheet()
    modifiers: dict[str, Optional[bool]] = field(init=False)

    # TODO: add a last night target for consecutive targeting (if relevant)

    def __post_init__(self):
        self.modifiers = dict(empowered=False, strongman=None,
                              ninja=False, blocked=False,
                              hijacked=False, temporary=False)

    def get_target_row(self, actions: list[Action]) -> Action:
        return [action for action in actions if action.user == self.target and
                ('Standard Shot' in action.desc or action.noise)][0]

    def succeeded(self, success: bool):
        self.success = success
        current_outcome_msg = self.cells['outcome'].value
        if 'fails' in current_outcome_msg or 'success' in current_outcome_msg:
            return
        success_msg = "success" if success else "fails"
        new_msg = current_outcome_msg + f', {success_msg}' if current_outcome_msg else success_msg
        self.sheet.update_cell(self.cells['outcome'].row, self.cells['outcome'].col, new_msg)
        time.sleep(5)
        self.cells['outcome'].value = new_msg

    def hijacked(self, redirected: Action):
        self.target = redirected.target
        current_outcome_msg = self.cells['outcome'].value
        if current_outcome_msg:
            new_msg = current_outcome_msg + f', redirected to {redirected.target}'
        else:
            new_msg = f'redirected to {redirected.target}'
        self.sheet.update_cell(self.cells['outcome'].row, self.cells['outcome'].col, new_msg)
        self.sheet.update_cell(self.cells['final target'].row, self.cells['final target'].col, redirected.target)
        time.sleep(5)
        self.cells['outcome'].value = new_msg
        self.cells['final target'].value = redirected.target

    def delayed(self):
        self.success = False
        current_outcome_msg = self.cells['outcome'].value
        if current_outcome_msg:
            new_msg = current_outcome_msg + ", delayed"
        else:
            new_msg = "delayed"
        self.sheet.update_cell(self.cells['outcome'].row, self.cells['outcome'].col, new_msg)
        time.sleep(5)
        self.cells['outcome'].value = new_msg

    def empowered(self):
        self.modifiers['empowered'] = True
        self.sheet.update_cell(self.cells['outcome'].row, self.cells['outcome'].col, 'strongwill')
        time.sleep(5)
        self.cells['outcome'].value = 'strongwill'

    def add_message(self, msg: str):
        current_outcome_msg = self.cells['outcome'].value
        if current_outcome_msg:
            new_msg = current_outcome_msg + f', {msg}'
        else:
            new_msg = msg
        self.sheet.update_cell(self.cells['outcome'].row, self.cells['outcome'].col, new_msg)
        time.sleep(5)
        self.cells['outcome'].value = new_msg

    def update_cell(self, label: str, value: int):
        current_value = int(self.cells[label].value) if self.cells[label].value else 0
        new_value = current_value + value
        self.sheet.update_cell(self.cells[label].row, self.cells[label].col, new_value)
        time.sleep(5)
        self.cells[label].value = new_value

    @staticmethod
    def filter_blocked(actions: list[Action]) -> list[Action]:
        return [action for action in actions if action.success is not False and action.target != '']  # fuck idlers
