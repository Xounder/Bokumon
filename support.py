import pygame

def blit_text(text, color, pos, font, right=False, center=False):
    display_surface = pygame.display.get_surface()
    overlay_txt = font.render(text, False, color)
    if right:
        overlay_txt_rect = overlay_txt.get_rect(topright= (pos))
    elif center:
        overlay_txt_rect = overlay_txt.get_rect(center= (pos))
    else:
        overlay_txt_rect = overlay_txt.get_rect(topleft= (pos))
        
    display_surface.blit(overlay_txt, overlay_txt_rect)

def blit_text_shadow(text, color, pos, font, back_color='black', right=False, center=False):
    blit_text(text, back_color, [pos[0] + 2, pos[1] + 2], font, right, center)
    blit_text(text, color, pos, font, right, center)

def save_game(player, bag):
    # usado no menu_player
    file = open('saves/bokumon_save.txt', 'w')
    file.write(f'{player.name};{player.previous_status};{player.position};{player.tickets}')
    file.write('\n')
    for boku in player.bokumons:
        file.write(f'{boku.name};{boku.level};{boku.life};{boku.atual_life};{boku.attack};{boku.defense};{boku.speed};{boku.critical_chance};{boku.atual_exp};{boku.up_exp};{boku.all_exp};{boku.ball};{boku.atual_name}/{boku.moves[0]}/{boku.moves[1]}/{boku.moves[2]}/{boku.moves[3]}/')
    file.write('\n')
    for boku in player.bokumon_storage:
        file.write(f'{boku.name};{boku.level};{boku.life};{boku.atual_life};{boku.attack};{boku.defense};{boku.speed};{boku.critical_chance};{boku.atual_exp};{boku.up_exp};{boku.all_exp};{boku.ball};{boku.atual_name}/{boku.moves[0]}/{boku.moves[1]}/{boku.moves[2]}/{boku.moves[3]}/')
    file.write('\n')
    for section in bag.all_items.values():
        for items in section:
            file.write(f'{items}/')
        file.write('\n')

def load_game():
    # usado no level menu
    try:
        file = open('saves/bokumon_save.txt', 'r')
        line = file.readlines()
        list_words = []
        aux_list = []
        for i, l in enumerate(line):
            if l.count('/') == 0:
                list_words.append(l.replace('\n','').split(';'))
            else:
                for seq in l.split('/'):
                    if seq.split(';')[0] != '\n':
                        aux_list.append(seq.split(';'))
                list_words.append(aux_list[:])
                aux_list.clear()
        return list_words
    except Exception as e:
        return False

def text_to_list(text):
    text = text.replace('[','').replace(']','').replace(' ','').split(',')
    for i in range(len(text)):
        if text[i].isnumeric():
            text[i] = int(text[i])
    return text

def list_text_to_int(list_text):
    for i in range(len(list_text)):
        if list_text[i].replace('.','').isnumeric():
            list_text[i] = int(float(list_text[i]))
    return list_text

