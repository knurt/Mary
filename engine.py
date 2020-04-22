import tcod 
import numpy as np

#엔티티 및 컴포너트
from entity import Entity
from components.luminary import Luminary
from map_objects.game_map import GameMap

#렌더링 기능
from renderer.lighting_functions import compute_light
from renderer.render_functions import clear_all, render_all
from renderer.fov_functions import initialize_fov, recompute_fov

#조작 및 기타
from input_handlers import handle_keys
from debugs import Debug

#변수 정보
from data import *

def main():

    """
    객체 생성
    """
    #플레이어 객체 생성. 위치는 맵 중앙.
    luminary_component = Luminary(luminosity=3)
    player = Entity(int(map_width/2),int(map_height/2),'@',tcod.white, 'player', blocks=False, luminary=luminary_component)
    entities = [player]

    #지도 객체 생성: y,x는 game_map 객체에서 알아서 처리
    game_map = GameMap(map_width,map_height)

    #FOV
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    """
    디버그 명령 목록
    passwall: 벽 통과 가능
    showpos: 플레이어 x,y좌표 표시. 다른 엔티티 좌표도 표시할 수 있게 고칠 것
    """
    #디버그용 객체 생성. 디버그 기능들은 기본적으로 꺼져 있고, 인자를 넣으면 활성화
    debug = Debug()

    
    #키보드, 마우스 입력 처리용 객체 생성
    key = tcod.Key()
    mouse = tcod.Mouse()

    #콘솔 con 생성
    con = tcod.console.Console(screen_width, screen_height)



    #폰트 설정: 10x10파일, 이미지 파일은 그레이스케일, 배열 방식은 TCOD
    #tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    #폰트 설정: 32x32파일, 이미지 파일은 그레이스케일, 배열 방식은 CP437
    tcod.console_set_custom_font('terminal32x32.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_CP437)

    #스크린 생성: 스크린 가로/세로, 이름, 전체화면 여부
    tcod.console_init_root(screen_width, screen_height, 'tcod tutorial revised', False, vsync=True)
    

    #TCOD 루프
    while not tcod.console_is_window_closed():
        """
        입력
        """
        #사용자 입력을 받음: 키 누를 시, 키보드, 마우스
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        
        
        """
        화면 표시
        """
        #플레이어 시야
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        """
        광원 계산
        """
        for E in entities:
            try:
                #이 구문을 뚫으면 광원이 있는거. 루프를 돌려서 광원 지도를 구해온다.
                #광원 지도는 fov_function을 이용할 것
                compute_light(fov_map,E.x,E.y)
            except:
                pass
        
        """
        화면 표시
        """
        #표시할 모든 객체를 화면에 배치함
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

        #화면 출력
        tcod.console_flush()

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
            if debug.passwall == False:
                if not game_map.is_blocked(player.x + dx, player.y + dy):
                    player.move(dx, dy)

                    fov_recompute = True
            else:
                if game_map.is_blocked(player.x + dx, player.y + dy):
                    debug.dbg_msg("You magically pass through solid wall.")
                player.move(dx, dy)

        #최대화면이 True일 시, 전체화면이 아니라면 콘솔을 전체화면으로 전환함
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        """
        기타
        """

        #플레이어 위치 표시
        if debug.showpos: debug.show_pos(player,'player')

        #벽 설치
        toggle_wall = action.get('toggle_wall')

        #광원 설치
        create_luminary = action.get('create_luminary')

        if toggle_wall:
            game_map.toggle_wall(player.x, player.y)
            #지형이 변했으니 새로 지형 맵을 짜야 함
            fov_map = initialize_fov(game_map)
        
        if create_luminary:
            game_map.create_luminary(entities, player.x, player.y)

        
        """
        엔티티
        """
        #광원 없는 엔티티에게 호출하면 에러뜸
        for E in entities:
            try:
                print (F"{E.name} luminosity:{E.luminary.luminosity}")
            except:
                print (F"{E.name} is not a lighting source")




if __name__ == '__main__':
    main()