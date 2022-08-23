#-*- coding: iso-8859-2 -*-


"""sql = "SELECT login FROM logdata"
    cursor.execute(sql)
    dupa = cursor.fetchall()
    rafinacja = []
    for x in range(len(dupa)):
        rafinacja.append(str(dupa[x][0]))
    print(str(dupa[0][0]))
    print(rafinacja)"""
from ast import Is
from audioop import add
from optparse import AmbiguousOptionError
import os
from re import T, TEMPLATE
from tokenize import group
from types import NoneType
os.system('color')
from termcolor import colored
from calendar import day_name
from dataclasses import dataclass
from msilib.schema import Class
import random
import time as tajm
from datetime import datetime
from datetime import time
import mysql.connector, secrets, keyboard, sys
currHour, currDate, login, credentials, ClassesBeingTaught, idNauczyciela, przedmiot, studentsID, idUczniaForParentUse, groupStatus, amounttt, listaForEditorUse = None, None, None, None, [], None, None, [], None, None, 0, []
daysOfWeek = {
    1: 'Poniedziałek',
    2: 'Wtorek',
    3: 'Środa',
    4: 'Czwartek',
    5: 'Piątek'
    }
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="fusiondziennik"
)
cursor = mydb.cursor(buffered=True)
def MAIN():
    while True:
        try:
            def getCurrentTime():
                global currHour,currDate
                now = datetime.now()
                if len(str(now.hour)) == 1:
                    hour = '0'+str(now.hour)
                else:
                    hour = str(now.hour)
                
                if len(str(now.minute)) == 1:
                    min = '0'+str(now.minute)
                else:
                    min = str(now.minute)
                
                currHour = hour+':'+min
                del hour,min
                month, day = str(now.month),str(now.day)
                if len(month) == 1:
                    month = '0'+month
                if len(day) == 1:
                    day = '0'+day
                currDate = str(now.year)+'-'+month+'-'+day

            def Menu():
                if groupStatus == 'parent':
                    menuParent()
                elif groupStatus == 'teacher':
                    menuTeacher()
                elif groupStatus == 'student':
                    menuStudent()
                else:
                    menuAdmin()
                pass

            def passwdChange(login):
                print('\nRozpoczęto procedurę zmiany hasła dla użytkownika: '+login)
                print('Aby wyjść wpisz "Anuluj".\n')
                currentPasswd = input('Podaj swoje obecne hasło: ')
                cursor.execute('SELECT password FROM logdata WHERE login = %s', (login, ))
                if cursor.fetchone()[0] != currentPasswd:
                    print('Błąd hasła. Procedura zmiany hasła została przerwana.\n')
                    if groupStatus == 'parent':
                        menuParent()
                    elif groupStatus == 'teacher':
                        menuTeacher()
                    else:
                        menuStudent()
                else:
                    print('Podaj swoje nowe hasło (rozróżniana jest wielkość znaków i znaki specjalne!):')
                    cursor.execute('UPDATE logdata SET password = %s WHERE login = %s', (input(), login))
                    mydb.commit()
                    print('Operacja zakończona sukcesem.\n')
                    if groupStatus == 'parent':
                        menuParent()
                    elif groupStatus == 'teacher':
                        menuTeacher()
                    else:
                        menuStudent()

            def Lessons(ParentModeKlasa):
                print('\nWybierz dzień:')
                for x in range(1, 6):
                    cursor.execute('SELECT idlekcji FROM planlekcji WHERE klasa = %s AND dzien = %s', (ParentModeKlasa, x))
                    kupciadupcia = cursor.fetchall()
                    quantity = []
                    for i in range(len(kupciadupcia)):
                        quantity.append(kupciadupcia[i][0])
                    if type(quantity) == NoneType: 
                        print(str(x)+'. '+daysOfWeek[x]+'   '+'(zaplanowane lekcje: 0)')
                    else:
                        print(str(x)+'. '+daysOfWeek[x]+'   '+'(zaplanowane lekcje: '+str(len(quantity))+')')
                chosenDayOfWeek = input()
                if chosenDayOfWeek.isdigit() == True:
                    chosenDayOfWeek = int(chosenDayOfWeek)
                else:
                    if groupStatus == 'parent':
                        menuParent()
                    else:
                        menuStudent()
                cursor.execute('SELECT idlekcji FROM planlekcji WHERE klasa = %s AND dzien = %s', (ParentModeKlasa, chosenDayOfWeek))
                quantity = cursor.fetchone()
                print('\nPlan lekcji dla klasy {} na dzień {}:'.format(ParentModeKlasa, daysOfWeek[chosenDayOfWeek]))
                if type(quantity) == NoneType:
                    print('Nie znaleziono lekcji tego dnia.')
                    kupa = input()
                    del kupa
                    Lessons()
                else:
                    cursor.execute('SELECT nrgodziny, lekcja, idnauczyciela FROM planlekcji WHERE klasa = %s AND dzien = %s', (ParentModeKlasa, chosenDayOfWeek))
                    tempFetch = cursor.fetchall()
                    LenOftempFetch = len(tempFetch)
                    for i in range(LenOftempFetch):
                        for x in range(len(tempFetch[i])):
                            tempFetch.append(tempFetch[i][x])
                    for _ in range(LenOftempFetch):
                        tempFetch.pop(0)
                    del LenOftempFetch
                    for x in range(int(len(tempFetch) / 3)):
                        cursor.execute('SELECT nazwisko, imie FROM nauczyciele WHERE idnauczyciela = %s', (int(tempFetch[((x+1)*3)-1]), ))
                        resultQuery = cursor.fetchone()
                        print('{}. {} - {} \n{}  Nauczyciel: {}\n'.format(str(x+1), printableTime(x+1, 'start'), printableTime(x+1, 'end'), tempFetch[x*3 + 1], str(resultQuery[0] + ' ' + resultQuery[1])))
                    kupa = input()
                    del kupa
                    Lessons(ParentModeKlasa)
                pass

            def viewGradesOfSpecificStudent(idUcznia, parentalMode):
                global idNauczyciela, groupStatus
                idOcen = []
                print('')
                if parentalMode == True:
                    cursor.execute('SELECT ocena, idoceny FROM oceny WHERE iducznia = %s', (idUcznia,))
                else:
                    cursor.execute('SELECT ocena, idoceny FROM oceny WHERE iducznia = %s AND idnauczyciela = %s', (idUcznia, idNauczyciela))
                oceny = cursor.fetchall()
                lengthOfOceny = len(oceny)
                for x in range(len(oceny)):
                    oceny.append(oceny[x][0])
                    idOcen.append(oceny[x][1])
                for _ in range(lengthOfOceny):
                    oceny.pop(0)
                del lengthOfOceny
                for x in range(len(oceny)):
                    cursor.execute('SELECT typ, przedmiot, opis, data, idnauczyciela FROM oceny WHERE idoceny = %s', (idOcen[x],))
                    GradeInfo = cursor.fetchall()
                    for y in range(len(GradeInfo[0])):
                        GradeInfo.append(GradeInfo[0][y])
                    GradeInfo.pop(0)
                    cursor.execute('SELECT nazwisko, imie FROM nauczyciele WHERE idnauczyciela = %s', (GradeInfo[4],))
                    rawDane = cursor.fetchone()
                    daneWstawiajacego = rawDane[0] + ' ' + rawDane[1]
                    del rawDane
                    print(str(x+1)+'.'+'\nOcena: '+oceny[x]+'\nOpis: '+GradeInfo[2]+'\nTyp oceny: '+GradeInfo[0]+'\nPrzedmiot: '+GradeInfo[1]+'\nWstawił(a): '+daneWstawiajacego+'\nData: '+str(GradeInfo[3].strftime('%Y-%m-%d'))+'\n')
                if parentalMode == False:
                    menuTeacher()
                else:
                    if parentalMode == 'parent':
                        menuParent()
                    else:
                        menuStudent()

            def generateList(visible):
                global ClassesBeingTaught, tempStudents, studentsID
                print('Wybierz klasę: ')
                for x in range(len(ClassesBeingTaught)):
                    print(str(x+1)+'. '+ClassesBeingTaught[x])
                chosenClass = int(input()) - 1
                sql = 'SELECT nazwisko, imie FROM uczniowie WHERE klasa = %s ORDER BY nazwisko'
                cursor.execute(sql, (ClassesBeingTaught[chosenClass],))
                tempStudents = cursor.fetchall()
                for x in range(len(tempStudents)):
                    tempStudents.append(str(tempStudents[x][0]))
                    tempStudents.append(str(tempStudents[x][1]))
                for _ in range(x+1):
                    tempStudents.pop(0) 
                i = 0
                sql = 'SELECT iducznia FROM uczniowie WHERE klasa = %s ORDER BY nazwisko'
                cursor.execute(sql, (ClassesBeingTaught[chosenClass],))
                studentsID = cursor.fetchall()
                for a in range(len(studentsID)):
                    studentsID.append(str(studentsID[a][0]))
                for _ in range(len(studentsID) - a-1):
                    studentsID.pop(0) # mamy pobrane iducznia po kolei, lecz brakuje nam mozliwosci polaczenia ich z uczniem
                if visible == False:
                    pass
                else:
                    print('\nWybierz ucznia:')
                    for x in range(0, len(tempStudents), 2):
                        print(str(i+1)+'. '+tempStudents[x] + ' ' + tempStudents[x+1])
                        i += 1

            def viewGrades():
                print('')
                generateList(True)
                loc = 0
                for x in range(int(input()) - 1):
                    loc += 2
                # print(loc)
                # print(studentsID)
                viewGradesOfSpecificStudent(studentsID[int(loc/2)], False)

            def addGrades():
                global ClassesBeingTaught, tempStudents, przedmiot, idNauczyciela, studentsID
                print('\n')
                sql = 'INSERT INTO oceny(iducznia, ocena, przedmiot, typ, opis, data, idnauczyciela) VALUES(%s,%s,%s,%s,%s,%s,%s)'
                opis = input('Podaj opis oceny: \n')
                print('')
                generateList(True)
                print('\nKomu wystawiasz ocenę?')
                inp = input()
                # loc = 0
                # for x in range(int(inp) - 1):
                #     loc += 2

                if inp.isnumeric() == False:
                    for x in range(0, len(tempStudents), 2):
                        ocena = input('Podaj ocenę dla ucznia'+' '+tempStudents[x]+' '+tempStudents[x+1]+':\n')
                        if ocena.isnumeric() == True:
                            typ = 'cząstkowa'
                        else:
                            typ = 'opisowa'
                        loc = x / 2
                        idUcznia = studentsID[int(loc)]
                        now = datetime.now()
                        Data = now.strftime('%Y-%m-%d')
                        cursor.execute(sql, (int(idUcznia), ocena, przedmiot, typ, opis, Data, idNauczyciela))
                    mydb.commit()
                    print('')
                    menuTeacher()
                else:
                    loc = 0
                    for x in range(int(inp) - 1):
                        loc += 2
                    ocena = input('\nPodaj ocenę dla ucznia'+' '+tempStudents[loc]+' '+tempStudents[loc+1]+':\n')
                    if ocena.isnumeric() == True:
                        typ = 'cząstkowa'
                    else:
                        typ = 'opisowa'
                    
                    idUcznia = studentsID[int(loc/2)]
                    now = datetime.now()
                    Data = now.strftime('%Y-%m-%d')
                    cursor.execute(sql, (int(idUcznia), ocena, przedmiot, typ, opis, Data, idNauczyciela))
                    mydb.commit()
                    print('')
                    menuTeacher()

            def beginLesson():
                pass

            def menuStudent():
                pass

            def menuParent():
                global currDate, currHour, login, idUczniaForParentUse
                cursor.execute('SELECT imie, nazwisko, klasa, iducznia FROM uczniowie WHERE parentUserID = %s', (login, ))
                Info = cursor.fetchall()
                LenOfInfo = len(Info)
                for x in range(len(Info[0])):
                    Info.append(Info[0][x])
                for _ in range(LenOfInfo):
                    Info.pop(0)
                del LenOfInfo
                print('Użytkownik: '+Info[1]+' '+Info[0]+' (rodzic)')
                print('Klasa: '+ Info[2])
                getCurrentTime()
                print('Data:',currDate)
                print('Godzina:',currHour+'\n')
                print('"1" - widok ocen')
                print('"2" - plan lekcji')
                print('"passwd" - zmiana hasła\n')
                print('Co chcesz zrobić?')
                answer = input()
                if answer == '1':
                    viewGradesOfSpecificStudent(Info[3], True)
                elif answer == '2':
                    Lessons(Info[2])
                elif answer == 'passwd':
                    passwdChange(login)
                else:
                    print('Spróbuj ponownie.\n')
                    menuAdmin()
                pass

            def menuAdmin():
                global currDate,currHour
                print('Użytkownik: SuperAdministrator')
                getCurrentTime() 
                print('Data:',currDate)
                print('Godzina:',currHour+'\n')
                print('"1" - dodawanie nowych uczniów')
                print('"2" - dodawanie nowych nauczycieli')
                print('"3" - tworzenie siatki godzin')
                print('"4" - tworzenie planu lekcji\n')
                print('Co chcesz zrobić?')
                answer = input()
                if answer == '1':
                    addingNewStudents()
                elif answer == '2':
                    addingNewTeachers()
                elif answer == '3':
                    settingUpHoursSchedule()
                elif answer == '4':
                    LessonsScheduleEditor()
                else:
                    print('Spróbuj ponownie.\n')
                    menuAdmin()
                pass

            def menuTeacher():
                global currDate,currHour, login, ClassesBeingTaught, credentials, idNauczyciela, przedmiot
                sql = 'SELECT imie, nazwisko, idnauczyciela FROM nauczyciele WHERE teacherUserID = %s'
                cursor.execute(sql, (login,))
                result = cursor.fetchall()
                credentials = result[0][0]+' '+result[0][1]
                idNauczyciela = result[0][2]
                print('Użytkownik:',credentials)
                getCurrentTime()
                print('Data:',currDate)
                print('Godzina:',currHour)
                sql = 'SELECT przedmiot FROM nauczyciele WHERE teacherUserID = %s'
                cursor.execute(sql, (login,))
                przedmiot = cursor.fetchone()[0]
                print('Przedmiot:',przedmiot)
                sql = 'SELECT uczoneKlasy FROM nauczyciele WHERE teacherUserID = %s'
                cursor.execute(sql, (login,))
                result = cursor.fetchone()[0]
                tempClass = ''
                ClassesBeingTaught = []
                for x in range(len(result)):
                    if result[x] == ';':
                        ClassesBeingTaught.append(tempClass)
                        tempClass = ''
                    else:
                        tempClass = tempClass + result[x]
                ClassesBeingTaught.append(tempClass)

                print('Uczone klasy:')
                for x in range(len(ClassesBeingTaught)):
                    print(str(x+1)+'. '+ClassesBeingTaught[x])
                print('')
                print('"1" - dodaj nową ocenę')
                print('"2" - widok ocen')
                print('"3" - rozpocznij nową lekcję')
                print('"4" - plan lekcji')
                print('"passwd" - zmiana hasła\n')
                print('Co chcesz zrobić?')
                answer = input()
                if answer == '1':
                    addGrades()
                elif answer == '2':
                    viewGrades()
                elif answer == '3':
                    beginLesson()
                elif answer == '4':
                    print(' ')
                    print('Aby przejść do wyświetlenia planu lekcji dla danej (uczonej) klasy, wpisz ją.\nAby kontynuować wyświetlanie planu dla Ciebie, kliknij Enter.')
                    choice = input()
                    if choice == '':
                        Lessons4Teacher(idNauczyciela)
                    else:
                        if (choice in ClassesBeingTaught) == True:
                            Lessons(choice)
                        else:
                            print('Spróbuj ponownie.\n')
                            menuTeacher()

                elif answer == 'passwd':
                    passwdChange(login)
                
                else:
                    print('Spróbuj ponownie.\n')
                    menuTeacher()
                pass

            def NdStepLogin():
                global login, groupStatus
                passwd = input('Proszę podaj hasło: ')
                sql = 'SELECT password FROM logdata WHERE login = %s'
                cursor.execute(sql, (login,))
                if str(cursor.fetchone()[0]) == passwd:
                    print('Nastąpiło poprawne zalogowanie!\n')
                    sql = 'SELECT groupStatus FROM logdata WHERE login = %s'
                    cursor.execute(sql, (login,))
                    groupStatus = cursor.fetchone()[0]
                    if groupStatus == 'student':
                        menuStudent()
                    elif groupStatus == 'parent':
                        menuParent()
                    elif groupStatus == 'teacher':
                        menuTeacher()
                    else:
                        menuAdmin()
                else:
                    print('Błędne hasło! Spróbuj ponownie.\n')
                    NdStepLogin()

            def StStepLogin():
                global login
                login = input('Proszę podaj login: ')
                sql = "SELECT login FROM logdata WHERE login = %s"
                cursor.execute(sql, (login,))
                temp = cursor.fetchall()
                if len(temp) == 0:
                    print('Błędny login! Spróbuj ponownie.\n')
                    StStepLogin()
                elif temp[0][0] != login:
                    print('Błędny login! Spróbuj ponownie.\n')
                    StStepLogin()
                else:
                    print('\nWitaj użytkowniku!')
                    NdStepLogin()

            def addingNewStudents():
                hasla = []
                klasa = input('Jaką klasę chcesz utworzy?? ')
                howMany = int(input('Ilu nowych uczniów chcesz dodać do klasy? '))
                for _ in range(howMany):
                    sql = "INSERT INTO uczniowie(imie, nazwisko, pesel, plec, klasa, studentUserID, parentUserID) VALUES(%s, %s, %s, %s, %s,%s,%s)"
                    daneOsobowe = []
                    daneOsobowe.append(input('Podaj imię ucznia:\n'))
                    daneOsobowe.append(input('Podaj nazwisko ucznia:\n'))
                    daneOsobowe.append(input('Podaj PESEL ucznia:\n'))
                    if int(daneOsobowe[2][9]) % 2 == 0:
                        daneOsobowe.append('K')
                    else:
                        daneOsobowe.append('M')
                    daneOsobowe.append(klasa)
                    parentUserID = str(random.randrange(2900000,3000000,1))
                    studentUserID = parentUserID+'u'
                    password4parent = secrets.token_urlsafe(9)
                    password4student = secrets.token_urlsafe(9)
                    hasla.append((parentUserID+'   '+password4parent+'   '+daneOsobowe[1]+' '+daneOsobowe[0]))
                    hasla.append((studentUserID+'  '+password4student+'   '+daneOsobowe[1]+' '+daneOsobowe[0]+'   '+'// Uczeń'))
                    cursor.execute(sql, (daneOsobowe[0], daneOsobowe[1],daneOsobowe[2],daneOsobowe[3],daneOsobowe[4], studentUserID, parentUserID))
                    mydb.commit()
                    sql = 'INSERT INTO logdata(login,password,groupStatus) VALUES(%s,%s,%s)'
                    cursor.execute(sql, (studentUserID, password4student, 'student'))
                    mydb.commit()
                    cursor.execute(sql, (parentUserID, password4parent, 'parent'))
                    mydb.commit()
                print('\n\n\n')
                for y in range(len(hasla)):
                    print(hasla[y])
                print('\n\n\n')
                menuAdmin()

            def addingNewTeachers():
                try:
                    howMany = int(input('Ilu nauczycieli chcesz dodać do systemu? '))
                    for _ in range(howMany):
                        sql = "INSERT INTO nauczyciele(imie, nazwisko, przedmiot, uczoneKlasy, teacherUserID) VALUES(%s, %s, %s, %s,%s)"
                        hasla = []
                        daneOsobowe = []
                        daneOsobowe.append(input('Podaj imię nauczyciela:\n'))
                        daneOsobowe.append(input('Podaj nazwisko nauczyciela:\n'))
                        daneOsobowe.append(input('Podaj przedmiot, którego naucza nauczyciel:\n'))
                        daneOsobowe.append(input('Podaj klasy, które naucza nauczyciel (w formacie KLASA;KLASA..)\n'))
                        teacherUserID = str(random.randrange(3000000,3100000,1))
                        password4teacher = secrets.token_urlsafe(10)
                        hasla.append((teacherUserID+'   '+password4teacher+daneOsobowe[1],daneOsobowe[0]))
                        cursor.execute(sql, (daneOsobowe[0], daneOsobowe[1], daneOsobowe[2], daneOsobowe[3], teacherUserID))
                        mydb.commit()
                        sql = 'INSERT INTO logdata(login,password,groupStatus) VALUES(%s,%s,%s)'
                        cursor.execute(sql, (teacherUserID, password4teacher, 'teacher'))
                        mydb.commit()
                except:
                    print('Spróbuj ponownie.\n')
                    Menu()
                print(hasla)

            def LessonsScheduleEditor():
                global chosenClass, chosenDayOfWeek, listaForEditorUse
                # zaciagamy klasy w szkole
                cursor.execute('SELECT uczoneKlasy FROM nauczyciele')
                uczoneKlasy, tempClass = [], ''
                GeneraluczoneKlasy = cursor.fetchone()[0]
                for x in range(len(GeneraluczoneKlasy)):
                    if GeneraluczoneKlasy[x] == ';':
                        if (tempClass in uczoneKlasy) == False:
                            uczoneKlasy.append(tempClass)
                        else:
                            pass
                        tempClass = ''
                    else:
                        tempClass = tempClass + GeneraluczoneKlasy[x]
                if (tempClass in uczoneKlasy) == False:
                    uczoneKlasy.append(tempClass)
                else:
                    pass
                del GeneraluczoneKlasy, tempClass
                print('\nWybierz klasę dla której wejdziesz w tryb edytora:')
                for dupa in range(len(uczoneKlasy)):
                    print(str(dupa+1)+'. '+uczoneKlasy[dupa])
                choose = input()
                if choose.isdigit() == True:
                    choose = int(choose)
                else:
                    menuAdmin()
                    return
                chosenClass = uczoneKlasy[int(choose)-1]
                del choose
                print('\nWybierz dzień:')
                for x in range(1, 6):
                    cursor.execute('SELECT idlekcji FROM planlekcji WHERE klasa = %s AND dzien = %s', (chosenClass, x))
                    kupciadupcia = cursor.fetchall()
                    quantity = []
                    for i in range(len(kupciadupcia)):
                        quantity.append(kupciadupcia[i][0])
                    if type(quantity) == NoneType: 
                        print(str(x)+'. '+daysOfWeek[x]+'   '+'(zaplanowane lekcje: 0)')
                    else:
                        print(str(x)+'. '+daysOfWeek[x]+'   '+'(zaplanowane lekcje: '+str(len(quantity))+')')
                chosenDayOfWeek = input()
                if chosenDayOfWeek.isdigit() == True:
                    chosenDayOfWeek = int(chosenDayOfWeek)
                else:
                    LessonsScheduleEditor()
                cursor.execute('SELECT idlekcji FROM planlekcji WHERE klasa = %s AND dzien = %s', (chosenClass, chosenDayOfWeek))
                quantity = cursor.fetchone()
                print('\nPlan lekcji dla klasy {} na dzień {}:'.format(chosenClass, daysOfWeek[chosenDayOfWeek]))
                if type(quantity) == NoneType:
                    print('Nie znaleziono lekcji tego dnia.')
                    print('\nWybierz operację:')
                    print('"1" - dodaj lekcje')
                else:
                    cursor.execute('SELECT nrgodziny, lekcja, idnauczyciela, idlekcji FROM planlekcji WHERE klasa = %s AND dzien = %s', (chosenClass, chosenDayOfWeek))
                    tempFetch = cursor.fetchall()
                    LenOftempFetch = len(tempFetch)
                    for i in range(LenOftempFetch):
                        for x in range(len(tempFetch[i])):
                            tempFetch.append(tempFetch[i][x])
                    for _ in range(LenOftempFetch):
                        tempFetch.pop(0)
                    del LenOftempFetch
                    print('')
                    for x in range(int(len(tempFetch) / 4)):
                        cursor.execute('SELECT nazwisko, imie FROM nauczyciele WHERE idnauczyciela = %s', (int(tempFetch[((x+1)*4)-2]), ))
                        resultQuery = cursor.fetchone()
                        print('{}. \nGodzina nr {} : {} - {}\n{}  Nauczyciel: {}\n'.format(str(x+1), str(tempFetch[x*4]), printableTime(tempFetch[x*4], 'start'), printableTime(tempFetch[x*4], 'end'), tempFetch[x*4 + 1], str(resultQuery[0] + ' ' + resultQuery[1])))
                    print('\nWybierz operację:')
                    print('"1" - dodaj lekcje')
                    print('"2" - edytuj lekcję')
                    print('"3" - usuń lekcję')
                choice = input()
                if choice == '':
                    print('')
                    LessonsScheduleEditor()
                else:
                    choice = int(choice)    
                    if choice == 1:
                        addLessons()
                    elif choice == 2:
                        listaForEditorUse = tempFetch
                        editLesson(listaForEditorUse)
                    elif choice == 3:
                        listaForEditorUse = tempFetch
                        deleteLesson(listaForEditorUse)

            def deleteLesson(lista):
                print('Wybierz lekcję, którą chcesz usunąć...')
                wybor = input() 
                if wybor.isdigit() == False:
                    print('Spróbuj ponownie.\n')
                    deleteLesson(listaForEditorUse)
                    return
                else:
                    wybor = int(wybor)
                    if (wybor in lista) == False:
                        print('Spróbuj ponownie.\n')
                        deleteLesson(listaForEditorUse)
                        return

            def addLessons():
                print('\nIle lekcji chcesz dodać dla klasy {}?'.format(chosenClass))
                amountOfLessonsToBeAdded = input()
                if amountOfLessonsToBeAdded.isdigit() == False:
                    print('Spróbuj ponownie.\n')
                    addLessons()
                    return 0
                else:
                    amountOfLessonsToBeAdded = int(amountOfLessonsToBeAdded)
                    cursor.execute('SELECT nrgodziny FROM siatkagodzin ORDER BY nrgodziny DESC LIMIT 1')
                    topHour = cursor.fetchone()[0]
                    cursor.execute('SELECT nrgodziny FROM planlekcji WHERE klasa = %s AND dzien = %s ORDER BY nrgodziny DESC LIMIT 1', (chosenClass, chosenDayOfWeek))
                    obecnaGodzina = cursor.fetchone()
                    if type(obecnaGodzina) == NoneType:
                        obecnaGodzina = 0
                    else:
                        obecnaGodzina = obecnaGodzina[0]
                        obecnaGodzina = int(obecnaGodzina)
                    Sample = amountOfLessonsToBeAdded + obecnaGodzina
                    if Sample > topHour:
                        print('Wykraczasz poza granicę siatki godzin. Dodaj nowe lub popraw błąd.\n')
                        addLessons()
                        return 0
                    else:
                        for nrgodziny in range(obecnaGodzina + 1, obecnaGodzina + amountOfLessonsToBeAdded + 1, 1):
                            print('\nPodaj przedmiot lekcji na godzinie lekcyjnej nr {}:'.format(str(nrgodziny)))
                            lajk = '%'+chosenClass+'%'
                            cursor.execute('SELECT DISTINCT przedmiot FROM nauczyciele WHERE uczoneKlasy LIKE %s', (lajk,))
                            fetch = cursor.fetchall()
                            przedmioty = []
                            for x in range(len(fetch)):
                                przedmioty.append(fetch[x][0])
                            del fetch
                            for x in range(len(przedmioty)):
                                print('{}. {}'.format(x+1, przedmioty[x]))
                            choice = input()
                            if choice.isdigit() == False:
                                print('\nSpróbuj ponownie.')
                                addLessons()
                            else:
                                #zmienna lekcji jaka dodajemy
                                lekcja = przedmioty[int(choice)-1]
                                print('\nWybierz nauczyciela dla lekcji {} na godzinie lekcyjnej nr {} dla klasy {}:'.format(lekcja, nrgodziny, chosenClass))
                                cursor.execute('SELECT idnauczyciela FROM nauczyciele WHERE przedmiot = %s AND uczoneKlasy LIKE %s', (lekcja, lajk))
                                fetch = cursor.fetchall()
                                nauczyciele = []
                                for x in range(len(fetch)):
                                    nauczyciele.append(fetch[x][0])
                                del fetch
                                sql = 'SELECT nazwisko, imie FROM nauczyciele WHERE idnauczyciela = %s'
                                for x in range(len(nauczyciele)):
                                    cursor.execute(sql, (nauczyciele[x],))
                                    fetch = cursor.fetchone()
                                    print('{}. {} {}'.format(str(x+1), fetch[0], fetch[1]))
                                choice = input()
                                if choice.isdigit() == False:
                                    print('\nSpróbuj ponownie.')
                                    addLessons()
                                else:
                                    choice = int(choice)
                                    tempIdNauczyciela = choice
                                print('ID nauczyciela: '+str(tempIdNauczyciela))
                                print('Lekcja: '+str(lekcja))
                                print('Numer godziny: '+str(nrgodziny))
                                print('Klasa: '+str(chosenClass))
                                print('Dzień: '+daysOfWeek[chosenDayOfWeek])
                                cursor.execute('INSERT INTO planlekcji(nrgodziny, idnauczyciela, lekcja, klasa, dzien) VALUES(%s, %s, %s, %s, %s)', (int(nrgodziny), int(nauczyciele[tempIdNauczyciela - 1]), lekcja, chosenClass, chosenDayOfWeek))
                                mydb.commit()


            def waitUntil(condition, output): #defines function
                wU = True
                while wU == True:
                    if condition: #checks the condition
                        output
                        wU = False
                    tajm.sleep(0.15)

            def purify(lista):
                for _ in range(len(lista)):
                    for i in range(len(lista[0])):
                        lista.append(lista[0][i])
                    lista.pop(0)
                return lista
                        

            def increment():
                global amounttt
                amounttt += 1
                pass

            def editLesson(lista):
                global amounttt
                # print('Klasa: '+chosenClass)
                # print('Dzień: '+str(daysOfWeek[chosenDayOfWeek]))
                print('Wybierz numer lekcji: ')
                choice = input()
                if choice.isdigit() == False:
                    print('Spróbuj ponownie.\n')
                    editLesson(listaForEditorUse)
                else:
                    choice = int(choice)
                    numerLekcyjkiPilny = choice
                    if int(len(lista) / 4) < choice:
                        print('Wybrano błędną lekcję. Spróbuj ponownie. \n')
                        editLesson(listaForEditorUse)
                        return
                    else:
                        idLekcji = lista[choice*4 - 1]
                        decisionBeenMade = None
                        cursor.execute('SELECT nrgodziny, idnauczyciela, lekcja, klasa, dzien FROM planlekcji WHERE idlekcji = %s ORDER BY nrgodziny ASC LIMIT 1', (idLekcji, ))
                        fetch = cursor.fetchone()
                        print('')
                        print('Numer godziny: {} ({} - {})'.format(str(fetch[0]), printableTime(fetch[0], 'start'), printableTime(fetch[0], 'end')))
                        print('Nauczyciel: {} (ID: {})'.format(downloadTeacherData(fetch[1]), str(fetch[1])))
                        print('Przedmiot: {}'.format(fetch[2]))
                        print('Klasa: '+chosenClass)
                        print('Dzień: '+str(daysOfWeek[chosenDayOfWeek]+'\n'))
                        print('Który parametr modyfikujesz?\n')
                        GetComponentOfLessonToEdit = {
                            'nrGodziny': int(fetch[0]),
                            'idNauczyciela': fetch[1],
                            'przedmiot': fetch[2],
                            'klasa': chosenClass,
                            'rawDzien': int(chosenDayOfWeek),
                            'dzien': daysOfWeek[chosenDayOfWeek],
                            'idLekcji': idLekcji
                        }
                        amounttt = 0
                        decisionBeenMade = False
                        while decisionBeenMade == False:
                            if keyboard.read_key() == 'enter':
                                decisionBeenMade = True
                                dupa = input()
                                if amounttt % 5 == 0:
                                    
                                    print('Obecny parametr (numer godziny): {}'.format(str(fetch[0])))
                                    print('Wybierz godzinę na którą chcesz przenieść daną lekcję: \n')

                                    # robimy listę wszystkich godzin w szkole
                                    cursor.execute('SELECT nrgodziny FROM siatkagodzin')
                                    wszystkieGodziny = cursor.fetchall()
                                    for _ in range(len(wszystkieGodziny)):
                                        wszystkieGodziny.append(wszystkieGodziny[0][0])
                                        wszystkieGodziny.pop(0)

                                    # robimy listę godzin, na których uczy wybrany nauczyciel w kontekście całej szkoły 
                                    cursor.execute('SELECT nrgodziny FROM planlekcji WHERE idnauczyciela = %s AND dzien = %s', (fetch[1], chosenDayOfWeek))
                                    hoursWhenTeacherIsBusy = cursor.fetchall()
                                    if type(hoursWhenTeacherIsBusy) == NoneType:
                                        hoursWhenTeacherIsBusy = []
                                    else:
                                        for _ in range(len(hoursWhenTeacherIsBusy)):
                                            hoursWhenTeacherIsBusy.append(hoursWhenTeacherIsBusy[0][0])
                                            hoursWhenTeacherIsBusy.pop(0)
                                    
                                    # robimy listę godzin, kiedy dana klasa ma lekcję
                                    cursor.execute('SELECT nrgodziny FROM planlekcji WHERE klasa = %s AND dzien = %s', (chosenClass, chosenDayOfWeek))
                                    hoursWhenClassIsBusy = cursor.fetchall()
                                    if type(hoursWhenClassIsBusy) == NoneType:
                                        hoursWhenClassIsBusy = []
                                    else:
                                        for _ in range(len(hoursWhenClassIsBusy)):
                                            hoursWhenClassIsBusy.append(hoursWhenClassIsBusy[0][0])
                                            hoursWhenClassIsBusy.pop(0)
                                    freeLessons = []
                                    for x in range(wszystkieGodziny[0], (wszystkieGodziny[len(wszystkieGodziny) - 1] + 1), 1):
                                        conflict = ''
                                        if x == choice:
                                            conflict = conflict + 'GODZINA WYBRANEJ LEKCJI'
                                        else:
                                            if (x in hoursWhenTeacherIsBusy) == True:
                                                cursor.execute('SELECT klasa FROM planlekcji WHERE nrgodziny = %s AND idnauczyciela = %s AND dzien = %s',(x, fetch[1], chosenDayOfWeek))
                                                conflict = conflict + 'NAUCZYCIEL ZAJĘTY (LEKCJA Z KLASĄ ' + cursor.fetchone()[0]+')    '
                                            if (x in hoursWhenClassIsBusy) == True:
                                                cursor.execute('SELECT idnauczyciela FROM planlekcji WHERE nrgodziny = %s AND klasa = %s AND dzien = %s', (x, chosenClass, chosenDayOfWeek))
                                                conflict = conflict + 'KLASA ZAJĘTA (LEKCJA Z {})'.format(downloadTeacherData(cursor.fetchone()[0]))
                                        if conflict == '':
                                            conflict = 'WOLNA'
                                            freeLessons.append(x)
                                        print('{}. {}'.format(str(x), conflict))
                                    # dupa = input()
                                    sys.stdout.write("\033[K")
                                    wybor = input()
                                    if wybor.isdigit() == False:
                                        print('Spróbuj ponownie. \n')
                                        editLesson(listaForEditorUse)
                                        return
                                    else:                            
                                        wybor = int(wybor)
                                        if (wybor in freeLessons) == False:
                                            print('Spróbuj ponownie. \n')
                                            editLesson(listaForEditorUse)
                                            return
                                        else:
                                            print('Czy na pewno chcesz zamienić lekcję {} ({}) z godziny lekcyjnej nr {} na godzinę nr {}?'.format(fetch[2], downloadTeacherData(fetch[1]), str(fetch[0]), str(wybor)))
                                            wybur = input()
                                            if wybur == '' or 'tak' or 'Tak' or 'TAK':
                                                cursor.execute('UPDATE planlekcji SET nrgodziny = %s WHERE idlekcji = %s', (wybor, idLekcji))
                                                mydb.commit()
                                                print('Aktualizacja planu udana.')
                                            LessonsScheduleEditor()
                                            return

                                if amounttt % 5 == 1:
                                    
                                    print('Wybierz nauczyciela, który ma poprowadzić daną lekcję: (jeśli nie widzisz chcianego nauczyciela, zmień przedmiot)')
                                    cursor.execute('SELECT idnauczyciela FROM nauczyciele WHERE przedmiot = %s', (fetch[2], ))
                                    nauczycieleSpelniajacyWymagania = purify(cursor.fetchall())
                                    nauczycieleSpelniajacyWymagania.pop(nauczycieleSpelniajacyWymagania.index(fetch[1]))
                                    conflictTeachers = []
                                    for x in range(len(nauczycieleSpelniajacyWymagania)):
                                        additionalInfo = ''
                                        cursor.execute('SELECT uczoneKlasy FROM nauczyciele WHERE idnauczyciela = %s', (nauczycieleSpelniajacyWymagania[x],))
                                        uczoneKlasy = cursor.fetchone()[0]
                                        if (chosenClass in uczoneKlasy) == False:
                                            additionalInfo += '!NAUCZYCIEL NIE UCZY KLASY! '
                                            conflictTeachers.append(x)
                                            conflictTeachers.append('class')
                                        cursor.execute('SELECT klasa FROM planlekcji WHERE nrgodziny = %s AND idnauczyciela = %s AND dzien = %s', (fetch[0], nauczycieleSpelniajacyWymagania[x], chosenDayOfWeek))
                                        rezultat = cursor.fetchone()
                                        if type(rezultat) != NoneType:
                                            additionalInfo += '!NAUCZYCIEL JEST ZAJĘTY (LEKCJA Z KLASĄ {})!'.format(rezultat[0])
                                            conflictTeachers.append(x)
                                            conflictTeachers.append('busy')
                                        print('{}. {}   {}'.format(str(x + 1), downloadTeacherData(nauczycieleSpelniajacyWymagania[x]), additionalInfo))
                                    dupa = input()
                                    del dupa
                                    print('', end='\r')
                                    sys.stdout.write('\033[2K\033[1G')
                                    choice = ''
                                    good = False
                                    while good != True:
                                        try:
                                            print('Wybierz nauczyciela: ')
                                            choice = input()
                                            nauczycieleSpelniajacyWymagania[int(choice) - 1]
                                            good = True
                                        except:
                                            print('Spróbuj ponownie. \n')

                                    choice = int(choice) - 1
                                    if choice in conflictTeachers:
                                        index = conflictTeachers.index(choice)
                                        if conflictTeachers[index + 1] == 'busy':
                                            print('Nauczyciel jest zajęty. Przesuń godziny, a następnie spróbuj ponownie.\n')
                                        else:
                                            
                                            print('Nauczyciel nie uczy danej klasy. Czy chcesz dodać go do listy nauczycieli uczących klasę {}?'.format(chosenClass))
                                            wybur = input() 
                                            if wybur == '' or 'tak' or 'Tak':
                                                cursor.execute('SELECT uczoneKlasy FROM nauczyciele WHERE idnauczyciela = %s', (nauczycieleSpelniajacyWymagania[choice],))
                                                uczoneKlasy = cursor.fetchone()[0]
                                                if uczoneKlasy[len(uczoneKlasy)-1] != ';':
                                                    uczoneKlasy += ';'
                                                uczoneKlasy += chosenClass
                                                cursor.execute('UPDATE nauczyciele SET uczoneKlasy = %s WHERE idnauczyciela = %s', (uczoneKlasy, nauczycieleSpelniajacyWymagania[choice]))
                                                mydb.commit()
                                            else:
                                                editLesson(listaForEditorUse)
                                    else:
                                        print('Czy na pewno chcesz zmienić nauczyciela lekcji nr {} dla klasy {} na {}?'.format(str(fetch[0]), chosenClass, downloadTeacherData(nauczycieleSpelniajacyWymagania[choice])))
                                        wybur = input()
                                        if wybur != 'nie' or 'n' or 'Nie':
                                            editLesson(listaForEditorUse)
                                            return
                                        else:
                                            cursor.execute('UPDATE planlekcji SET idnauczyciela = %s WHERE idlekcji = %s', (nauczycieleSpelniajacyWymagania[choice], idLekcji)) 
                                            print('Aktualizacja planu udana.\n')

                                if amounttt % 5 == 2:
                                    print('Wybierz przedmiot, na który chcesz zamienić lekcję {} ({}) na godzinie lekcyjnej nr {}:'.format(fetch[2], downloadTeacherData(fetch[1]), fetch[0]))
                                    lajk = '%'+chosenClass+'%'
                                    cursor.execute('SELECT DISTINCT przedmiot FROM nauczyciele WHERE uczoneKlasy LIKE %s', (lajk, ))
                                    dostepnePrzedmioty = purify(cursor.fetchall())
                                    cursor.execute('SELECT DISTINCT przedmiot FROM nauczyciele')
                                    allPrzedmioty = purify(cursor.fetchall())
                                    unikalneNieUczonePrzedmioty = [a for a in allPrzedmioty if a not in dostepnePrzedmioty]
                                    del allPrzedmioty
                                    for x in range(len(dostepnePrzedmioty)):
                                        theSame = ''
                                        if dostepnePrzedmioty[x] == fetch[2]:
                                            theSame.join('  !! TEN SAM PRZEDMIOT !!')
                                        print('{}. {}'.format(str(x+1), dostepnePrzedmioty[x]))
                                    print('\nPRZEDMIOTY, KTÓRE NIE SĄ PRZYPISANE DO DANEJ KLASY\n')
                                    for y in range(len(unikalneNieUczonePrzedmioty)):
                                        print('{}. {}'.format(x+1+y+1, unikalneNieUczonePrzedmioty[y]))
                                    print('')
                                    good = False
                                    while good != True:
                                        try:
                                            print('Wybierz przedmiot: ')
                                            choice = input()
                                            choice = int(choice)
                                            good = True
                                        except:
                                            print('Spróbuj ponownie. \n')
                                    if choice > len(dostepnePrzedmioty)+len(unikalneNieUczonePrzedmioty):
                                        print('Spróbuj ponownie. \n')
                                    else:

                                        if choice <= len(dostepnePrzedmioty): 
                                            # tutaj robimy kiedy przedmiot jest juz od nauczyciela uczacego
                                            wybranyPrzedmiot = dostepnePrzedmioty[choice-1]
                                            cursor.execute('SELECT idnauczyciela FROM nauczyciele WHERE przedmiot = %s AND uczoneKlasy LIKE %s', (wybranyPrzedmiot, str('%'+GetComponentOfLessonToEdit['klasa']+'%')))
                                            print('Wybierz nauczyciela przedmiotu {} dla klasy {}:\n'.format(wybranyPrzedmiot, GetComponentOfLessonToEdit['klasa']))
                                            gitNauczyciele = purify(cursor.fetchall())
                                            for x in range(len(gitNauczyciele)):
                                                print('{}. {}'.format(str(x+1), gitNauczyciele[x]))
                                            good = False
                                            while good != True:
                                                try:
                                                    choice = input('Wybór: ')
                                                    choice = int(choice)
                                                    teacherID = gitNauczyciele[choice-1]
                                                    good = True
                                                except:
                                                    print('Spróbuj ponownie.\n')   
                                            cursor.execute('UPDATE planlekcji SET idnauczyciela = %s AND lekcja = %s WHERE idlekcji = %s', (teacherID, wybranyPrzedmiot, GetComponentOfLessonToEdit['idLekcji']))
                                            mydb.commit() 
                                            print('Aktualizacja planu udana.')


                                        elif choice <= len(dostepnePrzedmioty)+len(unikalneNieUczonePrzedmioty):
                                            # tutaj robimy procedure dodawania klasy do przedmiotu !!
                                            busyTeachers = []
                                            wybranyPrzedmiot = unikalneNieUczonePrzedmioty[choice-len(dostepnePrzedmioty)-1]
                                            cursor.execute('SELECT DISTINCT idnauczyciela FROM nauczyciele WHERE przedmiot = %s', (wybranyPrzedmiot, ))
                                            gitNauczyciele = purify(cursor.fetchall())
                                            print('Wybierz nauczyciela przedmiotu {} dla klasy {}:\n(spowoduje to dodanie wybranego nauczyciela do listy uczących daną klasę)\n'.format(wybranyPrzedmiot, GetComponentOfLessonToEdit['klasa']))
                                            for x in range(len(gitNauczyciele)):
                                                cursor.execute('SELECT nrgodziny FROM planlekcji WHERE idnauczyciela = %s AND dzien = %s', (gitNauczyciele[x], GetComponentOfLessonToEdit['rawDzien']))
                                                if (GetComponentOfLessonToEdit['nrGodziny'] in purify(cursor.fetchall())) == True: 
                                                    busyTeachers.append(gitNauczyciele[x])
                                                    cursor.execute('SELECT klasa FROM planlekcji WHERE idnauczyciela = %s AND nrgodziny = %s AND dzien = %s', (gitNauczyciele[x], GetComponentOfLessonToEdit['nrGodziny'], GetComponentOfLessonToEdit['rawDzien']))
                                                    klasa = cursor.fetchall()
                                                    print('{}. {}   !NAUCZYCIEL ZAJĘTY NA GODZINIE NR {} (KLASA {})!\n'.format(str(x+1), downloadTeacherData(gitNauczyciele[x]), GetComponentOfLessonToEdit['nrGodziny'], purify(klasa)[0]))
                                                    del klasa
                                                else:
                                                    print('{}. {}'.format(str(x+1), downloadTeacherData(gitNauczyciele[x])))
                                            good = False
                                            while good != True:
                                                try:
                                                    choice = input('Wybór: ')
                                                    choice = int(choice)
                                                    teacherID = gitNauczyciele[choice-1]
                                                    good = True
                                                except:
                                                    print('Spróbuj ponownie.\n')                           
                                            
                                            if (teacherID in busyTeachers) == True:
                                                print('Nauczyciel zajęty. Zwolnij termin i spróbuj ponownie.\n')
                                                Menu()
                                                return
                                            else:
                                                print('Czy na pewno chcesz dodać {} do listy nauczycieli uczących klasę {}?'.format(downloadTeacherData(teacherID), GetComponentOfLessonToEdit['klasa']))
                                                if input() == '' or 'tak' or 'TAK':
                                                    cursor.execute('SELECT uczoneKlasy FROM nauczyciele WHERE idnauczyciela = %s', (teacherID,))
                                                    uczoneKlasy = str(cursor.fetchone()[0])
                                                    if uczoneKlasy[len(uczoneKlasy)-1] != ';':
                                                        uczoneKlasy += ';'
                                                    uczoneKlasy += GetComponentOfLessonToEdit['klasa']
                                                    cursor.execute('UPDATE nauczyciele SET uczoneKlasy = %s WHERE idnauczyciela = %s', (uczoneKlasy, teacherID))
                                                    mydb.commit()
                                                    print('Nastąpi reset funkcji. Wpisz numer tej lekcji ( dla przypomnienia {} :) ), a potem wybierz tę lekcję ( dla przypomnienia {} :) ).'.format(str(numerLekcyjkiPilny), str(wybranyPrzedmiot)))
                                                    editLesson(listaForEditorUse)
                                                    pass
                                                    return

                                                else:
                                                    LessonsScheduleEditor()
                                            pass

                                        else: #koniec if ogolnego 
                                            print('Spróbuj ponownie. \n')                                
                                        
                                            

                                        
                                if amounttt % 5 == 3:
                                    sys.stdout.write('\033[2K\033[1G')
                                    print('Klasa', end='\r')
                                if amounttt % 5 == 4:
                                    sys.stdout.write('\033[2K\033[1G')
                                    print('Dzień', end='\r')
                            else:
                                waitUntil(keyboard.read_key() == "up", increment())
                                if amounttt % 5 == 0:
                                    sys.stdout.write('\033[2K\033[1G')
                                    print('Numer godziny', end='\r')
                                if amounttt % 5 == 1:
                                    sys.stdout.write('\033[2K\033[1G')
                                    print('Nauczyciel', end='\r')
                                if amounttt % 5 == 2:
                                    sys.stdout.write('\033[2K\033[1G')
                                    print('Przedmiot', end='\r')
                                if amounttt % 5 == 3:
                                    sys.stdout.write('\033[2K\033[1G')
                                    print('Klasa', end='\r')
                                if amounttt % 5 == 4:
                                    sys.stdout.write('\033[2K\033[1G')
                                    print('Dzień', end='\r')
                                


            def downloadTeacherData(idTeachera):
                cursor.execute('SELECT nazwisko, imie FROM nauczyciele WHERE idnauczyciela = %s', (idTeachera, ))
                fetch = cursor.fetchone()
                teacher = fetch[0] + ' ' + fetch[1]
                return teacher

            def printableTime(nrgodziny, what):
                if what == 'start':
                    cursor.execute('SELECT godzinaRozpoczecia FROM siatkagodzin WHERE nrgodziny = %s', (nrgodziny, ))
                else:
                    cursor.execute('SELECT godzinaZakonczenia FROM siatkagodzin WHERE nrgodziny = %s', (nrgodziny, ))
                return str(cursor.fetchone()[0])[:-3]
            def settingUpHoursSchedule():
                # cursor.execute('SELECT godzinaRozpoczecia FROM siatkagodzin WHERE nrgodziny = 1')
                # hour = str(cursor.fetchone()[0])[:-3] /// metoda konwersji godziny z MySQL na printowalną 
                print('\nWitamy w kreatorze godzin lekcyjnych! Ile godzin utworzyć?')
                for x in range(int(input())):
                    cursor.execute('INSERT INTO siatkagodzin(godzinaRozpoczecia, godzinaZakonczenia) VALUES(%s,%s)', (time(int(input('\nPodaj godzinę rozpoczęcia (HH): ')), int(input('Podaj minutę rozpoczęcia (MM): ')), 0), time(int(input('\nPodaj godzinę zakończenia (HH): ')), int(input('Podaj minutę zakończenia (MM): ')), 0)))
                    print('')
                mydb.commit()
                menuAdmin()


            getCurrentTime()
            print('  ______         _             _____      _                  _ _    ')
            print(' |  ____|       (_)           |  __ \    (_)                (_) |   ')
            print(' | |__ _   _ ___ _  ___  _ __ | |  | |_____  ___ _ __  _ __  _| | __')
            print(" |  __| | | / __| |/ _ \| '_ \| |  | |_  / |/ _ \ '_ \| '_ \| | |/ /")
            print(' | |  | |_| \__ \ | (_) | | | | |__| |/ /| |  __/ | | | | | | |   < ')
            print(" |_|   \__,_|___/_|\___/|_| |_|_____//___|_|\___|_| |_|_| |_|_|_|\_\\")
            print(' ')
            print('Witaj w FusionDziennik! Jest godzina',currHour+'.')
            StStepLogin()
        except:
            print('Wystąpił krytyczny błąd. \n\n\n')
MAIN()