import pymysql
import logging
from yml_config import SysConfig


class DB(SysConfig):
    def __init__(self):
        super(DB, self).__init__()
        self._config = {
            "host": self.config['db']['host'],
            "user": self.config['db']['user'],
            "password": self.config['db']['password'],
            "database": self.config['db']['database']
        }
        logging.debug("数据库配置为%s" % self._config)

    def opr_db_table(self, _sql):
        logging.info("数据操作语句为")
        logging.info(_sql)
        db = pymysql.connect(**self._config)
        cursor = db.cursor()
        sql = _sql
        result = cursor.execute(sql)
        logging.info("数据操作结果为")
        logging.info(result)
        db.commit()  # 提交数据
        cursor.close()
        db.close()

    def qry_db_table(self, _sql):
        logging.info("数据操作语句为")
        logging.info(_sql)
        db = pymysql.connect(**self._config)
        cursor = db.cursor()
        cursor.execute(_sql)
        data = cursor.fetchall()
        logging.info("数据操作结果为")
        logging.info(data)
        db.commit()  # 提交数据
        cursor.close()
        db.close()
        return data


# DB().opr_db_table("update TBL_DATE_SYS_STAT set txn_status=0")
