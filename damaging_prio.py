from action import Action


def resolve_standard(actions: list[Action]):
    shots = [action for action in actions if 'Standard Shot' in action.desc]
    non_blocked_shots = Action.filter_blocked(shots)
    for shot in non_blocked_shots:
        shot.succeeded(True)
        print(f'shooter: {shot}')
        shot_target = shot.get_target_row(actions)
        print(f'target: {shot_target}')
        # shot_target should be a list with one element, if not then you messed up somewhere
        shot_target.update_cell('damage', shot.mt)


def resolve_vig(actions: list[Action]):
    vigs = Action.filter_blocked([action for action in actions if 'Vigilante' in action.desc])
    for vig in vigs:
        print(vig)
        vig.succeeded(True)
        vig_target = vig.get_target_row(actions)
        vig_target.update_cell('damage', vig.mt)


def resolve(actions: list[Action]):
    resolve_vig(actions)
    resolve_standard(actions)


