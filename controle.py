from PyQt5 import uic, QtWidgets
import mysql.connector

#Cria o banco de dados para ser usado na aplicação.
banco_de_dados = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='cadastro_produtos'
)

def funcao_principal():
    #Resgata os valores dos campos do formulário
    codigo = formulario.lineEdit.text()
    descricao = formulario.lineEdit_2.text()
    preco = formulario.lineEdit_3.text()
    categoria = ''

    #Checa qual opção esta marcada no radio Button
    if formulario.radioButton.isChecked():
        categoria = 'Informática'
    elif formulario.radioButton_2.isChecked():
        categoria = 'Alimentos'
    else:
        categoria = 'Eletrônicos'

    #coloca os dados inseridos, no terminal
    print('='*30)
    print('Código: ', codigo)
    print('Descrição: ', descricao)
    print('Categoria: ', categoria)
    print('Preço: ', preco)
    print('='*30)

    cursor = banco_de_dados.cursor() #Cria o cursor
    comando_SQL = "INSERT INTO produtos (codigo,descricao,categoria,preco) VALUES (%s,%s,%s,%s)"#Insere os dados no banco de dados MySQL
    dados = (str(codigo), str(descricao), str(categoria), str(preco))#Insere os valores 
    cursor.execute(comando_SQL,dados)
    banco_de_dados.commit()
    
    #Limpa os campos após o envio
    formulario.lineEdit.setText('')
    formulario.lineEdit_2.setText('')
    formulario.lineEdit_3.setText('')
    formulario.radioButton.setCheckable(False)


def chama_listagem():
    listagem.show()

    cursor = banco_de_dados.cursor() #Cria o cursor
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    print(dados_lidos)

    listagem.tableWidget.setRowCount(len(dados_lidos))
    listagem.tableWidget.setColumnCount(5)

    for linha in range(0, len(dados_lidos)):
        for coluna in range(0,5):
            listagem.tableWidget.setItem(linha,coluna,QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))


app=QtWidgets.QApplication([])#Cria a aplicação
formulario=uic.loadUi("formulario01.ui")#Cria o formulário
listagem=uic.loadUi("listagem.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_listagem)


formulario.show()
app.exec()