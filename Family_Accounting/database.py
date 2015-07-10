#Create and manage the database.

import sqlite3

class Database():
  def __init__(self, path):
    self.path = path
    self.conn = None
    self.c = None
    self.TABLE_SOURCE = "money_source"
    self.TABLE_MOVEMENT = "movements"
    self.create_tables()

  def connect(self):
    self.conn = sqlite3.connect(self.path)
    self.c = self.conn.cursor()

  def create_tables(self):
    self.connect()
    self.c.execute("create table if not exists " + self.TABLE_SOURCE 
          + " (id INTEGER PRIMARY KEY AUTOINCREMENT, " 
          + "name blob not null, total int not null);")
    self.c.execute("create table if not exists " 
          + self.TABLE_MOVEMENT + " (id INTEGER PRIMARY KEY AUTOINCREMENT, "
          + "source_id int not null, name mediumblob not null, "
          + "movement_date date not null, income int, outgoing int, "
          + "constraint source_id_movementsfk foreign key(source_id) "
          + "references money_source(id) on update cascade on delete cascade);")
    self.conn.commit()
    self.conn.close()
  
  def get_all_movements(self, start_index, number_elements):
    self.connect()
    self.c.execute("select * from " + self.TABLE_MOVEMENT 
          + " order by movement_date desc limit "+ str(start_index) 
          + ", " + str(number_elements) +";")
    res = self.c.fetchall()
    self.conn.commit()
    self.conn.close()
    return res
  
  def get_sources(self, start_index, number_elements):
    self.connect()
    self.c.execute("select * from " + self.TABLE_SOURCE + " limit " 
          + str(start_index) + ", " + str(number_elements) + ";")
    res = self.c.fetchall()
    self.conn.commit()
    self.conn.close()
    return res

  def get_source(self, source_id):
    self.connect()
    self.c.execute("select * from " + self.TABLE_SOURCE
          + " where id=" + str(source_id))
    res = self.c.fetchone()
    self.conn.commit()
    self.conn.close()
    return res

  def get_movement(self, movement_id):
    self.connect()
    self.c.execute("select * from " + self.TABLE_MOVEMENT
          + " where id=" + str(movement_id) + ";")
    res = self.c.fetchone()
    self.conn.commit()
    self.conn.close()
    return res

  def update_total_value(self, source_id, value):
    self.c.execute("update " + self.TABLE_SOURCE + " set total=total+"
          + str(value) + " where id=" + str(source_id) + ";")
    self.conn.commit()

  def get_movements_source(self, source_id):
    self.connect()
    self.c.execute("select * from " + self.TABLE_MOVEMENT
          + " where source_id=" + str(source_id) + ";")
    res = self.c.fetchall()
    self.conn.commit()
    self.conn.close()
    return res

  def get_source_name(self, source_id):
    self.connect()
    self.c.execute("select name from " + self.TABLE_SOURCE
          + " where id=" + str(source_id) + ";")
    res = self.c.fetchone()[0]
    self.conn.commit()
    self.conn.close()
    return res

  def new_source(self, name, total):
    self.connect()
    self.c.execute("insert into " + self.TABLE_SOURCE
          + " (name, total) values ('" + name + "', " + str(total) + ");")
    self.conn.commit()
    self.conn.close()

  def edit_source(self, source_id, name, total):
    self.connect()
    self.c.execute("select total from " + self.TABLE_SOURCE
          + " where id=" + str(source_id) + ";")
    if total != self.c.fetchone()[0]:
      self.c.execute("select income, outgoing from " + self.TABLE_MOVEMENT
          + " where source_id=" + str(source_id) + ";")
      rows = self.c.fetchall()
      count_movement_total = 0
      for row in rows:
        count_movement_total += row[0]
        count_movement_total -= row[1]
      self.c.execute("update " + self.TABLE_SOURCE + " set name=\""
            + name + "\", total=" + str((float(total) + count_movement_total))
            + " where id=" + str(source_id) + ";")
    else:
        self.c.execute("update " + self.TABLE_SOURCE + " set name=\""
            + name + "\" where id=" + str(source_id))
    self.conn.commit()
    self.conn.close()

  def delete_source(self, source_id):
    self.connect()
    self.c.execute("delete from " + self.TABLE_SOURCE 
            + " where id=" + str(source_id))
    self.delete_all_movements_from_source(source_id)
    self.conn.commit()
    self.conn.close()

  def delete_all_movements_from_source(self, source_id):
    self.c.execute("delete from " + self.TABLE_MOVEMENT 
                   + " where source_id="+str(source_id))
    self.conn.commit()

  def new_movement(self, name, source_id, movement_date, income, outgoing):
    self.connect()
    self.c.execute('insert into '
          + self.TABLE_MOVEMENT
          + '(source_id, name, movement_date, income, outgoing) values ('
          + str(source_id) + ', "' + name + '", "' + movement_date
          + '", ' + str(income) + ', ' + str(outgoing) + ');')
    if float(outgoing) > 0:
      self.update_total_value(source_id, str(-float(outgoing)))
    else:      
      self.update_total_value(source_id, income)
    self.conn.commit()
    self.conn.close()

  def edit_movement(self, movement_id, name, source_id, movement_date, income,
                    outgoing):
    movement = self.get_movement(movement_id)
    self.connect()
    self.c.execute("update " + self.TABLE_MOVEMENT + " set source_id="
          + str(source_id) + ", name=\"" + name + "\", movement_date=\""
          + movement_date + "\", income=" + str(income) + ", outgoing="
          + str(outgoing) + " where id=" + str(movement_id) + ";")
    if income != movement[4] | outgoing != movement[5]:
      self.update_total_value(source_id, float(income))
      self.update_total_value(source_id, -float(outgoing))
      self.update_total_value(movement[1], -float(movement[4]))
      self.update_total_value(movement[1], float(movement[5]))
    self.conn.commit()
    self.conn.close()

  def delete_movement(self, movement_id):
    self.connect()
    self.c.execute("delete from " + self.TABLE_MOVEMENT + " where id="
          + str(movement_id))
    self.conn.commit()
    self.conn.close()

  def count_rows_source(self):
    self.connect()
    self.c.execute('select count(id) from ' + self.TABLE_SOURCE + ';')
    res = self.c.fetchone()[0]
    self.conn.commit()
    self.conn.close()
    return res

  def count_rows_movement(self):
    self.connect()
    self.c.execute('select count(id) from ' + self.TABLE_MOVEMENT + ';')
    res = self.c.fetchone()[0]
    self.conn.commit()
    self.conn.close()
    return res