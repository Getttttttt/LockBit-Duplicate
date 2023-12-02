#!/usr/bin/env python
#coding:utf8 
import crypt

# 获取shadow文件并赋给变量user_pwfile
user_pwfile = "/etc/shadow"
# 定义获取密码函数get_pw()
def get_pw(u_p):
	# 定义用户名和密码对应的字典
	user_pw = {}
	# 读取shadow文件
	f = open(u_p,'r')
	userline = f.readlines()
	f.close()
	for l in userline:
		# 筛选掉系统用户
		if len(l.split(":")[1]) > 3:
			# 将用户和密码加入字典user_pw
			user_pw[l.split(":")[0]] = l.split(":")[1]
	return user_pw

# 获取本地字典集文件并赋给dicti
dicti = "/kevin/passwd.txt"
# 定义读取本地字典集函数
def get_dic(g_d):
	f = open(g_d,'r')
	mw_dic = f.readlines()
	f.close()
	return mw_dic

# 定义主函数
def main():
	# 主函数中用户名和密码（字典）
	user_passwd = get_pw(user_pwfile)
	# 主函数中本地字典集
	mw_dic = get_dic(dicti)
	# 循环出用户键名
	for u in user_passwd:
		# 获得每个用户密码
		passwd = user_passwd[u]
		# 获得每个用户盐值
		salt = "$6$" + passwd.split("$")[2]
		for pw_mv in mw_dic:
			#rstrip()去除空行（\n）
			if passwd == crypt.crypt(pw_mv.rstrip(),salt):
				print("用户名：%s  密码：%s" %(u,pw_mv.rstrip()))
	
if __name__ == "__main__":
	main()
