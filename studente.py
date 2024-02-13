import socket
#Classe per gestire il client studente
class StudentClient:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5555  # Porta su cui il server universitario è in ascolto
        self.client_socket = None

    #Metodo per connettersi al server universitario 
    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    #Metodo per richiedere gli esami disponibili al server universitario 
    def request_available_exams(self):
        self.client_socket.send("AVAILABLE_EXAMS".encode("utf-8")) #Invia la richiesta degli esami disponibili
        response = self.client_socket.recv(1024).decode("utf-8") #Riceve la risposta dal server
        print(response)

    #Metodo per richiedere la prenotazione di un esame al server universitario
    def request_exam_booking(self, exam_name, student_name):
        #Invia la richiesta per verificare la disponibilità dell'esame al server
        self.client_socket.send("CHECK_EXAM_AVAILABILITY {}".format(exam_name).encode("utf-8"))
        availability_response = self.client_socket.recv(1024).decode("utf-8") #Riceve la risposta dal server
        if "available" in availability_response:
            #Se l'esame è disponibile , invia la richiesta di prenotazione 
            self.client_socket.send("BOOK_EXAM {} {}".format(exam_name, student_name).encode("utf-8"))
            booking_response = self.client_socket.recv(1024).decode("utf-8") #Riceve la risposta dal server
            print(booking_response)
        else:
            print("Exam {} not available.".format(exam_name))
    #Metodo per chiudere la connessione al server 
    def close_connection(self):
        self.client_socket.close() #Chiude il socket del client 

if __name__ == "__main__":
    student_client = StudentClient()
    student_client.connect() #Connessione al server 

    while True:
        print("\n1. Request Available Exams")
        print("2. Request Exam Booking")
        print("3. Exit")
        choice = input("Enter your choice: ") #Richiede all'utente di inserire una scelta 

        if choice == "1":
            student_client.request_available_exams() #Richiede gli esami disponibili 
        elif choice == "2":
            exam_name = input("Enter exam name: ")
            student_name = input("Enter your name: ")
            student_client.request_exam_booking(exam_name, student_name) #Richiede la prenotazione dell'esame 
        elif choice == "3":
            student_client.close_connection() #Chiude la connessione al server 
            break #Esce dal ciclo while
        else:
            print("Invalid choice. Please try again.")
