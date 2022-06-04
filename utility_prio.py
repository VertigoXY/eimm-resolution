from action import Action


def resolve_shot_empower(actions: list[Action]):
    empowers = [action for action in actions if 'Shot Empower' in action.desc]
    non_blocked_empowers = Action.filter_blocked(empowers)
    shots = [action for action in actions if 'Standard Shot' in action.desc]
    for empower in non_blocked_empowers:
        empower.succeeded(True)
        for shot in shots:
            if shot.user == empower.target:
                shot.empowered()


def resolve_shotblock(actions: list[Action]):
    shotblocks = [action for action in actions if 'Shotblock' in action.desc]
    non_blocked_shotblocks = Action.filter_blocked(shotblocks)
    shots = [action for action in actions if 'Standard Shot' in action.desc]
    for shotblock in non_blocked_shotblocks:
        shotblock.succeeded(True)
        print(f'shotblock succeeds: {shotblock}')
        for shot in shots:
            if shot.user == shotblock.target and shot.modifiers['empowered'] is False:
                shot.succeeded(False)
                print(f'shot blocked: {shot}')


# Reminder that blocked shots cannot be redirected or delayed
def resolve_shot_hijack(actions: list[Action]):
    shotjacks = [action for action in actions if 'Shot Hijack (input)' in action.desc]
    redirect_to = [action for action in actions if 'Shot Hijack (output)' in action.desc]
    non_blocked_shotjacks = Action.filter_blocked(shotjacks)
    redirect_to = Action.filter_blocked(redirect_to)
    shots = Action.filter_blocked([action for action in actions if 'Standard Shot' in action.desc])
    for _input, output in zip(non_blocked_shotjacks, redirect_to):
        _input.succeeded(True)
        output.succeeded(True)
        for shot in shots:
            if shot.user == _input.target and shot.modifiers['empowered'] is False:
                shot.hijacked(output)


def resolve_shot_delay(actions: list[Action]):
    delays = [action for action in actions if 'Shot Delay' in action.desc]
    non_blocked_delays = Action.filter_blocked(delays)
    shots = Action.filter_blocked([action for action in actions if 'Standard Shot' in action.desc])
    for delay in non_blocked_delays:
        delay.succeeded(True)
        for shot in shots:
            if shot.user == delay.target and shot.modifiers['empowered'] is False:
                shot.delayed()


def resolve_mt_modifiers(actions: list[Action]):
    buffs = Action.filter_blocked([action for action in actions if 'MT Buff' in action.desc])
    debuffs = Action.filter_blocked([action for action in actions if 'MT Debuff' in action.desc])
    shots = [action for action in actions if 'Standard Shot' in action.desc]
    for buff in buffs:
        print(buff)
        buff.succeeded(True)
        for shot in shots:
            if shot.user == buff.target:
                shot.mt += buff.mt
                shot.add_message(f'{shot.mt} mt')
    for debuff in debuffs:
        print(debuff)
        debuff.succeeded(True)
        for shot in shots:
            if shot.user == debuff.target:
                shot.mt -= debuff.mt
                shot.add_message(f'{shot.mt} mt')


def resolve_doc(actions: list[Action]):
    doctors = [action for action in actions if 'Doctor' in action.desc]
    non_blocked_docs = Action.filter_blocked(doctors)
    for doctor in non_blocked_docs:
        print(doctor)
        doctor.succeeded(True)
        doc_target = doctor.get_target_row(actions)
        doc_target.update_cell('protection', doctor.mt)


def resolve(actions: list[Action]):
    resolve_shot_empower(actions)
    resolve_doc(actions)
    resolve_mt_modifiers(actions)
    resolve_shotblock(actions)
    resolve_shot_hijack(actions)
    resolve_shot_delay(actions)
