import socket

class SecretaryClient:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5555
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("Errore di connessione: il server potrebbe non essere in esecuzione o in ascolto sulla porta corretta.")
            self.client_socket = None

    def send_request(self, request):
        if self.client_socket is None:
            print("Non si riesce a connettere al server.")
            return

        self.client_socket.sendall(request.encode())

        response = self.client_socket.recv(1024)
        print(response.decode())

    def add_exam(self, exam_name):
        request = f"ADD_EXAM {exam_name}"
        self.send_request(request)

    def forward_booking_request(self, exam_name, student_name):
        request = f"BOOK_EXAM {exam_name} {student_name}"
        self.send_request(request)

    def forward_available_exams_request(self):
        request = "AVAILABLE_EXAMS"
        self.send_request(request)

    def forward_exam_availability_request(self, exam_name):
        request = f"CHECK_EXAM_AVAILABILITY {exam_name}"
        self.send_request(request)

    def close_connection(self):
        self.client_socket.close()

if __name__ == "__main__":
    secretary_client = SecretaryClient()
    secretary_client.connect()

    while True:
        print("\n1. Add Exam")
        print("2. Forward Booking Request")
        print("3. Forward Available Exams Request")
        print("4. Forward Exam Availability Request")
        print("5. Close Connection")
        choice = input("Enter your choice: ")

        if choice == "1":
            exam_name = input("Enter exam name: ")
            secretary_client.add_exam(exam_name)
        elif choice == "2":
            exam_name = input("Enter exam name: ")
            student_name = input("Enter student name: ")
            secretary_client.forward_booking_request(exam_name, student_name)
        elif choice == "3":
            secretary_client.forward_available_exams_request()
        elif choice == "4":
            exam_name = input("Enter exam name: ")
            secretary_client.forward_exam_availability_request(exam_name)
        elif choice == "5":
            secretary_client.close_connection()
            break
        else:
            print("Invalid choice. Please try again.")