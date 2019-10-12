import MySQLdb
import redis

# global null
# null = ''

host_uat = '10.12.64.205'
port_uat = '6889'
password_uat = 'v3X7yNFK'

connection_uat = MySQLdb.connect(
    host='10.12.64.202',
    user='root',
    passwd='RounDz1x2c3v4b5',
    port=3306,
    db='rts_member',
    charset="utf8"
    )

r_uat = redis.Redis(host=host_uat, port=port_uat, password=password_uat, db=1, decode_responses=True)

member_id = input('请输入顾客id：')

# 使用cursor()方法获取操作游标
c = connection_uat.cursor()

sql = 'select * from tb_member_customer where id=' + member_id
sql1 = 'delete from tb_member_customer_ascription where Member_Customer_Id=' + member_id
sql2 = 'delete from tb_member_customer_extend_info where Member_Customer_Id=' + member_id
sql3 = 'delete from tb_member_customer where ID=' + member_id

rows_aff = c.execute(sql)
open_id = c.fetchall()[0][4]

login_key = r_uat.keys('rts:LoginToken.'+ open_id)
login_get_key = r_uat.get('rts:LoginToken.'+ open_id)

# eval()可以去去掉字符串的引号
login_get_key1 = r_uat.keys('rts:LoginToken.' + eval(login_get_key))

login_key1 = r_uat.keys(login_key[0])


try:
    # 执行sql语句
    delete_cus_ascr = c.execute(sql1)
    delete_cus_extend = c.execute(sql2)
    delete_cus = c.execute(sql3)

    # 修改数据后需要提交才能同步到数据库中
    connection_uat.commit()

    r_uat.delete(login_get_key1[0])

    r_uat.delete(login_key1[0])

except:
    # 如果失败会回滚到上一个版本
    print('执行失败')
    # connection.rollback()