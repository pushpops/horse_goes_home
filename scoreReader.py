def make_notes_time_ary(bpm, score):
    # 数字一つが16分音符を表す
    time_16th_note = 60/bpm/4 # 60秒/bpmで4分音符の長さ、それを1/4して16分音符の長さ
    notes_time = []
    is_hurdle = []
    time = 0

    for i in range(len(score)):
        for j in range(len(score[i])):
            # 0は16部休符　何もしない
            if score[i][j] == 0:
                pass
            # 1は普通のノーツ、時間を配列に格納、フラグは立てない
            elif score[i][j] == 1:
                notes_time.append(time)
                is_hurdle.append(False)
            # 2はジャンプのノーツ、時間を配列に格納、フラグを立てる
            elif score[i][j] == 2:
                notes_time.append(time)
                is_hurdle.append(True)
            # 時間を進める
            time += time_16th_note
    return notes_time, is_hurdle