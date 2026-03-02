from modules.crypto import zip_password

if __name__ == "__main__":
    name = "Excel.zip"
    password = zip_password(zip_name=name)
    print("Excel.zip password is ", password)
