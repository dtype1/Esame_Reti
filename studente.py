import socket

class StudentClient:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5555  # Porta su cui il server universitario è in ascolto
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def request_available_exams(self):
        self.client_socket.send("AVAILABLE_EXAMS".encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(response)

    def request_exam_booking(self, exam_name, student_name):
        self.client_socket.send("CHECK_EXAM_AVAILABILITY {}".format(exam_name).encode("utf-8"))
        availability_response = self.client_socket.recv(1024).decode("utf-8")
        if "available" in availability_response:
            self.client_socket.send("BOOK_EXAM {} {}".format(exam_name, student_name).encode("utf-8"))
            booking_response = self.client_socket.recv(1024).decode("utf-8")
            print(booking_response)
        else:
            print("Exam {} not available.".format(exam_name))

    def close_connection(self):
        self.client_socket.close()

if __name__ == "__main__":
    student_client = StudentClient()
    student_client.connect()

    while True:
        print("\n1. Request Available Exams")
        print("2. Request Exam Booking")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            student_client.request_available_exams()
        elif choice == "2":
            exam_name = input("Enter exam name: ")
            student_name = input("Enter your name: ")
            student_client.request_exam_booking(exam_name, student_name)
        elif choice == "3":
            student_client.close_connection()
            break
        else:
            print("Invalid choice. Please try again.")
