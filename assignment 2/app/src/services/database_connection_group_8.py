from mysql.connector import connect

db_password = "KUnet1235"
sql_query_template = {}
sql_query_template["get_dcr_role"] = (
    f"SELECT Role FROM DCRUsers WHERE Email = %(email)s"
)

sql_query_template["get_dcr_role"] = (
    f"SELECT Role FROM DCRUsers WHERE Email = %(email)s"
)
sql_query_template["update_dcr_role"] = (
    f"UPDATE DCRUsers SET Role = %(role)s WHERE Email = %(email)s"
)
sql_query_template["get_all_instances"] = f"SELECT * FROM Instances"
sql_query_template["get_instances_for_user"] = (
    f"SELECT i.* FROM Instances i JOIN UserInstances ui ON i.InstanceID = ui.InstanceID WHERE ui.Email = %(email)s"
)
sql_query_template["insert_instance"] = (
    f"INSERT INTO Instances (InstanceID, IsInValidState) VALUES (%(instance_id)s, %(is_valid)s)"
)
sql_query_template["insert_instance_for_user"] = (
    f"INSERT INTO UserInstances (Email, InstanceID) VALUES (%(email)s, %(instance_id)s)"
)
sql_query_template["update_instance"] = (
    f"UPDATE Instances SET IsInValidState = %(is_valid)s WHERE InstanceID = %(instance_id)s"
)
sql_query_template["delete_instance_from_user_instance"] = (
    f"DELETE FROM UserInstances WHERE InstanceID = %(instance_id)s"
)
sql_query_template["delete_instance"] = (
    f"DELETE FROM Instances WHERE InstanceID = %(instance_id)s"
)


#Event data:
sql_query_template["insert_or_update_choice_data"] = (
    f"INSERT INTO DataEvents (InstanceID, EventID, Choice) "
    f"VALUES (%(instance_id)s, %(event_id)s, %(choice_value)s) "
    f"ON DUPLICATE KEY UPDATE Choice = %(choice_value)s"
)

sql_query_template["select_personal_data"] = (
    f"SELECT Choice FROM DataEvents "
    f"WHERE InstanceID = %(instance_id)s AND EventID = %(event_id)s"
)

sql_query_template["delete_choice_data"] = (
    f"DELETE FROM DataEvents WHERE InstanceID = %(instance_id)s"
)




def db_connect():
    from pathlib import Path

    resources_folder = Path(__file__).parent.resolve()
    cert_filepath = str(resources_folder.joinpath("DigiCertGlobalRootCA.crt.pem"))
    cnx = connect(
        user="group8",
        password=db_password,
        host="tasklistgroup8.mysql.database.azure.com",
        port=3306,
        database="database",
        ssl_ca=cert_filepath,
        ssl_disabled=False,
    )
    print(f"[i] cnx is connected: {cnx.is_connected()}")
    return cnx


def get_dcr_role(email):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template["get_dcr_role"], {"email": email})
        query_result = cursor.fetchone()[0]
        cursor.close()
        cnx.close()
        return query_result
    except Exception as ex:
        print(f"[x] error get_dcr_role! {ex}")
        return None


def update_dcr_role(email, role):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(
            sql_query_template["update_dcr_role"],
            {"role": role, "email": email},
            multi=False,
        )
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f"[x] error update_dcr_role! {ex}")


def get_all_instances():
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template["get_all_instances"])
        query_result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return query_result
    except Exception as ex:
        print(f"[x] error get_all_instances! {ex}")
        return None


def get_instances_for_user(email):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template["get_instances_for_user"], {"email": email})
        query_result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return query_result
    except Exception as ex:
        print(f"[x] error get_instances_for_user! {ex}")
        return None


def insert_instance(id, valid, email):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(
            sql_query_template["insert_instance"],
            {"instance_id": id, "is_valid": valid},
            multi=False,
        )
        cursor.execute(
            sql_query_template["insert_instance_for_user"],
            {"email": email, "instance_id": id},
            multi=False,
        )
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f"[x] error insert_instance! {ex}")


def update_instance(id, valid):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(
            sql_query_template["update_instance"],
            {"instance_id": id, "is_valid": valid},
            multi=False,
        )
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f"[x] error update_instance! {ex}")


def delete_instance(id):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(
            sql_query_template["delete_instance_from_user_instance"],
            {"instance_id": id},  # Changed to instance_id to match template
            multi=False,
        )
        cursor.execute(
            sql_query_template["delete_choice_data"], 
            {"instance_id": id},  # Delete choice data.
            multi=False
        )
        cursor.execute(
            sql_query_template["delete_instance"], 
            {"instance_id": id},  # Changed to instance_id to match template
            multi=False
        )
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f"[x] error delete_instance! {ex}")



####
# Event data functions:
####

def insert_or_update_choice(instance_id, event_id, choice_value):
    try:
        cnx = db_connect()
        cursor = cnx.cursor(buffered=True)
        cursor.execute(sql_query_template["insert_or_update_personal_data"], 
                       {"instance_id": instance_id, 
                        "event_id": event_id, 
                        "choice_value": choice_value})
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as ex:
        print(f"[x] Error in insert_or_update_choice: {ex}")

