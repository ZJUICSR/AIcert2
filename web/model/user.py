#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ZJUICSR'
__copyright__ = 'Copyright © 2024/07/22'

import pymysql


class User:
    def __init__(self, db):
        self.db = db
        self.table = "users"

    def find(self, size=1, **kwargs):
        """
        查找用户，用于登录等操作
        :param email:
        :param username:
        :param password:
        :param kwargs:
        :return:
        """
        sql = f"SELECT * FROM `{self.table}` WHERE"
        for k, v in kwargs.items():
            if sql[-1] == " ":
                sql += f"AND "
            sql += f" {k}='{v}' "
        sql += f" limit {size};"
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql.replace("  ", " "))
            if size == 1:
                data = cursor.fetchone()
            else:
                data = cursor.fetchall()
        except Exception as e:
            tt, data = 0, None
            print('Error: unable to fecth data, error message: {}'.format(e))
        finally:
            cursor.close()
            return data

    def insert_user(self, username, email, password, invitation_code, group="public", **kwargs):
        sql1 = f"UPDATE `invitation_code` SET status=2 WHERE code='{invitation_code}';"
        sql2 = (f"INSERT INTO `{self.table}` (`username`, `email`, `password`, `invitation_code`, `group`) "
               f"VALUES ('{username}', '{email}', '{password}', '{invitation_code}', '{group}');")

        cursors = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursors.execute(sql1.replace("  ", " "))
            cursors.execute(sql2.replace("  ", " "))
        except Exception as e:
            tt, data = 0, None
            self.db.rollback()
            print('Error: unable to fecth data, error message: {}'.format(e))
        finally:
            self.db.commit()
            cursors.close()
            return True











