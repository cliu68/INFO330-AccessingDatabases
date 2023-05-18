import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# open the database connection and create a cursor object
pokemon = sqlite3.connect("pokemon.sqlite")
con = pokemon.cursor()

# execute python script: python3 TeamAnalyzer.py 1 2 3 4 5 6

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()
# create an empty list to store the team
team = []

# loop through the list of pokedex numbers in the input list
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    # get the name of the Pokemon with the given pokedex number from the "pokemon table"
    pokedex_number = int(arg)
    query = f"select name from pokemon where pokedex_number={pokedex_number}"
    con.execute(query)
    result = con.fetchone()
    name = result[0]


    # get the types of the Pokemon from the "pokemon_types_view" table
    query = f"select type1, type2 from pokemon_types_view where name = '{name}'"
    con.execute(query)
    type = con.fetchone()
    type1 = type[0]
    type2 = type[1]

    #get the "against" values from the "pokemon_types_battle_view" table
    query= f"select * from pokemon_types_battle_view where type1name = '{type1}'and type2name= '{type2}'"
    #con.execute(query)
    #result = con.fetchone()
    against = con.execute(query).fetchone()

    # determine which types are strong or weak against the Pokemon based on the "against" value
    strong_against = []
    weak_against = []
    for i, t in enumerate(against):
        if i == 0 or i == 1:
            continue
        if t > 1:
            strong_against.append(types[i-2])
        if t < 1:
            weak_against.append(types[i - 2])
    
    # add the pokemon and its strong/weak types to the team list
    team.append({"name": name, "strong":strong_against, "weak": weak_against})
    # print the analysis for the pokemon
    #print(f"{name}: strong against {', '(strong_against)}; weak against {', '(weak_against)}")
    print (name + "type: " + type1 + type2 + "strong: " + str(strong_against) + "weak: " + str(weak_against))


# ask the user if they want to save the team
answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

# run it in command line: python TeamAnalyzer.py 1 2 3 4 5 6



