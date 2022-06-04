import re
import gspread
from action import Action, get_sheet


def get_records():
    return get_sheet().get_all_records()


def get_mt_value(action_desc: str):
    template_regex = '^(\d) MT ([\w\s\-\(\)\,\.]+)$'
    if (match := re.search(template_regex, action_desc)) is not None:
        return int(match.group(1))
    else:
        return None


def state_after_disruptive(outcome_value: str):
    success = False if re.search('fail|block', outcome_value) is not None else None
    empowered = True if re.search('strongwill', outcome_value) is not None else False
    return success, empowered


def get_actions():
    records = get_records()
    actions = list()
    for row, record in enumerate(records, start=2):
        noise = True if 'Noise' in record['Player'] else False
        if record['Action Name'] == '' and not noise: continue  # idgaf about empty cells
        user = record['Alias']
        desc = record['Action Description']
        priority = record['Priority']
        effect = record['B/H/N']
        target = record['Final Target'] if record['Final Target'] else record['Input']
        mt = int(record['MT']) if record['MT'] else get_mt_value(desc)
        success, empowered = state_after_disruptive(record['Outcome'])
        cells = dict()
        cells['outcome'] = gspread.Cell(row, 16, record['Outcome'])
        cells['damage'] = gspread.Cell(row, 21, record['Dmg'])
        cells['protection'] = gspread.Cell(row, 20, record['Prt'])
        cells['final target'] = gspread.Cell(row, 15, record['Final Target'])

        action = Action(user, noise, mt, desc, priority, effect, target, success, cells)
        action.modifiers["ninja"] = True if record['Ninja'] == 'TRUE' else False
        action.modifiers["temporary"] = True if record['Temp'] == 'TRUE' else False
        action.modifiers["empowered"] = empowered

        actions.append(action)
    return actions
