import random
import requests

POKEMON_LIST = [
    "arceus",
    "greninja",
    "snorlax",
    "jynx",
    "gengar",
    "ditto"
]

API_URL = "https://pokeapi.co/api/v2/pokemon/{}"


def get_pokemon_data(name):
    """Retrieve a Pokemon's data from PokeAPI."""
    try:
        response = requests.get(API_URL.format(name.lower()), timeout=10)

        if response.status_code == 404:
            print(f"Pokemon '{name}' was not found.")
            return None

        response.raise_for_status()
        data = response.json()

        return {
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "abilities": [ability["ability"]["name"] for ability in data["abilities"]],
        }

    except requests.exceptions.Timeout:
        print("The request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        print("Could not connect to PokeAPI. Check your internet connection.")
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")
    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")
    except (KeyError, ValueError):
        print("Could not process the data returned by the API.")

    return None


def play_game():
    pokemon_name = random.choice(POKEMON_LIST)
    pokemon = get_pokemon_data(pokemon_name)

    if pokemon is None:
        print("Unable to start the game because Pokémon data could not be retrieved.")
        return
    
    height_m = pokemon["height"] / 10
    weight_kg = pokemon["weight"] / 10

    print("\n=== WHO'S THAT POKÉMON? ===")
    print("Guess the Pokémon using the clues below.")
    print(f"Height: {height_m:.1f} meters")
    print(f"Weight: {weight_kg:.1f} kilograms")
    print(f"Abilities: {', '.join(pokemon['abilities'])}")
    print("You have 3 attempts.")
    print("=============================\n")

    for attempt in range(1, 4):
        guess = input(f"Attempt {attempt}/3 - Your guess: ").strip().lower()

        if not guess:
            print("Please enter a Pokémon name.")
            continue

        guessed_pokemon = get_pokemon_data(guess)
        if guessed_pokemon is None:
           
            print("That is not a valid Pokémon name. Try again.")
            continue

        if guessed_pokemon["name"] == pokemon["name"]:
            print("================================\n")
            print(f"Correct! It's {pokemon['name'].capitalize()}!")
            print("================================\n")
            return

        if attempt < 3:
            print("Incorrect guess. Try again.")

    print(f"Out of attempts! The correct Pokémon was {pokemon['name'].capitalize()}.")


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame ended.")
