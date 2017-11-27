import urwid
import subprocess
from ScrollText import ExtendedText
import consts


class MenuButton(urwid.Button):
    def __init__(self, caption, callback):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')


class SubMenu(urwid.WidgetWrap):
    def __init__(self, caption, choices):
        super(SubMenu, self).__init__(MenuButton(
            [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
        line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.AttrMap(urwid.Text([u"\n  ", caption]), 'heading'),
            urwid.AttrMap(line, 'line'),
            urwid.Divider()] + choices + [urwid.Divider()]))
        self.menu = urwid.AttrMap(listbox, 'options')

    def open_menu(self, button):
        menu.open_box(self.menu)


class Choice(urwid.WidgetWrap):
    def __init__(self, caption):
        super(Choice, self).__init__(
            MenuButton(caption, self.item_chosen))
        self.caption = caption

    def item_chosen(self, button):
        if self.caption == u'Exit':
            exit_program("Q")
 #       response = urwid.Text([u'  You chose ', self.caption, u'\n'])
 #       done = MenuButton(u'Ok', exit_program)
 #       response_box = urwid.Filler(urwid.Pile([response, done]))
 #       menu.open_box(urwid.AttrMap(response_box, 'options'))
        for command in consts.RUN_CMD:
            if self.caption == command['title']:
                subprocess_command(command=command['bash_cmd'])
        else:
            print("command not found")


class HorizontalBoxes(urwid.Columns):
    def __init__(self):
        super(HorizontalBoxes, self).__init__([], dividechars=1)

    def open_box(self, box):
        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append((urwid.AttrMap(box, 'options', focus_map),
            self.options('given', 45)))
        self.focus_position = len(self.contents) - 1


main_menu = SubMenu(u'ATP Test App', [
    SubMenu(u'WTF', [
        Choice(u'Run Wtf Cmd'),
        Choice(u'Help on Wtf'),
        Choice(u'Exit'),
    ]),
    SubMenu(u'Aircard Controller PSoc Ver', [
        Choice(u'Run PSoc Ver Test'),
        Choice(u'Help on PSoc Ver'),
        Choice(u'Exit'),
    ]),
    SubMenu(u'DC Voltage Check', [
        Choice(u'Run DC Voltage Test'),
        Choice(u'Help on DC Voltage Test'),
        Choice(u'Exit'),
    ]),
    SubMenu(u'ARINC429 Loopback Test', [
        Choice(u'Run A429 Loopback Test'),
        Choice(u'Help on A429 Loopback'),
        Choice(u'Exit'),
    ]),
    SubMenu(u'Run Automated ATP', [
        Choice(u'Run full ATP'),
        Choice(u'Help on ATP'),
        Choice(u'Exit'),
    ]),
    Choice(u'Exit'),
])

palette = [
    (None,  'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('focus options', 'black', 'light gray'),
    ('selected', 'white', 'dark red')]
focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}


def exit_program(key):
    raise urwid.ExitMainLoop()


def received_output(data):
    output_widget.set_text(output_widget.text + data)
#    urwid.connect_signal(output_widget, 'changed', output_widget.set_auto_scroll)


def subprocess_command(command):
    subprocess.Popen(command, stderr=write_fd, stdout=write_fd, close_fds=True)


if __name__ == "__main__":
    output_widget = ExtendedText("journalctl output of test:\n\n")
    subprocess_widget = urwid.Frame(
        body=urwid.Filler(output_widget, valign='top', height='flow'),
        focus_part='body')
    menu = HorizontalBoxes()
    menu.open_box(main_menu.menu)
    menu_frame = urwid.BoxAdapter(menu, 90)
    subprocess_frame = urwid.BoxAdapter(subprocess_widget, 200)

    placeholder = urwid.DARK_BLUE
    loop = urwid.MainLoop(placeholder, palette=palette)
    write_fd = loop.watch_pipe(received_output)

    loop.widget = urwid.AttrMap(placeholder, 'bg')

    loop.widget.original_widget = urwid.Filler(urwid.Columns([menu_frame, subprocess_frame]))
    loop.run()
