import socket  # Importa il modulo socket per la comunicazione di rete
import threading  # Importa il modulo threading per gestire più connessioni contemporaneamente
import random  # Importa il modulo random per la generazione casuale
import time  # Importa il modulo time per gestire il tempo

class UniversityServer:
    def __init__(self):
        # Inizializza l'indirizzo IP del server e la porta su cui ascoltare
        self.host = "127.0.0.1"
        self.port = 5555
        # Dizionario per memorizzare gli studenti prenotati e gli esami disponibili
        self.students = {}
        self.exams = {}
        # Contatore per il numero progressivo di prenotazioni
        self.booking_counter = 0

    def start(self):
        # Crea un socket TCP per il server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Associa il socket all'indirizzo e alla porta del server
        self.server_socket.bind((self.host, self.port))
        # Avvia l'ascolto del socket con un massimo di 5 connessioni in coda
        self.server_socket.listen(5)
        print("Server started, listening on port", self.port)

        while True:
            # Accetta la connessione del client e restituisce una tupla (socket_cliente, indirizzo_cliente)
            client_socket, client_address = self.server_socket.accept()
            # Avvia un thread per gestire la connessione del client
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            # Riceve la richiesta del client e la decodifica da UTF-8
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break

            if request.startswith("BOOK_EXAM"):
                # Gestisce la richiesta di prenotazione di un esame da parte dello studente
                exam_name = request.split()[1]
                student_name = request.split()[2]
                if exam_name in self.exams:
                    if student_name not in self.exams[exam_name]:
                        # Incrementa il contatore delle prenotazioni e aggiunge lo studente all'esame
                        self.booking_counter += 1
                        self.exams[exam_name].append(student_name)
                        # Crea la risposta con il numero di prenotazione progressivo
                        response = "Student {} successfully booked for exam {}. Booking number: {}.".format(student_name, exam_name, self.booking_counter)
                    else:
                        response = "Student {} already booked for exam {}.".format(student_name, exam_name)
                else:
                    response = "Exam {} not found.".format(exam_name)
                # Invia la risposta al client dopo la codifica in UTF-8
                client_socket.send(response.encode("utf-8"))
                
            elif request.startswith("SECRETARY_"):
                # Inoltra la richiesta della segreteria
                self.forward_secretary_request(request)
                continue

            elif request.startswith("ADD_EXAM"):
                # Aggiunge un nuovo esame alla lista degli esami disponibili
                exam_name = request.split()[1]
                if exam_name not in self.exams:
                    self.exams[exam_name] = []
                    response = "Exam {} added successfully.".format(exam_name)
                else:
                    response = "Exam {} already exists.".format(exam_name)
                client_socket.send(response.encode("utf-8"))

            elif request.startswith("AVAILABLE_EXAMS"):
                # Invia al client l'elenco degli esami disponibili
                available_exams = ", ".join(self.exams.keys())
                response = "Available exams: {}".format(available_exams)
                client_socket.send(response.encode("utf-8"))

            elif request.startswith("CHECK_EXAM_AVAILABILITY"):
                # Verifica la disponibilità di un esame specifico
                exam_name = request.split()[1]
                if exam_name in self.exams:
                    response = "Exam {} is available.".format(exam_name)
                else:
                    response = "Exam {} not found.".format(exam_name)
                client_socket.send(response.encode("utf-8"))

        # Chiude il socket del client dopo aver terminato la comunicazione
        client_socket.close()

    def forward_secretary_request(self, request):
        # Crea un socket per la connessione alla segreteria
        secretary_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connessione al server della segreteria, presumibilmente sulla porta successiva a quella del server universitario
        secretary_socket.connect((self.host, self.port + 1))
        # Invia la richiesta alla segreteria dopo la codifica in UTF-8
        secretary_socket.send(request.encode("utf-8"))
        # Riceve la risposta dalla segreteria e la decodifica da UTF-8
        response = secretary_socket.recv(1024).decode("utf-8")
        print("Secretary response:", response)
        # Chiude il socket della segreteria dopo aver terminato la comunicazione
        secretary_socket.close()

if __name__ == "__main__":
    # Crea un'istanza del server universitario e avvia il server
    server = UniversityServer()
    server.start()
