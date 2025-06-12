HIDE_ST_STYLE = """
<style>
    #MainMenu {
        visibility: hidden;
        height: 0%;
    }
    header {
        visibility: hidden;
        height: 0%;
    }
    footer {
        visibility: hidden;
        height: 0%;
    }
    .appview-container .main .block-container{
        padding-top: 1rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 1rem;
    }  
    .reportview-container {
        padding-top: 0rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 0rem;
    }
    header[data-testid="stHeader"] {
        z-index: -1;
    }
    div[data-testid="stToolbar"] {
        z-index: 100;
    }
    div[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
    }
    div[data-testid="stDecoration"] {
        visibility: hidden;
        height: 0%;
        position: fixed;
        z-index: 100;
    }
    [data-testid=stSidebar] {
        background-color: #D1EDFA;
    }
    img[data-testid="stLogo"] {
        height: 10rem;
    }
    
    /* --- ファイルアップローダーのカスタマイズ --- */
    /* ドロップゾーン全体 */
    section[data-testid="stFileUploaderDropzone"] {
        background: #f8f9fa !important;
        border: 2px dashed #d1d5db !important;
        border-radius: 8px !important;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s;
        margin-bottom: 8px;
    }
    /* ホバー時 */
    section[data-testid="stFileUploaderDropzone"]:hover {
        border-color: #ff4b4b !important;
        background: #fff0f0 !important;
    }
    /* ボタン */
    section[data-testid="stFileUploaderDropzone"] button {
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        padding: 8px 24px !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
    }
    section[data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #e63946 !important;
        transform: translateY(-1px) !important;
    }
    /* アイコンとテキスト部分 */
    div[data-testid="stFileUploaderDropzoneInstructions"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    /* テキスト */
    div[data-testid="stFileUploaderDropzoneInstructions"] span,
    div[data-testid="stFileUploaderDropzoneInstructions"] small {
        color: #6c757d !important;
        font-size: 0.8rem !important;
        display: none !important;   /* 既存の制限テキストを非表示 */
    }    
    /* カスタムテキストを追加 */
    div[data-testid="stFileUploaderDropzoneInstructions"]::before {
        content: "データをアップロードしてください";
        color: #6c757d;
        font-size: 1rem;
        font-weight: 500;
    }    
    /* カスタム制限テキストを追加 */
    div[data-testid="stFileUploaderDropzoneInstructions"]::after {
        content: "最大200MBまでのCSVファイル形式に対応";
        color: #6c757d;
        font-size: 0.8rem;
        margin-top: 4px;
        display: block;
    }
</style>
""" 
