import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {  #練習３　押下キーと移動量の辞書
    pg.K_UP: (0, -5),  #横方向移動量、縦方向移動量
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()  #こうかとんのれくとを抽出
    kk_rct.center = (900, 400)  #こうかとんの初期座標

    bb_img = pg.Surface((20, 20))  #練習　１透明のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  #練習１　半径10の赤色の円を作る
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  #四角形を抽出
    bb_rct.centerx = random.randint(0, WIDTH)  #x座標を設定
    bb_rct.centery = random.randint(0, HEIGHT)  #y座標を設定
    vx, vy = +5, -5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():  #キーが押された際にsum_mvに合計移動量が足される
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  #練習２爆弾の移動処理
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()