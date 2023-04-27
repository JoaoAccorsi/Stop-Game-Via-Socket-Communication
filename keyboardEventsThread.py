import threading

class KeyboardEventsThread(threading.Thread):
    def __init__(self, conn, user_answer_dictionary, identifier, send_stop_call):
      threading.Thread.__init__(self)
      self.conn = conn
      self.stop_flag = threading.Event()
      self.user_answer_dictionary = user_answer_dictionary
      self.identifier = identifier
      self.send_stop_call = send_stop_call

    def get_should_break_input_thread(self):
      if self.stop_flag.is_set():
        return True
      else:
        return False

    def run(self):
      while True:
        if self.stop_flag.is_set():
          break

        name = input("Nome: ")
        if self.get_should_break_input_thread(): break
        self.user_answer_dictionary['name'] = name

        cep = input("CEP: ")
        if self.get_should_break_input_thread(): break
        self.user_answer_dictionary['cep'] = cep

        food = input("Comida: ")
        if self.get_should_break_input_thread(): break
        self.user_answer_dictionary['food'] = food

        object = input("Objeto: ")
        if self.get_should_break_input_thread(): break
        self.user_answer_dictionary['object'] = object

        team = input("Time de futebol: ")
        if self.get_should_break_input_thread(): break
        self.user_answer_dictionary['team'] = team
        self.send_stop_call(self.identifier)
        self.stop_flag.set()
        pass
      
      return
    
    def stop(self):
      self.stop_flag.set()
      