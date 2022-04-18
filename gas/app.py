# coding:UTF-8
import base64, sys, os, requests, json, re, colorama
from csv import field_size_limit
from itertools import count
from colorama import Fore, Back, Style
from collections import Counter
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), './blas_rest'))
from blas_client import BlasClient
from blas_rest import log

colorama.init()

# コンフィグの読み込み
with open("../setting_history/tool_config_{}.json".format(sys.argv[1]), encoding='utf-8') as f:
    cfg = json.load(f)


def debug_print(msg):
    if cfg["debug"]:
        print(msg)

def send_image_to_ai_server(filename): # AI Serverに画像を送信し、予測結果をjson形式で受信

    if cfg["debug"]:
        AI_URL = cfg["ai_url_debug"]
    else:
        AI_URL = cfg["ai_url"]
        
    file = {'file': open(filename, 'rb') }
    response = requests.post(AI_URL, files=file)

    if response.status_code == 200:
        return response.json()

    return None

def set_ai_data(response, ai_records):
    if bool(response["screen"]):
        ai_records["screen"] = response["screen"]

    if response["gasmeter"]["before"]["GasUsage"] != "":
        ai_records["gasmeter"]["GasUsage"].append(response["gasmeter"]["before"]["GasUsage"])

    if response["gasmeter"]["before"]["SerialNumber"] != "":
        ai_records["gasmeter"]["SerialNumber"].append(response["gasmeter"]["before"]["SerialNumber"])

    if response["gasmeter"]["after"]["GasUsage"] != "":
        ai_records["gasmeter"]["GasUsage"].append(response["gasmeter"]["after"]["GasUsage"])

    if response["gasmeter"]["after"]["SerialNumber"] != "":
        ai_records["gasmeter"]["SerialNumber"].append(response["gasmeter"]["after"]["SerialNumber"])
    
    return ai_records

def get_worker_data(bc): # 作業者が入力した値を取得
    compare_fields = cfg["compare_blas_fields"]
    worker_data = {}
    # 作業者入力の値取得
    for field_name in compare_fields:
        fld_col = bc.get_fldname(field_name)
        data = item['Item'][fld_col]
        worker_data[field_name] = data

    return worker_data

def compare_worker_data(worker_records, ai_records): # 作業者が入力した値とAIが予測した値比較関数
    results = {}
    compare_fields = cfg["compare_blas_fields"]

    for compare_field in compare_fields: 
        result_field = compare_fields[compare_field]["result_field"]
        if compare_field == "【作業員入力】指針値入力":
            if worker_records[compare_field] in ai_records["gasmeter"]["GasUsage"]:
                results[result_field] = "OK"
            else:
                results[result_field] = "NG"
        elif compare_field == "【作業員入力】現地メーターQR読取り":
            if worker_records[compare_field] in ai_records["gasmeter"]["SerialNumber"]:
                results[result_field] = "OK"
            else:
                results[result_field] = "NG"
        elif compare_field == "【作業員入力】スペース蛍QRコード読取り":
            if worker_records[compare_field] in ai_records["screen"]:
                results[result_field] = "OK"
            else:
                results[result_field] = "NG"

    return results

# 画像同士を比較する
def compare_images(ai_records):
    
    compare_list = cfg["compare_images"]
    result_field = compare_list["result_field"]
    results = {}

    gasmeter_gasusage = [ gasusage.replace(".", "")[:-1] for gasusage in ai_records["gasmeter"]["GasUsage"]]
    screen_gasusage = [ gasusage[1:] for gasusage in ai_records["screen"]]

    if (set(gasmeter_gasusage) & set(screen_gasusage)):
        results[result_field] = "OK"
    else:
        results[result_field] = "NG"

    return results

if __name__ == '__main__':
    # BLASクライアントの生成
    log.init()

    if cfg["debug"]:
        BLAS_URL = cfg["blas_url_debug"]
    else:
        BLAS_URL = cfg["blas_url"]

    # BLASに接続
    log.output(BLAS_URL)
    bc = BlasClient(cfg["blas_user_name"], cfg["blas_password"], cfg["blas_project"], BLAS_URL)

    cond = cfg["conditions"]
    date_cond = cfg["date_search"]

    # データ読み込み。全部取得する。
    item_records = bc.get_items(conditions=cond, date_conditions=date_cond)
    # json形式のレコードを一括でvalueだけ取り出した状態に変換する
    bc.all_convert(item_records)

    # BLASからダウンロードした画像を保存するパス
    if not os.path.exists("download"):
        os.makedirs("download")

    # レコードの数を取得
    ITEM_RECORD_MAX = len(item_records['records'])
    for i, item in enumerate(item_records['records']):
        item_id = item['Item']['item_id']
    
        # AIが読み取った結果を画像単位で保存するデータ
        ai_records = {"gasmeter":{"GasUsage":[], "SerialNumber":[]}, "screen": {}}
        
        log.output("===================== item_id:{} 進捗 {}/{} =====================".format(item_id, i+1 , ITEM_RECORD_MAX))

        #ここですでに入力済みのレコードはスキップする処理を追加すること
        check_field = cfg["check_field"]
        if len(check_field) != 0:
            check_column = check_field["column"]
            
            fld_name = bc.get_fldname(check_column)
            skip_flg = False
            for check_word in check_field["skip_word"]:
                if item['Item'][fld_name] == check_word:
                    log.output("item_id: {}はすでにチェック済みです".format(item_id))
                    skip_flg = True
                    break
            if skip_flg is True:
                continue

        # 画像データのダウンロード
        img_exists = True
        for image_column in cfg["images"]:
            try:
                save_file,_,ext = bc.image_download(item_id, image_column, "download")
                # BLASサーバから画像ダウンロード出来なかった場合
                if save_file is None:
                    img_exists = False
                    break
                
            except:
                log.output("\033[31m{}画像のダウンロードに失敗しました\033[0m".format(image_column))
                img_exists = False
                break
            # 画像をAIサーバにアップロードする
            response = send_image_to_ai_server(save_file)
        
            if response is not None:
                # AIが返してきたデータを画像ごとにリスト化していく
                ai_records = set_ai_data(response, ai_records)           
        
        if img_exists is True:
            # 作業者のデータを取得する
            worker_data = get_worker_data(bc)

            # 作業者のデータとAIのデータを比較する
            compare_results = compare_worker_data(worker_data, ai_records)

            # 画像同士をコンペアする
            image_compare_results = compare_images(ai_records)

            # AIの結果をBLASに書き込む
            blas_record = {}
            blas_record.update(compare_results)
            blas_record.update(image_compare_results)
            
            update_fld = {}
            for key in blas_record:
                fld_name = bc.get_fldname(key)
                update_fld[fld_name] = blas_record[key]

            bc.update_item(item_id, update_fld) # BLASに書き込む
            log.output("item_id:{}を更新しました".format(item_id))


            # ここを修理
            # コンペアリストの結果について出力する
            log.output("[作業員入力と画像の比較結果]")
            for key in blas_record:
                v = blas_record[key]
                if v == "OK":
                    log.output("{}:{}".format(key, v), color="green")
                else:
                    log.output("{}:{}".format(key, v), color="red")

        else:
            log.output("画像がダウンロードできないため、スキップします", color="red")

        # ダウンロードした画像削除
        filelist = [ f for f in os.listdir("download") ]
        for f in filelist:
            os.remove(os.path.join("download", f))