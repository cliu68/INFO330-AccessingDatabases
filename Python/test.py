import sqlite3
import sys

pokemon = sqlite3.connect("../pokemon.sqlite")
con = pokemon.cursor()

types = ["bug", "dark", "dragon", "electric", "fairy", "fight", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water"]

if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []

for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    pokedex_number = int(arg)
    query = f"SELECT name FROM pokemon WHERE pokedex_number={pokedex_number}"
    con.execute(query)
    result = con.fetchone()
    name = result[0]

    query = f"SELECT type1, type2 FROM pokemon_types_view WHERE name = '{name}'"
    con.execute(query)
    result = con.fetchone()
    type1 = result[0]
    type2 = result[1]

    query = f"SELECT * FROM pokemon_types_battle_view WHERE type1name = '{type1}' AND type2name = '{type2}'"
    con.execute(query)
    result = con.fetchone()

    strong_against = []
    weak_against = []
    for t in types:
        against_column = f"against_{t}"
        against_value = result[result.description.index((against_column,))]
        if against_value > 1:
            strong_against.append(t)
        elif against_value < 1:
            weak_against.append(t)

    team.append({"name": name, "strong": strong_against, "weak": weak_against})
    print(f"{name}: strong against {', '.join(strong_against)}; weak against {', '.join(weak_against)}")

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")
