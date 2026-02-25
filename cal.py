num1= float (input("enter first num:"))
num2= float (input("enter second num:"))
print("operation")
print("+")
print("-")
print("*")
print("/")
choice = input ("enter operator(+,-,*,/):") 
if choice =='+':
    print("result:", num1 + num2)
elif choice =='-':
    print("result:", num1 - num2)
elif choice =='*':
    print("result:", num1 * num2)
elif choice =='/':
    if num2 !=0:
      print("result:", num1 / num2)
    else:
       print("error! division by zero.") 

else:
        print("invalid operator")