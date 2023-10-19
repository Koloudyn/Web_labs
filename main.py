import sqlite3
import pandas as pd

# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("booking.sqlite")
f_damp = open('booking.db','r', encoding ='utf-8-sig')
damp = f_damp.read()
f_damp.close()
con.executescript(damp)
con.commit()

print("Задание 1")
df = pd.read_sql('''
    SELECT guest_name, room_name, check_in_date, (JULIANDAY(check_out_date) - JULIANDAY(check_in_date) + 1) AS Количество_дней
    FROM guest, room, room_booking, status
    WHERE  status.status_name = "Занят" AND status.status_id = room_booking.status_id
    AND guest.guest_id = room_booking.guest_id
    AND room.room_id = room_booking.room_id
    AND check_in_date BETWEEN '2020-11-30' AND '2021-01-30'
    ORDER BY guest_name, room_name, check_in_date DESC
    ''', con)
print(df, end="\n\n")

print("Задание 2")
df = pd.read_sql('''
        SELECT room_name AS Номер, strftime('%Y', check_in_date) AS Год, COUNT(strftime('%Y', check_in_date)) AS Количество
        FROM room_booking, status, room
        WHERE room_booking.status_id = status.status_id AND status.status_name = "Занят"
        AND room.room_id = room_booking.room_id
        GROUP BY room_booking.room_id, strftime('%Y', check_in_date)
        ORDER BY room_name, strftime('%Y', check_in_date) DESC
    ''', con)
print(df, end="\n\n")

print("Задание 3")
df = pd.read_sql('''
        SELECT room_booking.guest_id, guest_name AS "ФИО", COUNT(room_booking.guest_id) AS "Количество"
        FROM room_booking, status, guest
        WHERE room_booking.status_id = status.status_id AND status.status_name = "Занят"
        AND guest.guest_id = room_booking.guest_id
        GROUP BY room_booking.guest_id
        HAVING COUNT (room_booking.guest_id) = (
            SELECT MAX(count)
            FROM (
                SELECT guest_id, COUNT(guest_id) AS count
                FROM room_booking, status
                WHERE room_booking.status_id = status.status_id AND status.status_name = "Занят"
                GROUP BY guest_id
            )
        )
        ORDER BY guest_name;
    ''', con)
print(df, end="\n\n")

con.close()
