from random import randint, choice

bokumons_name = [
    ['Pan', 'Popan', 'Pandaro'],
    ['Hippop', 'Papotas','Hippapo'],
    ['Fant', 'Mast', 'Masfant'],
    ['Girf', 'Ferg', 'Girarff'],
    ['Oik', 'Linok', 'Cokinik'],
    ['Koely', 'Ryolty', 'Robity'],
    ['Parrot', 'Pardok', 'Pardokan'],
    ['Ping', 'Pong', 'Pingpong'],
    ['Snacks', 'Serpett','Snakonda'],
    ['Monk','Mukiny','Monking']]

bokumons_base_stats = {
        # life, attack, defense, speed, crit_chance
        'Pan': [18, 14, 17, 9, 0],
        'Popan': [24, 20, 23, 15, 2], # +6
        'Pandaro': [30, 26, 29, 21, 4], # +12

        'Hippop': [15, 18, 19, 9, 1],
        'Papotas': [21, 24, 25, 15, 2],
        'Hippapo': [27, 30, 31, 21, 3],

        'Fant': [17, 17, 16, 8, 0],
        'Mast': [23, 23, 22, 14, 1],
        'Masfant': [29, 29, 28, 20, 2],

        'Girf': [16, 13, 16, 10, 0],
        'Ferg': [22, 19, 22, 16, 2],
        'Girarff':[28, 25, 28, 22, 3],

        'Oik':  [13, 14, 16, 10, 2],
        'Linok': [19, 20, 22, 16, 4],
        'Cokinik':[25, 26, 28, 22, 5],

        'Koely': [14, 11, 11, 19, 2],
        'Ryolty': [20, 17, 17, 25, 3],
        'Robity': [26, 23, 23, 31, 5],

        'Parrot': [12, 19, 11, 17, 5], 
        'Pardok': [18, 25, 17, 23, 5], 
        'Pardokan': [24, 31, 23, 29, 7], 

        'Ping': [15, 16, 16, 12, 2],
        'Pong': [21, 22, 22, 18, 3],
        'Pingpong': [27, 28, 28, 24, 4],

        'Snacks': [13, 15, 11, 19, 3],
        'Serpett': [19, 21, 17, 25, 4],
        'Snakonda': [25, 27, 23, 31, 5],

        'Monk': [12, 15, 15, 18, 4],
        'Mukiny': [18, 21, 21, 24, 5],
        'Monking': [24, 27, 27, 30, 6],
    }

def initial_atrib(name, lvl_diff):
    boku_lvl_diff = lvl_diff if lvl_diff > 0 else 0
    boku_stats = [randint(bokumons_base_stats[name][0] + round(1.5*boku_lvl_diff), bokumons_base_stats[name][0] + round(2.5*boku_lvl_diff)),
                  randint(bokumons_base_stats[name][1] + round(1.5*boku_lvl_diff), bokumons_base_stats[name][1] + round(2.5*boku_lvl_diff)),
                  randint(bokumons_base_stats[name][2] + round(1.5*boku_lvl_diff), bokumons_base_stats[name][2] + round(2.5*boku_lvl_diff)),
                  randint(bokumons_base_stats[name][3] + round(1.5*boku_lvl_diff), bokumons_base_stats[name][3] + round(2.5*boku_lvl_diff)),
                  randint(bokumons_base_stats[name][4] + round(boku_lvl_diff/2), bokumons_base_stats[name][4] + boku_lvl_diff)]

    if lvl_diff < 0:
        boku_stats[0] -= randint(0, 3)
        boku_stats[1] -= randint(0, 3)
        boku_stats[2] -= randint(0, 3)
        boku_stats[3] -= randint(0, 2)
        boku_stats[4] -= 1 if boku_stats[4] > 0 else 0

    return boku_stats

def bokumons_spawn_selector(boku_player_lvl):
    boku_selected = bokumons_name[randint(0, len(bokumons_name)-1)]
    list_sel = [[0,1,0,1,0,1,0,1,1,1], [2,2,1,2,1,2,1,2,0,2]] #[40%-0| 60%-1] , [60%-2,30%-1,10%-0]
    boku_name = ''
    if boku_player_lvl <= 16:
        boku_name = boku_selected[0]
    elif 16 < boku_player_lvl <= bokumons_evo_lvl[boku_selected[1]] + 2: 
        boku_name = boku_selected[choice(list_sel[0])]
    else: 
        boku_name = boku_selected[choice(list_sel[1])]
    return boku_name

bokumons_evo_lvl = {
    'Pan': 16,
    'Popan': 36,

    'Hippop': 14,
    'Papotas': 30,

    'Fant': 20,
    'Mast': 38,

    'Girf': 15,
    'Ferg': 26,

    'Oik': 18,
    'Linok': 27,

    'Koely': 12,
    'Ryolty': 23,

    'Parrot': 16,
    'Pardok': 36,

    'Ping': 28,
    'Pong': 36,

    'Snacks': 20,
    'Serpett': 40,

    'Monk': 16,
    'Mukiny': 36
}

bokumons_evo_steps = {
    'Pan': ['Popan', 'Pandaro'],
    'Popan': ['Pandaro'],
    'Pandaro': [],

    'Hippop': ['Papotas', 'Hippapo'],
    'Papotas': ['Hippapo'],
    'Hippapo': [],

    'Fant': ['Mast', 'Masfant'],
    'Mast': ['Masfant'],
    'Masfant': [],

    'Girf': ['Ferg', 'Girarff'],
    'Ferg': ['Girarff'],
    'Girarff': [],

    'Oik': ['Linok', 'Cokinik'],
    'Linok': ['Cokinik'],
    'Cokinik': [],

    'Koely': ['Ryolty', 'Robity'],
    'Ryolty': ['Robity'],
    'Robity': [],

    'Parrot': ['Pardok', 'Pardokan'],
    'Pardok': ['Pardokan'],
    'Pardokan': [],

    'Ping': ['Pong', 'Pingpong'],
    'Pong': ['Pingpong'],
    'Pingpong': [],

    'Snacks': ['Serpett', 'Snakonda'],
    'Serpett': ['Snakonda'],
    'Snakonda': [],

    'Monk': ['Mukiny', 'Monking'],
    'Mukiny': ['Monking'],
    'Monking': []
}