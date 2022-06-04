import gspread

SHEET_NAME = ''
PAGE_NAME = ''


# TODO: change from raw sheet requests to actions

def get_records() -> list[dict]:
    client = gspread.oauth(credentials_filename='conf/google_credentials.json')
    page = client.open(SHEET_NAME).worksheet(PAGE_NAME)

    return page.get_all_records()


def track(track_target: str):
    records = get_records()
    tracked = set()
    for record in records:
        action_has_target = record['Input'] != ''
        is_target = record['Alias'] == track_target
        ninja = record['Ninja'] == 'TRUE'
        if is_target and action_has_target and not ninja:
            tracked.add(record['Input'])

    if len(tracked) == 0:
        print(f'{track_target} visited nobody.')
    else:
        print(f'{track_target} visited:')
        for elem in tracked:
            print(elem)


def watch(watcher: str, watch_target: str):
    records = get_records()
    watched = set()
    for record in records:
        ninja = record['Ninja'] == 'TRUE'
        instant_prio = record['Priority'] == 'Instant'
        self_watch = record['Alias'] == watcher
        is_target = record['Input'] == watch_target
        action_succeeded = 'succ' in record['Outcome']
        if is_target and not self_watch and not instant_prio and action_succeeded and not ninja:
            watched.add(record['Alias'])

    if len(watched) == 0:
        print(f'{watch_target} was visited by nobody.')
    else:
        print(f'{watch_target} was visited by:')
        for elem in watched:
            print(elem)


if __name__ == '__main__':
    pass
