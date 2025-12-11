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
    st.caption("「送信（Next Trial）」を押すことで、データを保持したまま次の入力へ進めます。リロードするとデータは消えませんが、パラメータ設定がリセットされます。")

    # --- サイドバー設定 ---
    with st.sidebar:
        st.header("拡大機能の設定")
        # 1. 拡大機能ON/OFFトグルスイッチに変更
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
        # 2. 移動順序の設定（規則的の場合に順序指定可能にする）
        move_pattern = st.radio("移動順序モード", ["規則的 (順序指定)", "ランダム"], index=0)

        # 方向定義
        dir_labels = ["上", "右上", "右", "右下", "下", "左下", "左", "左上"]
        dir_vectors = {
            "上": (0, -1), "右上": (1, -1), "右": (1, 0), "右下": (1, 1),
            "下": (0, 1), "左下": (-1, 1), "左": (-1, 0), "左上": (-1, -1)
        }
        
        directions = []

        if move_pattern == "ランダム":
            random_seed = st.number_input("乱数シード (Seed)", value=42, step=1, help="同じ値を入力すると同じランダム順序が再現されます")
            # ランダム生成
            base_dirs = list(dir_vectors.values())
            random.seed(random_seed)
            random.shuffle(base_dirs)
            directions = base_dirs
        else:
            # 規則的 (順序指定)
            st.caption("以下で移動する順番を設定してください (デフォルト: 時計回り)")
            with st.expander("移動順序の編集", expanded=True):
                # デフォルトの時計回りの順序
                default_order = ["上", "右上", "右", "右下", "下", "左下", "左", "左上"]
                
                # 8ステップ分の入力欄を作成
                for i in range(8):
                    selected_label = st.selectbox(
                        f"{i+1}番目の移動先", 
                        dir_labels, 
                        index=dir_labels.index(default_order[i]),
                        key=f"dir_step_{i}"
                    )
                    directions.append(dir_vectors[selected_label])

    # --- CSS Keyframes の生成 ---
    total_move_duration = one_move_duration * 8
    
    keyframes_css = "@keyframes floatKeyframes {"
    step_percent = 100 / 8 
    
    for i, (dx, dy) in enumerate(directions):
        start_p = i * step_percent
        mid_p   = start_p + (step_percent / 2)
        end_p   = (i + 1) * step_percent
        
        tx = dx * move_range
        ty = dy * move_range
        
        if i == 0:
            keyframes_css += f"0% {{ transform: translate(0px, 0px); }}"
        keyframes_css += f"{mid_p:.2f}% {{ transform: translate({tx}px, {ty}px); }}"
        keyframes_css += f"{end_p:.2f}% {{ transform: translate(0px, 0px); }}"

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
            {"label": "Tab", "sub": "", "val": "\t", "w": 1.5, "align": "left"},
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
            {"label": "Caps", "sub": "", "val": "", "w": 1.8, "align": "left"},
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
            {"label": "Enter", "sub": "", "val": "\n", "w": 2.2, "align": "right"},
        ],
        # Row 4
        [
            {"label": "Shift", "sub": "", "val": "", "w": 2.3, "align": "left"},
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
            {"label": "Shift", "sub": "", "val": "", "w": 2.7, "align": "right"},
        ],
        # Row 5
        [
            {"label": "Ctrl", "sub": "", "val": "", "w": 1.5},
            {"label": "Fn", "sub": "", "val": "", "w": 1},
            {"label": "Win", "sub": "", "val": "", "w": 1},
            {"label": "Alt", "sub": "", "val": "", "w": 1},
            {"label": "", "sub": "", "val": " ", "w": 6},
            {"label": "Alt", "sub": "", "val": "", "w": 1},
            {"label": "Win", "sub": "", "val": "", "w": 1},
            {"label": "Ctrl", "sub": "", "val": "", "w": 1},
            {"label": "←", "sub": "", "val": "", "w": 1},
            {"label": "↑↓", "sub": "", "val": "", "w": 1, "is_arrow": True},
            {"label": "→", "sub": "", "val": "", "w": 1},
        ]
    ]

    rows_json = json.dumps(rows)
    
    # CSS変数の準備
    anim_scale_play_state = "running" if scale_enabled else "paused"
    anim_move_play_state = "running" if move_enabled else "paused"

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
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            overflow: hidden;
            user-select: none;
        }}

        /* 1. 入力欄 */
        #screen {{
            width: 95%;
            height: 50px;
            background-color: #333;
            color: #0f0;
            font-size: 20px;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            border: 2px solid #555;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            font-family: monospace;
            resize: none;
            box-sizing: border-box;
            z-index: 200;
            position: relative;
        }}

        /* 2. コントロールエリア */
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
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-family: 'Noto Sans JP', sans-serif;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: 0.2s;
        }}
        button:active {{ transform: translateY(2px); box-shadow: 0 2px 2px rgba(0,0,0,0.2); }}

        #next-btn {{ background-color: #2196F3; color: white; font-weight: bold; }}
        #next-btn:hover {{ background-color: #1e88e5; }}

        #download-btn {{ background-color: #4CAF50; color: white; }}
        #download-btn:hover {{ background-color: #45a049; }}

        #reset-btn {{ background-color: #f44336; color: white; }}
        #reset-btn:hover {{ background-color: #d32f2f; }}

        #data-count {{ 
            color: #333; 
            font-size: 14px; 
            font-weight: bold; 
            background: #fff;
            padding: 5px 10px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }}

        /* --- アニメーション定義 --- */
        @keyframes breathe {{
            0% {{ transform: scaleX({scale_min}) scaleY({scale_min}); }}
            50% {{ transform: scaleX({scale_max}) scaleY({scale_max}); }}
            100% {{ transform: scaleX({scale_min}) scaleY({scale_min}); }}
        }}

        {keyframes_css}

        /* 3. キーボードエリア */
        .movement-wrapper {{
            animation: floatKeyframes {total_move_duration}s infinite linear;
            animation-play-state: {anim_move_play_state};
            width: 95%;
            display: flex;
            justify-content: center;
            padding: {move_range + 10}px; 
            box-sizing: border-box;
        }}

        .keyboard-wrapper {{
            animation: breathe {breath_speed}s infinite ease-in-out;
            animation-play-state: {anim_scale_play_state};
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

        .arrow-stack {{
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100%; font-size: 10px; line-height: 10px;
        }}

    </style>
    </head>
    <body>
        <textarea id="screen" placeholder="ここに入力してください"></textarea>
        
        <div class="controls">
            <button id="next-btn" onclick="nextTrial()">送信 (Next Trial)</button>
            <button id="download-btn" onclick="downloadCSV()">CSVをダウンロード</button>
            <button id="reset-btn" onclick="resetData()">リセット</button>
            <span id="data-count">Trial: 1 | Rec: 0</span>
        </div>

        <div class="movement-wrapper" id="move-wrap">
            <div class="keyboard-wrapper" id="kb-wrap"></div>
        </div>

        <script>
            const rows = {rows_json};
            const kbContainer = document.getElementById('kb-wrap');
            const screen = document.getElementById('screen');
            const dataCountLabel = document.getElementById('data-count');

            // --- セッションストレージからデータを復元 ---
            let recordedData = JSON.parse(sessionStorage.getItem('kb_data') || '[]');
            let currentTrial = parseInt(sessionStorage.getItem('kb_trial') || '1');
            let lastDownTime = null;
            let lastUpTime = null;

            updateStatus();

            // --- キーボード生成 ---
            rows.forEach(row => {{
                const rowDiv = document.createElement('div');
                rowDiv.className = 'kb-row';

                row.forEach(k => {{
                    const keyDiv = document.createElement('div');
                    keyDiv.className = 'key';
                    keyDiv.style.flexGrow = k.w;
                    
                    if(k.color) keyDiv.classList.add('color-' + k.color);

                    let contentHtml = '';
                    if(k.is_arrow) {{
                        contentHtml = `<div class="arrow-stack"><span>▲</span><span>▼</span></div>`;
                    }} else {{
                        contentHtml = `<span class="label-top">${{k.label || ''}}</span><span class="label-sub">${{k.sub || ''}}</span>`;
                    }}
                    keyDiv.innerHTML = contentHtml;

                    keyDiv.onpointerdown = (e) => {{
                        e.preventDefault();
                        keyDiv.classList.add('active');
                        keyDiv.setPointerCapture(e.pointerId);

                        const now = Date.now();
                        const rect = kbContainer.getBoundingClientRect();
                        const style = window.getComputedStyle(kbContainer);
                        const matrix = new DOMMatrix(style.transform);
                        const currentScale = matrix.a;

                        let downDownTime = lastDownTime ? (now - lastDownTime) : '';
                        let upDownTime = lastUpTime ? (now - lastUpTime) : '';

                        keyDiv._currentData = {{
                            trial: currentTrial,
                            key: k.val || k.label || 'Unknown',
                            downTime: now,
                            downDown: downDownTime,
                            upDown: upDownTime,
                            kbScale: currentScale.toFixed(3),
                            kbX: rect.x.toFixed(1),
                            kbY: rect.y.toFixed(1),
                            pressure: e.pressure || 0,
                            area: (e.width * e.height).toFixed(2)
                        }};

                        lastDownTime = now;
                        
                        if (k.val === 'BS') {{
                            screen.value = screen.value.slice(0, -1);
                        }} else if (k.val) {{
                            screen.value += k.val;
                        }}
                        screen.scrollTop = screen.scrollHeight;
                    }};

                    keyDiv.onpointerup = (e) => {{
                        e.preventDefault();
                        keyDiv.classList.remove('active');
                        keyDiv.releasePointerCapture(e.pointerId);
                        
                        if (keyDiv._currentData) {{
                            const now = Date.now();
                            const holdTime = now - keyDiv._currentData.downTime;
                            
                            const record = {{
                                ...keyDiv._currentData,
                                upTime: now,
                                holdTime: holdTime
                            }};
                            
                            recordedData.push(record);
                            sessionStorage.setItem('kb_data', JSON.stringify(recordedData));
                            
                            lastUpTime = now;
                            updateStatus();
                            keyDiv._currentData = null;
                        }}
                    }};
                    
                    rowDiv.appendChild(keyDiv);
                }});

                kbContainer.appendChild(rowDiv);
            }});

            function updateStatus() {{
                dataCountLabel.innerText = `Trial: ${{currentTrial}} | Rec: ${{recordedData.length}}`;
            }}

            function nextTrial() {{
                currentTrial++;
                sessionStorage.setItem('kb_trial', currentTrial);
                screen.value = "";
                updateStatus();
            }}

            function resetData() {{
                if(confirm("データを全消去しますか？")) {{
                    recordedData = [];
                    currentTrial = 1;
                    sessionStorage.clear();
                    screen.value = "";
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
                    "DownTime(ms)", "UpTime(ms)", 
                    "HoldTime(ms)", "DownDown(ms)", "UpDown(ms)",
                    "Scale", "Kb_X", "Kb_Y", 
                    "Pressure", "FingerArea"
                ];

                const csvRows = [headers.join(",")];
                
                recordedData.forEach(d => {{
                    const row = [
                        d.trial,
                        `"${{d.key}}"`,
                        d.downTime,
                        d.upTime,
                        d.holdTime,
                        d.downDown,
                        d.upDown,
                        d.kbScale,
                        d.kbX,
                        d.kbY,
                        d.pressure,
                        d.area
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
