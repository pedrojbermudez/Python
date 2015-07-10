class Pagination():
  def __init__(self, total_elements, elements_per_page):
    self.total_elements = total_elements
    if total_elements <= elements_per_page:
      self.total_pages = 1
    else:
      self.total_pages = (self.total_elements / elements_per_page) + 1
  def pagination(
    self, current_page, first_button, last_button, previous_button, 
    next_button):
    '''Return a string with the pagination.
      You must check what does the user.'''
    string = ''

    #Check total pages.
    if self.total_pages == 1:
      return string
    else:
      if current_page == 1:
        string += 'Press ' + next_button + ' to go to the next page.\n'
        if self.total_pages > 2:
          string +='Press ' + last_button + ' to go to the last page(' + str(self.total_pages) + ')\n.'
      if current_page > 1:
        if self.total_pages > 2 and current_page > 2:
          string += 'Press ' + first_button + ' to go to the first page\n'
        string += 'Press ' + previous_button + ' to go to ' + str((current_page - 1)) + '\n'
        if current_page < self.total_pages:
          print(str(current_page) + "<- current_page")
          print(str(self.total_pages) + "<- total_pages")
          string += 'Press ' + next_button + ' to go to ' + str(current_page + 1) + '\n'
        if current_page < self.total_pages - 1 and self.total_pages >= 3:
          string += 'Press ' + last_button + ' to go to the last page (' + str(self.total_pages) +')\n'
      elif current_page == self.total_pages:
        string += 'Press ' + first_button + ' to go to the first page\n'+ 'Press ' + previous_button + ' to go to ' + str((current_page - 1)) + '\n'
      return string