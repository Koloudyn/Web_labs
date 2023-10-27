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

print("Задание 4") #UPDATE service_booking SET price = price * 0.85 WHERE room_booking_id = (
df = pd.read_sql('''
        SELECT * , (price * 0.85)
        FROM service_booking
        WHERE room_booking_id = (
            SELECT room_booking_id
            FROM room_booking
            WHERE guest_id = (
                SELECT guest_id 
                FROM guest 
                WHERE guest_name = "Астахов И.И."
            ) AND check_in_date = '2021-01-13'
        );
    ''', con)
print(df.to_string(), end="\n\n")

print("Задание 5")
df = pd.read_sql('''
        SELECT rtrim ( replace(substr ("January--February-March----April----May------June-----July-----August---SeptemberOctober--November-December", strftime ("%m", service_start_date) * 9 - 8, 9), "-", "")) AS "Месяц", 
        service_start_date AS "Дата", service_name AS "Услуга", price AS "Сумма", SUM(price) OVER (PARTITION BY service_start_date) AS "Сумма_с_накоплением"
        FROM service_booking, service
        WHERE service.service_id = service_booking.service_id
        ORDER BY service_start_date, service_name;
    ''', con)
print(df.to_string(), end="\n\n")

con.close()
