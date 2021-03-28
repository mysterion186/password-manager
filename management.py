import base64, json, csv,psycopg2
from clipboard import copy


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


################################################### CSV part      ################################################################################

def read_file(file_name):
    Temp = []
    with open(file_name,"r") as csv_file:
        file_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in file_reader:
            Temp.append(row)
    csv_file.close()
    return Temp

def add_entry(domain,login,password):
	with open("password.csv","a") as password_file :
		password_writer = csv.writer(password_file,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		password_writer.writerow([domain,login,str(code(password,1))])
	return True

#add_entry("facebook","Edward","Elric_1")
def retrieve_csv(result,envy):
	final_result = ""
	count = 0
	password_list = []
	for line in result:
		if envy in line :
			final_result +=str(count)+". "+line[0]+" "+line[1]+" "+line[2]+ " \n"
			
			password_list.append(line[2])
			count +=1
	print(final_result)
	choice = 0
	if len(password_list)>1 :
		choice = int(input("Select the password you want to copy "))
	elif len(password_list)==0 :
		print('There is no match ')
		return False
	copy(code(password_list[choice],2))
	print("Your password has been saved in your clipboard")
	return True

################################################### CSV part       ################################################################################

################################################### DATABASE part  ################################################################################


def connect():
    con = psycopg2.connect(
            host="localhost",
            database = "password",
            user = "kowsikan")
    return con

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
    copy(code(password_list[choice],2))
    return password_list

def add(domain,login,password,table_name = 'password'):
    con = connect()
    cur = con.cursor()
    cur.execute(f"INSERT INTO {table_name} (domain_name,login,password) VALUES ('{domain}','{login}','{str(code(password,1))}') ")
    con.commit()
    con.close()
    return True

################################################### DATABASE part  ################################################################################


################################################### PRINT  part    ################################################################################
def affiche_menu():
	print("="*20+" Your options are : "+"="*20)
	print("1. Get a password ")
	print("2. Add a new entry ")
	print("q. To leave the Password Manager")
	print("="*60)
	return True





def menu():
	is_On = True
	
	print("="*20+"Welcome to Password Manager "+"="*20)
	while is_On:
		result = read_file("password.csv")
		affiche_menu()
		choice = (input("What do you want to do ? "))
		if choice == '1':
			desire = input("Type the login or the domain name of what you want the password ")
			retrieve_csv(result,desire)
		elif choice == '2' :
			domain = input("Please  type the website domain ")
			login = input("Please type your login ")
			password = input("Please type your password ")
			add_entry(domain,login,password)
		elif choice == 'q' :
			is_On=False
			print("Thanks for using Password Manager :)")
		else :
			print("I don't see what you want to do, please choose a number according to your need")
	return True
################################################### PRINT  part    ################################################################################

menu()