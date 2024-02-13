import socket  # Importa il modulo socket per la comunicazione di rete
import time  # Importa il modulo time per gestire il tempo

class SecretaryClient:
    def __init__(self):
        # Inizializza l'indirizzo IP del server e la porta su cui connettersi
        self.host = "127.0.0.1"
        self.port = 5555
        # Inizializza il socket del client e il contatore di tentativi di connessione
        self.client_socket = None
        self.connection_attempts = 0
        # Inizializza il contatore di prenotazioni a 0
        self.booking_counter = 0

    def connect(self):
        # Funzione per connettersi al server, con un massimo di 3 tentativi
        while self.connection_attempts < 3:
            try:
                # Crea un socket TCP per il client e tenta la connessione al server
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.port))
                self.connection_attempts = 0  # Reimposta il contatore dei tentativi di connessione
                break  # Esce dal ciclo while se la connessione è riuscita
            except socket.error:
                # Incrementa il contatore dei tentativi e attende un tempo crescente prima di riprovare
                self.connection_attempts += 1
                print(f"Connection attempt {self.connection_attempts} failed. Retrying...")
                time.sleep(2**self.connection_attempts)
        else:
            # Se tutti i tentativi di connessione falliscono, mostra un messaggio di errore e chiude il socket del client
            print("Connection attempts failed. Exiting...")
            self.client_socket.close()
            self.client_socket = None

    def send_request(self, request):
        # Funzione per inviare una richiesta al server tramite il socket del client
        if self.client_socket is None:
            print("Client not connected to server.")
            return

        # Invia la richiesta al server tramite il socket del client e riceve la risposta
        self.client_socket.sendall(request.encode())
        response = self.client_socket.recv(1024)
        print(response.decode())

        # Chiude il socket del client dopo l'invio della richiesta e la ricezione della risposta
        if self.client_socket is not None:
            self.client_socket.close()
            self.client_socket = None

    def add_exam(self, exam_name):
        # Metodo per aggiungere un nuovo esame alla lista degli esami disponibili
        request = f"ADD_EXAM {exam_name}"  # Costruisce la richiesta con il nome dell'esame
        self.connect()  # Connessione al server
        self.send_request(request)  # Invia la richiesta al server

    def forward_booking_request(self, exam_name, student_name):
        # Metodo per inoltrare una richiesta di prenotazione di un esame alla segreteria
        self.booking_counter += 1  # Incrementa il contatore di prenotazioni
        request = f"BOOK_EXAM {exam_name} {student_name} {self.booking_counter}"  # Costruisce la richiesta con i dettagli della prenotazione
        self.connect()  # Connessione al server
        self.send_request(request)  # Invia la richiesta al server

    def forward_available_exams_request(self):
        # Metodo per inoltrare una richiesta degli esami disponibili alla segreteria
        request = "AVAILABLE_EXAMS"  # Costruisce la richiesta per ottenere gli esami disponibili
        self.connect()  # Connessione al server
        self.send_request(request)  # Invia la richiesta al server

    def forward_exam_availability_request(self, exam_name):
        # Metodo per inoltrare una richiesta sulla disponibilità di un esame alla segreteria
        request = f"CHECK_EXAM_AVAILABILITY {exam_name}"  # Costruisce la richiesta con il nome dell'esame
        self.connect()  # Connessione al server
        self.send_request(request)  # Invia la richiesta al server

    def close_connection(self):
        # Metodo per chiudere la connessione con il server
        if self.client_socket is not None:
            # Chiude il socket del client se è attivo
            self.client_socket.close()
            self.client_socket = None

if __name__ == "__main__":
    # Codice principale
    secretary_client = SecretaryClient()  # Crea un'istanza del client della segreteria

    while True:
        # Menu 
        print("\n1. Add Exam")
        print("2. Forward Booking Request")
        print("3. Forward Available Exams Request")
        print("4. Forward Exam Availability Request")
        print("5. Close Connection")
        choice = input("Enter your choice: ")  # Richiede all'utente di inserire la scelta

        if choice == "1":
            # Aggiunge un nuovo esame alla lista degli esami disponibili
            exam_name = input("Enter exam name: ")
            secretary_client.add_exam(exam_name)
        elif choice == "2":
            # Inoltra una richiesta di prenotazione di un esame alla segreteria
            exam_name = input("Enter exam name: ")
            student_name = input("Enter student name: ")
            secretary_client.forward_booking_request(exam_name, student_name)
        elif choice == "3":
            # Inoltra una richiesta degli esami disponibili alla segreteria
            secretary_client.forward_available_exams_request()
        elif choice == "4":
            # Inoltra una richiesta sulla disponibilità di un esame alla segreteria
            exam_name = input("Enter exam name :")
            secretary_client.forward_exam_availability_request(exam_name)
        elif choice == "5":
            # Chiude la connessione con il server e esce dal programma
            secretary_client.close_connection()
            break
        else:
            # Gestisce una scelta non valida dall'utente
            print("Invalid choice. Please try again.")
