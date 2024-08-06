import os.path
import subprocess
import gi
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw
from time import sleep

# VERSION = 1.0.4
ver = "1.0.4"

#=====================================================================================================
# GLOBAL VARIABLES
#=====================================================================================================
global thread
global thread_started
thread_started = False

global homedir
global topic
topic = "Main"
remove = 0
topic_edit = 0
old_topic = ""

entry_todo = Gtk.Entry()
entry_priority = Gtk.Entry()
listbox_todo = Gtk.ListBox()
hbox_topic = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
label_title = Gtk.Label()
listbox_topic = Gtk.ListBox()
box0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
box_00a = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
statusbar = Gtk.Statusbar()
entry_topic_1 = Gtk.Entry()

#=====================================================================================================
# STARTUP CHECKS
#=====================================================================================================
if not os.path.exists(os.path.expanduser("~") + "/.gtodo"):
    command = "mkdir " + os.path.expanduser("~") + "/.gtodo"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()
if not os.path.exists(os.path.expanduser("~") + "/.gtodo/Main.txt"):
    command = "touch " + os.path.expanduser("~") + "/.gtodo/Main.txt"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()
if not os.path.exists(os.path.expanduser("~") + "/.gtodo/Index.txt"):
    command = "touch " + os.path.expanduser("~") + "/.gtodo/Index.txt"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()



#=====================================================================================================
# ACCOUNT FOR DARK MODE ON MACOSX.
#=====================================================================================================
#def is_dark_mode_enabled():
#    command = 'osascript -e "tell app \\"System Events\\" to tell appearance preferences to get dark mode"'
#    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#    out, err = result.communicate()
#    out = out.strip()
#    if out == "true":
#        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)
#    else:
#        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", False)

#is_dark_mode_enabled()


#=====================================================================================================
# USER INTERFACE FUNCTIONS
#=====================================================================================================
def button_done_clicked(obj, listbox, row, label):
    global homedir
    global topic
    #print(str(obj))
    entry = label.get_text()
    #print(entry)
    listbox.remove(row)

    todo_list = ""
    with open(homedir + "/.gtodo/" + topic + ".txt") as f:
        content = f.readlines()
        for x in content:
            line = x.strip()
            line_split = line.split(";")
            if line_split[0]:
                if line_split[1] != entry:
                    todo_list = todo_list + line + "\n"

    output = homedir + "/.gtodo/" + topic + ".txt"
    new_topic_file = open(output, "w")
    new_topic_file.write(todo_list)
    new_topic_file.close()

    sleep(0.5)

    reload_lists()
    statusbar.push(0, "Todo item removed > " + entry)

def reload_lists():
    print("Reloading the todo lists.")
    listbox_todo.remove_all()
    sleep(0.5)
    hbox_todo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    listbox_todo.append(hbox_todo)

    label_todo_1 = Gtk.Button(label="Todo Items")
    # label_todo_1.set_xalign(0.0)
    label_todo_1.set_size_request(1000, 25)
    hbox_todo.append(label_todo_1)

    label_todo_2 = Gtk.Button(label="Priority")
    label_todo_2.set_size_request(170, -1)
    # label_todo_2.set_xalign(0.0)
    hbox_todo.append(label_todo_2)

    label_todo_3 = Gtk.Button(label="Done")
    label_todo_3.set_size_request(106, -1)
    hbox_todo.append(label_todo_3)

    hbox_spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    listbox_todo.append(hbox_spacer)

    seperator_2 = Gtk.Separator()
    hbox_spacer.append(seperator_2)
    sleep(0.5)
    load_todo_lists()
    entry_todo.set_text("")
    entry_todo.grab_focus()


def load_todo_lists():
    global homedir
    global topic
    print("loading todo lists.")
    homedir = os.path.expanduser("~")
    #print(homedir)
    if os.path.exists(homedir + "/.gtodo/" + topic + ".txt"):
        print("Found " + topic + ".txt")
        x = 0
        with open(homedir + "/.gtodo/" + topic + ".txt", "r") as file:
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
                        label_x_x.set_size_request(1000, -1)
                        label_x_x.set_xalign(0.0)
                        hbox_x_x.append(label_x_x)

                        entry_prio_x_x = Gtk.Entry()
                        entry_prio_x_x.set_size_request(10, -1)
                        entry_prio_x_x.set_max_length(1)
                        if topic != "Index":
                            entry_prio_x_x.set_editable(True)
                        else:
                            entry_prio_x_x.set_editable(False)
                        entry_prio_x_x.connect("activate", change_priority, label_x_x, entry_prio_x_x, row)
                        hbox_x_x.append(entry_prio_x_x)
                        entry_prio_x_x.set_text(todo_2[0])

                        button_done_x_x = Gtk.Button(label="Done")
                        button_done_x_x.set_size_request(107, -1)
                        button_done_x_x.connect("clicked", button_done_clicked, listbox_todo, row, label_x_x)
                        if topic != "Index":
                            hbox_x_x.append(button_done_x_x)


                        row.set_child(hbox_x_x)
                        listbox_todo.append(row)


def change_priority(obj, label_todo, entry_prio, row):
    global topic
    print("Changing priority.")
    todo = label_todo.get_text()
    prio = entry_prio.get_text()
    #print(todo)
    listbox_todo.remove(row)
    command = "cat " + homedir + "/.gtodo/" + topic + ".txt | grep -v \"" + todo + "\" > " + homedir + "/.gtodo/" + topic + ".txt.new"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()
    sleep(0.5)
    command = "cp " + homedir + "/.gtodo/" + topic + ".txt.new " + homedir + "/.gtodo/" + topic + ".txt; rm " + homedir + "/.gtodo/" + topic + ".txt.new"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()
    sleep(0.5)

    line = prio + ";" + todo

    file_path = homedir + "/.gtodo/" + topic + ".txt"
    with open(file_path, "a") as file:
        # Write the content to append
        file.write(line + "\n")
    sleep(1)

    command = "cat " + homedir + "/.gtodo/" + topic + ".txt | sort > " + homedir + "/.gtodo/" + topic + ".txt.new"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()
    sleep(0.5)
    command = "cp " + homedir + "/.gtodo/" + topic + ".txt.new " + homedir + "/.gtodo/" + topic + ".txt; rm " + homedir + "/.gtodo/" + topic + ".txt.new"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()
    sleep(0.5)

    reload_lists()

    statusbar.push(0, "Todo item priority changed > " + prio + " > "+ todo)


def button_todo_clicked(obj):
    global topic
    todo = entry_todo.get_text()
    prio = entry_priority.get_text()

    if entry_todo.get_text() != "" and ";" not in entry_todo.get_text() and "\"" not in entry_todo.get_text():
        print("Adding entry.")
        row = Gtk.ListBoxRow()
        hbox_todo = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label_todo = Gtk.Label(label=todo)

        label_todo.set_size_request(500, -1)
        label_todo.set_xalign(0.0)
        hbox_todo.append(label_todo)

        entry_prio_x_x = Gtk.Entry()
        entry_prio_x_x.set_size_request(10, -1)
        entry_prio_x_x.set_max_length(1)
        entry_prio_x_x.set_editable(True)
        entry_prio_x_x.connect("activate", change_priority, label_todo, entry_prio_x_x, row)
        hbox_todo.append(entry_prio_x_x)
        entry_prio_x_x.set_text(prio)

        button_done_x_x = Gtk.Button(label="Done")
        button_done_x_x.set_size_request(110, -1)
        button_done_x_x.connect("clicked", button_done_clicked, listbox_todo, row, label_todo)
        hbox_todo.append(button_done_x_x)

        row.set_child(hbox_todo)
        listbox_todo.append(row)

        line = prio + ";" + todo

        file_path = homedir + "/.gtodo/" + topic + ".txt"
        with open(file_path, "a") as file:
            # Write the content to append
            file.write(line + "\n")
        sleep(1)

        command = "cat " + homedir + "/.gtodo/" + topic + ".txt | sort > " + homedir + "/.gtodo/" + topic + ".txt.new"
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = result.communicate()
        sleep(0.5)
        command = "cp " + homedir + "/.gtodo/" + topic + ".txt.new " + homedir + "/.gtodo/" + topic + ".txt; rm " + homedir + "/.gtodo/" + topic + ".txt.new"
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = result.communicate()
        sleep(0.5)
        reload_lists()

        statusbar.push(0, "Todo item added > " + todo)


def new_topic(obj, entry):
    global topic
    global topic_edit
    global old_topic
    topic = entry.get_text()
    if topic != "" and ";" not in topic and "." not in topic and topic_edit == 0:
        if not os.path.exists(os.path.expanduser("~") + "/.gtodo/" + topic + ".txt"):
            command = "touch " + os.path.expanduser("~") + "/.gtodo/" + topic + ".txt"
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out = result.communicate()

            row = Gtk.ListBoxRow()
            label_topic = Gtk.Label(label=topic)
            row.set_child(label_topic)
            listbox_topic.append(row)
    if topic != "" and ";" not in topic and "." not in topic and topic_edit == 1 and topic != "Main":
        command = "mv " + os.path.expanduser("~") + "/.gtodo/" + old_topic + ".txt " + os.path.expanduser(
            "~") + "/.gtodo/" + topic + ".txt"
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out = result.communicate()
        topic_edit = 0
        label_topic = Gtk.Label(label=topic)

    entry.set_text("")
    listbox_topic.remove_all()
    load_topics()
    topic_changed(0, 0, 0, 0, label_topic)
    statusbar.push(0, "Created new topic.")



def load_topics():
    print("Loading topics.")
    global homedir
    global listbox_topic
    global hbox_topic
    global topic
    global remove

    row = Gtk.ListBoxRow()

    homedir = os.path.expanduser("~")
    #print("loading topics")
    command = "ls -l " + homedir + "/.gtodo/*.txt"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()
    #print(out[0])
    line = out[0].split("\n")

    listbox_topic.remove_all()
    sleep(0.5)

    x = 0

    label_topic_3 = Gtk.Label()
    label_topic_3.set_xalign(0.0)
    label_topic_3.set_text("Main")
    gesture = Gtk.GestureClick()
    gesture.connect("pressed", topic_changed, label_topic_3)
    label_topic_3.add_controller(gesture)

    row.set_child(label_topic_3)
    listbox_topic.append(row)


    while x < len(line) -1:
        name = line[x]
        topic_name = name.split("/")
        topic_real_name = topic_name[4].split(".")
        #print(topic_real_name[0])

        if topic_real_name[0] != "Main" and topic_real_name[0] != "Index":
            row = Gtk.ListBoxRow()
            label_topic = Gtk.Label()
            label_topic.set_xalign(0.0)
            label_topic.set_text(topic_real_name[0])
            gesture = Gtk.GestureClick()
            gesture.connect("pressed", topic_changed, label_topic)
            label_topic.add_controller(gesture)
            row.set_child(label_topic)
            listbox_topic.append(row)
            if topic_real_name[0] == topic:
                #print("ok")
                #print(topic_real_name[0] + str(row))
                listbox_topic.select_row(row)
        else:
            if remove == 1:
                listbox_topic.select_row(listbox_topic.get_row_at_index(0))
                remove = 0

        x = x + 1

    row = Gtk.ListBoxRow()
    label_topic_4 = Gtk.Label()
    label_topic_4.set_xalign(0.0)
    label_topic_4.set_text("Index")
    gesture1 = Gtk.GestureClick()
    gesture1.connect("pressed", show_index_of_all_items, label_topic_4)
    label_topic_4.add_controller(gesture1)

    row.set_child(label_topic_4)
    listbox_topic.append(row)




def button_topic_delete_clicked(obj):
    global topic
    global topic_title
    global remove
    remove = 1
    if topic != "Main":
        if os.path.exists(os.path.expanduser("~") + "/.gtodo/" + topic + ".txt"):
            command = "rm " + os.path.expanduser("~") + "/.gtodo/" + topic + ".txt"
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out = result.communicate()

        topic = "Main"
        label = Gtk.Label(label=topic)
        row = Gtk.ListBoxRow()

        row.set_child(label)
        listbox_topic.append(row)
        topic_changed(0, 0, 0, 0, label)
        load_topics()
        statusbar.push(0, "Topic removed.")


def topic_changed(obj, obj1, obj2, obj3, label):
    print("Topic changed.")
    global topic
    global label_title
    topic = label.get_text()
    label_title.set_text(" -> " + topic)
    reload_lists()
    statusbar.push(0, "Topic changed to: " + topic)


def button_topic_edit_clicked(obj):
    global topic
    global old_topic
    global topic_edit
    print("edit topic: " + topic)
    topic_edit = 1
    old_topic = topic
    entry_topic_1.set_text(topic)



def show_index_of_all_items(one, two, three, four, five):
    global homedir
    global topic
    topic = "Index"

    command = "cat " + homedir + "/.gtodo/*.txt | sort > " + homedir + "/.gtodo/Index.txt"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = result.communicate()
    sleep(0.5)
    listbox_todo.remove_all()
    load_todo_lists()

#=====================================================================================================
# CREATE THE USER INTERFACE
#=====================================================================================================
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Things will go here

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        # Load the CSS file
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("gtodo.css")

        # Apply the CSS to the default screen
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        win = MainWindow(application=app)
        win.set_title("gTodo " + ver)
        win.set_default_size(1920, 1000)
        win.set_resizable(True)
        global box0
        win.set_child(box0)

        seperator_5 = Gtk.Separator()
        box0.append(seperator_5)

        scrolled_window_1 = Gtk.ScrolledWindow()
        scrolled_window_1.set_size_request(400, 1000)

        box0.append(scrolled_window_1)

        global box_00a
        scrolled_window_1.set_child(box_00a)

        label_spacer_3 = Gtk.Label()
        label_spacer_3.set_size_request(-1, 17)
        box_00a.append(label_spacer_3)

        label_topic = Gtk.Button(label="TOPICS LIST")
        label_topic.set_size_request(100, -1)
        box_00a.append(label_topic)

        # Create listbox columns

        global entry_topic_1
        entry_topic_1.set_max_length(20)
        entry_topic_1.set_editable(True)
        entry_topic_1.set_placeholder_text("Add New Topic")
        entry_topic_1.connect("activate", new_topic, entry_topic_1)
        box_00a.append(entry_topic_1)

        label_topic_empty = Gtk.Label()
        label_topic_empty.set_size_request(100, 15)
        box_00a.append(label_topic_empty)

        box_00a.append(listbox_topic)

        load_topics()

        label_topic_delete_empty = Gtk.Label()
        box_00a.append(label_topic_delete_empty)

        button_topic_edit = Gtk.Button(label="Change Topic")
        button_topic_edit.connect("clicked", button_topic_edit_clicked)
        box_00a.append(button_topic_edit)

        button_topic_delete = Gtk.Button(label="Remove Topic")
        button_topic_delete.connect("clicked", button_topic_delete_clicked)
        box_00a.append(button_topic_delete)

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
        entry_todo.set_placeholder_text("New Todo Item")
        entry_todo.set_size_request(1000, -1)
        entry_todo.set_max_length(80)
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

        box_title = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_11a.append(box_title)
        box_statusbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_11a.append(box_statusbar)

        label_title.set_text(" -> " + topic)
        label_title.set_size_request(100, 35)
        label_title.set_xalign(0.0)
        box_title.append(label_title)

        label_spacer_2 = Gtk.Label()
        box_11a.append(label_spacer_2)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_size_request(700, 780)
        global listbox_todo
        box_11a.append(scrolled_window)
        scrolled_window.set_child(listbox_todo)

        # Create listbox columns

        reload_lists()

        seperator_3 = Gtk.Separator()
        box0.append(seperator_3)

        listbox_topic.select_row(listbox_topic.get_row_at_index(0))

        global statusbar
        statusbar.set_size_request(500, 30)
        box_statusbar.append(statusbar)
        statusbar.push(0, "Ready for input.")

        win.present()


#=====================================================================================================
# START THE APP
#=====================================================================================================
app = MyApp(application_id="com.sprokkel78.gtodo")
app.run(None)
