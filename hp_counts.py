import gspread

SHEET_NAME = "Turbo Xerox Metal Raiders Besieged: Ultimate Pro Tour Duelist Series signups (Responses)"  # change this
PAGE_NAME = "n5"  # change this too (each night)


def main():
    client = gspread.oauth(credentials_filename='google_credentials.json') # change this too (store them in a safe place)
    page = client.open(SHEET_NAME).worksheet(PAGE_NAME)

    records = page.get_all_records()

    for row in records:
        player = row["Player"]
        hp = row["Final"]
        action = row["Action Name"]
        not_a_player = player == "NOISE" or action == "Plusle Standard Shot" or action == "Cockroach NPC"
        # replace this with whatever non-player lines you have in your sheet (kept the xerox example here)

        if hp != "" and hp > 0 and not not_a_player:
            # i dont care about empty lines meh
            print(f"{player} {hp}")


if __name__ == "__main__":
    main()