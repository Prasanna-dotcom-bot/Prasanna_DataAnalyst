import streamlit as st
import mysql.connector
import datetime

# Custom CSS for background color and sidebar styling
def add_custom_styles():
    st.markdown(
        """
        <style>
        
        /* Center the title */
        .title {
            text-align: center;
            font-size: 2.5em; /* Adjust the font size as needed */
            color: #4B0082; /* Indigo color for the title */
        }
        
         /* Adjust sidebar width */
        .css-1n2mz7e3 {  /* Adjusts the sidebar container class */
            width: 50px;  /* Set the desired width in pixels */
        }
        
        /* Optional: Adjust the main content area to prevent overlap */
        .css-1v0mbdj {  /* Adjusts the main content area */
            margin-left: 220px;  /* Set to the width of your sidebar + some extra space */
        }
        
        /* Background color for the main app */
        .stApp {
            background-color: #ADD8E6; /* Light blue */
        }

        /* Sidebar background color */
        .css-1n2mz7e3 {  /* This targets the sidebar container */
            background-color: #f5f5dc; /* Cream color */
        }

        /* Universal sidebar selector to apply background for updated Streamlit versions */
        section[data-testid="stSidebar"] {
            background-color: #f5f5dc; /* Cream color */
        }

        /* Sidebar text and link color for menu items */
        div[data-testid="stSidebar"] .css-18e3th9 a {
            color: #4B0082; /* Indigo for unselected menu */
            font-weight: bold;
        }

        /* Hover effect for sidebar menu items */
        div[data-testid="stSidebar"] .css-18e3th9 a:hover {
            color: #FFA500; /* Orange on hover */
        }

        /* Selected menu item color */
        div[data-testid="stSidebar"] .css-1avcm0n .css-18e3th9 a {
            color: #DC143C; /* Crimson for selected menu */
        }

        /* Light peach background for Customer and Staff Options dropdown */
        div[data-testid="stSelectbox"] > div {
            background-color: #FFDAB9; /* Light peach color */
        }

        /* Dropdown text color */
        div[data-testid="stSelectbox"] > div select {
            color: #4B0082; /* Indigo color for dropdown text */
            font-weight: bold;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )
def add_loyalty_points():
    mydb = mysql.connector.connect(host="localhost", user="root", password="12345678", database="CMS")
    c = mydb.cursor()

    # Fetch customer IDs with total bill > 100 grouped by customer_id and date
    c.execute("""
        SELECT customer_id 
        FROM staff_add_loyalty_points 
        GROUP BY customer_id, date 
        HAVING SUM(total_bill) > 100
    """)
    loyal_customers = c.fetchall()

    if loyal_customers:
        st.subheader("Loyalty Points Update")
        
        # Iterate over each qualifying customer and add 10 loyalty points
        for (customer_id,) in loyal_customers:
            # Update the customer_details table to add 10 loyalty points
            c.execute("""
                UPDATE customer_details 
                SET loyalty_points = loyalty_points + 10 
                WHERE customer_id = %s
            """, (customer_id,))
            st.write(f"Loyalty points added for Customer ID: {customer_id}")

            mydb.commit()  # Commit the updates
            st.success("Loyalty points updated for qualifying customers.")
    else:
         st.write("No customers qualified for additional loyalty points.")

    c.close()
    mydb.close()

# Function to get unique department values
def get_unique_departments():
    mydb = mysql.connector.connect(host="localhost", user="root", password="12345678", database="CMS")
    c = mydb.cursor()
    c.execute("SELECT DISTINCT department FROM product_details")
    #row[0] refers to the first element in each tuple
    #departments = ['Sales', 'HR', 'Engineering', 'Marketing']
    #[('Sales',), ('HR',), ('Engineering',), ('Marketing',)]
    departments = [row[0] for row in c.fetchall()]#returns these rows as a list of tuples, where each tuple represents a row in the result set.
    c.close()
    mydb.close()
    return departments

# Function to get product details by department (ID, Name, Price, and Quantity)
def get_product_details_by_department(department):
    mydb = mysql.connector.connect(host="localhost", user="root", password="12345678", database="CMS")
    c = mydb.cursor()
    c.execute("SELECT product_id, product_name, price, quantity FROM product_details WHERE department = %s", (department,))
    #[(1, 'Laptop', 1000, 10), (2, 'Mouse', 25, 200),(3, 'Keyboard', 45, 150)]
    products = [{"product_id": row[0], "product_name": row[1], "price": row[2], "quantity": row[3]} for row in c.fetchall()]
    c.close()
    mydb.close()
    return products

# Function to insert order into the database
def add_order(cust_id,product_id, price, quantity):
    order_date = datetime.datetime.now()
    mydb = mysql.connector.connect(host="localhost", user="root", password="12345678", database="CMS")
    c = mydb.cursor()
    try:
        c.execute(
            "INSERT INTO orders (cust_id,product_id, price, quantity, order_date) VALUES (%s,%s, %s, %s, %s)",
            (cust_id,product_id, price, quantity, order_date)
        )
        # Update the quantity in product_details table
        c.execute(
            "UPDATE product_details SET quantity = quantity - %s WHERE product_id = %s",
            (quantity, product_id)
        )
        mydb.commit()
        st.success("Product added to cart successfully!")
        
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        c.close()
        mydb.close()

# Function to generate the final bill
def generate_bill(cust_id):
    mydb = mysql.connector.connect(host="localhost", user="root", password="12345678", database="CMS")
    c = mydb.cursor()
    c.execute("SELECT product_id, price, quantity, total_amount,order_date FROM orders where cust_id=%s",(cust_id,))
    #c.execute("SELECT product_id, price, quantity, total_amount, order_date FROM orders WHERE cust_id=%s AND order_date = CURRENT_DATE", (cust_id,))
    #returns a list of tuple
    #Each tuple contains five elements, corresponding to the columns product_id, price, quantity, total_amount, and order_date.[(),()]
    orders = c.fetchall()
    total_bill = 0

    if orders:
        st.subheader("Bill Summary")
        st.write("product_id | total_price | total_quantity | total_amount |  order_date")
        for order in orders:
            product_id, price, quantity, total_amount, order_date = order
            st.write(f"{product_id} | ${price} | {quantity} | ${total_amount}")
            total_bill += total_amount

        st.write(f"**Grand Total: ${total_bill}**")
        # Insert into staff_add_loyalty_points table
        current_date = datetime.datetime.now().date()
        c.execute("insert into staff_add_loyalty_points values(%s,%s,%s)",(cust_id, total_bill,order_date))
        mydb.commit()

    else:
        st.write("No items in cart.")
        
    
    c.close()
    mydb.close()

# Function to handle the return process
def process_return(order_id):
    mydb = mysql.connector.connect(host="localhost", user="root", password="12345678", database="CMS")
    c = mydb.cursor()
    try:
        # Fetch the order date and total amount for the specified order_id
        c.execute("SELECT order_date, total_amount,product_id,quantity FROM orders WHERE order_id = %s", (order_id,))
        order = c.fetchone()
        
        if order:
            order_date, total_amount,product_id,quantity = order
            current_date = datetime.datetime.now()
            date_difference = (current_date - order_date).days

            if date_difference > 90:
                st.error("Return not possible. Order is older than 90 days.")
            else:
                st.success(f"Return approved. Refunded amount: ${total_amount}")
                mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="CMS")
                c=mydb.cursor()
                # Add the returned quantity back to product_details
                c.execute(
                    "UPDATE product_details SET quantity = quantity + %s WHERE product_id = %s",
                    (quantity, product_id)
                )
                c.execute("Delete from orders where order_id=%s",(order_id,))
                mydb.commit()
                
        else:
            st.error("Order ID not found.")
    except Exception as e:
        st.error(f"Error processing return: {e}")
    finally:
        c.close()
        mydb.close()

# Call the function to apply custom styles
add_custom_styles()

# Sidebar Images
st.sidebar.image("C:/Users/sande/Desktop/ONLEI/Final_Portfolio_Projects/CustomerManagementSystem/cms_logo.png", width=150)
st.sidebar.image("C:/Users/sande/Desktop/ONLEI/Final_Portfolio_Projects/CustomerManagementSystem/customer_icon.png", caption="Customer Section", width=150)
st.sidebar.image("C:/Users/sande/Desktop/ONLEI/Final_Portfolio_Projects/CustomerManagementSystem/staff_icon.png", caption="Staff Section", width=150)
     

#st.title("CUSTOMER MANAGEMENT SYSTEM")
st.markdown("<h1 class='title'>CUSTOMER MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)
choice = st.sidebar.selectbox("My Menu", ("HOME","CREATE ACCOUNTS", "CUSTOMER", "STAFF"))

if choice == "HOME":
    # Set background color for the homepage
    #add_background("#ADD8E6")  # Light blue color
    st.image("C:/Users/sande/Desktop/ONLEI/Final_Portfolio_Projects/CustomerManagementSystem/mainimage.jpg",width=1000)
    st.write("This Project is developed as part of Training")
elif choice == "CREATE ACCOUNTS":
    submenu = st.sidebar.selectbox("Account Options", ("Create Customer Account", "Create Staff Account"))
    if submenu == "Create Customer Account":
         st.write(submenu)
         customer_id=st.text_input("customer_id")
         first_name = st.text_input("First Name")
         last_name = st.text_input("Last Name")
         email = st.text_input("Email")
         phone = st.text_input("Phone Number")
         address = st.text_area("Address")
         join_date = st.date_input("Join Date", datetime.date.today())
         loyalty_points = st.number_input("Loyalty Points", min_value=0, step=1, value=0)
         pwd=st.text_input("password")
         btn=st.button("Create Account")
         if btn:      
            mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="CMS")
            c=mydb.cursor()
            if first_name and last_name and email and phone and address:
                 try:
                    c.execute("insert into customer_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(customer_id,first_name,last_name,email,phone,address,join_date,loyalty_points,pwd))
                    mydb.commit()
                    st.subheader("Customer account created successfully!")
                 except Exception as e:
                    st.error(f"Error: {e}")
                 finally:  
                    c.close()
            else:
                 st.warning("Please fill out all required fields.")
    elif submenu == "Create Staff Account":
         staff_id=st.text_input("Staff_id")
         staff_pwd = st.text_input("staff_pwd")
         designation = st.text_input("Designation")
         btn=st.button("Create Account")
         if btn:      
            mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="CMS")
            c=mydb.cursor()
            if staff_id and staff_pwd and designation:
                 try:
                    c.execute("insert into staff_details values(%s,%s,%s)",(staff_id,staff_pwd,designation))
                    mydb.commit()
                    st.subheader("Staff Account created successfully!")
                 except Exception as e:
                    st.error(f"Error: {e}")
                 finally:  
                    c.close()
            else:
                 st.warning("Please fill out all required fields.")

        
elif choice == "CUSTOMER":
    #cust_id=st.number_input("Enter Customer ID")
    cust_id = st.text_input("Enter Customer ID")

    try:
       cust_id = int(cust_id) if cust_id else None
    except ValueError:
       st.error("Please enter a valid integer for Customer ID.")
    pwd=st.text_input("Enter Customer Password")
    if "islogin" not in st.session_state:
        st.session_state['islogin']=False
    btn=st.button("Login")
    if btn:
       mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="CMS")
       c=mydb.cursor()
       c.execute("select customer_id,pwd from customer_details")
       mydata=c.fetchall()
       for row in mydata:
         customer_id = row[0]  # Convert to string and trim whitespace for comparison
         password = row[1].strip()     
         if(customer_id==cust_id and password==pwd):
            st.session_state['islogin']=True
            break
       if(not st.session_state['islogin']):
          st.write("Incorrect ID or pwd")
    if(st.session_state['islogin']):
       st.write("Login Successful")
    # Submenu with customer options
       submenu = st.selectbox("Customer Options", ("Place Order", "Cancel Order", "Return/Exchange"))
       #st.write(submenu)
       if submenu == "Place Order":
           unique_departments = get_unique_departments()
        
        # Select box for departments
           if unique_departments:
               selected_department = st.selectbox("Select Department", unique_departments)
               st.write(f"You selected the department: {selected_department}")
            
               # Fetch and display product details for the selected department
               products = get_product_details_by_department(selected_department)
               if products:
                   # Format product options as "Product Name - $Price"
                   # [{"product_id": 1, "product_name": "Laptop", "price": 1000, "quantity": 10},{}]
                   product_options = [f"{product['product_name']} - ${product['price']}" for product in products]
                   selected_product_index = st.selectbox("Select Product", range(len(product_options)), format_func=lambda x: product_options[x])
                   selected_product = products[selected_product_index]

                   # Get quantity from user
                   quantity = st.number_input("Enter quantity", min_value=1, step=1)
                   btn = st.button("Add to Cart")
                   btn1=st.button("Checkout")
                              
                   if btn:
                       # Check if the quantity entered is available
                      available_quantity = selected_product['quantity']  # Now this attribute exists in the product dictionary
                      if quantity <= available_quantity:
                           # Insert order into database
                           add_order(cust_id,selected_product['product_id'], selected_product['price'], quantity)
                      else:
                           st.error("Requested quantity is not available.")
                   elif btn1:
                      generate_bill(cust_id)
                    
               else:
                  st.write("No products available in this department.")
       elif submenu == "Cancel Order":
            order_id = st.text_input("Enter Order ID")
            btn = st.button("CANCEL")

            if order_id:
               if btn:
                # Establish database connection
                   mydb = mysql.connector.connect(host="localhost", user="root", password="12345678", database="CMS")
                   c = mydb.cursor()

                   # Step 1: Fetch quantity and product_id for the given order_id
                   c.execute("SELECT product_id, quantity FROM orders WHERE order_id = %s", (order_id,))
                   #retrieves the first row of the query result, if it exists
                   #rder_details = (101, 3)
                   order_details = c.fetchone()
            
                   if order_details:
                      product_id, quantity = order_details#unpacks the order_details tuple into two variables

                      # Step 2: Delete the order
                      c.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
                      mydb.commit()

                   # Check if the order was successfully deleted
                      if c.rowcount > 0:
                    # Step 3: Update the product's quantity in the product_details table
                          c.execute(
                             "UPDATE product_details SET quantity = quantity + %s WHERE product_id = %s",
                             (quantity, product_id)
                           )
                          mydb.commit()
                     
                          st.write(f"Order ID {order_id} cancelled successfully, and stock updated.")
                   else:
                      st.write(f"Order ID {order_id} not available.")
               else:
                   st.write(f"Order ID {order_id} not found.")

            # Close the cursor and connection
                   c.close()
                   mydb.close()           
       
       elif submenu == "Return/Exchange":
            submenu = st.selectbox("Options", ("none", "Return", "Exchange"))
            if submenu == "Return":
                order_id=st.text_input("Enter Order ID")
                btn=st.button("Return")
                if btn:
                   process_return(order_id)
            elif submenu == "Exchange":
                order_id=st.text_input("Enter Order ID")
                btn=st.button("Exchange")
                st.write("order_id",order_id, "exchanged successfully")
elif choice == "STAFF":
    staff_id=st.text_input("Enter admin ID")
    staff_pwd=st.text_input("Enter admin Password")
    if "islogin" not in st.session_state:
        st.session_state['islogin']=False
    btn=st.button("Login")
    if btn:
       mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="CMS")
       c=mydb.cursor()
       c.execute("select staff_id,staff_pwd from staff_details")
       mydata=c.fetchall()
       for row in mydata:
         if(row[0]==staff_id and row[1]==staff_pwd):
            st.session_state['islogin']=True
            break
       if(not st.session_state['islogin']):
          st.write("Incorrect ID or pwd")
    if(st.session_state['islogin']):
       st.write("Login Successful")
       choice2=st.selectbox("Features",("DELETE CUSTOMER","CANCEL ORDER","Add Loyalty Points"))
       if(choice2=="DELETE CUSTOMER"):
          c_id1=st.text_input("Enter customer ID")
          btn=st.button("DELETE")
          if btn:
             mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="CMS")
             c=mydb.cursor()
             c.execute("DELETE FROM customer_details WHERE customer_id = %s", (c_id1,))
             mydb.commit()
             if c.rowcount == 0:
                    st.write(f"Customer ID {c_id1} not available.")
             else:
                    st.write(f"Customer ID {c_id1} deleted successfully.")

             #st.subheader("Customer Deleted successfully");
       elif(choice2=="CANCEL ORDER"):
          order_id=st.text_input("Enter Order ID")
          btn=st.button("DELETE")
          if btn:
             mydb=mysql.connector.connect(host="localhost",user="root",password="12345678",database="CMS")
             c=mydb.cursor()
             c.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
             mydb.commit()
             if c.rowcount == 0:
                    st.write(f"Order ID {order_id} not available.")
             else:
                    st.write(f"Order ID {order_id} cancelled successfully.")
       elif(choice2=="Add Loyalty Points"):              
            add_loyalty_points()                  
   
