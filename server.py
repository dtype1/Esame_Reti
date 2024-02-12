import socket
import threading
import random
import time

class UniversityServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5555
        self.students = {}
        self.exams = {}

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server started, listening on port", self.port)
        
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break

            if request.startswith("SECRETARY_"):
                # Inoltra la richiesta della segreteria
                self.forward_secretary_request(request)
                continue  # Salta il resto del loop per attendere la risposta

            if request.startswith("ADD_EXAM"):
                exam_name = request.split()[1]
                if exam_name not in self.exams:
                    self.exams[exam_name] = []
                    response = "Exam {} added successfully.".format(exam_name)
                else:
                    response = "Exam {} already exists.".format(exam_name)
                client_socket.send(response.encode("utf-8"))
            
            elif request.startswith("BOOK_EXAM"):
                exam_name = request.split()[1]
                student_name = request.split()[2]
                if exam_name in self.exams:
                    if student_name not in self.exams[exam_name]:
                        self.exams[exam_name].append(student_name)
                        response = "Student {} successfully booked for exam {}.".format(student_name, exam_name)
                    else:
                        response = "Student {} already booked for exam {}.".format(student_name, exam_name)
                else:
                    response = "Exam {} not found.".format(exam_name)
                client_socket.send(response.encode("utf-8"))

            elif request.startswith("AVAILABLE_EXAMS"):
                available_exams = ", ".join(self.exams.keys())
                response = "Available exams: {}".format(available_exams)
                client_socket.send(response.encode("utf-8"))

            elif request.startswith("CHECK_EXAM_AVAILABILITY"):
                exam_name = request.split()[1]
                if exam_name in self.exams:
                    response = "Exam {} is available.".format(exam_name)
                else:
                    response = "Exam {} not found.".format(exam_name)
                client_socket.send(response.encode("utf-8"))

        client_socket.close()

    def forward_secretary_request(self, request):
        secretary_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secretary_socket.connect((self.host, self.port + 1))  # Assumendo che il server della segreteria sia in ascolto sulla porta 5555
        secretary_socket.send(request.encode("utf-8"))
        response = secretary_socket.recv(1024).decode("utf-8")
        print("Secretary response:", response)
        secretary_socket.close()

if __name__ == "__main__":
    server = UniversityServer()
    server.start()
