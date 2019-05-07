#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os  
import os.path 
import paramiko
import datetime
import re
 
# 检查文件夹是否存在，不存在则创建
def check_folder(path,ssh1):
	stdin, stdout, stderr = ssh1.exec_command('find ' + path)
	result = stdout.read().decode('utf-8')
	if len(result) == 0 :
		#print('目录 %s 不存在，创建目录' % path)
		ssh1.exec_command('mkdir ' + path)
		#print('%s 创建成功' % path)
		return 1
	else:
		#print('目录 %s 已存在' % path)
		return 0
 
# 检查文件是否存在，不存在直接上传，存在检查大小是否一样，不一样则上传
def check_file(local_path, ssh_path, ssh1, sftp1):
	# 检查文件是否存在，不存在直接上传
	stdin, stdout, stderr = ssh1.exec_command('find ' + ssh_path)
	result = stdout.read().decode('utf-8')
	if len(result) == 0 :
		sftp1.put(local_path,ssh_path)
		#print('%s 上传成功' % (ssh_path))
		return 1
	else:
		# 存在则比较文件大小
		# 本地文件大小
		lf_size = os.path.getsize(local_path)
		# 目标文件大小
		stdin, stdout, stderr = ssh1.exec_command('du -b ' + ssh_path)
		result = stdout.read().decode('utf-8')
		tf_size = int(result.split('\t')[0])
		#print('本地文件大小为：%s，远程文件大小为：%s' % (lf_size, tf_size))
		if lf_size == tf_size:
			#print('%s 大小与本地文件相同，不更新' % (ssh_path))
			return 0
		else:
			sftp1.put(local_path,ssh_path)
			#print('%s 更新成功' % (ssh_path))
			return 1
 
# 上传流程开始
def upload_file(file_path,file_name,target_path='//home//robot//uploadtest//',hostname='10.8.4.170',port=22,username='robot',password='roborocks'):
    # 配置属性
    config = {
    	#本地项目路径 待上传文件所在的文件夹
    	'local_path' : file_path,
    	# 服务器项目路径 文件将要上传到的位置
    	'ssh_path' : target_path,
    	# 文件夹名 不存在则在服务器项目路径上创建
    	'project_name' : 'uploadtest',
    	# 忽视列表
    	'ignore_list' : [],
    	# ssh地址、端口、用户名、密码
    	'hostname' : hostname,
    	'port' : port,
    	'username' : username,
    	'password' : password,
    	# 是否强制更新
    	'mandatory_update' : False,
    	# 更新完成后是否重启tomcat
    	'restart_tomcat' : False,
    	# tomcat bin地址
    	'tomcat_path' : '',
    	# 被忽略的文件类型
    	'ignore_file_type_list' : []
    }
    
    print('上传开始')
    begin = datetime.datetime.now()
     
    # 文件夹列表
    folder_list = []
    # 文件列表
    file_list = [file_name]
    # ssh上文件列表
    ssh_file_list = []
     
    for parent,dirnames,filenames in os.walk(config['local_path']+config['project_name']):  
        #初始化文件夹列表
        for dirname in dirnames:
        	p = os.path.join(parent,dirname)
        	folder_list.append(p[p.find(config['project_name']):])
        #初始化文件列表
        for filename in filenames:
        	if config['ignore_list'].count(filename) == 0:
        		p = os.path.join(parent,filename)
        		file_list.append(p[p.find(config['project_name']):])
     
    print('共有文件夹%s个，文件%s个' % (len(folder_list),len(file_list)))
     
    # ssh控制台
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=config['hostname'], port=config['port'], username=config['username'], password=config['password'])
    # ssh传输
    transport = paramiko.Transport((config['hostname'],config['port']))
    transport.connect(username=config['username'],password=config['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)
     
    # 检查根目录是否存在
    root_path = config['ssh_path'] + config['project_name']
    stdin, stdout, stderr = ssh.exec_command('find ' + root_path)
    result = stdout.read().decode('utf-8')
    if len(result) == 0 :
    	#print('目录 %s 不存在，创建目录' % root_path)
    	ssh.exec_command('mkdir ' + root_path)
    	print('%s 创建成功' % root_path)
    else:
    	print('目录 %s 已存在，获取所有文件' % root_path)
    	ssh_file_list = re.split('\n',result)
     
    # 检查文件夹
    create_folder_num = 0
    for item in folder_list:
    	target_folder_path = config['ssh_path'] + item
    	create_folder_num = create_folder_num + check_folder(target_folder_path,ssh1=ssh)
     
    # 检查文件
    update_file_num = 0
    for item in file_list:
    	if config['ignore_file_type_list'].count(os.path.splitext(item)[1]) == 0:
    		local_file_path = config['local_path'] + item
    		target_file_path = config['ssh_path'] + item
    		if config['mandatory_update']:
    			sftp.put(local_file_path,target_file_path)
    			print('%s 强制更新成功' % (target_file_path))
    			update_file_num = update_file_num + 1
    		else:
    			update_file_num = update_file_num + check_file(local_file_path, target_file_path,ssh1=ssh,sftp1 = sftp)
    	else:
    		print('%s 在被忽略文件类型中，所以被忽略' % item)
     
    # 检查ssh是否有需要删除的文件
    delete_file_num = 0
    for item in ssh_file_list:
    	temp = item[item.find(config['project_name']):]
    	if folder_list.count(temp) == 0 and file_list.count(temp) == 0 and temp != config['project_name'] and temp != '':
    		#print('%s 在本地不存在，删除' % item)
    		ssh.exec_command('rm -rf ' + item)
    		delete_file_num = delete_file_num + 1
     
    end = datetime.datetime.now()
    print('本次上传结束：创建文件夹%s个，更新文件%s个，删除文件%s个，耗时：%s' % (create_folder_num, update_file_num, delete_file_num, end-begin))
     
    if config['restart_tomcat']:
    	#print('关闭tomcat')
    	ssh.exec_command('sh ' + config['tomcat_path'] + 'shutdown.sh')
    	#print('启动tomcat')
    	ssh.exec_command('sh ' + config['tomcat_path'] + 'startup.sh')
     
    # 关闭连接
    sftp.close()
    ssh.close()
    
#主函数
upload_file('C:\\Users\\DELL\\Desktop\\',file_name='average_2015APEC_second_half1.jpg')