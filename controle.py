from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

global_id = 0

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
    formulario.close()
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


def gerar_pdf():
    cursor = banco_de_dados.cursor() #Cria o cursor
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y=0

    pdf = canvas.Canvas('listagem_produtos.pdf')
    pdf.setFont('Times-Bold', 25)
    pdf.drawString(200,800, 'Produtos cadastrados: ')
    pdf.setFont('Times-Bold', 18)

    pdf.drawString(10,750, 'ID')
    pdf.drawString(110,750, 'CÓDIGO')
    pdf.drawString(210,750, 'DESCRIÇÃO')
    pdf.drawString(310,750, 'PREÇO')
    pdf.drawString(410,750, 'CATEGORIA')

 
    for i in range(0, len(dados_lidos)):
        y += 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print('PDF foi gerado com sucesso!')


def excluir_dados():
    linha = listagem.tableWidget.currentRow()
    listagem.tableWidget.removeRow(linha)

    cursor = banco_de_dados.cursor() #Cria o cursor
    cursor.execute('SELECT id FROM produtos')
    id = cursor.fetchall()
    valor_id = id[linha][0]
    cursor.execute(f'DELETE FROM produtos WHERE id = {str(valor_id)}')
    banco_de_dados.commit()


def editar_dados():
    global global_id

    linha = listagem.tableWidget.currentRow()

    cursor = banco_de_dados.cursor() #Cria o cursor
    cursor.execute('SELECT id FROM produtos')
    id = cursor.fetchall()
    valor_id = id[linha][0]
    cursor.execute('SELECT * FROM produtos WHERE id =' + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    global_id = valor_id

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))


def salvar_dados_editados():
    #captura o número do ID global
    global global_id
    #Valor presente nos campos da tela_editar
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    #Atualizar os dados do banco de dados
    cursor = banco_de_dados.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', preco = '{}', categoria = '{}', descricao = '{}' WHERE id = '{}'".format(codigo,preco,categoria,descricao,global_id))
    banco_de_dados.commit()
    print('='*20)
    print('Produto alterado com sucesso!')
    print('='*20)
    #Atualizar as janelas
    tela_editar.close()
    listagem.close()
    chama_listagem()
    

    

app=QtWidgets.QApplication([])#Cria a aplicação
formulario=uic.loadUi("formulario01.ui")#Cria o formulário
listagem=uic.loadUi("listagem.ui")
tela_editar = uic.loadUi('tela_salvar.ui')
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_listagem)
listagem.pushButton.clicked.connect(gerar_pdf)
listagem.pushButton_2.clicked.connect(excluir_dados)
listagem.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)




formulario.show()
app.exec()