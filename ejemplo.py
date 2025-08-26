
def app(cocos):
    chkkk = ""
    with open('nose.txt', 'r') as e:
        chkkk = e.read()
    with open('nose.txt', 'w') as f:
        f.write(cocos + "\n" + chkkk)

"""
Ejemplo de modificar donde dice
x = input("que desea agregar? ")
y = input("en que archivo? ")
z = input("donde dice que? ")
a = input("quiere un salto de linea antes? ")
A = False
if(a == "si"):
    A = True
b = input("quiere un salto de linea al final? ")
B = False
if(b == "si"):
    B = True
modificaDondedice(x, y, z, A, B)
"""

"""
x = input("Que archivo queres modificar? ")
y = input("Que le quieres sacar? ")
z = encontrarPorNombre(x)
w = input("Que desea agregar en su lugar? ")
print(z)
modificaDondedice(w, z, y, False, False)
sacarLoQueDice(z, y)
"""