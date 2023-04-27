screen_width = 800
screen_height = 600

tile_size = 32

# posição do wild bokumon e do player na batalha
boku_pos = [[600, 200], [170, 400]]
# posição dos textos da cena de batalha
overlay_battle_pos = [[20, 500], [20, 540], [screen_width/2 + 50, 500], [screen_width/2 + 250, 500], 
                                            [screen_width/2 + 50, 540], [screen_width/2 + 250, 540]]

overlay_bokumon_pos = [[50, 65], [250, 65], [screen_width/2 + 80, screen_height/2 + 45], 
                                       [screen_width/2 + 280, screen_height/2 + 45], [screen_width/2 + 240, 410]]

# posição dos nomes dos ataques
bokumon_moves_pos = [[25, 500], [220, 500], [25, 550], [220, 550]]

# posição do botao de seleção
select_button_pos = [[[screen_width/2 + 35, 505], [screen_width/2 + 235, 505]],
                     [[screen_width/2 + 35, 545], [screen_width/2 + 235, 545]]]

select_move_button_pos = [[[10, 505], [205, 505]],
                          [[10, 555], [205, 555]]]

# seleção da continuação da fight
select_cont_fight = [[screen_width - 110, screen_height - screen_height/4.5 + 35], 
                        [screen_width - 110, screen_height - screen_height/4.5 + 85]]


# menu descrições
menu_description = {
    'Bokumon': ['Check and organize Bokumon that are', 'traveling with you in your party.'],
    'Bag': ['Equipped with pockets for storing items you', 'bought, received, or found.'],
    'Save': ['Save your game with a complete record of', 'your progress to take a break.'],
    'Exit': ['Close this menu window.'],
}

