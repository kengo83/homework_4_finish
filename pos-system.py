import pandas as pd
import sys
import datetime

CSV_FILE_PATH = "./super.csv"
RECEIPT_FOLDER="./receipt"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_price_list = []
        self.item_order_list = []
        self.item_number_list = []
        self.item_master=item_master
        self.datetime()

    def datetime(self):
        self.datetime_now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    def add_item_order(self,item_code,number):
        self.item_order_list.append(item_code)
        self.item_number_list.append(number)
        
    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))

    def get_name_and_price(self, item_code): #課題1
        for master in self.item_master:
            if master.item_code == item_code:
                return master.item_name,master.price

    def Get_name_and_price(self, item_code): #課題1
        for master in self.item_master:
            if master.item_code == item_code:
                print(master.item_name, master.price)

    def add_order_by_terminal(self):
        while True:
            x = input('購入したい商品コードを入力して下さい、終了したければ0を入力して下さい:')
            if int(x) != 0: 
                a = self.get_name_and_price(x)
                if a != None:
                    y = input('購入したい商品の数を入力して下さい:')
                    self.add_item_order(x, y)
                    print('オーダー登録できました')
                else:
                    print('このコードは登録されていません')
            elif int(x) == 0:
                print('オーダー登録を終了します')
                break

    def show_name_and_price(self):
        for item_code in self.item_order_list:
            self.Get_name_and_price(item_code)

    def get_price(self, item_code): 
        for master in self.item_master:
            if master.item_code == item_code:
                self.item_price_list.append(master.price)

    def calculate_money(self):
        while True:
            price_list = [int(number)*int(price) for number,price in zip(self.item_number_list, self.item_price_list)] 
            b = sum(price_list)
            x = int(input('お預かり金額を入力して下さい:'))
            if x < b:
                print('金額が少ないです。')
            elif x >=b:
                change = x - b
                print('おつりは{}円です。'.format(change))
                break

    def view_order(self):
        self.log_file_name = 'receipt_{}.log'.format(self.datetime_now)
        number = 1
        self.create_log("-----------------------------")
        self.create_log("オーダー登録された商品一覧\n")
        for item_order,item_number in zip(self.item_order_list,self.item_number_list):
            result = self.get_name_and_price(item_order)
            receipt_data = '{0}.{1}({2}):￥{3} {4}個=￥{5}'.format(number,result[0],item_order,result[1],item_number,int(result[1])*int(item_number))
            self.create_log(receipt_data)
            number += 1

        for item_code in self.item_order_list: #self.item_price_listの作成
            self.get_price(item_code)
        price_list = [int(number)*int(price) for number,price in zip(self.item_number_list, self.item_price_list)] #self.item_price_listとself.item_number_listの要素を掛け、合計金額を求める
        b = sum(price_list)
        number_list = [int(i) for i in self.item_number_list]
        c = sum(number_list)
        sum_data = '合計金額は{}円です。個数は{}個です。'.format(b,c)
        self.create_log(sum_data)

    def create_log(self,text):
        print(text)
        with open(RECEIPT_FOLDER+'\\'+self.log_file_name,mode='a',encoding='utf-8_sig') as f:
            f.write(text+'\n')


def add_item_master_by_csv(csv_name_or_path): #課題3
    item_master = []
    data = []
    try:
        with open(csv_name_or_path,encoding="utf-8_sig") as f:
            for line in map(str.strip, f):
                data.append(line.split(','))
        for i in data:
            item_master.append(Item(i[0],i[1],i[2]))
        print('マスタ登録が完了しました')
        return item_master
    except:
        print('マスタ登録が失敗しました')

### メイン処理
def main():
    #マスタ登録
    item_master = add_item_master_by_csv(CSV_FILE_PATH)
    #オーダー登録
    order=Order(item_master)
    order.add_order_by_terminal()
    
    # オーダー表示
    #order.view_item_list()
    order.view_order()
    order.calculate_money()
    #order.get_name_and_price("002")
    
    
if __name__ == "__main__":
    main()