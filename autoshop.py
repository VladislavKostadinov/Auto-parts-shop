import sys
import itertools
import datetime

from Pending_user import add_clients, init_database, get_clients, update_clients, pending
from Admins import add_admins, init_admin_database, get_admins, update_admins
from Approved_users import add_approved_users, init_approved_users_database, get_approved_users, update_approved_users
from Cars import add_cars, init_database_cars, get_cars, update_cars
from Parts import add_parts, init_database_parts, get_parts, update_parts
from Orders import add_orders, init_database_orders, get_orders, update_orders

new_clients = {'first_name': '', 'last_name': '', 'e_mail': '', 'tel': 0, 'pass': '', 'date': ''}
new_admins = {'name': '', 'pass': ''}
approved_clients = {'first_name': '', 'last_name': '', 'e_mail': '', 'tel': 0, 'pass': '', 'date': ''}
cars = {'name': '', 'model': '', 'year': 0}
parts = {'code': 0, 'name': '', 'category': '', 'price': 0, 'compatible': [], 'producer': ''}
shopping_cart = []


def user_registration():
    user_first_name = str(input('First name: \n'))

    while not user_first_name.isalpha():
        print("Can't use numerical values.")
        user_first_name = str(input('First name: \n'))

    user_last_name = input('Last name: \n')

    while not user_last_name.isalpha():
        print("Can't use numerical values.")
        user_last_name = str(input('Last name: \n'))

    user_email = input('E-mail: \n')
    while True:
        try:
            user_phone = int(input('Telephone: \n'))
            break
        except ValueError:
            print('Can not use alphabetical symbols')

    user_pass = input('Password: \n')
    user_confirm_pass = input('Retype password: \n')
    p = 0
    while user_pass != user_confirm_pass:
        print("Password don't match. Retype password:")
        user_confirm_pass = input('Retype password: \n')
        p += 1
        if p == 2:
            print('You have entered a wrong password 3 times. System reboot.')
            break
    print('Your registration is pending. Wait for approval from the administrator.')
    new_clients['first_name'] += user_first_name
    new_clients['last_name'] += user_last_name
    new_clients['e_mail'] += user_email
    new_clients['tel'] += user_phone
    new_clients['pass'] += user_pass
    new_clients['date'] += str(datetime.datetime.now())

    add_clients(new_clients)
    login_screen()


class Add_admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        new_admins['name'] += username
        new_admins['pass'] += password
        add_admins(new_admins)
        print("New admin has been added.")
        print(new_admins)


def admin_actions():
    print('''1. View/Approve pending users
2. Change user profile data
3. View on-line shop inventory
4. View registration history
5. View orders
6. Exit
    ''')
    admin_choice = int(input())
    while True:
        if admin_choice == 1:
            pending_user_list()
            break
        elif admin_choice == 2:
            change_user_data()
            break
        elif admin_choice == 3:
            main_menu_client()
            break
        elif admin_choice == 6:
            print('See you next time.')
            sys.exit()
        elif admin_choice == 5:
            orders_history()
            break
        elif admin_choice == 4:
            user_reg_history()
            break


def orders_history():
    while True:
        if len(get_orders()) == 0:
            print('Orders are empty')
            break
        print('Orders: ')
        lst = len(get_orders())
        n = 0
        s = 0
        total = 0
        s_total = 0
        while s < lst:
            print(f'{s+1}. {get_orders()[s][0][0][::2]}')
            total = sum(get_orders()[s][0][0][::-2])
            print(f'{total}$')
            s_total += total
            n += 2
            s += 1
        if s == lst:
            print(f'Total income: {s_total}$')
            admin_return = int(input('To return to the main admin menu, type "0": '))
            if admin_return == 0:
                admin_actions()
            else:
                print('Error input. System reboot.')
                sys.exit()


def user_reg_history():
    le = len(get_approved_users())
    s = 0
    if le > 0:
        while s <= len(get_approved_users()) - 1:
            print(f'''{s + 1}. {get_approved_users()[s][0]["first_name"]}
    First name: {get_approved_users()[s][0]["first_name"]}
    Last name: {get_approved_users()[s][0]["last_name"]}
    E-mail: {get_approved_users()[s][0]["e_mail"]}
    Telephone: {get_approved_users()[s][0]["tel"]}
    Reg date: {get_approved_users()[s][0]["date"]}
            ''')
            s += 1
        if s >= len(get_approved_users()) - 1:
            a_return = int(input('To return to the previous screen, type "0": '))
            if a_return == 0:
                admin_actions()


def pending_user_list():
    init_database()
    n = 0
    le = len(get_clients())
    print(f'Pending users: {le}')
    while n <= len(get_clients()) - 1:
        nu = n + 1
        print(f'{nu}. {get_clients()[n][0]["first_name"]}')
        n += 1
    s = 0
    if le > 0:
        admin_approval = input('Please select the name of the user or type "R" to return: ').lower()
        while s <= len(get_clients()) - 1:
            if admin_approval == get_clients()[s][0]['first_name'].lower():
                print(f'''{s + 1}. {get_clients()[s][0]["first_name"]}
    First name: {get_clients()[s][0]["first_name"]}
    Last name: {get_clients()[s][0]["last_name"]}
    E-mail: {get_clients()[s][0]["e_mail"]}
    Telephone: {get_clients()[s][0]["tel"]}
    Password: {get_clients()[s][0]["pass"]}
    Reg date: {get_clients()[s][0]["date"]}
''')
                admin_u_approval = input('Approve (Y/N/R):')
                print(admin_u_approval)
                if admin_u_approval == 'R':
                    pending_user_list()
                elif admin_u_approval == "N":
                    del get_clients()[s]
                    update_clients()
                else:
                    approved_clients['first_name'] += get_clients()[s][0]["first_name"]
                    approved_clients['last_name'] += get_clients()[s][0]["last_name"]
                    approved_clients['e_mail'] += get_clients()[s][0]["e_mail"]
                    approved_clients['tel'] += get_clients()[s][0]["tel"]
                    approved_clients['pass'] += get_clients()[s][0]["pass"]
                    approved_clients['date'] += get_clients()[s][0]['date']
                    add_approved_users(approved_clients)
                    del get_clients()[s]
                    update_clients()
                    print(approved_clients)
                    pending_user_list()
                break
            elif admin_approval == 'R':
                admin_actions()

        else:
            s += 1
    else:
        print('There are no pending users.')
        admin_actions()


def change_user_data():
    init_database()
    n = 0
    le = len(get_approved_users())
    print(f'Approved users: {le}')
    while n <= len(get_approved_users()) - 1:
        nu = n + 1
        print(f'{nu}. {get_approved_users()[n][0]["first_name"]}')
        n += 1
    s = 0
    if le > 0:
        admin_user_choice = input('Please select the name of the user or type "R" to return: ').lower()
        while s <= len(get_approved_users()) - 1:
            if admin_user_choice == get_approved_users()[s][0]['first_name'].lower():
                print(f'''{s + 1}. {get_approved_users()[s][0]["first_name"]}
        First name: {get_approved_users()[s][0]["first_name"]}
        Last name: {get_approved_users()[s][0]["last_name"]}
        E-mail: {get_approved_users()[s][0]["e_mail"]}
        Telephone: {get_approved_users()[s][0]["tel"]}
        Password: {get_approved_users()[s][0]["pass"]}
        ''')
                admin_u_edit = int(input('''Choose which data to update: 
    1. E-mail (1)
    2. Telephone (2)
    3. Password (3) '''))
                print(admin_u_edit)
                if admin_u_edit == 1:
                    e_mail_edit = input('Enter the new e-mail or type "R" to return: ')
                    if e_mail_edit != 'R':
                        get_approved_users()[s][0]["e_mail"] = e_mail_edit
                        update_approved_users()
                    else:
                        change_user_data()
                elif admin_u_edit == 2:
                    telephone_edit = input('Enter the new telephone or type "R" to return: ')
                    if telephone_edit != "R":
                        get_approved_users()[s][0]["tel"] = telephone_edit
                        update_approved_users()
                    else:
                        change_user_data()
                else:
                    password_edit = input('Enter the new password or type "R" to return: ')
                    if password_edit != "R":
                        get_approved_users()[s][0]["pass"] = password_edit
                        update_approved_users()
                    else:
                        change_user_data()
                break
            elif admin_user_choice == 'R':
                admin_actions()
                break
            elif le == 0:
                print('There are not pending users.')
                admin_actions()
            else:
                s += 1
    else:
        print('There are no approved users.')
        admin_actions()


def login_screen():
    print('Welcome to "AutoMobile" shop.')
    login_actions = int(input('''1. Log in as a client (1)
2. Login as an administrator (2)
3. Register (3)
4. Exit (4)
Type your choice: '''))
    while True:
        if login_actions == 4:
            print('See you next time.')
            sys.exit()
        if login_actions == 1:
            client_log_in()
        elif login_actions == 2:
            admin_log_in()
        elif login_actions == 3:
            user_registration()
        else:
            print('Error, no such menu. Try again.')
            login_screen()


def client_log_in():
    client_log_name = input('Type in your First name: ')
    clients_check_name = [client for client in get_approved_users() if client[0]['first_name'] == client_log_name]
    c = 0
    if not clients_check_name:
        print('No such user. Please wait for approval, try again or register.')
        login_screen()
    while True:
        client_log_pass = input('Type in your password: ')
        clients_check_pass = [client for client in get_admins() if client[0]['pass'] == client_log_pass]
        if clients_check_name and clients_check_pass:
            print(f'Welcome, {clients_check_name[0][0]["first_name"]}. You are free to browse our shop and \
purchase items of your liking.')
            main_menu_client()
            break
        if not clients_check_pass:
            print('Wrong password')
            c += 1
        if c == 3:
            print('You have entered 3 invalid passwords. System reboot.')
            sys.exit()


def admin_log_in():
    admin_log_name = input('Type in your username: ')
    admin_check_name = [admin for admin in get_admins() if admin[0]['name'] == admin_log_name]
    if not admin_check_name:
        print('No such admin. Try again')
        login_screen()
    a = 0
    while True:
        admin_log_pass = input('Type in your password: ')
        admin_check_pass = [admin for admin in get_admins() if admin[0]['pass'] == admin_log_pass]
        if admin_check_name and admin_check_pass:
            print(f'Welcome, {admin_check_name[0][0]["name"]}. You are free to browse the shop, \
approve or deny pending users, edit user info and search purchase data.')
            admin_actions()
            break
        if not admin_check_pass:
            print('Wrong password')
            a += 1
        if a == 3:
            print('You have entered 3 invalid passwords. System reboot.')
            sys.exit()


def main_menu_client():
    m_menu = int(input('''1. Parts suitable for certain cars (1)
2. Cars suitable for certain parts (2)
3. Shopping cart (3)
4. Exit (4) \n'''))
    if m_menu == 1:
        parts_menu()
    if m_menu == 2:
        cars_menu()
    if m_menu == 3:
        shopping_basket()
    if m_menu == 4:
        sys.exit()


def cars_menu():
    n = 1
    s = 1
    for cars_all in get_cars():
        print(f'{s}. {cars_all[0]["name"]}, {cars_all[0]["model"]}, \
{cars_all[0]["year"]}:')
        s += 1
        for a_parts in get_parts():
            for com_cars in a_parts[0]['compatible']:
                if cars_all[0]['name'] == com_cars[0]['name']:
                    print(f'--{a_parts[0]["name"]}, {a_parts[0]["price"]}$ (For purchase type {n})')
                    n += 1
    car_part_shop()


def car_part_shop():
    basket = []
    part_purchase = int(input('Select an item to add to your cart or return to the \
previous menu by typing "0": '))
    if part_purchase == 0:
        print(basket)
        main_menu_client()
    while True:

        if part_purchase == 1 or part_purchase == 3:
            basket.append(get_parts()[0][0]["name"])
            basket.append(get_parts()[0][0]["price"])
        if part_purchase == 2 or part_purchase == 6:
            basket.append(get_parts()[5][0]["name"])
            basket.append(get_parts()[5][0]["price"])
        if part_purchase == 4 or part_purchase == 8:
            basket.append(get_parts()[3][0]["name"])
            basket.append(get_parts()[3][0]["price"])
        if part_purchase == 5 or part_purchase == 7:
            basket.append(get_parts()[1][0]["name"])
            basket.append(get_parts()[1][0]["price"])
        if part_purchase == 9 or part_purchase == 11:
            basket.append(get_parts()[2][0]["name"])
            basket.append(get_parts()[2][0]["price"])
        if part_purchase == 6 or part_purchase == 10:
            basket.append(get_parts()[4][0]["name"])
            basket.append(get_parts()[4][0]["price"])
        part_purchase = int(input('Item added. Select an item to add to your cart or return to the \
previous menu by typing "0": '))
        if part_purchase == 0:
            shopping_cart.append(basket)
            print(basket)
            main_menu_client()
            break


def parts_menu():
    categories = int(input('''Categories:
1. Engine (1)
2. Brakes (2)
3. Motor oil (3)

4. Return (4)
5. Exit (5) \n'''))
    if categories == 1:
        engine_menu()
    elif categories == 2:
        brakes_menu()
    elif categories == 3:
        oil_menu()
    elif categories == 4:
        main_menu_client()
    else:
        sys.exit()


def engine_menu():
    basket = []
    n = 1
    for e_parts in get_parts():
        if e_parts[0]['category'] == "Engine":
            print(f'''{n}. {e_parts[0]['name']} (For purchase type {n})''')
            for com_cars in e_parts[0]['compatible']:
                print(f'-- Suitable part for {com_cars[0]["name"]}, {com_cars[0]["model"]}, {com_cars[0]["year"]}')
            n += 1
    engine_purchase = int(input('Select an item to add to your cart or return to the \
previous menu by typing "0": '))
    if engine_purchase == 0:
        print(basket)
        parts_menu()
    while True:
        if engine_purchase != 1 and engine_purchase != 2 and engine_purchase != 0:
            print('Error. No such command')
        if engine_purchase == 1:
            basket.append(get_parts()[0][0]["name"])
            basket.append(get_parts()[0][0]["price"])
        if engine_purchase == 2:
            basket.append(get_parts()[5][0]["name"])
            basket.append(get_parts()[5][0]["price"])
        engine_purchase = int(input('Item added. Select another item to add or go back by pressing "0": '))
        if engine_purchase == 0:
            shopping_cart.append(basket)
            print(basket)
            parts_menu()
            break


def brakes_menu():
    basket = []
    n = 1
    for b_parts in get_parts():
        if b_parts[0]['category'] == "Brakes":
            print(f'''{n}. {b_parts[0]['name']} (For purchase type {n})''')
            for com_cars in b_parts[0]['compatible']:
                print(f'-- Suitable part for {com_cars[0]["name"]}, {com_cars[0]["model"]}, {com_cars[0]["year"]}')
            n += 1
    brake_purchase = int(input('Select an item to add to your cart or return to the \
previous menu by typing "0": '))
    if brake_purchase == 0:
        print(basket)
        parts_menu()
    while True:
        if brake_purchase != 1 and brake_purchase != 2 and brake_purchase != 0:
            print('Error. No such command')
        if brake_purchase == 1:
            basket.append(get_parts()[1][0]["name"])
            basket.append(get_parts()[1][0]["price"])
        if brake_purchase == 2:
            basket.append(get_parts()[4][0]["name"])
            basket.append(get_parts()[4][0]["price"])
        brake_purchase = int(input('Item added. Select another item to add or go back by pressing "0": '))
        if brake_purchase == 0:
            shopping_cart.append(basket)
            print(basket)
            parts_menu()
            break


def oil_menu():
    basket = []
    n = 1
    for o_parts in get_parts():
        if o_parts[0]['category'] == "Motor Oil":
            print(f'''{n}. {o_parts[0]['name']} (For purchase type {n})''')
            for com_cars in o_parts[0]['compatible']:
                print(f'-- Suitable part for {com_cars[0]["name"]}, {com_cars[0]["model"]}, {com_cars[0]["year"]}')
            n += 1
    oil_purchase = int(input('Select an item to add to your cart or return to the \
previous menu by typing "0": '))
    if oil_purchase == 0:
        parts_menu()
    while True:
        if oil_purchase != 1 and oil_purchase != 2 and oil_purchase != 0:
            print('Error. No such command')
        if oil_purchase == 1:
            basket.append(get_parts()[2][0]["name"])
            basket.append(get_parts()[2][0]["price"])
        if oil_purchase == 2:
            basket.append(get_parts()[3][0]["name"])
            basket.append(get_parts()[3][0]["price"])
        oil_purchase = int(input('Item added. Select another item to add or go back by pressing "0": '))
        if oil_purchase == 0:
            shopping_cart.append(basket)
            print(basket)
            parts_menu()
            break


def shopping_basket():
    while True:
        if len(shopping_cart[0]) == 0:
            print('Your cart is empty')
            break
        print('Your shopping basket: ')
        lst = len(shopping_cart[0])
        n = 0
        s = 1
        while n < lst:
            print(f'{s}. {shopping_cart[0][n]}, {shopping_cart[0][n+1]}$')
            n += 2
            s += 1
        clean_basket = int(input("Type the row you want to remove, type '0' to clean all or '99' to purchase: "))

        if clean_basket == 1:
            del shopping_cart[0][0]
            del shopping_cart[0][0]
            print("Item 1 has been removed.")
        if clean_basket == 2:
            del shopping_cart[0][2]
            del shopping_cart[0][2]
            print("Item 2 has been removed.")
        if clean_basket == 3:
            del shopping_cart[0][4]
            del shopping_cart[0][4]
            print("Item 2 has been removed.")
        if clean_basket == 4:
            del shopping_cart[0][6]
            del shopping_cart[0][6]
            print("Item 2 has been removed.")
        if clean_basket == 5:
            del shopping_cart[0][8]
            del shopping_cart[0][8]
            print("Item 2 has been removed.")
        if clean_basket == 6:
            del shopping_cart[0][10]
            del shopping_cart[0][10]
            print("Item 2 has been removed.")
        if clean_basket == 0:
            shopping_cart.clear()
        if clean_basket == 99:
            add_orders(shopping_cart)
            print('Successful purchase. Thank you for visiting our store.')
            sys.exit()


class Cars:
    def __init__(self, _name, _model, _year: int):
        self._name = _name
        self._model = _model
        self._year = _year
        cars['name'] += self._name
        cars['model'] += self._model
        cars['year'] += self._year
        add_cars(cars)


class Auto_parts:
    def __init__(self, _code, name, category, price: int, compatible: list, producer):
        self._code = _code
        self.name = name
        self.category = category
        self.price = price
        self.compatible = compatible
        self.producer = producer
        parts['code'] = self._code
        parts['name'] = self.name
        parts['category'] = self.category
        parts['price'] = self.price
        for spec_cars in compatible:
            parts['compatible'].append(get_cars()[spec_cars])
            print(spec_cars)
        parts['producer'] = self.producer
        add_parts(parts)


if __name__ == '__main__':
    init_database()
    init_approved_users_database()
    init_admin_database()
    init_database_cars()
    init_database_parts()
    init_database_orders()
    # user_registration()
    # Add_admin('VKostadinov', '123')
    # admin_actions()
    login_screen()
    # pending_user_list()
    # change_user_data()
    # client_log_in()
    # admin_log_in()
    # Cars('BMW', "330i xDrive", 2020)
    # Cars('Alfa Romeo', "4C Spider", 2017)
    # Cars('Audi', "A3 Prestige", 2019)
    # Cars('Cadillac', "ATS Luxury", 2015)
    # Cars('Jaguar', "E-Pace Turbo", 2021)
    # Cars('Toyota', "Corolla XSE", 2017)
    # Auto_parts(123321, 'Duralast Platinum', 'Engine', 200, [0, 1], 'EFB Technology')
    # Auto_parts(124678, 'Duralast Brake Rotor', 'Brakes', 56, [2, 3], 'Duralast')
    # Auto_parts(213586, 'Engine Oil', 'Motor Oil', 22, [4, 5], 'STP')
    # Auto_parts(331678, 'Transmission Fluid', 'Motor Oil', 9, [1, 3], 'STP')
    # Auto_parts(441578, 'Duralast Bracketed Brake Calliper', 'Brakes', 365, [2, 4], 'Duralast')
    # Auto_parts(981235, 'Grade A Remanufactured Long Block Engine', 'Engine', 4037, [0, 5], 'EFB Technology')
    # print(get_orders()[1])
    # print(get_approved_users()[3][0]['date'])
