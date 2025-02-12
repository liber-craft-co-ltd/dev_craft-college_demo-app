import os

# 苗字リスト
names = [
    "山田", "佐藤", "鈴木", "田中", "高橋", "伊藤", "渡辺", "中村", "小林", "加藤",
    "吉田", "山本", "松本", "井上", "斉藤", "林", "清水", "山口", "田村", "藤田",
    "岡田", "松田", "石田", "原田", "中島", "石井", "近藤", "上田", "森", "野村",
    "大塚", "土屋", "桜井", "大久保", "川上", "坂本", "宮崎", "内田", "水野", "新井",
    "高田", "菅原", "西村", "大西", "福田", "村田", "木下", "星野", "中田", "岡本",
    "藤井", "中川", "武田", "安藤", "平野", "川口", "宮本", "島田", "堀", "野田",
    "本田", "片山", "杉山", "川崎", "森田", "竹内", "松井", "橋本", "和田", "今村",
    "吉川", "原", "服部", "村上", "大石", "横山", "堀内", "長谷川", "植田", "青木",
    "高木", "山下", "平田", "野口", "坂井", "宮田", "長尾", "石川", "中沢", "谷口",
    "金子", "伊東", "片岡", "神田", "宮川", "望月", "木村", "大野", "矢野", "小野"
]

def renane_csv_files(d):
    files = [f for f in os.listdir(d) if f.startswith('user_') and f.endswith('.csv')]
    
    for file in files:
        # 数字部分の抽出
        n = file.replace('user_', '').replace('.csv', '')
        
        if n.isdigit():
            index = int(n) - 1
            
            if 0 <= index < len(names):
                new_name = f'{n}.{names[index]}.csv'
                old_path = os.path.join(d, file)
                new_path = os.path.join(d, new_name)
                
                # ファイル名変更
                os.rename(old_path, new_path)


renane_csv_files('data/user_data/')

