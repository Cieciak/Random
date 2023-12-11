import networking
import threading
import tkinter
import time

if __name__ == '__main__':
    ADDRESS = networking.Address('127.0.0.1', 20001)
    SERVER  = networking.Server(ADDRESS)

    USER_SET = set()
    CARDS = []

    PACKS = []

    root = tkinter.Tk()
    var = tkinter.StringVar(root, '', 'input')
    set_var = tkinter.StringVar(root, '', 'set')
    card_var = tkinter.StringVar(root, '', 'card')

    @SERVER.command('CONSOLE')
    def console(ctx: networking.Server, address: networking.Address, body: str):
        print(body)

    @SERVER.command('RESPONSE')
    def response(ctx: networking.Server, address: networking.Address, body: str):
        #print(f'Response from [{address.host}:{address.port}]: {body}')
        PACKS.append(body)

    @SERVER.command('ADD-TO-SET')
    def add_to_set(ctx: networking.Server, address: networking.Address, body: str):
        global USER_SET
        USER_SET = USER_SET.union(int(n) for n in body.split(' '))
        print(USER_SET)

    @SERVER.command('ADD-CARD')
    def add_card(ctx: networking.Server, address: networking.Address, body: str):
        global CARDS
        CARDS.append(body)

    set_label = tkinter.Label(root, textvariable=set_var)
    set_label.grid(column=1, row= 0)

    card_label = tkinter.Label(root, textvariable=card_var)
    card_label.grid(column=2, row=0)

    def loop():
        while True:
            if PACKS:
                print(PACKS)
                msg, n = PACKS.pop(0).split(' ')
                print(msg)

                label = tkinter.Label(root, text=msg)
                label.grid(row = int(n))
            set_var.set(f'{USER_SET}')
            card_var.set(f'{CARDS}')
            time.sleep(1/60)

            
            
                
    t = threading.Thread(
        target=loop,
        daemon = True,
    )
    t.start()

    SERVER.serve()



    button = tkinter.Button(root, text='A', command=lambda: SERVER.send(bytes(var.get(), 'UTF-8'), networking.Address('127.0.0.1', 20000)))
    button.grid()

    entry = tkinter.Entry(root, textvariable=var)
    entry.grid()

    SERVER.send(bytes('MAKE-ROOM test','UTF-8'), networking.Address('127.0.0.1', 20000))
    SERVER.send(bytes('JOIN-ROOM niko test','UTF-8'), networking.Address('127.0.0.1', 20000))
    SERVER.send(bytes('START-GAME test','UTF-8'), networking.Address('127.0.0.1', 20000))


    root.mainloop()