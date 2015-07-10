'''Make a command line interface to manage the program call main_menu().'''

import database
import time
import pagination
import time
import re

class CLI():
  '''The main class to manage the program.'''
  def __init__(self, path, first_button='a', last_button='f', previous_button='s', 
               next_button='d', back_button='b', exit_button='x', 
               number_elements=25):
    self.db = database.Database(path)
    self.first_button = first_button
    self.last_button = last_button
    self.previous_button = previous_button
    self.next_button = next_button
    self.back_button = back_button
    self.exit_button = exit_button
    self.number_elements = number_elements
    self.is_money = re.compile('^([-])?\d+([\.,][0-9]{2})?$')
    self.is_date = re.compile('([0][1-9]|[12][0-9]|[3][01])[/-]([0][1-9]|[1][0-2])[/-]([12]\d\d\d)')
    self.is_option = re.compile('\d{1}')
    self.is_number = re.compile('^\d+$')
    self.yn_error_message = 'Please type "Y/y" or "N/n".\n'

  def main_menu(self):
    '''Print main menu. There are a few options.
    This function asks to the user for a option and checks 
    if it's correct or not and if it's run the wished function.'''


    print('\nWelcome to Famly Accounting.')
    while True:
      print('\nPlease select an option.\n'
            '1. Source Menu\n'
            '2. Movement Menu\n'
            '3. Setting\n'
            '4. Exit')
      keyboard = raw_input('Choose an option: ')
      if self.is_option.match(keyboard) != None:
        # User typed a number.
        if keyboard == "1":
          # Run source_menu() function.
          self.source_menu()
        elif keyboard == "2":
          # Run movement_menu()
          self.movement_menu()
        elif keyboard == "3":
          # Run setting() function (doesn't work right now)
          self.setting()
        elif keyboard == "4":
          # Run exit_program() function
          self.exit_program()
        else:
          # User typed an incorrect option.
          print('The option you choose is incorrect.'
                'Please select a valid option.')
      else:
        print('You must type a number.')

  def source_menu(self):
    '''Print a menu with the necessary options to do all actions.
    The user can view, create, edit and delete money sources.
    This function checks if the user types a correct option.'''


    while True:
      print('\nPlease select an option.\n'
          '1.Create a new money source\n'
          '2.Edit an existing money source\n'
          '3.Delete an existing money source\n'
          '4.View all money sources\n'
          '5.Back to main menu\n'
          '6.Exit')
      keyboard = raw_input('Choose an option: ')
      if self.is_option.match(keyboard) != None:
        if keyboard == "1":
          # Run cli_create_source() function
          self.cli_create_source()
        elif keyboard == "2":
          # Run cli_edit_source() function
          self.cli_edit_source()
        elif keyboard == "3":
          # Run cli_delete_source() function
          self.cli_delete_source()
        elif keyboard == "4":
          # Run view_source() function
          self.view_sources()
        elif keyboard == "5":
          # User wants to back to main menu
          break
        elif keyboard == "6":
          # Run exit_program() function
          self.exit_program()
        else:
          # User typed an incorrect option.
          print('The option you choose is incorrect.'
                'Please select a valid option.')
      else:
        print('You must type a number.')

  def movement_menu(self):
    '''Print a menu with the necessary options to do all actions.
    The user can view, create, edit and delete movements.
    This function checks if the user types a correct option.'''


    while True:
      print('\nPlease select an option.\n'
          '1.Create a new movement\n'
          '2.Edit an existing movement\n'
          '3.Delete an existing movement\n'
          '4.View all movements\n'
          '5.Back to main menu\n'
          '6.Exit')
      keyboard = raw_input('Choose an option: ')
      if self.is_option.match(keyboard) != None:
        # User typed a number
        if keyboard == "1":
          # Run cli_create_movement() function
          self.cli_create_movement()
        elif keyboard == "2":
          # Run cli_edit_movement() function
          self.cli_edit_movement()
        elif keyboard == "3":
          # Run cli_delete_movement() funtion
          self.cli_delete_movement()
        elif keyboard == "4":
          # Run view_movements() function
          self.view_movements()
        elif keyboard == "5":
          # User wants to back to main menu
          break
        elif keyboard == "6":
          # Run exit_program() funtion
          self.exit_program()
        else:
          # User typed an incorrect option.
          print('The option you choose is incorrect.'
                'Please select a valid option.\n')
      else:
        print('You must type a number.')

  def view_sources(self):
    '''Function to view all sources. It has a pagination and 
    also has a default keyboard control on the constructor is the information
    to know the control.'''
    

    start_index = 0;
    current_page = 1
    total_elements = self.db.count_rows_source()
    pag = pagination.Pagination(self.db.count_rows_source(), self.number_elements)
    while True:
      # Start program instruction for the user.
      print('Select "' + self.back_button 
            + '" to back movement menu.\n'
            'Select "' + self.exit_button + '" to exit\n')
      for source in self.db.get_sources(start_index, self.number_elements):
        print('| ID: ' + str(source[0]) + ' | Source name: ' 
              + source[1] +' | Total: ' + str(source[2]) + ' |')
      print('Current page: ' + str(current_page) + '\n'
            + pag.pagination(current_page, self.first_button, 
              self.last_button, self.previous_button, self.next_button) + '\n')
      # End of program instruction for the user.
      keyboard = raw_input("Choose a money source or option: ")
      if keyboard == self.first_button and current_page > 2:
        # current_page higher than 2 and can go to the first page.
        current_page = 1
      elif(keyboard == self.last_button and 
            current_page < (total_elements / self.number_elements ) - 1):
        # current_page below than the total pages less one and 
        # can go to the last page
        current_page = total_elements / self.number_elements
      elif(keyboard == self.next_button and 
            current_page != (total_elements / self.number_elements) + 1):
        # current_page + 1 until current_page = total pages.
        current_page += 1 
      elif keyboard == self.previous_button and current_page != 1:
        # current_page - 1 until current_page = 1
        current_page -= 1
      elif keyboard == self.exit_button:
        # Calls exit_program() function.
        self.exit_program()
      elif keyboard == self.back_button:
        # Back to source_menu().
        break
      else:
        # User typed an incorrect option.
        print('Please select a valid option.\n')
      start_index = (current_page - 1) * self.number_elements

  def cli_create_source(self):
    '''Create a new money source. Check if have a name and a total value.'''
    name = ""
    total = ""
    while not name:
      name = raw_input('Insert a name: ')
    while self.is_money.match(total) == None:
      total = raw_input('Introduce the total value '
            + '(the current money in the source): ').replace(",", ".")
    self.db.new_source(name, total)

  def cli_edit_source(self):
    '''Edit an existing money source. Print all money sources and after
    this function will ask if want to change something.'''
    start_index = 0;
    current_page = 1
    total_elements = self.db.count_rows_source()
    pag = pagination.Pagination(total_elements, self.number_elements)
    name = None
    total = None
    id_list = []
    while True:
      index = 0
      # Print money sources.
      print('\nPlease select a source to edit it.\n'
            'Choose a number and press enter or go to other page.\n'
            'Select "' + self.back_button 
            + '" to back source menu.\n'
            'Select "' + self.exit_button + '" to exit\n'
            '-------------------------------------------------------------'
              '---------')
      for source in self.db.get_sources(start_index, self.number_elements):
        print('| ID: ' + str(source[0]) + ' | Name: ' 
              + source[1] + ' | Total: ' + str(source[2]) + ' |')
        id_list.insert(index, source[0])
        index += 1
      print('-------------------------------------------------------------'
            '---------\nCurrent page: ' + str(current_page) + '\n'
            + pag.pagination(current_page, self.first_button, 
                             self.last_button, self.previous_button, 
                             self.next_button))
      # Ask for a option or source.
      keyboard = raw_input("Choose a money source or option: ")
      # Check keyboard.
      if keyboard == self.first_button and current_page > 2:
        # User wants to go to first page.
        current_page = 1
      elif(keyboard == self.last_button and 
           current_page < total_elements / self.number_elements):
        # User wants to go to the last page.
        current_page = total_elements / self.number_elements + 1
      elif (keyboard == self.next_button and 
        current_page != (total_elements / self.number_elements) + 1):
        # User wants to go to the next page.
        current_page += 1 
      elif keyboard == self.previous_button and current_page != 1:
        # User wants to go to the previous page.
        current_page -= 1
      elif self.is_number.match(keyboard) != None:
        # keyboard is a number after we check if it's an ID.
        if int(keyboard) in id_list:
          while True:
            # keyboard is an ID and now we can ask if really the user wants to
            # edit it or not.
            answer = raw_input('Do you really want to change it?(Y/y/N/n)').lower()
            if answer == 'y':
              # User wants to change that money source and 
              # we get the source from th database
              source = self.db.get_source(keyboard)
              # Ask if the user wants to change the name.
              print('\nCurrent name: ' + source[1])
              answer = ""
              while answer != "y" and answer != "n":
                answer = raw_input('Do you want to change the name?(Y/y/N/n): ').lower()
                if answer == 'y':
                  name = raw_input('Type the new name: ')
                elif answer == 'n':
                  name = source[1]
                  print(name + " -> name en cli")
                else:
                  print(self.yn_error_message)
              # End asking for the name.

              # Asking for the total value.
              print('Total: ' + str(source[2])   + '\n')
              answer = None
              while answer != 'y' and answer != 'n':
                answer = raw_input('Do you want to change the total value?(Y/y/N/n): ').lower()
              if answer == 'y':
                while self.is_money.match(str(total)) == None:
                  total = raw_input('Type the new total: ')
              elif answer == 'n':
                total = str(source[2])
              else:
                print(self.yn_error_message)
              # End asking for the total value.

              # Editing on the database.
              self.db.edit_source(keyboard, name, total)
              break
            elif answer == 'n':
              break
            else:
              print(self.yn_error_message)
      elif keyboard == self.exit_button:
        self.exit_program()
      elif keyboard == self.back_button:
        break
      else:
        print('The option you choose is incorrect.'
              'Please select a valid option.\n')
      start_index = (current_page - 1) * self.number_elements

  def cli_delete_source(self):
    '''Delete a source. This part is only the interface'''

    start_index = 0;
    current_page = 1
    total_elements = 0
    id_list = []
    while True:
      # Because total_elements changes it's better let here
      # inside the while.
      total_elements = self.db.count_rows_source()
      pag = pagination.Pagination(total_elements, self.number_elements)
      index = 0
      # Print controls and sources.
      print('\nPlease select a source to remove it.\n'
            'Choose a number and press enter or go to other page.\n'
            'Select "' + self.back_button 
            + '" to back movement menu.\n'
            'Select "' + self.exit_button + '" to exit\n'
            '-------------------------------------------------------------'
              '---------')
      for source in self.db.get_sources(start_index, self.number_elements):
        print('| ID: ' + str(source[0]) + ' | Source name: ' 
              + source[1] +' | Total: ' + str(source[2]) + ' |')
        id_list.insert(index, source[0])
        index += 1
      print('-------------------------------------------------------------'
              '---------\nCurrent page: ' + str(current_page) + '\n'
            + pag.pagination(current_page, self.first_button, 
              self.last_button, self.previous_button, self.next_button) + '\n')
      # End of print.
      # Asking for an option.
      keyboard = raw_input("Choose a money source or option: ")
      if keyboard == self.first_button and current_page > 2:
        # User wants to go to first page.
        current_page = 1
      elif(keyboard == self.last_button and 
           current_page < total_elements / self.number_elements):
        # User wants to go to the last page.
        current_page = total_elements / self.number_elements + 1
      elif (keyboard == self.next_button and 
        current_page != (total_elements / self.number_elements) + 1):
        # User wants to go to the next page.
        current_page += 1 
      elif keyboard == self.previous_button and current_page != 1:
        # User wants to go to the previous page.
        current_page -= 1
      elif self.is_number.match(keyboard) != None:
        if int(keyboard) in id_list:
          # User wants to delete that source.
          # Asking if user is sure about this operation.
          answer = ""
          while answer != "y" and answer != "n":
            answer = raw_input('Do you really want to delete it?'
                              + '(Y/y/N/n): ').lower()
            if answer == "y":
              # Delete the source.
              self.db.delete_source(keyboard)
            elif answer != "n" or answer != "y":
              # Answer incorrect.
              print(self.yn_error_message)
      elif keyboard == self.exit_button:
        # User wants to exit of program.
        self.exit_program()
      elif keyboard == self.back_button:
        # User wants to back to source menu.
        break
      else:
        # User type an incorrect option.
        print('The option you choose is incorrect.'
              'Please select a valid option.\n')
      start_index = (current_page - 1) * self.number_elements


  def view_movements(self):
    '''Function to view all movements whatever is the source id.
    Display a pagination and all keyboard control. '''


    current_page = 1
    start_index = 0
    total_elements = self.db.count_rows_movement()
    pag = pagination.Pagination(total_elements, self.number_elements)
    print(total_elements)
    while True:
      print('Select "' + self.back_button 
            + '" to back movement menu.\n'
            'Select "' + self.exit_button + '" to exit\n'
            'Choose a number and press enter or select other button '
            'to go to another page.\n'
            '-------------------------------------------------------------'
              '---------')
      if total_elements > 0:
        for movement in self.db.get_all_movements(
              start_index, self.number_elements):
          print('| ID: ' + str(movement[0]) + ' | Source name: ' 
                + self.db.get_source_name(str(movement[1])) + ' | Name: ' 
                + movement[2] + ' | Movement date: ' 
                + self.format_date_europe(movement[3]) + ' | Income: '
                + str(movement[4]) + '| Outgoing: ' + str(movement[5]) + ' |\n'
                )
        print('Current page: ' + str(current_page) + '\n'
              + pag.pagination(current_page, self.first_button, 
                               self.last_button, self.previous_button, 
                               self.next_button)
              + '\n')
      else:
        print('There aren\'t movements.')
      print('-------------------------------------------------------------'
            '---------')
      keyboard = raw_input('Choose a movement or option: ')
      print(keyboard + ' keyboard')
      # When user type something we need to check it.
      if keyboard == self.first_button and current_page > 2:
        # User wants to go to first page.
        current_page = 1
      elif(keyboard == self.last_button and 
           current_page < total_elements / self.number_elements):
        # User wants to go to the last page.
        current_page = total_elements / self.number_elements + 1
      elif (keyboard == self.next_button and 
        current_page != (total_elements / self.number_elements) + 1):
        # User wants to go to the next page.
        current_page += 1 
      elif keyboard == self.previous_button and current_page != 1:
        # User wants to go to the previous page.
        current_page -= 1
      elif keyboard == self.back_button:
        # User wants to back to movement menu
        break
      else:
        # User type an incorrect option.
        print('Please type a valid option.')
      start_index = (current_page - 1) * self.number_elements

  def cli_create_movement(self):
    '''This is the interface for creating a new movment.'''

    name = ""
    source_id = None
    movement_date = None
    income = "0"
    outgoing = "0"
    current_page = 1
    start_index = 0 
    pag_source = pagination.Pagination(self.db.count_rows_source(), self.number_elements)
    while True:
      # Asking if the user wants to create a new movement or not.
      keyboard = raw_input('Do you really want to create a '
                           + 'new movement?(Y/y/N/n): ').lower()
      if keyboard == 'y':
        # User wants to create it. Asking for movement's name.
        while name == "":
          name = raw_input(
                "Introduce the name for the movement can\'t be empty: ")
        # End asking for the naxme.
        # Asking for the source ID.
        while True:
          index = 0
          print('Select a money source.\n'
                'If you wish to exit, please press "' + self.exit_button +'"\n' 
                'Current page: ' + str(current_page) + '\n'
                + pag_source.pagination(
                      current_page, self.first_button, self.last_button,
                      self.previous_button, self.next_button))
          id_list_source = []
          print('----------------------------------------------------------'
                '-----------')
          for source in self.db.get_sources(start_index, self.number_elements):
            print('| ID ' + str(source[0]) +' | Name : ' 
                  + source[1] + ' | Total: ' + str(source[2]) + ' |')
            id_list_source.insert(index, source[0])
            index += 1
          print('----------------------------------------------------------'
                  '-----------')
          keyboard_source = raw_input("Choose a source or option: ")
          if keyboard_source == self.first_button and current_page > 2:
            # User wants to go to first page.
            current_page = 1
          elif(keyboard_source == self.last_button and 
               current_page < total_elements / self.number_elements):
            # User wants to go to the last page.
            current_page = total_elements / self.number_elements + 1
          elif(keyboard_source == self.next_button and 
                current_page != (total_elements / self.number_elements) + 1):
            # User wants to go to the next page.
            current_page += 1 
          elif keyboard_source == self.previous_button and current_page != 1:
            # User wants to go to the previous page.
            current_page -= 1
          elif(self.is_number.match(keyboard_source) != None and 
              int(keyboard_source) in id_list_source):
            source_id = keyboard_source
            break
          elif keyboard_source == self.exit_button:
            self.exit_program()
          else:
            print('The option you choose is incorrect.'
                  'Please select a valid option.\n')
          start_index = self.number_elements * (current_page - 1)
        # ENd asking for source_id
        # Asking for the date.
        while True:
          keyboard = raw_input('Do you want this date '+ time.strftime("%d/%m/%Y") 
                + '?(y/n): ')
          if keyboard == 'y':
            movement_date = time.strftime("%Y/%m/%d")
            break
          elif keyboard == 'n':
            movement_date = ""
            while self.is_date.match(movement_date) == None:
              movement_date = raw_input(
                    'Introduce the date (dd/mm/yyyy or dd-mm-yyyy): ').replace(
                        '-', '/')
            if self.is_date.match(movement_date) != None:
              break
          else:
            print('Please select a valid option. ')
        # End for asking for the date.
        # Asking for income/outgoing.
        while True:
          number = raw_input('Please type a number.\n'
                +'Remember a negative number is an outgoing value and '
                + 'a positive number is an income value.\n'
                + 'Number can\'t be "0": ').replace(",", ".")
          if self.is_money.match(number) != None:
            if float(number) == 0:
              print('The number can\'t be 0')
            elif float(number) < 0 :
              outgoing = str(-float(number))
              break
            elif float(number) > 0:
              income = number
              break
          else:
            print('Please type a number and not equal to 0 '
                  '(can be either higher or lesser).')
        # End asking for income/outgoing
        self.db.new_movement(name, source_id, movement_date, income, outgoing)
        break
      elif keyboard == 'n':
        break
      else:
        print(self.yn_error_message)

  def cli_edit_movement(self):
    start_index = 0;
    current_page = 1
    total_elements = self.db.count_rows_movement()
    pag = pagination.Pagination(total_elements, self.number_elements)
    id_list = []
    movement_id = None
    name = None
    source_id = None
    income = 0
    outgoing = 0
    movement_date = ""
    movement_id = None
    edit = False

    # Asking for the movement to edit or option.
    while not edit:
      index = 0
      print('\nPlease select a movement to edit it.\n'
            'Select "' + self.back_button 
            + '" to back movement menu.\n'
            'Select "' + self.exit_button + '" to exit\n'
            'Choose a number and press enter or select other button '
            'to go to another page.\n')
      print('----------------------------------------------------------'
            '-----------')
      if total_elements > 0:
        for movement in self.db.get_all_movements(start_index, 
                                                  self.number_elements):
          print('| ID: ' + str(movement[0]) + ' | Source name: ' 
                + self.db.get_source_name(movement[1]) + ' | Name: ' 
                + movement[2] + ' | Movement date: ' 
                + self.format_date_europe(movement[3]) + ' | Income: '
                + str(movement[4]) + '| Outgoing: ' + str(movement[5]) 
                + ' |\n')
          id_list.insert(index, movement[0])
          index += 1
        print('Current page: ' + str(current_page) + '\n'
              + pag.pagination(current_page, self.first_button, 
                  self.last_button, self.previous_button, self.next_button)
            + '\n')
      else:
        prin('There aren\'t movements.')
      print('-------------------------------------------------------------'
            '---------')
      keyboard = raw_input('Choose a movement or option: ')
      # When user type something we need to check it.
      if keyboard == self.first_button and current_page > 2:
            # User wants to go to first page.
            current_page = 1
      elif(keyboard == self.last_button and 
           current_page < total_elements / self.number_elements):
        # User wants to go to the last page.
        current_page = total_elements / self.number_elements + 1
      elif(keyboard == self.next_button and 
           current_page != (total_elements / self.number_elements) + 1):
        # User wants to go to the next page.
        current_page += 1 
      elif keyboard == self.previous_button and current_page != 1:
            # User wants to go to the previous page.
            current_page -= 1
      elif(self.is_number.match(keyboard) != None and 
           int(keyboard) in id_list):
        # User type an id and it's correct.
        while True:
          # Ask if user wants to edit that movement or not
          answer = raw_input('Do you really want to edit '
                             + 'this movement?(Y/y/N/n): ').lower()
          if answer == 'y':
            # User wants to edit it.
            movement_id = keyboard
            movement_got = self.db.get_movement(movement_id)
            # Asking for the name
            print('Current name: ' + movement_got[2])
            while True:
              answer = raw_input('Do you want to change the current name?'
                                 + '(Y/y/N/n): ').lower()
              if answer == 'y':
                name = "" 
                while name == "":
                  name = raw_input('Introduce the new name: ')
                break
              elif answer == 'n':
                name = movement_got[2]
                break
              else:
                print(self.yn_error_message)
            # End asking for the name
            # Asking for the source id
            print('Current money source: ' 
                  + self.db.get_source_name(movement_got[1]))
            while True:
              index = 0
              answer = raw_input('Do you want to change the current'
                                 + ' money source?(Y/y/N/n): ').lower()
              if answer == 'y':
                start_index_source = 0
                current_page_source = 1
                total_sources = self.db.count_rows_source()
                pag_source = pagination.Pagination(total_sources, 
                                                   self.number_elements)
                print('Select a money source.\n'
                      'If you wish to exit, please press "' + self.exit_button +'"\n' 
                      'Current page: ' + str(current_page_source) + '\n'
                      + pag_source.pagination(
                                              current_page_source, 
                                              self.first_button, 
                                              self.last_button, 
                                              self.previous_button, 
                                              self.next_button))
                id_list_source = []
                print('---------------------------------------------------'
                      '------------------')
                for source in self.db.get_sources(start_index_source, 
                      self.number_elements):
                  print('| ID ' + str(source[0]) +' | Name : ' 
                        + source[1] + ' | Total: ' + str(source[2]) + ' |')
                  id_list_source.insert(index, source[0])
                  index += 1
                print('---------------------------------------------------'
                      '------------------')
                keyboard_source = raw_input("Choose a source or option: ")
                if keyboard_source == self.first_button and current_page > 2:
                  # User wants to go to first page.
                  current_page_source = 1
                elif(keyboard_source == self.last_button and 
                     current_page_source < total_sources / self.number_elements):
                  # User wants to go to the last page.
                  current_page = total_sources / self.number_elements + 1
                elif(keyboard_source == self.next_button and 
                      current_page_source != (
                                       total_sources / 
                                       self.number_elements) + 1):
                  # User wants to go to the next page.
                  current_page_source += 1 
                elif(keyboard_source == self.previous_button and 
                    current_page_source != 1):
                  # User wants to go to the previous page.
                  current_page_source -= 1
                elif(self.is_number.match(keyboard_source) != None and 
                     int(keyboard_source) in id_list_source):
                  source_id = keyboard_source
                  break
                elif keyboard_source == self.exit_button:
                  self.exit_program()
                else:
                  print('The option you choose is incorrect.'
                        'Please select a valid option.\n')
              elif answer == 'n':
                # User wants the previous source id.
                source_id = movement_got[1]
                break
              else:
                print(self.yn_error_message)
            # End asking for the source id
            # Asking for the date
            print('Current movement date: ' + self.format_date_europe(
                                                    movement_got[3]))
            while True:
              answer = raw_input('Do you want to change the '
                                 + 'current date?(Y/y/N/n): ').lower()
              if answer == 'y':
                while self.is_date.match(movement_date) == None:
                  movement_date = raw_input('Introduce the new date'
                                            + '(dd/mm/yyyy or '
                                            + 'dd-mm-yyyy) : ').replace(
                                                                    '-', '/')
                movement_date = (movement_date[6] + movement_date[7] + 
                                 movement_date[8] + movement_date[9] + 
                                 movement_date[2] + movement_date[3] + 
                                 movement_date[4] + movement_date[2] + 
                                 movement_date[0] + movement_date[1])
                break
              elif answer == 'n':
                movement_date = movement_got[3]
                break
              else:
                print(self.yn_error_message)
            # End asking for the date
            # Asking for the money value
            money = movement_got[4] if movement_got[4] > 0 else -movement_got[5]
            print(movement_got[4])
            print(-movement_got[5])
            print('Current money value (+number is income, '
                  + '-number is outgoing): ' + str(money))
            while True:
              answer = raw_input('Do you want to change the current money value?(Y/y/N/n): ')
              if answer == 'y':
                money = raw_input('Introduce the new money value '
                      + '(+number is income, '
                      + '-number is outgoing): ').replace(",", ".")
                if self.is_money.match(money) != None:
                  if money > 0:
                    income = float(money)
                    break
                  elif money < 0:
                    outgoing = -float(money)
                    break
                  elif money == 0:
                    print('Money value can\'t be 0.')
                else:
                  print('Please insert a number.')
              elif answer == 'n':
                income = movement_got[4]
                outgoing = movement_got[5]
                break
              else:
                print(self.yn_error_message)
            # End asking for the money value
            self.db.edit_movement(movement_id, name, source_id, movement_date,
                                  income, outgoing)
            edit = True
            break
          elif answer == 'n':
            # User doesn't want to edit that.
            break
          else:
            print(self.yn_error_message)
      elif keyboard in self.exit_button:
        self.exit_program()
      elif keyboard in self.back_button:
        break
      else:
        print('The option you choose is incorrect.'
              'Please select a valid option.\n')
      start_index = (1 - current_page) * self.number_elements

  def cli_delete_movement(self):
    start_index = 0;
    current_page = 1
    id_list = []
    while True:
      total_elements = self.db.count_rows_movement()
      pag = pagination.Pagination(total_elements, self.number_elements)
      index = 0
      print('Please select a movement to remove it.\n'
            'Choose a number and press enter or go to other page.\n'
            'Select "' + self.back_button 
            + '" to back movement menu.\n'
            'Select "' + self.exit_button + '" to exit\n')
      print('------------------------------------------------------------'
            '--------------------')
      for movement in self.db.get_all_movements(start_index, self.number_elements):
        print('| ID: ' + str(movement[0]) + ' | Source name: ' 
              + self.db.get_source_name(movement[1]) +' | Name: ' + movement[2]
              + ' | Movement date: ' + movement[3] + ' | Income: ' + str(movement[4])
              + ' | Outgoing: ' + str(movement[5]))
        id_list.insert(index, movement[0])
      print('------------------------------------------------------------'
            '--------------------')
      print('Current page: ' + str(current_page) + '\n'
            + pag.pagination(current_page, self.first_button, 
              self.last_button, self.previous_button, self.next_button) + '\n')
      keyboard = raw_input("Choose a movement or option: ")
      if keyboard == self.first_button and current_page > 2:
            # User wants to go to first page.
            current_page = 1
      elif(keyboard == self.last_button and 
           current_page < total_elements / self.number_elements):
        # User wants to go to the last page.
        current_page = total_elements / self.number_elements + 1
      elif(keyboard == self.next_button and 
           current_page != (total_elements / self.number_elements) + 1):
        # User wants to go to the next page.
        current_page += 1 
      elif keyboard == self.previous_button and current_page != 1:
            # User wants to go to the previous page.
            current_page -= 1
      elif(self.is_number.match(keyboard) != None and 
           int(keyboard) in id_list):
        answer = raw_input("Do you really want to delete it?(y/n): ")
        while True:
          if answer == 'y':
            self.db.delete_movement(keyboard)
            done = True
            break
          elif answer == 'n':
            break
          else:
            print('"Please type "y" or "n".')
      elif keyboard in self.exit_button:
        self.exit_program()
      elif keyboard in self.back_button:
        break
      else:
        print('The option you choose is incorrect.'
              'Please select a valid option.\n')
      start_index = (current_page - 1) * self.number_elements


  def format_date_usa(self, date):
    '''var:
      date -> the date in database format.
    Return the date with USA's format. 
    This only to Display for a user.'''
    

    return date[5] + date[6] + date[4] + date[8] + date[9] + date[4] + date[0]
    + date[1] + date[2] + date[3]

  def format_date_europe(self, date):
    '''var:
      date -> the date in database format.
    Return the date with USA's format. 
    This only to Display for a user.'''

    return date[8] + date[9] + date[4] + date[5] + date[6] + date[4] + date[0] + date[1] + date[2] + date[3]

  def exit_program(self):
    '''Exit from the program. Ask if want to exit.
    In case "y" the program will be closed, in case "n" 
    back to the last action.'''


    print('Are you sure you want to exit?(Y/y/N/n)\n')
    answer = None
    while answer != "y" and answer != "n":
      answer = raw_input('Please type "y" or "n": ').lower()
    if answer == "y":
      print("Exiting ....")
      time.sleep(1)
      exit()

def main():
  cli = CLI('Your path.')
  cli.main_menu()

if __name__ == "__main__":
  main()