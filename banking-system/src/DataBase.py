import random
import string

auto=1
# record each account and its balance
# 银行账户和余额的对应关系的字典
# account_balance={'11111':'10000','22222':'10000','33333':'10000','44444':'10000','2023123456':'500'}
# below is a test version for presentation
account_balance={'2023123456':'500','22222':'500','11111':'500'}

# record each account and its password
# 银行账户和密码的对应字典
# account_password={'11111':'11111','22222':'22222','33333':'33333','44444':'44444','2023123456':'123456'}
# below is a test version for presentation
account_password={'2023123456':'111111','22222':'22222','11111':'11111'}

# 键为当前账户，值为各种属性，用于打印各种交易记录
detail={}

# 记录当前ATM读取的银行卡
ATM_current_account=0

# app_instances 是一个保存所有通过后端发送字符串而开启的应用实例的字典，每启动一个app就进行添加，
# 该字典的键为"app{DataBase.app_count}"字符串，
# 值为用applog(new_x, DataBase.initial_y)创建出的 app_instance 对象
app_instances = {}  

# manual_instances 是一个保存所有通过手动开启的应用实例的列表，每登录一个app就进行添加，
# 该列表存储了所有处于appmain界面的实例
manual_instances=[]

app_count = 0  # 跟踪应用的数量
initial_x = 100  # 初始X坐标
initial_y = 700  # 初始Y坐标
increment_x = 600  # 每个新应用的X坐标增量

def generate_random_number():
    while True:
        random_number = ''.join(random.choices(string.digits, k=5))
        if random_number not in account_balance and random_number not in account_password:
            return random_number