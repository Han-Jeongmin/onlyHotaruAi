# coding:UTF-8
import os
import sys
import base64
import cv2
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), './blas_rest'))

from blas_rest import Auth, Project, Item, ImageField, Image, Field, log
log.output(os.path.dirname(__file__))

class BlasClient():
    def __init__(self, user_name, password, project_name, url="http://localhost/blas7/api/v1/"):
        self.fld_map = {}
        self.fld_type = {}
        self.auth = Auth.BlasRestAuth(url)

        self.project = Project.BlasRestProject(url)
        
        self.item = Item.BlasRestItem(url)
        
        self.image_field = ImageField.BlasRestImageField(url)
        
        self.image = Image.BlasRestImage(url)
        
        self.field = Field.BlasRestField(url)

        
        log.output("user_name:{} project_name:{}".format(user_name, project_name))

        # コンストラクタでトークンを取得する
        result = self.auth.login(user_name, password)
        self.token = result['records']['token']
        log.output("トークンを取得しました")

        # プロジェクトIDを取得する
        result = self.project.search(self.token, project_name)
        if result == None:
            log.output("プロジェクトの取得に失敗しました")
            log.output(result)
            sys.exit(1)
        elif result['error_code'] != 0:
            log.output(result['message'])
            sys.exit(result['error_code'])

        log.output("プロジェクト名を取得しました")
        self.project_id = result['records'][0]['Project']['project_id']

    
        # データカラムの情報を取得する
        result = self.field.search(self.token, self.project_id)
        if result == None:
            log.output("フィールドの取得に失敗しました")
            sys.exit(1)

        error_code = result['error_code']
        if error_code != 0:
            log.output(result['message'])
            sys.exit(1)

        flds = result['records']
        for fld in flds:
            col = fld['Field']['col']
            name = fld['Field']['name']
            self.fld_map[name] = "fld{}".format(col)
            fldname = "fld"+col
            self.fld_type[fldname] = fld['Field']['type']

        self.image_list = self.image_field.search(self.token, self.project_id)

    '''
    プロジェクトのデータを全部取得する
    conditiosには{'カラム名1':値,'カラム名2':値}の
    ディクショナリ形式で指定する
    '''
    def get_items(self, conditions, date_conditions=None):
        date_dict = {}
        # カラム名からfld名を取得して検索条件を作成する

        # データを取得する
        if bool(conditions):
            blas_conditions = []
            for condition in conditions:
                column_name = condition
                value = conditions[column_name]

                # 案件名からfld名に変換
                fld = self.fld_map[column_name]
                blas_conditions.append([fld, value])
        if date_conditions:
            # 日付の範囲指定
            for date_condition in date_conditions:
                field_name = date_condition["field"]
                fld = self.fld_map[field_name]

                date_condition['field'] = fld
                # 2021/06/22 セキュリティ問題で直接sql文を入れるのはダメ
                # if "from" in date_condition:
                #     from_date = date_condition["from"]
                #     k = "cast({} as date) >= ".format(fld)
                #     date_dict[k] = from_date

                # if "to" in date_condition:
                #     to_date = date_condition["to"]
                #     k = "cast({} as date) < ".format(fld)
                #     date_dict[k] = to_date
        
        if bool(conditions) and date_conditions:
            result = self.item.search(self.token, self.project_id, fld_list = blas_conditions, date_dict = date_conditions)
        elif not bool(conditions) and date_conditions:
            result = self.item.search(self.token, self.project_id, fld_list = None, date_dict = date_conditions)           
        elif bool(conditions) and not date_conditions:
            result = self.item.search(self.token, self.project_id, fld_list = blas_conditions, date_dict = None)  
        else:
            result = self.item.search(self.token, self.project_id, fld_list = None, date_dict = None)

        if result == None:
            log.output("itemの取得に失敗しました")
            sys.exit(1)
        error_code = result['error_code']
        if error_code != 0:
            log.output(result['message'])
            sys.exit(1)

        log.output("itemを取得しました")
        item_records = result

        return item_records

    def save_img(self, file_name, base64_image):
        decode_file = base64.b64decode(base64_image)
        with open(file_name, "wb") as f:
            f.write(decode_file)
        
    def test(self, image_col_name):
        result = self.image_field.search(self.token, self.project_id, image_col_name)

        records = result['records']
        for record in records:
            if record['ProjectImage']['name'] == image_col_name:
                return record

        return result

    def image_download(self, item_id, image_col_name, save_dir):
       # project_image_idは検索で見つける
        image_records = self.image_list['records']
        find = False
        for record in image_records:
            if record['ProjectImage']['name'] == image_col_name:
                find = True
                project_image_id = record['ProjectImage']['project_image_id']
                break

        if not find:
            log.output("{}をダウンロードに失敗しました".format(image_col_name))
            sys.exit(1)

        log.output("{}をダウンロードします".format(image_col_name))

       # log.output(result)
       # project_image_id = result['records'][0]['ProjectImage']['project_image_id']

        
        result = self.image.download(self.token, item_id, project_image_id)

        if result == None:
            log.output("画像の取得に失敗しました")
            sys.exit(1)
        
        error_code = result['error_code']
        if error_code != 0:
            log.output(result['message'])
            return None, None, None
  
        
        base64_img = result['records'][0]['Image']['image']
        ext = result['records'][0]['Image']['ext']
        
        save_file = os.path.join(save_dir, "{}-{}-{}.{}".format(item_id, project_image_id, image_col_name, ext))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # base64を画像で保存
        self.save_img(save_file, base64_img)

        return save_file, base64_img, ext
        

    """
    {serial_fld:serial, mac_fld:mac}
    set_paramsは辞書形式
    """
    def update_item(self, item_id, set_params):
        #log.output("{} {}".format(item_id, set_params))
        #log.output(self.project_id)
        rtn = self.item.update(self.token, self.project_id, item_id, set_params)
        if rtn == None:
            log.output("データ更新に失敗しました")
            sys.exit(1)
       # log.output(rtn)
        error_code = rtn['error_code']
        if error_code != 0:
            log.output(rtn['message'])

        return rtn

    def get_fldname(self, column_name):
        return self.fld_map[column_name]

    """
    フィールド名を指定すると、そのフィールドの型を取得する
    """
    def get_fldtype(self, fld_name):
        fld_type = -1
        if fld_name in self.fld_type:
            fld_type = self.fld_type[fld_name]

        return fld_type


    """
    JSON形式の型の場合、valueだけ取り出す。
    それ以外は元データをそのまま返す。
    record:itemテーブルのrecord['Item']['records'][]を指定する
    fld_name:fld1～fld150を指定する。
    """
    def get_data(self, record, fld_name):
        data =""
        fld_type = self.get_fldtype(fld_name)

        if fld_type == "28" or fld_type == "13" or fld_type == "16":
            if record[fld_name] != None:
                try:
                    d = json.loads(record[fld_name])
                    data = d['value']
                except:
                    data = record[fld_name]
        else:
            data = record[fld_name]

        return data

    def all_convert(self, items):
        for item in items["records"]:
            record = item['Item']
            for fld_name in self.fld_type:
                data = self.get_data(record, fld_name)
                record[fld_name] = data

    def get_projects(self):
        return self.project.search(self.token, None)
    
    def get_fields(self):
        return self.field.search(self.token, self.project_id)

    def get_img_fields(self):
        return self.image_field.search(self.token, self.project_id)


