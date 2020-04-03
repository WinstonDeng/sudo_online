import numpy as np
import time

	# have repeat item, return True
	return row_check(map) or col_check(map) or block_check(map)

	# TODO: bug
	def __init__(self, map):
		self.map = map
		self.BACKUP_MAP = init_map.copy()
	
	def back_track(self, i, j):
		x, y = i, j
		assert x >= 0
		if self.BACKUP_MAP[x, y]:
			x = i-1 if j-1<0 else i
			y = 8 if j-1<0 else j-1
			return self.back_track(x, y)
		else:
			if self.map[x, y] < 9:
				self.map[x, y] += 1
				if not global_check(self.map):
					return self.map, x, y
				else:
					return self.back_track(x, y)
			else:
				self.map[x, y] = 0
				x = i-1 if j-1<0 else i
				y = 8 if j-1<0 else j-1
				return self.back_track(x, y)
		
	def core_(self, x ,y):
		for i in range(self.map.shape[0]):
			for j in range(self.map.shape[1]):
				if self.map[i, j] == 0:
					for number in range(1, 10):
						self.map[i, j] = number
						if not global_check(self.map):
							break
						else:
							if number == 9:
								self.map, x, y = self.back_track(i, j)
								return self.core_(x, y)
							else:
								continue

		return self.map
	
	def core(self):
		return self.core_(0, 0)

class DictRemove():
	"""
		Source: https://github.com/maxiaoguai/sudoku/blob/master/sudoku.py
	"""
	def __init__(self, map):
		self.map = map
	def nine(self): 
		nine_data=np.zeros((3,3,3,3))
		for i in range(3):
			for j in range(3):
				nine_data[i,j]=self.map[i*3:(i*3)+3,j*3:(j*3)+3]
		return nine_data

	def fill_value(self, nine_data): 
		dict_data={} 
		for i in range(9):
			for j in range(9):
				if self.map[i,j]==0:
					dict_data[str(i)+str(j)]=set(range(10))-set(self.map[i,:])-set(self.map[:,j])\
					-set(nine_data[i//3,j//3].flatten()) 
		dict_data=sorted(dict_data.items(),key=lambda x:len(x[1])) 
		return dict_data

	def core(self):
		start_time=time.time() 
		insert_data=[] 
		while True:
			dict_data=self.fill_value(self.nine()) 
			if len(dict_data) == 0: 
				break 
			fisrt_values=dict_data[0] 
			key=fisrt_values[0]
			value=list(fisrt_values[1])
			insert_data.append((key,value)) 
			if len(value)!=0: 
				self.map[int(key[0]),int(key[1])]=value[0]
			else: 
				insert_data.pop() 
				for i in range(len(insert_data)): 
					recall=insert_data.pop() 
					if len(recall[1])==1: 
						self.map[int(recall[0][0]),int(recall[0][1])]=0 
					else:
						self.map[int(recall[0][0]),int(recall[0][1])]=recall[1][1] 
						insert_data.append((recall[0],recall[1][1:])) 
						break 
		end_time=time.time()
		print('time consume:', end_time-start_time)
		return self.map

def get_map_from_web_sudopk(chrome_driver_path, name, pwd):
	from selenium import webdriver
	from selenium.webdriver.common.by import By
	global browser # avoid to kill browser window 
	browser = webdriver.Chrome(executable_path=chrome_driver_path)
	# step1 : login
	url_login = 'https://www.oubk.com/login'
	browser.get(url_login)
	login_name = browser.find_element(By.ID, 'login_name')
	login_name.send_keys(name)
	password = browser.find_element(By.ID, 'password')
	password.send_keys(pwd)
	btn_login = browser.find_element_by_class_name('btn.btn-primary.btn-large')
	if btn_login is None:
		btn_login = browser.find_element(By.ID, 'btn_login')
	btn_login.click()
	# step2 : skip to check map
	url = 'https://www.oubk.com/DailySudoku/18355/5'
	browser.get(url)
	time.sleep(1)
	# step3 : bingo sudu 
	map = np.zeros((9,9))
	for i in range(9):
		for j in range(9):
			val = browser.find_element(By.ID, 'k{:d}s{:d}'.format(i+1, j+1)).get_attribute("value")
			if val == "" or val is None:
				map[i, j] = 0
			else:
				map[i, j] = int(val)
	print(map)
	
	method = DictRemove(map)
	out_map = method.core()
	
	for i in range(9):
		for j in range(9):
			input_box = browser.find_element(By.ID, 'k{:d}s{:d}'.format(i+1, j+1))
			input_box.send_keys(str(int(out_map[i, j])))
	button = browser.find_element(By.ID, 'btSave')
	if button is None:
		print('not find button')
	else:
		button.click()
	print('Finish! out_map is:')
	print(out_map)


if __name__ == '__main__':
	# your chrome_driver_path
	chrome_driver_path = r'D:\Anoconda\app\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe'
	name = 'your name'
	pwd = 'your password'
	get_map_from_web_sudopk(chrome_driver_path, name, pwd)
	
	
		


	
	