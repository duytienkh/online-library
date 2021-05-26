import os.path as path
import tkinter as tk
import xml.dom.minidom as minidom
import xml.etree.ElementTree as et


def show(login_gui):
    login_gui.withdraw()
    gui = tk.Toplevel(login_gui)
    gui.title("Server config")
    f = tk.Frame(gui)
    addr = tk.Entry(f)
    addr.insert(0, "Address")
    addr.pack(side=tk.LEFT)
    port = tk.Entry(f)
    port.insert(0, "Port")
    port.pack(side=tk.LEFT)
    load(addr, port)
    f.pack()

    save_btn = tk.Button(gui, text="Save")
    save_btn.pack()
    save_btn.config(command=lambda: save(on_closing, addr.get(), port.get()))

    def on_closing():
        gui.destroy()
        login_gui.deiconify()

    gui.protocol("WM_DELETE_WINDOW", on_closing)
    gui.mainloop()


def load(a, p):
    if not path.isfile("config.xml"):
        save(lambda: None, "127.0.0.1", "55555")
    doc = minidom.parse("config.xml")
    addr = doc.getElementsByTagName("address")[0].attributes["value"].value
    a.delete(0, tk.END)
    a.insert(0, addr)
    port = doc.getElementsByTagName("port")[0].attributes["value"].value
    p.delete(0, tk.END)
    p.insert(0, port)


def save(func, a, p):
    config = et.Element("config")
    addr = et.SubElement(config, "address")
    port = et.SubElement(config, "port")
    addr.set("value", a)
    port.set("value", p)
    data = et.tostring(config, encoding='unicode', method='xml')
    f = open("config.xml", "w")
    f.write(data)
    f.close()
    func()
