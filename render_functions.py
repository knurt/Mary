import tcod as libtcod

def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    #fov 재계산 시만
    if fov_recompute:
        #지도에 있는 모든 타일을 그림
        for y in range(game_map.height):
            for x in range(game_map.width):
                #wall 불리언에 tile의 block_sight이 True인지 여부를 대입
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, colors.get('pitch_black'), libtcod.BKGND_SET)


    #목록에 있는 모든 객체를 표시함.
    for entity in entities:
        draw_entity(con, entity, fov_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    #목록에 있는 모든 객체를 제거함.
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    #객체를 표시함.
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    #객체를 화면에서 지움
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)