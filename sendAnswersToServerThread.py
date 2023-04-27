import threading
import pickle

class SendAnswersToServerThread(threading.Thread):
    def __init__(self, conn, send_users_answers, listen_to_keyboard_thread, identifier):
      threading.Thread.__init__(self)
      self.conn = conn
      self.stop_flag = threading.Event()
      self.send_users_answers = send_users_answers
      self.listen_to_keyboard_thread = listen_to_keyboard_thread
      self.identifier = identifier

    def run(self):
      while True:
        if self.stop_flag.is_set():
          break
        new_received_data = self.conn.recv(4096)
        data = pickle.loads(new_received_data)
        data_event = data['event']
        data_identifier = data['finish_first_identifier']
        if (data_event == "send_answers"):
          if (data_identifier != self.identifier):
            print("\nO outro cliente terminou! Pressione enter para ver os resultados")
            self.listen_to_keyboard_thread.stop()
          self.send_users_answers()
          self.stop_flag.set()
          pass
    
    def stop(self):
      self.stop_flag.set()