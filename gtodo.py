import os.path
import socket
import subprocess
import sys
import gi
import threading

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gdk
from time import sleep

# VERSION = 1.0.1
ver = "1.0.1"


# GLOBAL VARIABLES
global thread
global thread_started
thread_started = False

global homedir

entry_todo = Gtk.Entry()
entry_priority = Gtk.Entry()
listbox_todo = Gtk.ListBox()

# STARTUP CHECKS

if not os.path.exists(os.path.expanduser("~") + "/.gtodo"):
    command = "mkdir " + os.path.expanduser("~") + "/.gtodo"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()
if not os.path.exists(os.path.expanduser("~") + "/.gtodo/Main.txt"):
    command = "touch " + os.path.expanduser("~") + "/.gtodo/Main.txt"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()

# ACCOUNT FOR DARK MODE.
def is_dark_mode_enabled():
    command = 'osascript -e "tell app \\"System Events\\" to tell appearance preferences to get dark mode"'
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = result.communicate()
    out = out.strip()
    if out == "true":
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)
    else:
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", False)

is_dark_mode_enabled()

def button_done_clicked(obj, listbox, row, label):
    global homedir
    #print(str(obj))
    entry = label.get_text()
    #print(entry)
    listbox.remove(row)
    command = "cat " + homedir + "/.gtodo/Main.txt | grep -v \"" + entry + "\" > " + homedir + "/.gtodo/Main.txt.new"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    command = "cp " + homedir + "/.gtodo/Main.txt.new " + homedir + "/.gtodo/Main.txt; rm " + homedir + "/.gtodo/Main.txt.new"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def load_todo_lists():
    global homedir
    print("loading todo lists")
    homedir = os.path.expanduser("~")
    #print(homedir)
    if os.path.exists(homedir + "/.gtodo/Main.txt"):
        print("Found Main.txt")
        x = 0
        with open(homedir + "/.gtodo/Main.txt", "r") as file:
            for line in file:
                if line != "\n":
                    #print(line)
                    todo_1 = line.split("\n")
                    #print(todo_1[0])
                    todo_2 = todo_1[0].split(";")
                    if len(todo_2) > 0:
                        #print(todo_2[0])
                        #print(todo_2[1])

                        hbox_x_x = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                        row = Gtk.ListBoxRow()

                        label_x_x = Gtk.Label(label=todo_2[1])
                        label_x_x.set_size_request(500, -1)
                        label_x_x.set_xalign(0.0)
                        hbox_x_x.append(label_x_x)

                        entry_prio_x_x = Gtk.Entry()
                        entry_prio_x_x.set_size_request(1, -1)
                        entry_prio_x_x.set_max_length(1)
                        hbox_x_x.append(entry_prio_x_x)
                        entry_prio_x_x.set_text(todo_2[0])

                        button_done_x_x = Gtk.Button(label="Done")
                        button_done_x_x.set_size_request(110, -1)
                        button_done_x_x.connect("clicked", button_done_clicked, listbox_todo, row, label_x_x)
                        hbox_x_x.append(button_done_x_x)

                        row.set_child(hbox_x_x)
                        listbox_todo.append(row)
def button_todo_clicked(obj):
    #print("ADD")
    todo = entry_todo.get_text()
    prio = entry_priority.get_text()

    #print(todo)
    if entry_todo.get_text() != "" and ";" not in entry_todo.get_text():
        print("adding entry")
        row = Gtk.ListBoxRow()

        hbox_todo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label_todo = Gtk.Label(label=todo)

        label_todo.set_size_request(500, -1)
        label_todo.set_xalign(0.0)
        hbox_todo.append(label_todo)

        entry_prio_x_x = Gtk.Entry()
        entry_prio_x_x.set_size_request(10, -1)
        entry_prio_x_x.set_max_length(1)
        hbox_todo.append(entry_prio_x_x)
        entry_prio_x_x.set_text(prio)

        button_done_x_x = Gtk.Button(label="Done")
        button_done_x_x.set_size_request(110, -1)
        button_done_x_x.connect("clicked", button_done_clicked, listbox_todo, row, label_todo)
        hbox_todo.append(button_done_x_x)

        row.set_child(hbox_todo)
        listbox_todo.append(row)

        line = prio + ";" + todo

        file_path = homedir + "/.gtodo/Main.txt"
        with open(file_path, "a") as file:
            # Write the content to append
            file.write(line + "\n")
        sleep(1)

        command = "cat " + homedir + "/.gtodo/Main.txt | sort > " + homedir + "/.gtodo/Main.txt.new"
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = result.communicate()
        sleep(0.5)
        command = "cp " + homedir + "/.gtodo/Main.txt.new " + homedir + "/.gtodo/Main.txt; rm " + homedir + "/.gtodo/Main.txt.new"
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = result.communicate()
        sleep(0.5)
        listbox_todo.remove_all()

        hbox_todo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        listbox_todo.append(hbox_todo)

        label_todo_1 = Gtk.Label(label=" -> Todo Items")
        label_todo_1.set_xalign(0.0)
        label_todo_1.set_size_request(500, 25)
        hbox_todo.append(label_todo_1)

        label_todo_2 = Gtk.Label(label="Priority")
        label_todo_2.set_size_request(85, -1)
        label_todo_2.set_xalign(0.0)
        hbox_todo.append(label_todo_2)

        label_todo_3 = Gtk.Label(label="Click when done")
        label_todo_3.set_size_request(80, -1)
        hbox_todo.append(label_todo_3)

        sleep(0.5)
        load_todo_lists()
        entry_todo.set_text("")
        entry_todo.grab_focus()

# CREATE THE USER INTERFACE
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Things will go here

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):

        win = MainWindow(application=app)
        win.set_title("gTodo " + ver)
        win.set_default_size(800, 500)
        win.set_resizable(False)
        box0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        win.set_child(box0)

        box_00a = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box0.append(box_00a)

        label_spacer_3 = Gtk.Label()
        label_spacer_3.set_size_request(-1, 23)
        box_00a.append(label_spacer_3)

        label_topic = Gtk.Label(label="TOPICS")
        label_topic.set_size_request(100, -1)
        box_00a.append(label_topic)

        label_spacer_4 = Gtk.Label()
        box_00a.append(label_spacer_4)

        listbox_topic = Gtk.ListBox()
        box_00a.append(listbox_topic)

        # Create listbox columns

        hbox_topic = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        listbox_topic.append(hbox_topic)

        label_topic_1 = Gtk.Label(label="Main")
        label_topic_1.set_size_request(100, 25)
        hbox_topic.append(label_topic_1)

        seperator_1 = Gtk.Separator()
        box0.append(seperator_1)

        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box0.append(box1)
        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box0.append(box2)

        box_11a = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box2.append(box_11a)

        label_spacer = Gtk.Label()
        box_11a.append(label_spacer)

        box_11b = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_11a.append(box_11b)

        global entry_todo
        entry_todo.set_placeholder_text("New Todo")
        entry_todo.set_size_request(500, -1)
        box_11b.append(entry_todo)

        global entry_priority
        entry_priority.set_placeholder_text("Priority")
        entry_priority.set_size_request(1, -1)
        entry_priority.set_max_length(1)
        entry_priority.set_text("3")
        box_11b.append(entry_priority)

        button_todo = Gtk.Button(label="Add")
        button_todo.set_size_request(110, -1)
        button_todo.connect("clicked", button_todo_clicked)
        box_11b.append(button_todo)

        label_spacer_1 = Gtk.Label()
        box_11a.append(label_spacer_1)

        box_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_11a.append(box_title)

        label_title = Gtk.Label(label="- Main -")
        label_title.set_size_request(100, -1)
        box_title.append(label_title)

        label_spacer_2 = Gtk.Label()
        box_11a.append(label_spacer_2)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_size_request(700, 400)
        global listbox_todo
        box_11a.append(scrolled_window)
        scrolled_window.set_child(listbox_todo)

        # Create listbox columns

        hbox_todo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        listbox_todo.append(hbox_todo)

        label_todo_1 = Gtk.Label(label=" -> Todo Items")
        label_todo_1.set_xalign(0.0)
        label_todo_1.set_size_request(500, 25)
        hbox_todo.append(label_todo_1)

        label_todo_2 = Gtk.Label(label="Priority")
        label_todo_2.set_size_request(85, -1)
        label_todo_2.set_xalign(0.0)
        hbox_todo.append(label_todo_2)

        label_todo_3 = Gtk.Label(label="Click when done")
        label_todo_3.set_size_request(80, -1)
        hbox_todo.append(label_todo_3)

        entry_todo.grab_focus()
        load_todo_lists()

        win.present()


# START THE APP

app = MyApp(application_id="com.sprokkel78.glanscan")
app.run(None)
