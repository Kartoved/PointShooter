import keyboard
import pyautogui
import json
import pygame
import PySimpleGUI as sg
import time

pygame.init()
s = pygame.mixer.Sound('screenshot.wav')  # звук скриншота

# подгрузка параметров из файла JSON
try:
    with open('parametrs.json') as f:
        parametrs = json.load(f)
except:
    parametrs = {"x": 0, "y": 0, "width": 300, "height": 300,
                 "counter": 1, "folder": "screenshots", "hotkey": 'alt+s'}
counter = parametrs["counter"]
folder = parametrs["folder"]


# прочие настройки

sg.theme('dark')
sg.SetOptions(font=('Calibry', 14),
              icon='sniper.ico')
menu_def = [['Настройки', ['Параметры скриншота', 'Настройка хоткея']],
            ['О программе', 'Как пользоваться программой']
            ]
text_about = '''Для создания скриншота нажмите на кнопку НАЖМИ МЕНЯ или используйте горячую клавишу.
Данная программа требует дополнительной настройки под ваш экран. Настройки можно найти в меню "Настройки"'''
text_hotkey = '''Вы можете выбрать сочетание из двух клавиш 
либо одну клавишу. 
Слева выберите первую клавишу,
справа напечайте вторую на английской раскладке.
Для второго варинта выберите "Без кнопки".
Регистр букв неважен.'''


# функции создания окон
def make_window_options():
    '''создание окна настроек'''
    layout = [[sg.Text('Введите необходимые значения в ячейки.\nИспользуйте ТОЛЬКО цифры (кроме последнего пункта)\nВыберите папку, куда будут сохряняться скриншоты')],
              [sg.Text('x', size=(7)), sg.Input(
                  size=(4), key='x', default_text=parametrs["x"])],
              [sg.Text('y', size=(7)), sg.Input(
                  size=(4), key='y', default_text=parametrs["y"])],
              [sg.Text('ширина', size=(7)), sg.Input(
                  size=(4), key='width', default_text=parametrs["width"])],
              [sg.Text('высота', size=(7)), sg.Input(
                  size=(4), key='height', default_text=parametrs["height"])],
              [sg.Text('счётчик', size=(7)), sg.Input(
                  size=(4), key='counter', default_text=parametrs["counter"])],
              [sg.FolderBrowse('выберите папку'), sg.Input(
                  size=40, key='folder', default_text=parametrs["folder"])],
              [sg.Button("принять изменения", size=20,
                         button_color='blue', border_width=4)]
              ]
    return sg.Window('Параметры скриншота', layout, finalize=True, return_keyboard_events=True, size=(600, 350))


def make_main_window():
    '''создание основного окна'''
    layout = [
        [sg.Menu(menu_def)],
        [sg.Button('нажми меня', pad=(20, 10), size=40, border_width=2)],
        [sg.Text('      чтобы сделать скрин', key='ALERT')]
    ]
    return sg.Window('Point shooter', layout, size=(270, 100), finalize=True, return_keyboard_events=True)


def make_hotkey_window():
    '''создаёт окно назначения горячей клавиши'''
    layout = [[sg.Text(text_hotkey)],
              [sg.Radio('Без кнопки', group_id=1, key='none',
                        default=parametrs["hotkey_dict"]["none"])],
              [sg.Radio('alt', group_id=1, key='alt',
                        default=parametrs["hotkey_dict"]["alt"])],
              [sg.Radio('ctrl', group_id=1, key='ctrl', default=parametrs["hotkey_dict"]["ctrl"]),
               sg.Input(key='hotkey2', pad=(50, 0), size=3, default_text="s")],
              [sg.Radio('shift', group_id=1, key='shift',
                        default=parametrs["hotkey_dict"]["shift"])],
              [sg.Button('сохранить')]
              ]
    return sg.Window('настройка хоткея', layout, finalize=True, size=(500, 300), return_keyboard_events=True,)


def choose_hotkey():
    '''настройка горячей клавиши'''
    if values['alt']:
        parametrs['hotkey'] = 'alt+' + window['hotkey2'].get()
        parametrs["hotkey_dict"]["none"] = False
        parametrs["hotkey_dict"]["alt"] = True
        parametrs["hotkey_dict"]["ctrl"] = False
        parametrs["hotkey_dict"]["shift"] = False
    elif values['ctrl']:
        parametrs['hotkey'] = 'ctrl+' + window['hotkey2'].get()
        parametrs["hotkey_dict"]["none"] = False
        parametrs["hotkey_dict"]["alt"] = False
        parametrs["hotkey_dict"]["ctrl"] = True
        parametrs["hotkey_dict"]["shift"] = False
    elif values['shift']:
        parametrs['hotkey'] = 'shift+' + window['hotkey2'].get()
        parametrs["hotkey_dict"]["none"] = False
        parametrs["hotkey_dict"]["alt"] = False
        parametrs["hotkey_dict"]["ctrl"] = False
        parametrs["hotkey_dict"]["shift"] = True
    else:
        parametrs['hotkey'] = window['hotkey2'].get()
        parametrs["hotkey_dict"]["none"] = True
        parametrs["hotkey_dict"]["alt"] = False
        parametrs["hotkey_dict"]["ctrl"] = False
        parametrs["hotkey_dict"]["shift"] = False
    keyboard.add_hotkey(parametrs["hotkey"], make_screenshot, suppress=False)
    with open('parametrs.json', 'w') as f:
        json.dump(parametrs, f)


def make_screenshot():
    global counter
    counter = int(parametrs["counter"])
    screenshot = pyautogui.screenshot(f"{folder}/{str(counter)}.png", region=(
        parametrs["x"], parametrs["y"], parametrs["width"], parametrs["height"]))
    counter += 1
    s.play()
    main_window['ALERT'].update(value=f"Сделан скриншот  {str(counter)}.png")
    update_counter()
    time.sleep(1)


def update_parametrs():
    '''обновление настроек'''
    try:
        parametrs["x"] = int(win_options["x"].get())
        parametrs["y"] = int(win_options["y"].get())
        parametrs["width"] = int(win_options["width"].get())
        parametrs["height"] = int(win_options["height"].get())
        parametrs["counter"] = int(win_options["counter"].get())
        win_options.close()
    except:
        sg.Popup('Используйте только цифры!!!', font=('Arial', 14, 'italic'))
    parametrs['folder'] = win_options["folder"].get()
    with open('parametrs.json', 'w') as f:
        json.dump(parametrs, f)


def update_counter():
    '''обновление счётчика'''
    parametrs["counter"] = counter
    with open('parametrs.json', 'w') as f:
        json.dump(parametrs, f)


# создаем главное окно, окно настроек пока выключено
main_window, win_options = make_main_window(), None
keyboard.add_hotkey(parametrs["hotkey"], make_screenshot, suppress=False)

# основной цикл
while True:
    window, event, values = sg.read_all_windows()
    # print(event, values)
    if event == 'нажми меня':
        make_screenshot()
    elif event == 'Параметры скриншота':
        win_options = make_window_options()
    elif event == 'принять изменения':
        update_parametrs()
    elif event == 'Как пользоваться программой':
        sg.popup('Как пользоваться программой',
                 text_about, font=('Arial', 14, 'italic'))
    elif event == 'Настройка хоткея':
        win_hotkey = make_hotkey_window()
    elif event == 'сохранить':
        choose_hotkey()
        win_hotkey.close()
    elif event == sg.WIN_CLOSED:
        window.close()
        if window == win_options:       # if closing win 2, mark as closed
            win_options = None
        elif window == main_window:     # if closing win 1, exit program
            break
window.close()


# TODO сделай нормальную фавиконку
# TODO сделать обновление
