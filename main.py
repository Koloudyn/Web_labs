import sqlite3
import pandas as pd

# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("booking.sqlite")
f_damp = open('booking.db','r', encoding ='utf-8-sig')
damp = f_damp.read()
f_damp.close()
con.executescript(damp)
con.commit()

df = pd.read_sql('''
    SELECT guest_name, room_name, check_in_date, check_out_date, DATEDIFF(check_out_date, check_in_date) AS Количество_дней
    FROM guest, room, room_booking, status
    WHERE  status.status_name = "Занят" AND status.status_id = room_booking.status_id
    AND guest.guest_id = room_booking.guest_id 
    AND room.room_id = room_booking.room_id
    AND check_in_date BETWEEN '2020-11-30' AND '2021-01-30'
    GROUP BY guest_name
    ''', con)
print(df)


con.close()