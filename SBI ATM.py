import tkinter as tk
from tkinter import messagebox
import mysql.connector
from decimal import Decimal

class ATM:
    def __init__(self,root):
        self.root = root
        self.root.configure(bg='blue')
        self.root.title("ATM")
        self.root.geometry("600x400+300+200")
        self.root.resizable(False,False)
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="daksh"
            )
        self.cursor = self.db.cursor()
        self.login_page()
    
    #login page in tkinter 
    def login_page(self):
        self.log_frame = tk.Frame(self.root)
        self.log_frame.place(x=0, y=0, relwidth=1, relheight=1)
        tk.Label(self.log_frame, text="Login ").place(x=300, y=10)
        tk.Label(self.log_frame, text="Account No.").place(x=220, y=50)
        tk.Label(self.log_frame, text="PIN").place(x=230, y=90)
        self.account_entry = tk.Entry(self.log_frame)
        self.account_entry.place(x=300, y=50)
        self.m_pin_entry = tk.Entry(self.log_frame, show="*")
        self.m_pin_entry.place(x=300, y=90)

        tk.Button(self.log_frame, text="Login",cursor='hand2',command=self.login_logic).place(x=300, y=190)
        
        tk.Label(self.log_frame,text="Don't have an account?",fg='black',bg='#fff',font=('Microsoft YaHei UI Light',8)).place(x=300,y=140)
        tk.Button(self.log_frame,text='Create a Account !',border=0,fg='#57a1f8',bg='white',cursor='hand2',command=self.new_account).place(x=430,y=140)
    
    def login_logic(self):
        account_no=self.account_entry.get()
        pin=self.m_pin_entry.get()
        query='use daksh'
        self.cursor.execute(query)
        query = "select * from acc where account_no=%s and pin=%s"
        self.cursor.execute(query, (account_no,pin))
        row=self.cursor.fetchone()
        if row==None:
         messagebox.showerror('Error','Invalid Account No or Pin !!')
         
        else:
           messagebox.showinfo('Welcome','Login in Sucessful')
           self.transction_page()
        
    #registration logic in tkinter
    def new_account(self):
        self.log_frame.destroy()
        self.reg_frame = tk.Frame(self.root)
        
        self.reg_frame.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.reg_frame, text="Registration").place(x=150, y=5)
        tk.Label(self.reg_frame, text="Name").place(x=50, y=50)
        tk.Label(self.reg_frame, text="Account No.").place(x=50, y=80)
        tk.Label(self.reg_frame, text="Initial Balance").place(x=50, y=110)
        tk.Label(self.reg_frame, text="PIN").place(x=50, y=140)

        self.name_entry = tk.Entry(self.reg_frame)
        self.acc_entry = tk.Entry(self.reg_frame)
        self.balance_entry = tk.Entry(self.reg_frame)
        self.pin_entry = tk.Entry(self.reg_frame, show="*")

        self.name_entry.place(x=200, y=50)
        self.acc_entry.place(x=200, y=80)
        self.balance_entry.place(x=200, y=110)
        self.pin_entry.place(x=200, y=140)

        tk.Button(self.reg_frame, text="Register",command=self.register).place(x=200, y=170)
        
    #registration logic in mysql         
    def register(self):
        name = self.name_entry.get()
        account_no = self.acc_entry.get()
        balance = float(self.balance_entry.get())
        pin = self.pin_entry.get()

        # Insert user data into the acc table
        insert_query = "INSERT INTO acc (name, account_no, balance, pin) VALUES (%s, %s, %s, %s)"
        user_data = (name, account_no, balance, pin)

        try:
            self.cursor.execute(insert_query, user_data)
            self.db.commit()
            messagebox.showinfo('Welcome','Your account has been created sucesfully!!') 
            self.login_page()
        except mysql.connector.IntegrityError:
            messagebox.showerror('Error','Connection is not established Try again !!')
            return
    
    
    #transction window 
    def transction_page(self):
        
        self.trans_frame = tk.Frame(self.root)
        self.trans_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        
        
        tk.Label(self.trans_frame, text="Welcome to Bank Of Baroda\n ATM ",font=('Microsoft YaHei UI Light',15)).place(x=150, y=5)
        
        tk.Button(self.trans_frame, text="Deposit",cursor='hand2',command=self.deposit_page).place(x=150, y=100)
        tk.Button(self.trans_frame, text="Withdraw",cursor='hand2',command=self.withdraw_page).place(x=350, y=100)
        tk.Button(self.trans_frame, text="Account Balance",cursor='hand2',command=self.check_balance).place(x=150, y=200)
        tk.Button(self.trans_frame, text="Log Out",cursor='hand2',command=self.login_page).place(x=350, y=200)
        
    #deposite window in tkinter 
    def deposit_page(self):
        self.trans_frame.destroy()
        self.deposit_frame = tk.Frame(self.root)
        self.deposit_frame.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.deposit_frame, text="Deposit Money",font=('Microsoft YaHei UI Light',15)).place(x=150, y=10)
        tk.Label(self.deposit_frame, text="Amount").place(x=90, y=90)

        self.deposit_entry = tk.Entry(self.deposit_frame)
        self.deposit_entry.place(x=180, y=90)

        tk.Button(self.deposit_frame, text="Deposit",cursor='hand2',command=self.deposit).place(x=150, y=130)
        tk.Button(self.deposit_frame, text="Back",cursor='hand2',command=self.transction_page).place(x=250, y=250)
    
    #deposite logic in mysql
    

    def deposit(self):
       account_no = self.account_entry.get()
       amount = Decimal(self.deposit_entry.get())  # Convert the amount to a Decimal

       query = "SELECT balance FROM acc WHERE account_no = %s"
       self.cursor.execute(query, [account_no])
       current_balance = self.cursor.fetchone()

       if current_balance is not None:  # Check if the account exists
        current_balance = current_balance[0]  # Extract the balance value

        new_balance = current_balance + amount

        update_query = "UPDATE acc SET balance = %s WHERE account_no = %s"
        self.cursor.execute(update_query, [new_balance, account_no])

        # Commit the changes to the database
        self.db.commit()

        messagebox.showinfo('Success', 'Money has been added successfully!')
        self.transction_page
       else:
        messagebox.showerror('Error', 'Account not found. Please check the account number.')


    #withraw in tkinter 
    def withdraw_page(self):
        self.trans_frame.destroy()
        self.withdraw_frame = tk.Frame(self.root)
        self.withdraw_frame.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(self.withdraw_frame, text="Withdraw Money").place(x=120, y=10)
        tk.Label(self.withdraw_frame, text="Amount to Withdraw").place(x=50, y=50)

        self.withdraw_entry = tk.Entry(self.withdraw_frame)
        self.withdraw_entry.place(x=200, y=50)

        tk.Button(self.withdraw_frame, text="Withdraw", command=self.make_withdrawal).place(x=200, y=80)
        tk.Button(self.withdraw_frame, text="Back", command=self.transction_page).place(x=150, y=120)
       
       
    #logic for making withrawal request

    def make_withdrawal(self):
       account_no = self.account_entry.get()
       amount = Decimal(self.withdraw_entry.get())  # Convert the amount to a Decimal

    # Retrieve the current balance
       query = "SELECT balance FROM acc WHERE account_no = %s"
       self.cursor.execute(query, (account_no,))
       current_balance = self.cursor.fetchone()

       if current_balance is not None:  # Check if the account exists
        current_balance = current_balance[0]  # Extract the balance value

        if current_balance >= amount:
            # Update the balance with the withdrawal amount
            new_balance = current_balance - amount
            update_query = "UPDATE acc SET balance = %s WHERE account_no = %s"
            self.cursor.execute(update_query, (new_balance, account_no))
            self.db.commit()
            messagebox.showinfo('Successful', 'Money has been deducted successfully!')
            self.transction_page
        else:
            messagebox.showerror('Error', 'Insufficient balance!')
       else:
        messagebox.showerror('Error', 'Account not found. Please check the account number.')
        
        
        #logic for checking balance 
    def check_balance(self):
        account_no = (self.account_entry.get())  

    # Retrieve the current balance
        query = "SELECT balance FROM acc WHERE account_no = %s"
        self.cursor.execute(query, (account_no,))
        current_balance = self.cursor.fetchone()

        if current_balance is not None:
          current_balance = current_balance[0]  # Extract the balance value

        # Display the balance to the user
          self.trans_frame.destroy()
          self.balance_frame = tk.Frame(self.root)
          self.balance_frame.place(x=0, y=0, relwidth=1, relheight=1)
 
          tk.Label(self.balance_frame, text="Account Balance").place(x=120, y=10)
          tk.Label(self.balance_frame, text=f"Current Balance: ₹{current_balance:.2f}").place(x=50, y=50)
          tk.Button(self.balance_frame, text="Back", command=self.transction_page).place(x=150, y=100)
        else:
           messagebox.showerror('Error', 'Account not found. Please check the account number.')


if __name__ == "__main__":
    root = tk.Tk()
    atm = ATM(root)
    root.mainloop()
