def createTree():
    treeTaskCreate.delete(*treeTaskCreate.get_children())
    f = open("files/tasksDoing.txt", "r", encoding="utf-8")
    ficheiro = f.readlines()
    f.close()
    for linha in ficheiro:
        campos=linha.split(";")
        for i in range(currentUser):
            if (currentUset[i]==campos[0]):
                treeTaskCreate.insert("", "end", values=(campos[1], campos[2], campos[3],campos[4]))

    f = open("file/tasksDone.txt", "r", encoding="utf-8")
    ficheiro = f.readlines()
    f.close()
    for linha in ficheiro:
        campos=linha.split(";")
        for i in range(currentUser):
            if (currentUset[i]==campos[0]):
                treeTaskCreate.insert("", "end", values=(campos[1], campos[2], campos[3],campos[4]))

    f = open("files/tasksNotDone.txt", "r", encoding="utf-8")
    ficheiro = f.readlines()
    f.close()
    for linha in ficheiro:
        campos=linha.split(";")
        for i in range(currentUser):
            if (currentUset[i]==campos[0]):
                treeTaskCreate.insert("", "end", values=(campos[1], campos[2], campos[3],campos[4]))



