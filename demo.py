#!/usr/bin/python

import subprocess
import urwid

choices = u'Chapman Cleese Gilliam Idle Jones Palin'.split()


palette = [
    (None,  'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('focus options', 'black', 'light gray'),
    ('selected', 'white', 'dark blue')]




def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def sub_menu(caption, choices):
    contents = main_menu(caption, choices)
    def open_menu(button):
        return top.open_box(contents)
    return menu_button([caption, u'...'], open_menu)

def main_menu(title, options):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    #body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice, u'\n'])
    done = urwid.Button(u'Ok')
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
    raise urwid.ExitMainLoop()

menu_top = main_menu(u'Main Menu', [
    sub_menu(u'Applications', [
        sub_menu(u'Accessories', [
            menu_button(u'Text Editor', item_chosen),
            menu_button(u'Terminal', item_chosen),
        ]),
    ]),
    sub_menu(u'System', [
        sub_menu(u'Preferences', [
            menu_button(u'Appearance', item_chosen),
        ]),
        menu_button(u'Lock Screen', item_chosen),
    ]),
])

# frame_widget = urwid.Frame(
#     header=main_menu,
#     body=urwid.Filler(output_widget, valign='bottom'),
#     focus_part='header')


main = urwid.Padding(main_menu(u'Gina\'s DO160 Tester!', choices), left=0, right=1)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='left', width=('relative', 30),
    valign='top', height=('relative', 60),
    min_width=20, min_height=9)

main2 = urwid.Padding(main_menu(u'Sub menu', choices), left=0, right=0)
top2 = urwid.Overlay(main2, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='left', width=('relative', 100),
    valign='bottom', height=('relative', 30),
    min_width=20, min_height=9)

# loop = urwid.MainLoop(menu_top).run()

output_widget = urwid.Text("journalctl output of test: %d:\n")
header_widget = urwid.Text("journalctl output of test: %d:\n")
frame_widget = urwid.Frame(
    body=urwid.Filler(output_widget, valign='top', height='flow'),
    focus_part='header')

def received_output(data):
    output_widget.set_text(output_widget.text + data)

#write_fd = loop.watch_pipe(received_output)


placeholder = urwid.SolidFill()
loop = urwid.MainLoop(placeholder, palette=[('reversed', 'standout', '')])
write_fd = loop.watch_pipe(received_output)
dummy_cmd = ['ping', '8.8.8.8']
proc = subprocess.Popen(dummy_cmd, stdout=write_fd, close_fds=True)




loop.widget = urwid.AttrMap(placeholder, 'bg')
gina_box = urwid.BoxAdapter(top, 60)
gina_box2 = urwid.BoxAdapter(frame_widget, 60)
loop.widget.original_widget = urwid.Filler(urwid.Columns([gina_box, gina_box2]))

loop.run()
