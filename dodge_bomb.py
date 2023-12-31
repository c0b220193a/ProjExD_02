import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {  # 練習３　押下キーと移動量の辞書
    pg.K_UP: (0, -5),  # 横方向移動量、縦方向移動量
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値多プルを返す関数
    引数 rct:こうかとんor爆弾SurfaceのRect
    戻り値: 横方向縦方向はみ出し判定結果 (画面内:True/画面外:False)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し判定
        yoko =  False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し判定
        tate = False
    return (yoko, tate)  # タプルを戻す


def check_kouka(sum_mv):
    """
    こうかとんが進んでいる方向の画像番号を出力する関数
    引数 こうかとんの進む sum_mv のx軸とy軸を引数とする。
    戻り値 正しい画像番号の数値 
    (押されているキーに応じたkk_imgsにおいてふさわしい画像番号を出力)
    """
    kakunum = [[0, +5, +5, +5, 0, -5, -5, -5],
               [-5, -5, 0, +5, +5, +5, 0, -5]]  # 位置の選択肢
    for i in range(8):  # ８回ループし、一つずつの検証をおこなう
        if (sum_mv[0] == kakunum[0][i] and sum_mv[1] == kakunum[1][i]):
            return int(i)
        

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_han = pg.transform.flip(kk_img, True, False)  # 画像を反転して保存
    kk_imgs = []  # こうかとんの角度を保存する画像のリストを作成する
    kk_img_new = kk_img  # 初期の定義をおこなう
    kk_num = [[90, 45, 0, -45, -90], [45, 0, -45]]
    for do in kk_num[0]:  # kk_imgsに角度におけるこうかとんの画像を追加
        kk_imgs.append(pg.transform.rotozoom(kk_img_han, do, 1.0))
    for do in kk_num[1]:
        kk_imgs.append(pg.transform.rotozoom(kk_img, do, 1.0))

    kk_img2 = pg.image.load("ex02/fig/4.png")  # 新しい画像の挿入 ゲーム終了時点の画像
    kk_img2 = pg.transform.rotozoom(kk_img2, 0, 2.5)

    kk_rct = kk_img.get_rect()  # こうかとんのれくとを抽出
    kk_rct.center = (900, 400)  # こうかとんの初期座標

    bb_img = pg.Surface((20, 20))  # 練習１ 透明のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習１半径10の赤色の円を作る
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  # 四角形を抽出
    bb_rct.centerx = random.randint(0, WIDTH)  # x座標を設定
    bb_rct.centery = random.randint(0, HEIGHT)  # y座標を設定
    vx, vy = +5, -5
    numnew = 100 # 最初にゲームオーバーしないように少し大きい値を設定しておく

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            numnew = 0  # 後に判定をおこなう関数を０にする
        
        # 少し後にゲーム終了するモノを判定する関数
        numnew += 1  # numnewがtmrのようにカウントしていく。

        if numnew == 30:  # 新しく設定したnumnewが30に到達したらゲームを終了する
            print("GameOver")  # ゲームを終了する
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():  # キーが押された際にsum_mvに合計移動量が足される
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        # こうかとん
        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        if sum_mv[0] != 0 or sum_mv[1] != 0:  # もし、キーボードが押されているならば
            kk_img_new = kk_imgs[check_kouka(sum_mv)]  # kk_img_newを更新する
        if numnew <= 99:  # 一度爆弾に触れると画像が変換される。爆弾に触れると
            kk_img_new = kk_img2  # 新しく挿入した画像を出力
        screen.blit(kk_img_new, kk_rct)

        # 爆弾
        for i in range(1, 11):  # 爆弾の加速処理、時間が達したら条件に合わせて足される
            if tmr == (i*100):  # tmrが100の倍数になったとき
                if vx >= 0:  # vxが０以上の時は加速度を１する
                    vx += 1
                else:  # vxが０未満の時は加速を-1する。
                    vx -= 1
                if vy >= 0:  # vyが０以上の時加速度を１する
                    vy += 1
                else:  # vyが０未満の時加速度を-1する。
                    vy -= 1
                
        bb_rct.move_ip(vx, vy)  # 練習２爆弾の移動処理
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)


        pg.display.update()
        tmr += 1
        clock.tick(50)  # フレームレートを50に設定する。


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()