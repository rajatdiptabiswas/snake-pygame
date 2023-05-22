from Snake_Game import *
from FF_narvivork import *

def jooksuta_mang_AI(game_window, fps_controller, weights):
    max_score = 0
    avg_score = 0
    test_mange = 1
    score1 = 0
    samme_mangu_kohta = 1000
    score2 = 0

    for _ in range(test_mange):
        snake_pos, snake_body, food_pos, score = alustamispositsioonid()

        loe_sama_suunda = 0
        eelmine_suund = 0

        for _ in range(samme_mangu_kohta):
            hetke_suuna_siht, on_ees_blokk, on_vasakul_blokk, on_paremal_blokk = blokeeritud_suunad(
                snake_body)
            nurk, ussi_suuna_siht, toidu_suuna_siht_normaliseeritud, ussi_suuna_siht_normaliseeritud = get_nurk_toiduga(
                snake_body, food_pos)
            ennustused = []
            ennustatud_suund = np.argmax(np.array(forward_propagation(np.array(
                [on_vasakul_blokk, on_ees_blokk, on_paremal_blokk, toidu_suuna_siht_normaliseeritud[0],
                 ussi_suuna_siht_normaliseeritud[0], toidu_suuna_siht_normaliseeritud[1],
                 ussi_suuna_siht_normaliseeritud[1]]).reshape(-1, 7), weights))) - 1

            if ennustatud_suund == eelmine_suund:
                loe_sama_suunda += 1
            else:
                loe_sama_suunda = 0
                eelmine_suund = ennustatud_suund

            uus_suund = np.array(snake_body[0]) - np.array(snake_body[1])
            if ennustatud_suund == -1:
                uus_suund = np.array([uus_suund[1], -uus_suund[0]])
            if ennustatud_suund == 1:
                uus_suund = np.array([-uus_suund[1], uus_suund[0]])

            button_direction = genereeri_liikumissuund(uus_suund)

            jargmine_samm = snake_body[0] + hetke_suuna_siht
            if aare_puutumine(snake_body[0]) == 1 or \
                    enda_puutumine(jargmine_samm.tolist(), snake_body) == 1:
                score1 += -150
                break

            else:
                score1 += 0

            snake_body, food_pos, score = mangi(snake_pos, snake_body, food_pos,
                                                button_direction, score, game_window, fps_controller)

            if score > max_score:
                max_score = score

            if loe_sama_suunda > 8 and ennustatud_suund != 0:
                score2 -= 1
            else:
                score2 += 2


    return score1 + score2 + max_score * 5000