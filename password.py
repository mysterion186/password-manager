import base64, json, csv,psycopg2
from clipboard import copy

# essaie gitignore
#use base64 to encode plain text
#mode 1 => encode the password
#mode 2 => decode the password
def code(text,mode):
	updated_text = ""
	if mode == 1:
		updated_text = base64.b64encode(str(text).encode())
		return str(updated_text)[2:-1]
	elif mode == 2:
		updated_text = base64.b64decode(text)
		updated_text[2:-1]
		return str(updated_text)[2:-1]



################################################### DATABASE part  ################################################################################

#initialize connection between the python program and the postgre database
def connect():
    con = psycopg2.connect(
            host="localhost",
            database = "password",
            user = "kowsikan")
    return con

#return all datatbase's row which correspond to the user envy 
def retrive(envy,table_name = 'password'):
    con = connect()
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table_name} WHERE domain_name = '{envy}' OR login = '{envy}'")
    count,choice = 0,0
    password_list = []
    result = ""
    rows = cur.fetchall()
    for row in rows :
        result += str(count)+" "+row[1]+" " +row[2]+" " +row[3]+"\n"
        password_list.append(row[3])
        count +=1
    print(result)
    con.close()
    if len(password_list) > 1 :
        choice = int(input('Select the password you want to copy '))
    elif len(password_list) == 0 :
        print('There is no match ! ')
        return False 
    copy(code(password_list[choice],2))
    return True

#add a row to the database
def add(domain,login,password,table_name = 'password'):
    con = connect()
    cur = con.cursor()
    cur.execute(f"INSERT INTO {table_name} (domain_name,login,password) VALUES ('{domain}','{login}','{str(code(password,1))}') ")
    con.commit()
    con.close()
    return True

################################################### DATABASE part  ################################################################################


################################################### PRINT  part    ################################################################################
#create the choice menu to the password manager
def affiche_menu():
	print("="*20+" Your options are : "+"="*20)
	print("1. Get a password ")
	print("2. Add a new entry ")
	print("q. To leave the Password Manager")
	print("="*60)
	return True



#create the menu for the password manager 
def menu():
	is_On = True
	print("="*20+"Welcome to Password Manager "+"="*20)
	while is_On:
		affiche_menu()
		choice = (input("What do you want to do ? "))
		if choice == '1':
			desire = input("Type the login or the domain name of what you want the password ")
			retrive(desire)
		elif choice == '2' :
			domain = input("Please  type the website domain ")
			login = input("Please type your login ")
			password = input("Please type your password ")
			add(domain,login,password)
		elif choice == 'q' :
			is_On=False
			print("Thanks for using Password Manager :)")
		else :
			print("I don't see what you want to do, please choose a number according to your need")
	return True
################################################### PRINT  part    ################################################################################

menu()