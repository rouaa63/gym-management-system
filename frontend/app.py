import tkinter as tk
from tkinter import messagebox, ttk
import urllib.request
import urllib.parse   
import urllib.error
import json

API_URL = ""
API_KEY = ""


def api_get(path):
    req = urllib.request.Request(API_URL.rstrip("/") + path)
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read())


def api_post(path, params):
    query = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
    full_url = API_URL.rstrip("/") + path + "?" + query
    req = urllib.request.Request(
        full_url,
        data=b"",
        method="POST",
        headers={"x-api-key": API_KEY},
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read())


def api_delete(path):
    req = urllib.request.Request(
        API_URL.rstrip("/") + path,
        method="DELETE",
        headers={"x-api-key": API_KEY},
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.loads(response.read())


def connect():
    global API_URL, API_KEY
    url = url_entry.get().strip()
    key = key_entry.get().strip()

    if not url or not key:
        messagebox.showerror("Error", "Please fill in both API URL and API Key")
        return

    API_URL = url
    API_KEY = key

    try:
        api_get("/members")
    except Exception as e:
        messagebox.showerror("Connection failed", f"Could not connect:\n{e}")
        return

    connect_window.destroy()
    open_main_window()


def open_main_window():
    main = tk.Tk()
    main.title("Gym Management System")
    main.geometry("550x480")

    notebook = ttk.Notebook(main)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    members_tab = tk.Frame(notebook)
    classes_tab = tk.Frame(notebook)
    bookings_tab = tk.Frame(notebook)
    notebook.add(members_tab, text="Members")
    notebook.add(classes_tab, text="Classes")
    notebook.add(bookings_tab, text="Bookings")

    # ---------- MEMBERS TAB ----------
    tk.Label(members_tab, text="Members", font=("Arial", 14, "bold")).pack(pady=10)

    m_columns = ("name", "phone", "type", "end_date")
    m_tree = ttk.Treeview(members_tab, columns=m_columns, show="headings")
    m_tree.heading("name", text="Name")
    m_tree.heading("phone", text="Phone")
    m_tree.heading("type", text="Type")
    m_tree.heading("end_date", text="End Date")
    m_tree.pack(fill="both", expand=True, padx=20, pady=10)

    members_cache = []

    def refresh_members():
        for row in m_tree.get_children():
            m_tree.delete(row)
        try:
            members = api_get("/members")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load members:\n{e}")
            return
        members_cache.clear()
        members_cache.extend(members)
        for m in members:
            m_tree.insert("", "end", values=(m["name"], m["phone"], m["membership_type"], m["membership_end_date"]))
        refresh_member_dropdown()

    def open_add_member_form():
        form = tk.Toplevel(main)
        form.title("Add New Member")
        form.geometry("300x300")

        tk.Label(form, text="Name:").pack(anchor="w", padx=20, pady=(15, 0))
        name_entry = tk.Entry(form, width=30)
        name_entry.pack(padx=20)

        tk.Label(form, text="Phone:").pack(anchor="w", padx=20, pady=(10, 0))
        phone_entry = tk.Entry(form, width=30)
        phone_entry.pack(padx=20)

        tk.Label(form, text="Membership type:").pack(anchor="w", padx=20, pady=(10, 0))
        type_entry = tk.Entry(form, width=30)
        type_entry.insert(0, "Monthly")
        type_entry.pack(padx=20)

        tk.Label(form, text="End date (YYYY-MM-DD):").pack(anchor="w", padx=20, pady=(10, 0))
        date_entry = tk.Entry(form, width=30)
        date_entry.insert(0, "2026-12-31")
        date_entry.pack(padx=20)

        def save_member():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            mtype = type_entry.get().strip()
            end_date = date_entry.get().strip()

            if not name or not phone or not mtype or not end_date:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            try:
                api_post("/members", {
                    "name": name,
                    "phone": phone,
                    "membership_type": mtype,
                    "membership_end_date": end_date,
                })
            except Exception as e:
                messagebox.showerror("Error", f"Could not create member:\n{e}")
                return

            messagebox.showinfo("Success", "Member added!")
            form.destroy()
            refresh_members()

        tk.Button(form, text="Save", command=save_member, bg="#E5000F", fg="white", width=15).pack(pady=20)

    tk.Button(members_tab, text="+ Add Member", command=open_add_member_form, bg="#E5000F", fg="white").pack(pady=5)
    tk.Button(members_tab, text="Refresh", command=refresh_members).pack(pady=5)

    # ---------- CLASSES TAB ----------
    tk.Label(classes_tab, text="Classes", font=("Arial", 14, "bold")).pack(pady=10)

    c_columns = ("name", "trainer", "day_time", "capacity", "booked")
    c_tree = ttk.Treeview(classes_tab, columns=c_columns, show="headings")
    c_tree.heading("name", text="Name")
    c_tree.heading("trainer", text="Trainer")
    c_tree.heading("day_time", text="Day/Time")
    c_tree.heading("capacity", text="Capacity")
    c_tree.heading("booked", text="Booked")
    c_tree.pack(fill="both", expand=True, padx=20, pady=10)

    classes_cache = []

    def refresh_classes():
        for row in c_tree.get_children():
            c_tree.delete(row)
        try:
            classes = api_get("/classes")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load classes:\n{e}")
            return
        classes_cache.clear()
        classes_cache.extend(classes)
        for c in classes:
            c_tree.insert("", "end", values=(c["name"], c["trainer_name"], c["day_time"], c["capacity"], c["booking_count"]))
        refresh_class_dropdown()

    def open_add_class_form():
        form = tk.Toplevel(main)
        form.title("Add New Class")
        form.geometry("300x300")

        tk.Label(form, text="Name:").pack(anchor="w", padx=20, pady=(15, 0))
        name_entry = tk.Entry(form, width=30)
        name_entry.pack(padx=20)

        tk.Label(form, text="Trainer name:").pack(anchor="w", padx=20, pady=(10, 0))
        trainer_entry = tk.Entry(form, width=30)
        trainer_entry.pack(padx=20)

        tk.Label(form, text="Day/Time (e.g. Tue 18:00):").pack(anchor="w", padx=20, pady=(10, 0))
        daytime_entry = tk.Entry(form, width=30)
        daytime_entry.pack(padx=20)

        tk.Label(form, text="Capacity:").pack(anchor="w", padx=20, pady=(10, 0))
        capacity_entry = tk.Entry(form, width=30)
        capacity_entry.insert(0, "10")
        capacity_entry.pack(padx=20)

        def save_class():
            name = name_entry.get().strip()
            trainer = trainer_entry.get().strip()
            daytime = daytime_entry.get().strip()
            capacity = capacity_entry.get().strip()

            if not name or not trainer or not daytime or not capacity:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            try:
                api_post("/classes", {
                    "name": name,
                    "trainer_name": trainer,
                    "day_time": daytime,
                    "capacity": capacity,
                })
            except Exception as e:
                messagebox.showerror("Error", f"Could not create class:\n{e}")
                return

            messagebox.showinfo("Success", "Class added!")
            form.destroy()
            refresh_classes()

        tk.Button(form, text="Save", command=save_class, bg="#E5000F", fg="white", width=15).pack(pady=20)

    tk.Button(classes_tab, text="+ Add Class", command=open_add_class_form, bg="#E5000F", fg="white").pack(pady=5)
    tk.Button(classes_tab, text="Refresh", command=refresh_classes).pack(pady=5)

    # ---------- BOOKINGS TAB ----------
    tk.Label(bookings_tab, text="Bookings", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(bookings_tab, text="Member:").pack(anchor="w", padx=30, pady=(10, 0))
    member_var = tk.StringVar()
    member_dropdown = ttk.Combobox(bookings_tab, textvariable=member_var, state="readonly", width=40)
    member_dropdown.pack(padx=30)

    tk.Label(bookings_tab, text="Class:").pack(anchor="w", padx=30, pady=(10, 0))
    class_var = tk.StringVar()
    class_dropdown = ttk.Combobox(bookings_tab, textvariable=class_var, state="readonly", width=40)
    class_dropdown.pack(padx=30)

    def refresh_member_dropdown():
        member_dropdown["values"] = [f'{m["id"]} - {m["name"]}' for m in members_cache]

    def refresh_class_dropdown():
        class_dropdown["values"] = [f'{c["id"]} - {c["name"]} ({c["day_time"]})' for c in classes_cache]

    b_columns = ("id", "class_name", "day_time", "date")
    b_tree = ttk.Treeview(bookings_tab, columns=b_columns, show="headings")
    b_tree.heading("id", text="Booking ID")
    b_tree.heading("class_name", text="Class")
    b_tree.heading("day_time", text="Day/Time")
    b_tree.heading("date", text="Booking Date")
    b_tree.pack(fill="both", expand=True, padx=20, pady=15)

    def refresh_bookings_for_selected_member():
        for row in b_tree.get_children():
            b_tree.delete(row)
        if not member_var.get():
            return
        member_id = member_var.get().split(" - ")[0]
        try:
            bookings = api_get(f"/members/{member_id}/bookings")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load bookings:\n{e}")
            return
        for b in bookings:
            b_tree.insert("", "end", values=(b["id"], b["class_name"], b["day_time"], b["booking_date"]))

    def do_book():
        if not member_var.get() or not class_var.get():
            messagebox.showerror("Error", "Please select both a member and a class")
            return
        member_id = member_var.get().split(" - ")[0]
        class_id = class_var.get().split(" - ")[0]
        try:
            api_post("/bookings", {
                "member_id": member_id,
                "class_id": class_id,
                "booking_date": "2026-08-10",
            })
        except urllib.error.HTTPError as e:
            if e.code == 409:
                messagebox.showerror("Class full", "This class has reached its capacity.")
            else:
                messagebox.showerror("Error", f"Could not create booking:\n{e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Could not create booking:\n{e}")
            return

        messagebox.showinfo("Success", "Booking created!")
        refresh_classes()
        refresh_bookings_for_selected_member()

    def do_cancel():
        selected = b_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a booking from the list to cancel")
            return
        booking_id = b_tree.item(selected[0])["values"][0]
        try:
            api_delete(f"/bookings/{booking_id}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not cancel booking:\n{e}")
            return
        messagebox.showinfo("Success", "Booking cancelled!")
        refresh_classes()
        refresh_bookings_for_selected_member()

    btn_frame = tk.Frame(bookings_tab)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Book", command=do_book, bg="#E5000F", fg="white", width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Cancel booking", command=do_cancel, width=15).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Show my bookings", command=refresh_bookings_for_selected_member, width=15).pack(side="left", padx=5)

    refresh_members()
    refresh_classes()

    main.mainloop()


connect_window = tk.Tk()
connect_window.title("Connect to Server")
connect_window.geometry("350x220")

tk.Label(connect_window, text="Connect to Gym Management Server", font=("Arial", 11, "bold")).pack(pady=10)

tk.Label(connect_window, text="API URL:").pack(anchor="w", padx=30)
url_entry = tk.Entry(connect_window, width=35)
url_entry.insert(0, "http://localhost:8000")
url_entry.pack(padx=30, pady=(0, 10))

tk.Label(connect_window, text="API Key:").pack(anchor="w", padx=30)
key_entry = tk.Entry(connect_window, width=35, show="*")
key_entry.pack(padx=30, pady=(0, 15))

tk.Button(connect_window, text="Connect", command=connect, width=15, bg="#003C7C", fg="white").pack(pady=5)

connect_window.mainloop()
