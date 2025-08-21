
def app(cocos):
    chkkk = ""
    with open('nose.txt', 'r') as e:
        chkkk = e.read()
    with open('nose.txt', 'w') as f:
        f.write(cocos + "\n" + chkkk)