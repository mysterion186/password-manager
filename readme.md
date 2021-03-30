You'll need to install the clipboard module  
There is commented line to create the csv file with the following information(domain name,login,password) [management.py]    
Your password will be stored in a csv file with a base64 encode (basic one) [management.py]  
Your password will be stored in a postgreSQL database with a base64 encode/decode function [password.py]  
futur improvement :  
  -  create a encode/decode function using a key (main password of the user )