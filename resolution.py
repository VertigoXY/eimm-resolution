import utils
import utility_prio
import damaging_prio


def main():
    actions = utils.get_actions()
    for action in actions:
        print(action)

    utility_prio.resolve(actions)
    damaging_prio.resolve(actions)


if __name__ == '__main__':
    main()
