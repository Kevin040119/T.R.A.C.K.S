import tkinter as tk
import MySQLdb
import threading
from PIL import Image, ImageTk

def Interface(IDkereta):
    j = 0
    def display_seat_availability():
        # Membuat fungsi untuk memperbarui tampilan
        def update_display():
            # Menghapus semua widget pada window
            for widget in window.winfo_children():
                widget.destroy()
            
            # Koneksi ke database
            connection = MySQLdb.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="project"
            )
            
            # Membuat kursor
            cursor = connection.cursor()
            
            # Query untuk mengambil data tempat duduk
            query = "SELECT * FROM trains WHERE train_id = "+str(IDkereta)
            cursor.execute(query)
            
            seat_map = {}
            
            # Mengambil hasil query
            rows = cursor.fetchall()
            
            for row in rows:
                carriage = row[2]
                seat = row[3]
                availability = row[4]
                
                if carriage not in seat_map:
                    seat_map[carriage] = {}
                
                seat_map[carriage][seat] = availability
            
            for carriage, seats in seat_map.items():
                #carriage_frame = tk.LabelFrame(window, text="Gerbong " + str(carriage), bg="white")
                carriage_frame = tk.LabelFrame(window, text="Stasiun KRL Cisauk" , bg="white")
                carriage_frame.pack(pady=10)
                
                for seat, availability in seats.items():
                    frame = tk.Frame(carriage_frame, bg="white")
                    frame.pack(side="left", padx=5)

                    seat_label = tk.Label(frame, text="Gerbong " + seat + ":", width=15, anchor="w", bg="white")
                    seat_label.pack()

                    availability_label = tk.Label(frame, text="", width=10, height=5, anchor="w", relief="solid", bg="#00ff00" if availability > 0 else "#ff0000", fg="white")
                    availability_label.pack()

                    availability_text = tk.Label(frame, text="      Capacity: " + str(availability), width=15, anchor="w", bg="white")
                    availability_text.pack()

                separator = tk.Frame(window, height=1, bd=1, relief="groove", bg="white")
                separator.pack(fill="x", padx=10, pady=5)
                            
            # Menutup kursor dan koneksi database
            cursor.close()
            connection.close()
            
            # Perbarui tampilan setiap ? detik
            window.after(500, update_display)
        
        # Membuat window Tkinter
        window = tk.Tk()
        window.title("Ketersediaan Tempat Duduk")
        
        # Memulai pembaruan tampilan
        update_display()
        
        window.mainloop()

    # Menampilkan ketersediaan tempat duduk secara real-time
    display_seat_availability()





def get_value():
    value = entry.get()
    ID_kereta = value
    #root.quit()
    #cv2.startWindowThread()
    Interface(value)

root = tk.Tk()
# Atur ukuran jendela
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = int((screen_width / 2) - (window_width / 2))
y_position = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Tambahkan gambar
image_path = "gambar.jpg"  
image = Image.open(image_path)
image = image.resize((300, 150))  
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.pack()

label = tk.Label(root, text="Masukkan ID kereta:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Submit", command=get_value)
button.pack()
root.mainloop()
