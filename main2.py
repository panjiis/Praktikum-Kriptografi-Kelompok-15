import streamlit as st
import mysql.connector
import string

def affine_encrypt(plaintext, a, b):
    alphabet = string.digits + string.ascii_uppercase  # Gunakan digit dan huruf uppercase saja
    encrypted_text = ""
    for char in plaintext:
        if char.isalnum(): 
            if char.isdigit():  # Angka tetap
                x = alphabet.index(char)
            else:  # Huruf
                x = alphabet.index(char.upper())
            encrypted_text += alphabet[(a * x + b) % len(alphabet)]
        else:
            encrypted_text += char
    return encrypted_text

def affine_decrypt(ciphertext, a, b):
    alphabet = string.digits + string.ascii_uppercase
    if gcd(a, len(alphabet)) != 1:
        raise ValueError(f"Nilai a ({a}) tidak memiliki invers modular terhadap {len(alphabet)}.")
    
    a_inv = pow(a, -1, len(alphabet))  
    decrypted_text = ""
    for char in ciphertext:
        if char.isalnum():
            if char.isdigit():  # Angka tetap
                x = alphabet.index(char)
            else:  # Huruf
                x = alphabet.index(char.upper())
            decrypted_text += alphabet[a_inv * (x - b) % len(alphabet)]
        else:
            decrypted_text += char
    return decrypted_text

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def next_prime(n):
    while True:
        n += 1
        if is_prime(n):
            return n

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="",  
        database="user",  
        port=3306 
    )

def columnar_encrypt(chippertext, key):
    n = len(key)
    m = len(chippertext)
    num_columns = n
    num_rows = m // n + (m % n > 0)  # jumlah baris
    encrypted_text = [''] * n
    
    # Mengurutkan kunci
    sorted_key = sorted(enumerate(key), key=lambda x: x[1])  # Sorting berdasarkan kunci
    key_order = [k[0] for k in sorted_key]  # Menyimpan urutan index berdasarkan kunci yang sudah disort
    
    # Mengisi kolom sesuai urutan key
    for i, k in enumerate(key_order):
        for j in range(num_rows):
            idx = j * n + k
            if idx < m:
                encrypted_text[i] += chippertext[idx]
            else:
                encrypted_text[i] += 'x'  # Isi dengan 'x' jika ada kekosongan
    
    return ''.join(encrypted_text)

def columnar_decrypt(encrypted_text, key):
    n = len(key)
    m = len(encrypted_text)
    num_columns = n
    num_rows = m // n  # jumlah baris
    decrypted_text = [''] * (num_rows * n)
    
    # Mengurutkan kunci
    sorted_key = sorted(enumerate(key), key=lambda x: x[1])  # Sorting berdasarkan kunci
    key_order = [k[0] for k in sorted_key]  # Menyimpan urutan index berdasarkan kunci yang sudah disort
    
    # Membaca kolom sesuai urutan kunci
    index = 0
    for i, k in enumerate(key_order):
        for j in range(num_rows):
            decrypted_text[j * n + k] = encrypted_text[index]
            index += 1
    
    return ''.join(decrypted_text)

st.title("Aplikasi Register dan Login")

def register():
    st.subheader("Register")
    username = st.text_input("Username (12 digit angka)", max_chars=12)
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username and password:
            if not password.isalnum():
                st.error("Password hanya boleh mengandung angka dan huruf!")
                return

            user_digits = username[-4:]  # 4 digit terakhir dari username
            key_digits = [int(char) for char in user_digits]  # Konversi ke list angka
            
            user_digit = username[-2:]  # 2 digit terakhir dari username

            # Menghitung nilai a sebagai bilangan berikutnya dari dua digit terakhir
            a = next_prime(int(user_digit)) 
            b = int(user_digit)  # 2 digit terakhir sebagai b

            encrypted_password = affine_encrypt(password, a, b)

            # Enkripsi columnar menggunakan key dari 4 digit terakhir username
            columnar_encrypted_password = columnar_encrypt(encrypted_password, key_digits)

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, columnar_encrypted_password))
            conn.commit()

            cursor.close()
            conn.close()

            st.success("User berhasil terdaftar!")


def login():
    st.subheader("Login")
    username = st.text_input("Username (12 digit angka)", max_chars=12)
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()

            if user:
                encrypted_password = user[0]

                user_digits = username[-4:]
                key_digits = [int(char) for char in user_digits]  

                user_digit = username[-2:]

                a = next_prime(int(user_digit))
                b = int(user_digit) 

                decrypted_password_columnar = columnar_decrypt(encrypted_password, key_digits)
                decrypted_password_affine = affine_decrypt(decrypted_password_columnar, a, b)

                if decrypted_password_affine.upper() == password.upper():
                    st.success("Login berhasil!")
                else:
                    st.error("Password salah!")
            else:
                st.error("Username tidak ditemukan!")

            cursor.close()
            conn.close()

option = st.selectbox("Pilih opsi", ["Login", "Register"])

if option == "Login":
    login()
else:
    register()
