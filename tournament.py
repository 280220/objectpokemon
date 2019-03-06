import sys
import argparse
import importlib.util
import random
# from importlib.machinery import SourceFileLoader

def load_pokemon_from_file(filepath):
    spec = importlib.util.spec_from_file_location("", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # return SourceFileLoader("", filepath).load_module()
    return module

def pokemon_alive(poke1, poke2):
    return poke1.is_alive() and poke2.is_alive()

def simulate_battle(poke1, poke2):
    # Choose a random pokemon to start
    if random.randint(0, 1) == 1:
        attacking_poke, defending_poke = poke1, poke2
    else:
        attacking_poke, defending_poke = poke2, poke1

    print("Pokemon", attacking_poke.get_name(), "gets to start")

    while pokemon_alive(poke1, poke2):
        move = attacking_poke.choose_move(defending_poke)
        print(attacking_poke.get_name(), "chooses", move.get_name())
        inflicted = defending_poke.inflict(move, attacking_poke)
        print(attacking_poke.get_name(), "inflicts", inflicted, "damage on", defending_poke.get_name())

        attacking_poke, defending_poke = defending_poke, attacking_poke

    if attacking_poke.is_alive():
        winner = attacking_poke
    else:
        winner = defending_poke

    print("The winner is", winner.get_name(), "with", winner.hp, "HP left")
    return winner


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Runs a pokemon tournament')
    parser.add_argument('pokemon_files', type=str, nargs='+',
                        help='the files that contain pokemon classes')
    parser.add_argument('-b', type=int, help='how many battles to run')

    args = parser.parse_args()

    num_battles = args.b if args.b else 100
    if len(args.pokemon_files) < 2:
        print('too few pokemon for a tournament')
        sys.exit(1)

    pokemon = []
    for pokemon_file in args.pokemon_files:
        print('loading', pokemon_file)
        poke = load_pokemon_from_file(pokemon_file)
        pokemon.append(poke)

    wins_table = [[0]*len(pokemon) for _ in range(len(pokemon))]

    for i, poke_mod_1 in enumerate(pokemon):
        for j, poke_mod_2 in enumerate(pokemon):
            for _ in range(num_battles):
                p1 = poke_mod_1.Pokemon()
                p2 = poke_mod_2.Pokemon()
                winner = simulate_battle(p1, p2)
                if winner == p1:
                    wins_table[i][j] += 1
                else:
                    wins_table[j][i] += 1
                print()

    string_wins = [[str(x) for x in row] for row in wins_table]
    # Insert names into wins table
    names = [pm.Pokemon().get_name() for pm in pokemon]
    for i, name in enumerate(names):
        string_wins[i].insert(0, name)
    string_wins.insert(0, [''] + names)

    # Work out longest names and so formatting
    col_lens = [max(map(len, col)) for col in zip(*string_wins)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in col_lens)
    string_table = [fmt.format(*row) for row in string_wins]
    print('\n'.join(string_table))


