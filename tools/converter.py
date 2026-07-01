import csv
import glob
import os

def convert_all_dictionaries():
    # 1. カレントディレクトリ内から「読み辞書*.csv」に一致するファイルをすべて取得
    input_files = glob.glob('読み辞書*.csv')
    
    if not input_files:
        print("実行時のディレクトリ内に「読み辞書*.csv」に一致するファイルが見つかりませんでした。")
        return

    for input_file in input_files:
        # 2. 出力ファイル名の作成（拡張子 .csv を .dic に変更）
        # os.path.splitext('読み辞書XXX.csv') は ('読み辞書XXX', '.csv') を返すので、[0] で名前部分を取得
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + '.dic'
        
        print(f"変換中: {input_file} -> {output_file}")
        
        # 3. SJISのCSVを読み込む（文字化け対策として 'cp932' を使用）
        with open(input_file, 'r', encoding='utf-16', newline='') as f_in:
            reader = csv.reader(f_in)
            # 不正な行や空行を除外するため、しっかり2列以上ある行だけをリストに格納
            data = [row for row in reader if len(row) >= 2]

        # 4. key（1列目: row[0]）の長さが長い順（降順）にソート
        data.sort(key=lambda x: len(x[0]), reverse=True)

        # 5. UTF-8のTSV（タブ区切り）として .dic ファイルに出力
        with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
            # delimiter='\t' でタブ区切り（TSV）を指定
            writer = csv.writer(f_out, delimiter='\t')
            
            # ソートされたデータを、末尾に '1' と '0' を追加して書き込み
            for row in data:
                key = row[0]
                val = row[1]
                writer.writerow([key, val, '1', '0'])

if __name__ == "__main__":
    convert_all_dictionaries()
    print("すべてのファイルの変換処理が完了しました。")