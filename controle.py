from PyQt5 import uic, QtWidgets
import mysql.connector

banco_de_dados = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='cadastro_produtos'
)

def funcao_principal():
    codigo = formulario.lineEdit.text()
    descricao = formulario.lineEdit_2.text()
    preco = formulario.lineEdit_3.text()
    categoria = ''

    if formulario.radioButton.isChecked():
        categoria = 'Informática'
    elif formulario.radioButton_2.isChecked():
        categoria = 'Alimentos'
    else:
        categoria = 'Eletrônicos'

    print('='*30)
    print('Código: ', codigo)
    print('Descrição: ', descricao)
    print('Categoria: ', categoria)
    print('Preço: ', preco)
    print('='*30)

    cursor = banco_de_dados.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,categoria,preco) VALUES (%s,%s,%s,%s)"
    dados = (str(codigo), str(descricao), str(categoria), str(preco))
    cursor.execute(comando_SQL,dados)
    banco_de_dados.commit()


app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario01.ui")
formulario.pushButton.clicked.connect(funcao_principal)

formulario.show()
app.exec()