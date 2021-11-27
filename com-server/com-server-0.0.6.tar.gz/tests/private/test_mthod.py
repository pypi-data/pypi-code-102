all_me = []

class A:
    global all_me

    def asdf():
        return 1
    
    all_me.append(asdf)

print(all_me[0])


