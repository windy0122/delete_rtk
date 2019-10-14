import MySQLdb
import redis
from delete_rtk.read_ini import ReadIni


class DeleteRtkTest(object):
    def __init__(self):
        self.test_data = ReadIni(node='Uat')

        self.host_uat = self.test_data.get_value('host_uat_redis')
        self.port_uat = self.test_data.get_value('port_uat_redis')
        self.password_uat = self.test_data.get_value('password_uat_redis')
        self.r_test = redis.Redis(host=self.host_uat, port=self.port_uat, password=self.password_uat, db=1, decode_responses=True)

        # self.r_test = DeleteRtkTest.connect_redis(self)

        self.connection_test = MySQLdb.connect(
            host=self.test_data.get_value('host_uat'),
            user=self.test_data.get_value('user_uat'),
            passwd=self.test_data.get_value('password_uat'),
            port=int(self.test_data.get_value('port_uat')),
            db=self.test_data.get_value('db_uat'),
            charset=self.test_data.get_value('charset_uat')
        )

        self.c = self.connection_test.cursor()

    def sql_handle(self, member_id):
        # c = DeleteRtkTest.connect_data(self)

        sql = 'select * from tb_member_customer where id=' + member_id
        sql1 = 'delete from tb_member_customer_ascription where Member_Customer_Id=' + member_id
        sql2 = 'delete from tb_member_customer_extend_info where Member_Customer_Id=' + member_id
        sql3 = 'delete from tb_member_customer where ID=' + member_id

        rows_aff = self.c.execute(sql)
        open_id = self.c.fetchall()[0][4]

        # return open_id
        login_key = self.r_test.keys('rts:LoginToken.' + open_id)
        print(login_key)
        login_get_key = self.r_test.get('rts:LoginToken.' + open_id)
        print(login_get_key)

        # eval()可以去去掉字符串的引号
        login_get_key1 = self.r_test.keys('rts:LoginToken.' + eval(login_get_key))
        print(login_get_key1)

        try:
            # 执行sql语句
            self.c.execute(sql1)
            self.c.execute(sql2)
            self.c.execute(sql3)

            # 修改数据后需要提交才能同步到数据库中
            self.connection_test.commit()

            self.r_test.delete(login_get_key1[0])

            self.r_test.delete(login_key[0])

        except:
            # 如果失败会回滚到上一个版本
            print('执行失败')
            # connection.rollback()


if __name__ == '__main__':
    delete_test = DeleteRtkTest()
    delete_test.sql_handle('373438592263938048')

