import argparse, csv, random, string
from zk import ZK, const
from UID_Generator import UID_Generator

# data needed to enter a user -> UID , name , privilege , password , *group_id , user_id

# generate password for each user
# def generate_password(length=8):
#     characters = string.ascii_letters + string.digits + string.punctuation + string.ascii_lowercase + string.ascii_uppercase
#     return ''.join(random.choice(characters) for _ in range(length))

# insert every user from the input file to the selected device
def insert_employees_to_device(ip, port, csv_file):
    # connect to the attendance device
    zk = ZK(ip, port=port, timeout=5)
    conn = None
    uid_generator = UID_Generator()

    try:
        conn = zk.connect()
        conn.disable_device()

        # read the csv file
        with open(csv_file, mode='r', encoding='utf-16') as file:
            reader = csv.DictReader(file)
            for row in reader:
                UID = uid_generator.generate_uid()
                name = " ".join([row.get('name_f'), row.get('name_l')])# row.get('name_f') + " " + row.get('name_l')
                privilege =  int(row.get('Privilege'))
                password = row.get('UID', '') 
                group_id = row.get('Group_Id', '')
                user_id = str(row.get('Field No'))

                conn.set_user(uid=UID, name=name, privilege=privilege, password=password, group_id=group_id, user_id=user_id)
                print(f"Added user: {user_id} - {name} with password: {password}")
    except Exception as exc:
        print(f"Process failed with {exc}")
    finally:
        if conn:
            conn.enable_device()
            conn.disconnect()

parser = argparse.ArgumentParser(description="Add all the employees to the selected attendance device")
parser.add_argument('--ip', required=True, help="IP address of the attendance device")
parser.add_argument('-p', '--port', type=int, default=4370, help="Port of the attendance device (defailt: 4370)")
parser.add_argument('-f', '--file', required=True, help="Path to the CSV file containing all pf the employees to be added")

args = parser.parse_args()

insert_employees_to_device(args.ip, args.port, args.file)
