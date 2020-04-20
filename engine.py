import tcod as libtcod
from entity import Entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

from debugs import Debug

#메인 루프
def main():
    #스크린 가로/세로 크기
    screen_width = 40
    screen_height = 25
    map_width = 30
    map_height = 20

    #타일 색깔
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    """
    객체 생성
    """
    #플레이어 객체 생성
    player = Entity(int(screen_width/2),int(screen_height/2),'@',libtcod.white)
    entities = [player]

    #지도 객체 생성
    game_map = GameMap(map_width, map_height)

    #디버그용 객체 생성
    debug = Debug()
    
    #키보드, 마우스 입력 처리용 객체 생성
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    #콘솔 con 생성
    con = libtcod.console_new(screen_width, screen_height)



    #폰트 설정: 10x10파일, 이미지 파일은 그레이스케일, 배열 방식은 TCOD
    #libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    #폰트 설정: 32x32파일, 이미지 파일은 그레이스케일, 배열 방식은 CP437
    libtcod.console_set_custom_font('terminal32x32.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)

    #스크린 생성: 스크린 가로/세로, 이름, 전체화면 여부
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    

    #TCOD 루프
    while not libtcod.console_is_window_closed():
        """
        입력
        """
        #사용자 입력을 받음: 키 누를 시, 키보드, 마우스
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        
        """
        화면 표시
        """
        #표시할 모든 객체를 화면에 배치함
        render_all(con, entities, game_map, screen_width, screen_height, colors)

        #화면 출력
        libtcod.console_flush()

        #화면 초기화
        clear_all(con, entities)

        """
        입력에 대한 상호작용
        """
        #action 변수에 키보드 입력값을 사전 형태로 받아옴
        action = handle_keys(key)

        #action 변수에 입력한 키워드에 대응한 값을 move 변수에 대입
        move = action.get('move') 
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        #move변수에 대입된 값이 있을 시 이동
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        """
        기타
        """
        #최대화면이 True일 시, 전체화면이 아니라면 콘솔을 전체화면으로 전환함
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        #플레이어 위치 표시
        debug.show_pos(player,'player')


if __name__ == '__main__':
    main()