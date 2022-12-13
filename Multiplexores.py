# Multiplexores, sin librerias.
import math
import time

class Utils:

    @staticmethod
    def StrToInt(tempValue: str) -> int:
        try:
            finalInt = int(tempValue)

            if finalInt < 0 or finalInt > 1:
                raise ValueError("notValid")

        except ValueError:
            return -1

        return finalInt

    @staticmethod
    def calcExp(base: int, resultado: int) -> int:
        # Igualo
        log1: float = math.log(base)
        log2: float = math.log(resultado)

        x: int = math.floor((log2 / log1))
        return x

    @staticmethod
    def demux(a, s0, s1):
        out = [0, 0, 0, 0]

        # s0 y s1 lo uso como índices del array
        out[s0 * 2 + s1] = a

        # devuelvo las salidas en una tupla
        return tuple(out)


    @staticmethod
    def randomInt(low: int, high: int) -> int:
        # Genero una seed con el tiempo unix
        import time
        random_seed = int(time.time())

        # Uso la semilla para generar un número aleatorio
        random_int = low + (random_seed % (high - low))
        return random_int

# Multiplexor Base (Constructor)
# Se encarga de gestionar las entradas y selectores correspondientes
class MultiplexorBase:

    @staticmethod
    def Build(tipoMux: str, entradas: int) -> (list[bool], list[bool]):
        print(f"Construyendo Multiplexor \"{tipoMux}\" con: {entradas} entradas.\n")
        boolList: list[bool] = []

        for i in range(entradas):

            while True:
                tempStr = str(input(f"Entrada #{i}: "))
                intValue: int = Utils.StrToInt(tempStr)

                if intValue == -1:
                    print(f"El valor introducido: {tempStr} no es valido. Asegurate que es 0 o 1.\n")
                    continue

                boolValue: bool = bool(intValue)
                boolList.append(boolValue)

                # print(f"Entrada #{i} guardada con: {boolValue}\n")
                break

        print(f"\n¡Entradas del MUX \"{tipoMux}\" ({len(boolList)}) creadas correctamente!")
        time.sleep(0.9)

        return boolList, MultiplexorBase.Selector(tipoMux, len(boolList))

    @staticmethod
    def Selector(muxType: str, cantidadEntradas: int) -> list[bool]:
        print(f"Ahora, Elige los selectores del MUX \"{muxType}\".\n")

        # Pido los selectores en base a la formula: 2^X = entradas donde X es el número de selectores del Multiplexor.
        cantidadSelectores: int = Utils.calcExp(2, cantidadEntradas)
        boolList: list[bool] = []

        for i in range(cantidadSelectores):

            while True:
                tempStr = str(input(f"Selector #{i}: "))
                intValue: int = Utils.StrToInt(tempStr)

                if intValue == -1:
                    print(f"El valor introducido: {tempStr} no es valido. Asegurate que es 0 o 1.\n")
                    continue

                boolValue: bool = bool(intValue)
                boolList.append(boolValue)

                # print(f"Sel #{i} guardada con: {boolValue}\n")
                break

        print(f"\n¡Selectores del MUX \"{muxType}\" ({len(boolList)}) construidos correctamente!")
        time.sleep(0.9)

        return boolList

    @staticmethod
    def Execute(t2Func, t4Func, t8Func, muxType: str, entradas: list[bool], selectores: list[bool],
                skipDelay: bool = False) -> int:
        print(f"[-+-] Probando MUX \"{muxType}\" con {len(entradas)} entradas y {len(selectores)} selectores...\n")
        time.sleep(0.5)

        result: int = -1  # Esto devuelve Execute()

        if len(selectores) == 0:
            print("Ups. No hay selectores. Vuelve a empezar.")
            return -1

        elif len(selectores) == 1:
            result = t2Func(entradas[0], entradas[1], selectores[0])
        elif len(selectores) == 2:
            result = t4Func(entradas[0], entradas[1], entradas[2], entradas[3], selectores[0], selectores[1])
        elif len(selectores) == 3:
            result = t8Func(entradas[0], entradas[1], entradas[2], entradas[3], entradas[4], entradas[5], entradas[6],
                            entradas[7], selectores[0], selectores[1], selectores[2])

        else:
            print(f"Ups. No hay disponible una función para {len(selectores)}. Vuelve a empezar.")

        if not skipDelay:
            print(f"¡Prueba finalizada! ====> {int(result)}")
            time.sleep(2)

        # Se pasa el bool a int para devolver la salida en 0 o 1.
        return int(result)


# Multiplexor OR
class MultiplexorBasico:
    muxType: str = "OR"

    @staticmethod
    def Build(entradas: int) -> (list[bool], list[bool]):
        return MultiplexorBase.Build(MultiplexorBasico.muxType, entradas)

    @staticmethod
    def Execute(entradas: list[bool], selectores: list[bool], skipDelay: bool = False) -> int:
        return MultiplexorBase.Execute(MultiplexorBasico._T2, MultiplexorBasico._T4, MultiplexorBasico._T8,
                                       MultiplexorBasico.muxType,
                                       entradas, selectores, skipDelay)

    # Funciones de Cálculo
    # T2 -> 2:1 (2 entradas y 1 selector)
    # T4 -> 4:1 (4 entradas y 2 selectores)
    # T8 -> 8:1 (8 entradas y 3 selectores)
    # Uso el _ para indicar que estas funciones no se deben llamar directamente.

    @staticmethod
    def _T2(a, b, s):
        return a if s == 0 else b

    @staticmethod
    def _T4(a, b, c, d, s0, s1):

        # A través de manipulación de bits, hago encode de s0 y s1 en una sola variable (integer).
        # Se pueden añadir casos adicionales si hace falta, incrementando el tamaño de la lookup table.
        # Esto es posible hacerlo ya que s0 y s1, siempre son 0 o 1.
        s = (s1 << 1) | s0

        # Uso la lookup table para devolver el valor correspondiente al usuario.
        return [a, b, c, d][s]


    @staticmethod
    def _T8(a, b, c, d, e, f, g, h, s0, s1, s2):

        s = (s2 << 2) | (s1 << 1) | s0
        return [a, b, c, d, e, f, g, h][s]


# Multiplexor AND
class MultiplexorAnd:
    muxType: str = "AND"

    @staticmethod
    def Build(entradas: int) -> (list[bool], list[bool]):
        return MultiplexorBase.Build(MultiplexorAnd.muxType, entradas)

    @staticmethod
    def Execute(entradas: list[bool], selectores: list[bool], skipDelay: bool = False) -> int:
        return MultiplexorBase.Execute(MultiplexorAnd._T2, MultiplexorAnd._T4, MultiplexorAnd._T8,
                                       MultiplexorAnd.muxType,
                                       entradas, selectores, skipDelay)

    @staticmethod
    def _T2(a, b, s):
        return a and b if s == 0 else False

    @staticmethod
    def _T4(a, b, c, d, s0, s1):

        s = (s1 << 1) | s0
        return [a and b, a and c, a and d, b and c][s]

    @staticmethod
    def _T8(a, b, c, d, e, f, g, h, s0, s1, s2):

        s = (s2 << 2) | (s1 << 1) | s0
        return [a and b, c and d, e and f, g and h, a and c, b and d, e and g, f and h][s]

# Multiplexor NOT
class MultiplexorNot:
    muxType: str = "NOT"

    @staticmethod
    def Build(entradas: int) -> (list[bool], list[bool]):
        return MultiplexorBase.Build(MultiplexorNot.muxType, entradas)

    @staticmethod
    def Execute(entradas: list[bool], selectores: list[bool], skipDelay: bool = False) -> int:
        return MultiplexorBase.Execute(MultiplexorNot._T2, MultiplexorNot._T4, MultiplexorNot._T8,
                                       MultiplexorNot.muxType,
                                       entradas, selectores, skipDelay)

    @staticmethod
    def _T2(a, b, s):
        inputs = [a, b]

        output = not inputs[s]
        return output

    @staticmethod
    def _T4(a, b, c, d, s0, s1):
        inputs = [a, b, c, d]

        output = not inputs[s0 + 2 * s1]
        return output

    @staticmethod
    def _T8(a, b, c, d, e, f, g, h, s0, s1, s2):
        inputs = [a, b, c, d, e, f, g, h]

        output = not inputs[s0 * 4 + s1 * 2 + s2]
        return output

# Multiplexor NOR
class MultiplexorNor:
    muxType: str = "NOR"

    @staticmethod
    def Build(entradas: int) -> (list[bool], list[bool]):
        return MultiplexorBase.Build(MultiplexorNor.muxType, entradas)

    @staticmethod
    def Execute(entradas: list[bool], selectores: list[bool], skipDelay: bool = False) -> int:
        return MultiplexorBase.Execute(MultiplexorNor._T2, MultiplexorNor._T4, MultiplexorNor._T8,
                                       MultiplexorNor.muxType,
                                       entradas, selectores, skipDelay)

    # Aprovecho la implementación del Multiplexor OR.

    @staticmethod
    def _T2(a, b, s):
        return not MultiplexorBasico._T2(a, b, s)

    @staticmethod
    def _T4(a, b, c, d, s0, s1):
        return not MultiplexorBasico._T4(a, b, c, d, s0, s1)

    @staticmethod
    def _T8(a, b, c, d, e, f, g, h, s0, s1, s2):
        return not MultiplexorBasico._T8(a, b, c, d, e, f, g, h, s0, s1, s2)


# Multiplexor XOR
class MultiplexorXor:
    muxType: str = "XOR"

    @staticmethod
    def Build(entradas: int) -> (list[bool], list[bool]):
        return MultiplexorBase.Build(MultiplexorXor.muxType, entradas)

    @staticmethod
    def Execute(entradas: list[bool], selectores: list[bool], skipDelay: bool = False) -> int:
        return MultiplexorBase.Execute(MultiplexorXor._T2, MultiplexorXor._T4, MultiplexorXor._T8,
                                       MultiplexorXor.muxType,
                                       entradas, selectores, skipDelay)

    @staticmethod
    def _T2(a, b, s):
        return a if s == 0 else a ^ b

    @staticmethod
    def _T4(a, b, c, d, s0, s1):
        return a if s0 == 0 and s1 == 0 else b if s0 == 0 and s1 == 1 else a ^ c ^ d

    @staticmethod
    def _T8(a, b, c, d, e, f, g, h, s0, s1, s2):
        inputs = [a, b, c, d, e, f, g, h]

        output = inputs[s0] ^ inputs[s1] ^ inputs[s2]
        return output


# Multiplexor Xnor
class MultiplexorXnor:
    muxType: str = "XNOR"

    @staticmethod
    def Build(entradas: int) -> (list[bool], list[bool]):
        return MultiplexorBase.Build(MultiplexorXnor.muxType, entradas)

    @staticmethod
    def Execute(entradas: list[bool], selectores: list[bool], skipDelay: bool = False) -> int:
        return MultiplexorBase.Execute(MultiplexorXnor._T2, MultiplexorXnor._T4, MultiplexorXnor._T8,
                                       MultiplexorXnor.muxType,
                                       entradas, selectores, skipDelay)

    @staticmethod
    def _T2(a, b, s):
        return not MultiplexorXor._T2(a, b, s)

    @staticmethod
    def _T4(a, b, c, d, s0, s1):
        return not MultiplexorXor._T4(a, b, c, d, s0, s1)

    @staticmethod
    def _T8(a, b, c, d, e, f, g, h, s0, s1, s2):
        return not MultiplexorXor._T8(a, b, c, d, e, f, g, h, s0, s1, s2)


# Multiplexor NAND
class MultiplexorNand:
    muxType: str = "NAND"

    @staticmethod
    def Build(entradas: int) -> (list[bool], list[bool]):
        return MultiplexorBase.Build(MultiplexorNand.muxType, entradas)

    @staticmethod
    def Execute(entradas: list[bool], selectores: list[bool], skipDelay: bool = False) -> int:
        return MultiplexorBase.Execute(MultiplexorNand._T2, MultiplexorNand._T4, MultiplexorNand._T8,
                                       MultiplexorNand.muxType,
                                       entradas, selectores, skipDelay)

    @staticmethod
    def _T2(a, b, s):
        return not MultiplexorAnd._T2(a, b, s)

    @staticmethod
    def _T4(a, b, c, d, s0, s1):
        return not MultiplexorAnd._T4(a, b, c, d, s0, s1)

    @staticmethod
    def _T8(a, b, c, d, e, f, g, h, s0, s1, s2):
        return not MultiplexorAnd._T8(a, b, c, d, e, f, g, h, s0, s1, s2)


class UIUtils:

    @staticmethod
    def ChooseBasicMux(notAvailable: bool = False, randomDoor: bool = False):
        while True:
            # Muestro el menú al usuario
            print("\n"
                  "1 - OR (Basico)\n"
                  "2 - AND\n"
                  "3 - NOT\n"
                  "4 - XOR\n"
                  "5 - XNOR\n"
                  "6 - NOR\n"
                  "7 - NAND\n"                  
                  "8 - Volver\n")

            option: str = ""

            if not randomDoor:
                option = str(input("Elige una puerta lógica: "))
            else:
                option = str(Utils.randomInt(1, 3))

            if option == "1":
                return MultiplexorBasico.Build, MultiplexorBasico.Execute, MultiplexorBasico.muxType
            elif option == "2":
                return MultiplexorAnd.Build, MultiplexorAnd.Execute, MultiplexorAnd.muxType
            elif option == "3":
                if not notAvailable:
                    print("NOT no disponible\n")
                    return None, None

                return MultiplexorNot.Build, MultiplexorNot.Execute, MultiplexorNot.muxType

            elif option == "4":
                return MultiplexorXor.Build, MultiplexorXor.Execute, MultiplexorXor.muxType
            elif option == "5":
                return MultiplexorXnor.Build, MultiplexorXnor.Execute, MultiplexorXnor.muxType
            elif option == "6":
                return MultiplexorNor.Build, MultiplexorNor.Execute, MultiplexorNor.muxType
            elif option == "7":
                return MultiplexorNand.Build, MultiplexorNand.Execute, MultiplexorNand.muxType
            else:
                return None, None


    # Funcion encargada de crear MUXs parciales
    @staticmethod
    def BuildPartialMux(muxBaseSize:int, times: int) -> int:
        entradasGlobal: list[bool] = []
        (builderPointer, executePointer, muxType) = UIUtils.ChooseBasicMux()

        for i in range(times):
            print(f"MUX #{i + 1}\n")

            (entradas, selectores) = builderPointer(muxBaseSize)
            entradasGlobal.append(executePointer(entradas, selectores, True))

        selectoresGlobal: list[bool] = MultiplexorBase.Selector(muxType, len(entradasGlobal))
        return executePointer(entradasGlobal, selectoresGlobal)

    # Funcion helper de BuildDoor
    @staticmethod
    def BuildPartialDoor(muxBaseSize:int, times: int, randomDoor: bool = False) -> list[bool]:
        entradasGlobal: list[bool] = []

        for i in range(times):
            print(f"Puerta #{i + 1}\n")

            (builderPointer, executePointer, muxType) = UIUtils.ChooseBasicMux(True, randomDoor)

            (entradas, selectores) = builderPointer(muxBaseSize)
            entradasGlobal.append(executePointer(entradas, selectores, True))

        return entradasGlobal

    # Funcion helper de BuildDoor
    @staticmethod
    def BuildPartialDoorWith(times: int, entradasParam: list[bool], randomDoor: bool = False) -> list[bool]:
        entradasGlobal: list[bool] = []

        for i in range(times):
            print(f"Puerta #{i + 1}\n")

            (builderPointer, executePointer, muxType) = UIUtils.ChooseBasicMux(True, randomDoor)
            selectores: list[bool] = MultiplexorBase.Selector(muxType, len(entradasParam))

            entradasGlobal.append(executePointer(entradasParam, selectores, True))

        return entradasGlobal

    # Funcion encargada de construir las Puertas G1-G4
    @staticmethod
    def BuildDoor(randomDoors: bool = False):
        print("\nCreando Grupo G1")
        entradasG1: list[bool] = UIUtils.BuildPartialDoor(4, 8, randomDoors)

        print("\nCreando Grupo G2")
        entradasG2: list[bool] = UIUtils.BuildPartialDoorWith(4, entradasG1, randomDoors)


        print("Asignar G1/G2 aleatoriamente?\n 1 - No 2 - Si")
        option: str = str(input("Elige una opción: "))

        if option == "1":
            randomInt = Utils.randomInt(1, 2)

            if randomInt == 1:
                entradasG2 = entradasG1



        print("\nCreando Grupo G3")
        entradasG3: list[bool] = UIUtils.BuildPartialDoorWith(2, entradasG2, randomDoors)

        print("\nCreando Grupo G4")
        entradasG4: list[bool] = UIUtils.BuildPartialDoorWith(1, entradasG3, randomDoors)


        if not randomDoors:
            print("\n Detectada salida por G4! Ahora solo indica los selectores")
        else:
            print("\n Detectada salida por G4!")

        (builderPointer, executePointer, muxType) = UIUtils.ChooseBasicMux(True, randomDoors)
        selectores: list[bool] = MultiplexorBase.Selector(muxType, len(entradasG4))

        finalResult: int = executePointer(entradasG4, selectores)
        print(f"\n¡Resultado recibido! Final: {finalResult}")


# Empieza la UI
while True:
    print("¡Bienvenido a MUX!\n")

    print("\n\n" "1 - Elegir y crear Multiplexor\n" "2 - Multiplexor personalizado\n" "3 - DeMux 1:4\n" "4 - Salir\n")
    option: str = str(input("Elige una opción: "))

    # Crear multiplexor
    if option == "1":
        while True:
            # Muestro el menú al usuario
            print("\n-- Multiplexores --\n\n" "1 - MUX 2:1\n" "2 - MUX 4:1\n" "3 - MUX 8:1\n" "4 - MUX 16:1 (combina 2:1 o 4:1)\n" "5 - Volver\n")
            option: str = str(input("Elige una opción: "))

            # Creación de MUX
            if option == "1":
                # Obtengo las referencias a las funciones
                (builderPointer, executePointer, _) = UIUtils.ChooseBasicMux()

                # Construyo las entradas y selectores y ejecuto
                (entradas, selectores) = builderPointer(2)
                executePointer(entradas, selectores)

            elif option == "2":
                # Obtengo las referencias a las funciones
                (builderPointer, executePointer, _) = UIUtils.ChooseBasicMux()

                (entradas, selectores) = builderPointer(4)
                executePointer(entradas, selectores)

            elif option == "3":
                # Obtengo las referencias a las funciones
                (builderPointer, executePointer, _) = UIUtils.ChooseBasicMux()

                (entradas, selectores) = builderPointer(8)
                executePointer(entradas, selectores)

            elif option == "4":
                while True:
                    # Muestro el menú al usuario
                    print("\n-- Bases del MUX 16:1 --\n\n" "1 - MUX 2:1 (8 MUXs)\n" "2 - MUX 4:1 (4 MUXs)\n" "3 - Volver\n")
                    option: str = str(input("Elige una base: "))

                    if option == "1":
                        UIUtils.BuildPartialMux(2, 8)

                    elif option == "2":
                        UIUtils.BuildPartialMux(4, 4)

                    elif option == "3":
                        break
                    else:
                        continue

            elif option == "5":
                break
            else:
                continue

            #break

    # Mutliplexor personalizado (G1-G4)
    elif option == "2":
        print("\n-- MUX 8:1 personalizado --\n\n" "1 - Elegir puertas G1-G4\n" "2 - Selección aleatoria\n" "3 - Volver\n")
        option: str = str(input("Elige una opción: "))

        if option == "1":
           UIUtils.BuildDoor()

        elif option == "2":
            UIUtils.BuildDoor(True)
        elif option == "3":
            break
        else:
            continue

    # DeMux 1:4
    elif option == "3":
        #1 entrada, 2 seleccion, 4 salidas

        tempStr = str(input(f"Entrada #0: "))
        entrada: int = Utils.StrToInt(tempStr)
        selectores: list[int] = []

        if entrada == -1:
            print(f"El valor introducido: {tempStr} no es valido. Asegurate que es 0 o 1.\n")
            continue

        for i in range(2):
            while True:
                tempStr = str(input(f"Selector #{i}: "))
                sel: int = Utils.StrToInt(tempStr)

                if sel == -1:
                    print(f"El valor introducido: {tempStr} no es valido. Asegurate que es 0 o 1.\n")
                    continue

                selectores.append(sel)
                break

        deMuxResult: tuple = Utils.demux(entrada, selectores[0], selectores[1])

        print("\nFinalizado Demux 1:4 ==>")
        print(deMuxResult)

        time.sleep(2)
        print("\n")

    else:
        print("\n¡Adios!")
        break
