#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/23'

import pymysql


class InvitationCode:
    def __init__(self, db):
        self.db = db
        self.table = "invitation_code"

    def find(self, code, size=1, **kwargs):
        """
        查找用户，用于登录等操作
        :param email:
        :param username:
        :param password:
        :param kwargs:
        :return:
        """
        sql = f"SELECT * FROM `{self.table}` WHERE code='{code}'"
        for k, v in kwargs.items():
            if sql[-1] == " ":
                sql += f"AND "
            sql += f" {k}='{v}' "
        sql += f" limit {size};"

        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql.replace("  ", " "))
            data = cursor.fetchone()
        except Exception as e:
            tt, data = 0, None
            print('Error: unable to fecth data, error message: {}'.format(e))
        finally:
            cursor.close()
            return data

    def expired_code(self, code):
        sql = f"UPDATE `{self.table}` SET status=2 WHERE code='{code}';"
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql.replace("  ", " "))
        except Exception as e:
            tt, data = 0, None
            print('Error: unable to fecth data, error message: {}'.format(e))
        finally:
            cursor.close()
            return True

    def insert_code(self, code):
        pass










