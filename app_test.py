import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(layout="wide", page_title="Accumulated Data Keyboard")

    # --- CSS設定 (Streamlit自体のスタイル) ---
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
                max-width: 100%;
            }
            iframe {
                width: 100% !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("大きさの変わるキーボードアプリ")
    st.caption("「Start」ボタンを押すと全画面表示になります。10文字入力すると自動的に次の回に進みます（全25回）。")

    # --- サイドバー設定 ---
    with st.sidebar:
        st.header("拡大機能の設定")
        scale_enabled = st.toggle("拡大機能 ON/OFF", value=True)
        
        breath_speed = st.slider("変化速度 (秒/周期)", 0.1, 10.0, 2.0, 0.1)
        scale_min = st.slider("最小サイズ", 0.0, 1.0, 0.8, 0.1)
        scale_max = st.slider("最大サイズ", 1.0, 2.0, 1.1, 0.1)

        st.divider()

        st.header("移動機能の設定")
        move_enabled = st.toggle("移動機能 ON/OFF", value=True)
        
        one_move_duration = st.slider("移動の速さ (秒/回)", 0.1, 20.0, 1.0, 0.1)
        move_range = st.slider("移動範囲 (px)", 0, 200, 30, 10)

        st.subheader("移動の規則性")
        move_pattern = st.radio("移動順序モード", ["規則的 (順序指定)", "ランダム"], index=1)

        # 方向定義
        dir_labels = ["上", "右上", "右", "右下", "下", "左下", "左", "左上"]
        dir_vectors = {
            "上": (0, -1), "右上": (1, -1), "右": (1, 0), "右下": (1, 1),
            "下": (0, 1), "左下": (-1, 1), "左": (-1, 0), "左上": (-1, -1)
        }
        
        # 移動パスの生成
        generated_path = []
        cycle_count = 20 
        
        base_dirs = list(dir_vectors.values())
        
        if move_pattern == "ランダム":
            random_seed = st.number_input("乱数シード (Seed)", value=42, step=1, help="同じ値を入力すると再現性が保たれます")
            rng = random.Random(random_seed)
            for _ in range(cycle_count):
                cycle = base_dirs.copy()
                rng.shuffle(cycle)
                generated_path.extend(cycle)
        else:
            st.caption("以下で移動する順番を設定してください (デフォルト: 時計回り)")
            user_order = []
            with st.expander("移動順序の編集", expanded=True):
                default_order = ["上", "右上", "右", "右下", "下", "左下", "左", "左上"]
                for i in range(8):
                    selected_label = st.selectbox(
                        f"{i+1}番目の移動先", 
                        dir_labels, 
                        index=dir_labels.index(default_order[i]),
                        key=f"dir_step_{i}"
                    )
                    user_order.append(dir_vectors[selected_label])
            
            for _ in range(cycle_count):
                generated_path.extend(user_order)

    # --- CSS Keyframes の生成 ---
    total_steps = len(generated_path)
    total_move_duration = one_move_duration * total_steps
    
    keyframes_css = "@keyframes floatKeyframes {"
    step_percent = 100 / total_steps
    
    for i, (dx, dy) in enumerate(generated_path):
        start_p = i * step_percent
        mid_p   = start_p + (step_percent / 2)
        end_p   = (i + 1) * step_percent
        
        tx = dx * move_range
        ty = dy * move_range
        
        if i == 0:
            keyframes_css += f"0% {{ transform: translate(0px, 0px); }}"
        
        keyframes_css += f"{mid_p:.4f}% {{ transform: translate({tx}px, {ty}px); }}"
        keyframes_css += f"{end_p:.4f}% {{ transform: translate(0px, 0px); }}"

    keyframes_css += "}"


    # --- キーボードデータ定義 ---
    rows = [
        # Row 1
        [
            {"label": "~", "sub": "`", "val": "`", "w": 1},
            {"label": "!", "sub": "1 ぬ", "val": "1", "w": 1},
            {"label": "@", "sub": "2 ふ", "val": "2", "w": 1},
            {"label": "#", "sub": "3 あ", "val": "3", "w": 1},
            {"label": "$", "sub": "4 う", "val": "4", "w": 1},
            {"label": "%", "sub": "5 え", "val": "5", "w": 1},
            {"label": "^", "sub": "6 お", "val": "6", "w": 1},
            {"label": "&", "sub": "7 や", "val": "7", "w": 1},
            {"label": "*", "sub": "8 ゆ", "val": "8", "w": 1},
            {"label": "(", "sub": "9 よ", "val": "9", "w": 1},
            {"label": ")", "sub": "0 わ", "val": "0", "w": 1},
            {"label": "-", "sub": "ー", "val": "-", "w": 1,},
            {"label": "+", "sub": "=", "val": "=", "w": 1},
            {"label": "BS", "sub": "", "val": "BS", "w": 2,},
        ],
        # Row 2
        [
            {"label": "Tab", "sub": "", "val": "Tab", "w": 1.5, "align": "left"},
            {"label": "Q", "sub": "た", "val": "q", "w": 1},
            {"label": "W", "sub": "て", "val": "w", "w": 1},
            {"label": "E", "sub": "い", "val": "e", "w": 1},
            {"label": "R", "sub": "す", "val": "r", "w": 1,},
            {"label": "T", "sub": "か", "val": "t", "w": 1},
            {"label": "Y", "sub": "ん", "val": "y", "w": 1},
            {"label": "U", "sub": "な", "val": "u", "w": 1},
            {"label": "I", "sub": "に", "val": "i", "w": 1},
            {"label": "O", "sub": "ら", "val": "o", "w": 1},
            {"label": "P", "sub": "せ", "val": "p", "w": 1},
            {"label": "{", "sub": "「", "val": "{", "w": 1,},
            {"label": "}", "sub": "」", "val": "}", "w": 1,},
            {"label": "|", "sub": "ー", "val": "|", "w": 1,},
        ],
        # Row 3
        [
            {"label": "Caps", "sub": "", "val": "Caps", "w": 1.8, "align": "left"},
            {"label": "A", "sub": "ち", "val": "a", "w": 1},
            {"label": "S", "sub": "と", "val": "s", "w": 1},
            {"label": "D", "sub": "し", "val": "d", "w": 1,},
            {"label": "F", "sub": "は", "val": "f", "w": 1,},
            {"label": "G", "sub": "き", "val": "g", "w": 1},
            {"label": "H", "sub": "く", "val": "h", "w": 1},
            {"label": "J", "sub": "ま", "val": "j", "w": 1},
            {"label": "K", "sub": "の", "val": "k", "w": 1},
            {"label": "L", "sub": "り", "val": "l", "w": 1},
            {"label": ":", "sub": ";", "val": ":", "w": 1},
            {"label": "\"", "sub": "'", "val": "\"", "w": 1}, 
            {"label": "Enter", "sub": "", "val": "Enter", "w": 2.2, "align": "right"},
        ],
        # Row 4
        [
            {"label": "Shift", "sub": "", "val": "LShift", "w": 2.3, "align": "left"}, # LShift
            {"label": "Z", "sub": "つ", "val": "z", "w": 1},
            {"label": "X", "sub": "さ", "val": "x", "w": 1},
            {"label": "C", "sub": "そ", "val": "c", "w": 1},
            {"label": "V", "sub": "ひ", "val": "v", "w": 1},
            {"label": "B", "sub": "こ", "val": "b", "w": 1},
            {"label": "N", "sub": "み", "val": "n", "w": 1},
            {"label": "M", "sub": "も", "val": "m", "w": 1},
            {"label": "<", "sub": "、", "val": "<", "w": 1},
            {"label": ">", "sub": "。", "val": ">", "w": 1},
            {"label": "?", "sub": "・", "val": "?", "w": 1},
            {"label": "Shift", "sub": "", "val": "RShift", "w": 2.7, "align": "right"}, # RShift
        ],
        # Row 5
        [
            {"label": "Ctrl", "sub": "", "val": "LCtrl", "w": 1.5}, # LCtrl
            {"label": "Fn", "sub": "", "val": "Fn", "w": 1},
            {"label": "Win", "sub": "", "val": "LWin", "w": 1},   # LWin
            {"label": "Alt", "sub": "", "val": "LAlt", "w": 1},   # LAlt
            {"label": "", "sub": "", "val": "Space", "w": 5},
            {"label": "Alt", "sub": "", "val": "RAlt", "w": 1},   # RAlt
            {"label": "Win", "sub": "", "val": "RWin", "w": 1},   # RWin
            {"label": "Ctrl", "sub": "", "val": "RCtrl", "w": 1}, # RCtrl
            {"label": "←", "sub": "", "val": "Left", "w": 1},
            {"label": "↑", "sub": "", "val": "Up", "w": 1},
            {"label": "↓", "sub": "", "val": "Down", "w": 1},
            {"label": "→", "sub": "", "val": "Right", "w": 1},
        ]
    ]

    rows_json = json.dumps(rows)
    
    # --- HTML/CSS/JS テンプレート ---
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500&family=Noto+Sans+JP:wght@400&display=swap');

        body {{
            font-family: 'Roboto Mono', 'Noto Sans JP', monospace;
            background-color: transparent;
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            overflow: hidden;
            user-select: none;
        }}

        #experiment-area {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding-top: 20px;
            background-color: transparent; 
            transition: background-color 0.3s;
        }}

        #experiment-area:fullscreen {{
            background-color: white; 
            padding-top: 50px;
            justify-content: center;
        }}

        #experiment-area.pseudo-fullscreen {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background-color: white !important;
            z-index: 9999 !important;
            padding-top: 50px;
            justify-content: center;
        }}

        .input-container {{
            position: relative;
            width: 95%;
            height: 50px;
            margin-bottom: 20px;
            z-index: 200;
        }}

        #target-text {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            font-size: 24px;
            font-family: 'Roboto Mono', monospace; 
            color: #ccc; 
            display: flex;
            align-items: center;
            padding: 10px;
            box-sizing: border-box;
            z-index: 1;
            pointer-events: none;
            letter-spacing: 0px; 
            white-space: pre; 
        }}

        #screen {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.1); 
            color: #000;
            font-size: 24px;
            font-family: 'Roboto Mono', monospace;
            border-radius: 8px;
            padding: 10px;
            border: 2px solid #555;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            box-sizing: border-box;
            z-index: 2;
            letter-spacing: 0px;
            display: flex;
            align-items: center;
            overflow: hidden;
            white-space: pre;
        }}
        
        #screen.focused {{
            border-color: #2196F3;
            background-color: transparent; 
        }}

        .controls {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            z-index: 300;
            position: relative;
            align-items: center;
            flex-wrap: wrap;
            justify-content: center;
            width: 95%;
        }}

        button {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-family: 'Noto Sans JP', sans-serif;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: 0.2s;
        }}
        button:active {{ transform: translateY(2px); box-shadow: 0 2px 2px rgba(0,0,0,0.2); }}

        #start-btn {{ background-color: #ff9800; color: white; font-weight: bold; font-size: 18px; padding: 12px 30px; }}
        #start-btn:hover {{ background-color: #f57c00; }}
        
        .hidden {{ display: none !important; }}

        #next-btn {{ background-color: #2196F3; color: white; }}
        #next-btn:hover {{ background-color: #1e88e5; }}
        #next-btn:disabled {{ background-color: #90caf9; cursor: not-allowed; }}

        #download-btn {{ background-color: #4CAF50; color: white; }}
        #download-btn:hover {{ background-color: #45a049; }}

        #reset-btn {{ background-color: #f44336; color: white; }}
        #reset-btn:hover {{ background-color: #d32f2f; }}

        #data-count {{ 
            color: #333; 
            font-size: 18px; 
            font-weight: bold; 
            background: #fff;
            padding: 8px 15px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }}

        @keyframes breathe {{
            0% {{ transform: scaleX({scale_min}) scaleY({scale_min}); }}
            50% {{ transform: scaleX({scale_max}) scaleY({scale_max}); }}
            100% {{ transform: scaleX({scale_min}) scaleY({scale_min}); }}
        }}

        {keyframes_css}

        .movement-wrapper {{
            animation: floatKeyframes {total_move_duration}s infinite linear;
            animation-play-state: paused;
            width: 95%;
            display: flex;
            justify-content: center;
            padding: {move_range + 10}px; 
            box-sizing: border-box;
            opacity: 0.5;
            pointer-events: none;
            transition: opacity 0.3s;
        }}
        
        .movement-wrapper.active {{
            animation-play-state: {'running' if move_enabled else 'paused'};
            opacity: 1.0;
            pointer-events: auto;
        }}

        .keyboard-wrapper {{
            animation: breathe {breath_speed}s infinite ease-in-out;
            animation-play-state: paused;
            padding: 10px;
            background-color: #e8eaed;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 100%;
            height: 50vh; 
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
        }}
        
        .movement-wrapper.active .keyboard-wrapper {{
             animation-play-state: {'running' if scale_enabled else 'paused'};
        }}

        .kb-row {{
            display: flex;
            justify-content: space-between;
            width: 100%;
            height: 18%;
        }}

        .key {{
            background-color: white;
            border: 1px solid #999;
            border-bottom: 3px solid #777;
            border-radius: 4px;
            margin: 0 1px;
            position: relative;
            cursor: pointer;
            transition: background-color 0.1s;
            user-select: none;
            box-shadow: 0 2px 2px rgba(0,0,0,0.1);
            flex-basis: 0; 
            height: 100%;
            touch-action: none;
        }}

        .key.active {{
            transform: translateY(2px);
            border-bottom: 1px solid #777;
            background-color: #f0f0f0;
        }}

        .label-top {{
            position: absolute; top: 4px; left: 6px; font-size: 14px; color: #333; font-weight: bold;
        }}
        .label-sub {{
            position: absolute; bottom: 4px; right: 6px; font-size: 10px; color: #888;
        }}
        @media (max-width: 800px) {{
             .label-top {{ font-size: 10px; }}
             .label-sub {{ font-size: 8px; }}
        }}
        .color-red {{ background-color: #ea9999; border-color: #c06666; }}
        .color-yellow {{ background-color: #ffe599; border-color: #d1b866; }}
        .color-green {{ background-color: #b6d7a8; border-color: #7b9e6d; }}

    </style>
    </head>
    <body>
        <div id="experiment-area">
            
            <div class="input-container">
                <div id="target-text">password18</div>
                <div id="screen"></div>
            </div>
            
            <div class="controls">
                <button id="start-btn" onclick="startTask()">Start (Fullscreen)</button>
                <button id="next-btn" onclick="nextTrial()" disabled>送信 (Next Trial)</button>
                <button id="download-btn" onclick="downloadCSV()">CSVをダウンロード</button>
                <button id="reset-btn" onclick="resetData()">リセット</button>
                <span id="data-count">Trial: 1 | Rec: 0</span>
            </div>

            <div class="movement-wrapper" id="move-wrap">
                <div class="keyboard-wrapper" id="kb-wrap"></div>
            </div>
        </div>

        <script>
            const rows = {rows_json};
            const kbContainer = document.getElementById('kb-wrap');
            const screen = document.getElementById('screen');
            const targetText = document.getElementById('target-text');
            const dataCountLabel = document.getElementById('data-count');
            const startBtn = document.getElementById('start-btn');
            const nextBtn = document.getElementById('next-btn');
            const moveWrap = document.getElementById('move-wrap');
            const experimentArea = document.getElementById('experiment-area');
            
            const targetString = "password18";
            
            const MAX_INPUT_LENGTH = 10;
            const MAX_TRIALS = 25; 

            // --- 状態管理 ---
            let recordedData = JSON.parse(sessionStorage.getItem('kb_data') || '[]');
            let currentTrial = parseInt(sessionStorage.getItem('kb_trial') || '1');
            let lastDownTime = null;
            let lastUpTime = null;
            let taskStartTime = null; 
            let isStarted = false;
            
            let currentInputText = "";

            updateStatus();
            updateScreenDisplay(); 

            // ★ 完了時の処理
            function finishAllTrials() {{
                isStarted = false;
                moveWrap.classList.remove('active');
                screen.classList.remove('focused');
                
                // 全画面解除
                experimentArea.classList.remove('pseudo-fullscreen');
                if (document.exitFullscreen) document.exitFullscreen().catch(e => {{}});
                
                screen.textContent = "FINISHED";
                targetText.textContent = "";
                dataCountLabel.innerText = "Task Completed!";
                
                startBtn.disabled = true;
                nextBtn.disabled = true;
                alert("25トライアル終了しました。お疲れ様でした。CSVをダウンロードしてください。");
            }}

            function updateScreenDisplay() {{
                const inputLen = currentInputText.length;
                screen.textContent = "•".repeat(inputLen);
                
                const hiddenPrefix = " ".repeat(inputLen);
                const visibleSuffix = targetString.slice(inputLen);
                targetText.textContent = hiddenPrefix + visibleSuffix;
            }}

            function startTask() {{
                if (currentTrial > MAX_TRIALS) {{
                     finishAllTrials();
                     return;
                }}

                // ★ iPad対応: 常にCSSの疑似フルスクリーンを適用する (APIが効いても効かなくてもOK)
                experimentArea.classList.add('pseudo-fullscreen');

                // 一応PC向けに標準APIも試みる
                if (experimentArea.requestFullscreen) {{
                    experimentArea.requestFullscreen().catch(err => {{
                        console.log("Native fullscreen blocked, using pseudo-fullscreen.");
                    }});
                }} else if (experimentArea.webkitRequestFullscreen) {{ /* Safari */
                    experimentArea.webkitRequestFullscreen();
                }} else if (experimentArea.msRequestFullscreen) {{ /* IE11 */
                    experimentArea.msRequestFullscreen();
                }}

                isStarted = true;
                taskStartTime = Date.now();
                lastDownTime = taskStartTime;
                lastUpTime = taskStartTime;
                
                moveWrap.classList.add('active');
                screen.classList.add('focused');
                startBtn.classList.add('hidden');
                
                // スタート直後は送信ボタンを無効化
                nextBtn.disabled = true;
            }}

            rows.forEach(row => {{
                const rowDiv = document.createElement('div');
                rowDiv.className = 'kb-row';

                row.forEach(k => {{
                    const keyDiv = document.createElement('div');
                    keyDiv.className = 'key';
                    keyDiv.style.flexGrow = k.w;
                    if(k.color) keyDiv.classList.add('color-' + k.color);

                    let contentHtml = `<span class="label-top">${{k.label || ''}}</span><span class="label-sub">${{k.sub || ''}}</span>`;
                    keyDiv.innerHTML = contentHtml;

                    // ★修正点1: onpointerdown では記録の準備だけ行い、文字数は増やさない
                    keyDiv.onpointerdown = (e) => {{
                        if (!isStarted) return; 
                        e.preventDefault();

                        let keyVal = k.val || k.label || 'Unknown';

                        // 上限チェック
                        if (currentInputText.length >= MAX_INPUT_LENGTH) {{
                            return; 
                        }}

                        keyDiv.classList.add('active');
                        keyDiv.setPointerCapture(e.pointerId);

                        const now = Date.now();
                        const rect = kbContainer.getBoundingClientRect();
                        const style = window.getComputedStyle(kbContainer);
                        const matrix = new DOMMatrix(style.transform);
                        const currentScale = matrix.a;

                        let downDownTime = (now - lastDownTime);
                        let upDownTime = (now - lastUpTime);
                        let timeFromStart = (now - taskStartTime);

                        keyDiv._currentData = {{
                            trial: currentTrial,
                            key: keyVal,
                            downTime: now,
                            timeFromStart: timeFromStart,
                            downDown: downDownTime,
                            upDown: upDownTime,
                            kbScale: currentScale.toFixed(3),
                            kbX: rect.x.toFixed(1),
                            kbY: rect.y.toFixed(1),
                            pressure: e.pressure || 0,
                            area: (e.width * e.height).toFixed(2)
                        }};

                        lastDownTime = now;
                        // ここでは文字を増やさない！
                    }};

                    // ★修正点2: キャンセル時は、まだ文字が増えていないので、単に状態リセットするだけで良い
                    keyDiv.onpointercancel = (e) => {{
                        e.preventDefault();
                        if (!keyDiv._currentData) return;

                        // アクティブ状態解除のみ
                        keyDiv.classList.remove('active');
                        keyDiv.releasePointerCapture(e.pointerId);
                        keyDiv._currentData = null;
                        
                        // 文字数は変わっていないのでupdateScreenDisplayもしなくてOK
                    }};

                    // ★修正点3: onpointerup (指を離して保存確定) のタイミングで文字数を更新する
                    keyDiv.onpointerup = (e) => {{
                        if (!isStarted) return;
                        e.preventDefault();
                        
                        if (!keyDiv._currentData) return;

                        keyDiv.classList.remove('active');
                        keyDiv.releasePointerCapture(e.pointerId);
                        
                        const now = Date.now();
                        const holdTime = now - keyDiv._currentData.downTime;
                        
                        const record = {{
                            ...keyDiv._currentData,
                            upTime: now,
                            holdTime: holdTime
                        }};
                        
                        // ★ここで初めて文字数を操作＆データ保存 (完全同期)
                        if (currentInputText.length < MAX_INPUT_LENGTH) {{
                            let keyVal = record.key;
                            
                            if (keyVal === 'BS') {{
                                currentInputText = currentInputText.slice(0, -1);
                            }} else {{
                                if (keyVal.length === 1) {{
                                    currentInputText += keyVal;
                                }} else if (keyVal === 'Space') {{
                                    currentInputText += ' ';
                                }} else {{
                                    currentInputText += '■';
                                }}
                            }}
                            updateScreenDisplay();
                            
                            // データを保存
                            recordedData.push(record);
                            sessionStorage.setItem('kb_data', JSON.stringify(recordedData));
                            
                            lastUpTime = now;
                            updateStatus();
                        }}
                        
                        keyDiv._currentData = null;

                        // 自動遷移判定
                        if (currentInputText.length >= MAX_INPUT_LENGTH) {{
                            setTimeout(() => {{
                                if (currentTrial < MAX_TRIALS) {{
                                    nextTrial();
                                }} else {{
                                    finishAllTrials();
                                }}
                            }}, 200); 
                        }}
                        
                        // ボタン制御
                        if (currentInputText.length >= MAX_INPUT_LENGTH) {{
                            nextBtn.disabled = false;
                        }} else {{
                            nextBtn.disabled = true;
                        }}
                    }};
                    
                    rowDiv.appendChild(keyDiv);
                }});
                kbContainer.appendChild(rowDiv);
            }});

            function updateStatus() {{
                dataCountLabel.innerText = `Trial: ${{currentTrial}} / ${{MAX_TRIALS}} | Rec: ${{recordedData.length}}`;
            }}

            function nextTrial() {{
                currentTrial++;
                sessionStorage.setItem('kb_trial', currentTrial);
                
                currentInputText = "";
                updateScreenDisplay();
                
                taskStartTime = Date.now(); 
                lastDownTime = taskStartTime;
                lastUpTime = taskStartTime;
                
                updateStatus();
                // 次のトライアル開始時もボタンを無効化
                nextBtn.disabled = true;
            }}

            function resetData() {{
                if(confirm("データを全消去しますか？")) {{
                    recordedData = [];
                    currentTrial = 1;
                    sessionStorage.clear();
                    
                    currentInputText = "";
                    updateScreenDisplay();
                    
                    isStarted = false;
                    taskStartTime = null;
                    lastDownTime = null;
                    lastUpTime = null;
                    
                    moveWrap.classList.remove('active');
                    screen.classList.remove('focused');
                    
                    startBtn.classList.remove('hidden'); 
                    startBtn.disabled = false;
                    nextBtn.disabled = true;
                    
                    screen.textContent = "";

                    // 全画面解除
                    experimentArea.classList.remove('pseudo-fullscreen');
                    if (document.exitFullscreen) document.exitFullscreen().catch(e => {{}});

                    updateStatus();
                }}
            }}

            function downloadCSV() {{
                if (recordedData.length === 0) {{
                    alert("No data collected yet!");
                    return;
                }}
                const headers = [
                    "Trial", "Key", 
                    "TimeFromStart(ms)", "DownTime(ms)", "UpTime(ms)", 
                    "HoldTime(ms)", "DownDown(ms)", "UpDown(ms)",
                    "Scale", "Kb_X", "Kb_Y", 
                    "Pressure", "FingerArea"
                ];
                const csvRows = [headers.join(",")];
                recordedData.forEach(d => {{
                    let safeKey = d.key.replace(/"/g, '""');
                    const row = [
                        d.trial, `"${{safeKey}}"`, d.timeFromStart,
                        d.downTime, d.upTime, d.holdTime,
                        d.downDown, d.upDown, d.kbScale,
                        d.kbX, d.kbY, d.pressure, d.area
                    ];
                    csvRows.push(row.join(","));
                }});
                const csvString = csvRows.join("\\n");
                const blob = new Blob([csvString], {{ type: "text/csv" }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = "keyboard_data.csv";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }}
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=800, scrolling=False)

if __name__ == "__main__":
    main()
