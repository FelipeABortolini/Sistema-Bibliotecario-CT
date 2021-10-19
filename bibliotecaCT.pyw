from abc import abstractproperty
from os import truncate
from re import L
import eel
import sqlite3
import hashlib

# -------------------- CLASSE -------------------- #
class Constantes:
    def __init__(self):
        self.tela_atual = ""
        self.tela_anterior = ""
        self.periodo = 0
        self.valor = 0.0

    def set_periodo(self, status):
        self.periodo = status

    def set_valor(self, status):
        self.valor = status

# -------------------- OBJETOS -------------------- #
const = Constantes()

# -------------------- FUNÇÕES -------------------- #

@eel.expose
def atualizaParam(periodo, valor):
    if periodo != 0: const.set_periodo(periodo)
    if valor != 0: const.set_valor(valor)

    sql = f'UPDATE parametros SET periodo="{periodo}", valor="{valor}"'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print('Erro ao atualizar parâmetros no banco de dados!')
    else:
        print('Parâmetros atualizados no banco de dados com sucesso!')

    return True


@eel.expose
def atualizaParamVal(valor):
    if valor != 0: const.set_valor(valor)

    sql = f'UPDATE parametros SET valor="{valor}"'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print('Erro ao atualizar parâmetros no banco de dados!')
    else:
        print('Parâmetros atualizados no banco de dados com sucesso!')

    return True


@eel.expose
def atualizaParamPer(periodo):
    if periodo != 0: const.set_periodo(periodo)

    sql = f'UPDATE parametros SET periodo="{periodo}"'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print('Erro ao atualizar parâmetros no banco de dados!')
    else:
        print('Parâmetros atualizados no banco de dados com sucesso!')

    return True


@eel.expose
def getParam():
    lista = []

    lista.append(const.periodo)
    lista.append(const.valor)

    return lista


def initParam():
    sql = 'SELECT * FROM parametros'
    dados = None

    try:
        cursor.execute(sql)
        dados = cursor.fetchall()
    except:
        print(f'Erro ao buscar parâmetros no banco de dados!')
    else:
        print(f'Parâmetros encontrado no banco de dados com sucesso!')

    const.set_periodo(dados[0][0])
    const.set_valor(dados[0][1])


@eel.expose
def altera_tela_atual(nome_tela):
    const.tela_anterior = const.tela_atual
    const.tela_atual = nome_tela
    print(f'Tela anterior: {const.tela_anterior}')
    print(f'Tela atual: {const.tela_atual}')


@eel.expose
def busca_livro_id(id):

    sql = f"SELECT * FROM livro WHERE id={id}"
    #l = []
    dados = None

    try:
        cursor.execute(sql)
        dados = cursor.fetchall()
    except:
        print(f'Erro ao buscar livro no banco de dados!')
    else:
        print(f'Livro encontrado no banco de dados com sucesso!')

    '''for i in dados:
        dictDados = {'id': i[0], 'nome': i[1], 'autor': i[2], 'exemplares': i[3], 'disponiveis': i[4]}
        l.append(dictDados)'''

    #print(dados)
    return dados


@eel.expose
def atualizaDisponiveis(array):

    for id_livro in array:

        sql = f"SELECT disponiveis FROM livro WHERE id={id_livro}"
        dados = None

        try:
            cursor.execute(sql)
            dados = cursor.fetchall()
        except:
            print(f'Erro ao buscar quantos livros tem disponiveis no banco de dados!')
        else:
            print(f'Quantidade de livros disponiveis encontrados com sucesso!')

        disponiveis = dados[0][0]

        disponiveis-=1

        sql = f'UPDATE livro SET disponiveis="{disponiveis}" WHERE id={id_livro}'

        try:
            cursor.execute(sql)
            banco.commit()
        except:
            print('Erro ao atualizar livros disponiveis no banco de dados!')
        else:
            print('Livros disponiveis atualizados no banco de dados com sucesso!')


@eel.expose
def atualizaDisponiveisUp(array):

    for id_aluguel in array:

        sql = f"SELECT id_livro FROM aluguel WHERE id={id_aluguel}"
        dados = None

        try:
            cursor.execute(sql)
            dados = cursor.fetchall()
        except:
            print(f'Erro ao buscar id_livro no banco de dados!')
        else:
            print(f'id_livro encontrado com sucesso!')

        #print(f'dados: {dados}')
        id_livro = dados[0][0]

        sql = f"SELECT disponiveis FROM livro WHERE id={id_livro}"
        dados = None

        try:
            cursor.execute(sql)
            dados = cursor.fetchall()
        except:
            print(f'Erro ao buscar quantos livros tem disponiveis no banco de dados!')
        else:
            print(f'Quantidade de livros disponiveis encontrados com sucesso!')

        #print(f'dados: {dados}')
        disponiveis = dados[0][0]

        disponiveis+=1

        sql = f'UPDATE livro SET disponiveis="{disponiveis}" WHERE id={id_livro}'

        try:
            cursor.execute(sql)
            banco.commit()
        except:
            print('Erro ao atualizar livros disponiveis no banco de dados!')
        else:
            print('Livros disponiveis atualizados no banco de dados com sucesso!')


@eel.expose
def regitra_editavel_bd(array):
    id = array[0]

    sql = f"SELECT * FROM livro WHERE id={id}"
    dados = None

    try:
        cursor.execute(sql)
        dados = cursor.fetchall()
    except:
        print(f'Erro ao buscar livro no banco de dados!')
    else:
        print(f'Livro encontrado no banco de dados com sucesso!')

    sql = f'DELETE FROM editavel WHERE rem=1'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print('Erro ao tentar remover regitros de editavel!')
    else:
        print('Registros de editavel removidos com sucesso!')

    sql = f'INSERT INTO editavel (nome, autor, exemplares, disponiveis, rem, id) VALUES ("{dados[0][1]}", "{dados[0][2]}", {dados[0][3]}, {dados[0][4]}, 1, {dados[0][0]})'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print('Erro ao tentar inserir editável no banco de dados!')
    else:
        print('Editável inserido no banco de dados com sucesso!')


@eel.expose
def busca_editavel():
    sql = f"SELECT * FROM editavel"
    dados = None

    try:
        cursor.execute(sql)
        dados = cursor.fetchall()
    except:
        print(f'Erro ao buscar livro no banco de dados!')
    else:
        print(f'Livro encontrado no banco de dados com sucesso!')

    #print(f'dados {dados}')
    return dados


@eel.expose
def editar_livro(nome, autor, exemplares, disponiveis, id):

    sql = f'UPDATE livro SET nome="{nome}", autor="{autor}", exemplares={exemplares}, disponiveis={disponiveis} WHERE id={id}'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print('Erro ao tentar editar o livro no banco de dados!')
        eel.mensagem('Erro ao tentar editar livro!')
    else:
        print('Livro editado no banco de dados com sucesso!')
        eel.mensagem('Livro editado com sucesso!')


@eel.expose
def buscaAluno(info, funcao):

    lista = []
    dados = busca_retiradas()

    for d in dados:
        if(info in d['nome_aluno']):
            lista.append(d['id_ret'])
            lista.append(f"{d['nome_aluno']} | {d['turma_aluno']} | {d['nome_livro']} | {d['autor_livro']} | {d['data_retirada'][8:10]}/{d['data_retirada'][5:7]}/{d['data_retirada'][0:4]} | {d['data_entrega'][8:10]}/{d['data_entrega'][5:7]}/{d['data_entrega'][0:4]}")

    lista.append(funcao)

    #print(lista)
    return lista


@eel.expose
def buscaPesquisa(info, funcao):

    l = []

    if funcao == 'emAberto' or funcao == 'historico':

        #----------- FROM ALUNO

        sql = f"SELECT * FROM aluno WHERE nome LIKE '%{info}%' OR turma LIKE '%{info}%'"
        dados_aluno_from_aluno = None
        lista_dados_alunos_from_alunos = []
        lista_dados_aluguel_from_aluno = []
        lista_dados_livro_from_aluno = []

        try:
            cursor.execute(sql)
            dados_aluno_from_aluno = cursor.fetchall()
            #print(f'dados_aluno_from_aluno: {dados_aluno_from_aluno}')
            for i in dados_aluno_from_aluno:
                lista_dados_alunos_from_alunos.append(i)
        except:
            print(f'dados_aluno_from_aluno fail!')
        else:
            print(f'dados_aluno_from_aluno sucesso!')

        if(len(lista_dados_alunos_from_alunos) != 0):
            for i in lista_dados_alunos_from_alunos:
                if funcao == 'emAberto':
                    sql = f"SELECT * FROM aluguel WHERE id_aluno='{i[0]}'"
                elif funcao == 'historico':
                    sql = f"SELECT * FROM historico WHERE nome_aluno='{i[1]}'"
                dados_aluguel_from_aluno = None

                try:
                    cursor.execute(sql)
                    dados_aluguel_from_aluno = cursor.fetchall()
                    lista_dados_aluguel_from_aluno.append(dados_aluguel_from_aluno)
                    #print(f'dados_aluguel_from_aluno: {dados_aluguel_from_aluno}')
                except:
                    print(f'dados_aluguel_from_aluno fail!')
                else:
                    print(f'dados_aluguel_from_aluno sucesso!')

                if(len(dados_aluguel_from_aluno) != 0):
                    for i in dados_aluguel_from_aluno:
                        #print(f'i: {i}')
                        if funcao == 'emAberto':
                            sql = f"SELECT * FROM livro WHERE id='{i[1]}'"
                        elif funcao == 'historico':
                            sql = f"SELECT * FROM historico_livros WHERE nome='{i[3]}' AND autor='{i[4]}'"

                        dados_livro_from_aluno = None

                        try:
                            cursor.execute(sql)
                            dados_livro_from_aluno = cursor.fetchall()
                            lista_dados_livro_from_aluno.append(dados_livro_from_aluno)
                            #print(f'dados_livro_from_aluno: {dados_livro_from_aluno}')
                        except:
                            print(f'dados_livro_from_aluno fail!')
                        else:
                            print(f'dados_livro_from_aluno sucesso!')
                else:
                    if funcao == 'emAberto':
                        lista_dados_livro_from_aluno.append([])

        #print(f'lista_id_alunos_from_alunos: {lista_dados_alunos_from_alunos}')
        #print(f'lista_dados_aluguel_from_aluno: {lista_dados_aluguel_from_aluno}')
        #print(f'lista_dados_livro_from_aluno: {lista_dados_livro_from_aluno}')

        #----------- FROM LIVRO

        if funcao == 'emAberto':
            sql = f"SELECT * FROM livro WHERE nome LIKE '%{info}%'"
        elif funcao == 'historico':
            sql = f"SELECT * FROM historico_livros WHERE nome LIKE '%{info}%'"

        dados_livro_from_livro = None
        lista_dados_livros_from_livros = []
        lista_dados_aluguel_from_livros = []
        lista_dados_aluno_from_livros = []

        try:
            cursor.execute(sql)
            dados_livro_from_livro = cursor.fetchall()
            #print(f'dados_livro_from_livro: {dados_livro_from_livro}')
            for i in dados_livro_from_livro:
                lista_dados_livros_from_livros.append(i)
        except:
            print(f'dados_livro_from_livro fail!')
        else:
            print(f'dados_livro_from_livro sucesso!')

        if(len(lista_dados_livros_from_livros) != 0):
            for i in lista_dados_livros_from_livros:
                if funcao == 'emAberto':
                    sql = f"SELECT * FROM aluguel WHERE id_livro='{i[0]}'"
                elif funcao == 'historico':
                    sql = f"SELECT * FROM historico WHERE livro='{i[1]}' AND autor='{i[2]}'"
                dados_aluguel_from_livro = None

                try:
                    cursor.execute(sql)
                    dados_aluguel_from_livro = cursor.fetchall()
                    lista_dados_aluguel_from_livros.append(dados_aluguel_from_livro)
                    #print(f'dados_aluguel_from_livro: {dados_aluguel_from_livro}')
                except:
                    print(f'dados_aluguel_from_livro fail!')
                else:
                    print(f'dados_aluguel_from_livro sucesso!')

                if(len(dados_aluguel_from_livro) != 0):
                    for i in dados_aluguel_from_livro:
                        if funcao == 'emAberto':
                            sql = f"SELECT * FROM aluno WHERE id='{i[2]}'"
                        elif funcao == 'historico':
                            sql = f"SELECT * FROM aluno WHERE nome='{i[1]}'"

                        dados_aluno_from_livro = None

                        try:
                            cursor.execute(sql)
                            dados_aluno_from_livro = cursor.fetchall()
                            lista_dados_aluno_from_livros.append(dados_aluno_from_livro)
                            #print(f'dados_aluno_from_livro: {dados_aluno_from_livro}')
                        except:
                            print(f'dados_aluno_from_livro fail!')
                        else:
                            print(f'dados_aluno_from_livro sucesso!')

        #print(f'lista_id_livros_from_livros: {lista_dados_livros_from_livros}')
        #print(f'lista_dados_aluguel_from_livros: {lista_dados_aluguel_from_livros}')
        #print(f'lista_dados_aluno_from_livros: {lista_dados_aluno_from_livros}')

    #-------- NO 'emAberto' NO 'historico'

    else:
        sql = f"SELECT * FROM livro WHERE nome LIKE '%{info}%' OR autor LIKE '%{info}%'"
        dados_livro = None

        try:
            cursor.execute(sql)
            dados_livro = cursor.fetchall()
            #print(f'dados_livro: {dados_livro}')
        except:
            print(f'Erro ao buscar pesquisa no banco de dados!')
        else:
            print(f'Pesquisa encontrada no banco de dados com sucesso!')

    if funcao == 'emAberto' or funcao == 'historico':

        #-- FROM ALUNO
        for i in lista_dados_alunos_from_alunos:
            #print(f'FROM ALUNO i: {i}')
            for j in lista_dados_aluguel_from_aluno:
                #print(f'FROM ALUNO j: {j}')
                for k in lista_dados_livro_from_aluno:
                    #print(f'FROM ALUNO k: {k}')
                    if(len(j) != 0 and len(k) != 0):
                        for n in j:
                            #print(f'FROM ALUNO n: {n}')
                            for m in k:
                                #print(f'FROM ALUNO m: {m}')
                                if i[0] == n[2] and n[1] == m[0] and funcao == 'emAberto':
                                    #print('entrou')
                                    dictDados = {'id_aluguel': n[0], 'id_aluno': i[0], 'nome_aluno': i[1], 'turma': i[2], 'id_livro': m[0], 'nome_livro': m[1], 'autor': m[2], 'exemplares': m[3], 'disponiveis': m[4], 'data_retirada': n[3], 'prazo_entrega': n[4]}

                                    insereEmL = True

                                    for p in l:
                                        if p['id_aluguel'] == dictDados['id_aluguel']:
                                            insereEmL = False
                                            break
                                    if insereEmL:
                                        l.append(dictDados)
                                    #l.append(dictDados)
                                    #print(f'l: {l}')

                                if i[1] == n[1] and n[3] == m[1] and n[4] == m[2] and funcao == 'historico':
                                    #print('entrou')
                                    dictDados = {'id_historico': n[0], 'id_aluno': i[0], 'nome_aluno': i[1], 'turma': i[2], 'id_livro': m[0], 'nome_livro': m[1], 'autor': m[2], 'data_retirada': n[5], 'prazo_entrega': n[6], 'data_devolucao': n[7], 'multa': n[8]}

                                    insereEmL = True

                                    for p in l:
                                        if p['id_historico'] == dictDados['id_historico']:
                                            insereEmL = False
                                            break
                                    if insereEmL:
                                        l.append(dictDados)
                                    #l.append(dictDados)
                                    #print(f'l: {l}')

        #-- FROM LIVRO
        for i in lista_dados_livros_from_livros:
            #print(f'FROM LIVRO i: {i}')
            for j in lista_dados_aluguel_from_livros:
                #print(f'FROM LIVRO j: {j}')
                for k in lista_dados_aluno_from_livros:
                    #print(f'FROM LIVRO k: {k}')
                    if(len(j) != 0 and len(k) != 0):
                        for n in j:
                            #print(f'FROM LIVRO n: {n}')
                            for m in k:
                                #print(f'FROM LIVRO m: {m}')
                                if i[0] == n[1] and n[2] == m[0] and funcao == 'emAberto':
                                    #print('entrou')
                                    dictDados = {'id_aluguel': n[0], 'id_aluno': m[0], 'nome_aluno': m[1], 'turma': m[2], 'id_livro': i[0], 'nome_livro': i[1], 'autor': i[2], 'exemplares': i[3], 'disponiveis': i[4], 'data_retirada': n[3], 'prazo_entrega': n[4]}

                                    insereEmL = True

                                    for p in l:
                                        if p['id_aluguel'] == dictDados['id_aluguel']:
                                            insereEmL = False
                                            break
                                    if insereEmL:
                                        l.append(dictDados)

                                if i[1] == n[3] and n[1] == m[1] and i[2] == n[4] and funcao == 'historico':
                                    #print('entrou')
                                    dictDados = {'id_historico': n[0], 'id_aluno': m[0], 'nome_aluno': m[1], 'turma': m[2], 'id_livro': i[0], 'nome_livro': i[1], 'autor': i[2], 'data_retirada': n[5], 'prazo_entrega': n[6], 'data_devolucao': n[7], 'multa': n[8]}

                                    insereEmL = True

                                    for p in l:
                                        if p['id_historico'] == dictDados['id_historico']:
                                            insereEmL = False
                                            break
                                    if insereEmL:
                                        l.append(dictDados)

    else:
        for i in dados_livro:
            dictDados = {'id_livro': i[0], 'nome_livro': i[1], 'autor': i[2], 'exemplares': i[3], 'disponiveis': i[4]}
            l.append(dictDados)
        organizar_alfabeticamente(l)

    lista = []

    if funcao=='emAberto':
        for d in l:
            lista.append(d['id_aluguel'])
            lista.append(f"{d['nome_aluno']} | {d['turma']} | {d['nome_livro']} | {d['autor']} | {d['data_retirada'][8:10]}/{d['data_retirada'][5:7]}/{d['data_retirada'][0:4]} | {d['prazo_entrega'][8:10]}/{d['prazo_entrega'][5:7]}/{d['prazo_entrega'][0:4]}")

    elif funcao=='historico':

        l = sorted(l, key=lambda k: k['data_devolucao'], reverse=True)

        for d in l:
            lista.append(d['id_historico'])
            lista.append(f"{d['nome_aluno']} | {d['turma']} | {d['nome_livro']} | {d['autor']} | {d['data_retirada'][8:10]}/{d['data_retirada'][5:7]}/{d['data_retirada'][0:4]} | {d['prazo_entrega'][8:10]}/{d['prazo_entrega'][5:7]}/{d['prazo_entrega'][0:4]} | {d['data_devolucao'][8:10]}/{d['data_devolucao'][5:7]}/{d['data_devolucao'][0:4]} | R$ {d['multa']:.2f}")

    else:
        i = 0
        for d in l:
            lista.append(d['id_livro'])
            if(funcao=='retirada' or funcao=='remover'):
                lista.append(i)
            lista.append(f"{d['nome_livro']} | {d['autor']} | {d['exemplares']}")
            i+=1

    lista.append(funcao)

    #print(lista)
    return lista


@eel.expose
def buscaDateHist(marcado, info):
    if marcado == 'retirada':
        sql = f"SELECT * FROM historico WHERE data_retirada='{info}'"
        dados = None

        try:
            cursor.execute(sql)
            dados = cursor.fetchall()
            #print(dados)
        except:
            print(f'Erro ao buscar data_retirada no banco de dados!')
        else:
            print(f'data_retirada pesquisada no banco de dados com sucesso!')

    elif marcado == 'prazo':
        sql = f"SELECT * FROM historico WHERE prazo_entrega='{info}'"
        dados = None

        try:
            cursor.execute(sql)
            dados = cursor.fetchall()
            #print(dados)
        except:
            print(f'Erro ao buscar prazo_entrega no banco de dados!')
        else:
            print(f'prazo_entrega pesquisado no banco de dados com sucesso!')

    elif marcado == 'entrega':
        sql = f"SELECT * FROM historico WHERE data_devolucao='{info}'"
        dados = None

        try:
            cursor.execute(sql)
            dados = cursor.fetchall()
            #print(dados)
        except:
            print(f'Erro ao buscar data_devolucao no banco de dados!')
        else:
            print(f'data_devolucao pesquisada no banco de dados com sucesso!')

    l = []

    for i in dados:
        dictDados = {'id': i[0], 'nome_aluno': i[1], 'turma': i[2], 'livro': i[3], 'autor': i[4], 'data_retirada': i[5], 'prazo_entrega': i[6], 'data_devolucao': i[7], 'multa': i[8]}
        l.append(dictDados)

    lista = []

    for d in l:
        lista.append(d['id'])
        lista.append(f"{d['nome_aluno']} | {d['turma']} | {d['livro']} | {d['autor']} | {d['data_retirada'][8:10]}/{d['data_retirada'][5:7]}/{d['data_retirada'][0:4]} | {d['prazo_entrega'][8:10]}/{d['prazo_entrega'][5:7]}/{d['prazo_entrega'][0:4]} | {d['data_devolucao'][8:10]}/{d['data_devolucao'][5:7]}/{d['data_devolucao'][0:4]} | R$ {d['multa']:.2f}")

    lista.append('historico')

    #print(lista)
    return lista


@eel.expose
def registraAluno(nome, turma):

    sql = f"SELECT * FROM aluno WHERE nome='{nome}'"
    dados = None

    try:
        cursor.execute(sql)
        dados = cursor.fetchall()
    except:
        print(f'Erro ao buscar aluno no banco de dados!')
    else:
        print(f'Aluno pesquisado no banco de dados com sucesso!')

    if len(dados) == 0:

        sql = f'INSERT INTO aluno (nome, turma) VALUES ("{nome}", "{turma}")'

        try:
            cursor.execute(sql)
            banco.commit()
        except:
            print('Erro ao cadastrar aluno no banco de dados!')
        else:
            print('Aluno cadastrado no banco de dados com sucesso!')

    elif dados[0][2] != int(turma):

        sql = f'UPDATE aluno SET turma="{turma}" WHERE nome="{nome}"'

        try:
            cursor.execute(sql)
            banco.commit()
        except:
            print('Erro ao atualizar turma do aluno no banco de dados!')
        else:
            print('Turma do aluno atualizada no banco de dados!')


        sql = f'UPDATE historico SET turma="{turma}" WHERE nome="{nome}"'

        try:
            cursor.execute(sql)
            banco.commit()
        except:
            print('Erro ao atualizar turma do aluno no histórico do banco de dados!')
        else:
            print('Turma do aluno atualizada no histórico do banco de dados!')


    else:
        print('Aluno já estava cadastrado no banco de dados!')


@eel.expose
def testeAlugueisAluno(array, nomeGuerra):

    sql = f"SELECT id FROM aluno WHERE nome='{nomeGuerra}'"
    id_aluno = None

    try:
        cursor.execute(sql)
        id_aluno = cursor.fetchall()
    except:
        print(f'Erro ao buscar id do aluno no banco de dados!')
        return False
    else:
        print(f'Id do aluno encontrado com sucesso!')

    sql = f"SELECT COUNT(id) FROM aluguel WHERE id_aluno='{id_aluno[0][0]}'"
    num_alugueis = None

    try:
        cursor.execute(sql)
        num_alugueis = cursor.fetchall()
    except:
        print(f'Erro ao buscar quantidade de alugueis do aluno no banco de dados!')
        return False
    else:
        print(f'Quantidade de alugueis do aluno encontrado com sucesso!')

    num_alugados = num_alugueis[0][0]

    num_posterior_alugados = num_alugados + len(array)

    if(num_posterior_alugados > 3):
        eel.mensagem('O aluno não pode retirar essa quantidade de livros pois, somando com os livros pendentes do mesmo, o total é maior que 3. Cada aluno pode ter no máximo 3 livros pendentes para entrega!')
        return False

    return True


@eel.expose
def registraRetirada(array, nomeGuerra, dataRetirada, dataEntrega):

    sql = f"SELECT id FROM aluno WHERE nome='{nomeGuerra}'"
    id_aluno = None

    try:
        cursor.execute(sql)
        id_aluno = cursor.fetchall()
    except:
        print(f'Erro ao buscar id do aluno no banco de dados!')
        eel.mensagem('Erro ao registrar retirada no banco de dados, tente novamente!')
        return False
    else:
        print(f'Id do aluno encontrado com sucesso!')

    for id_livro in array:

        sql = f'INSERT INTO aluguel (id_livro, id_aluno, data_retirada, data_entrega) VALUES ({id_livro}, {id_aluno[0][0]}, "{dataRetirada}", "{dataEntrega}")'

        try:
            cursor.execute(sql)
            banco.commit()
        except:
            print('Erro ao regitrar retirada no banco de dados!')
            eel.errRegistrarRetirada()
            return False
        else:
            print('Retirada regitrada no banco de dados com sucesso!')

    if(len(array) == 1):
        eel.mensagem('Retirada registrada com sucesso!')
    elif(len(array) > 1):
        eel.mensagem('Retiradas registrada com sucesso!')

    return True


@eel.expose
def removerLivros(livros):
    for id in livros:

        sql = f'SELECT nome FROM livro WHERE id="{id}"'

        try:
            cursor.execute(sql)
            nome = cursor.fetchall()
        except:
            print(f'Erro ao buscar o nome do livro!')

        sql = f'DELETE FROM livro WHERE id="{id}" AND exemplares = disponiveis'

        try:
            cursor.execute(sql)
            banco.commit()
        except:
            print(f'Erro ao tentar remover livro com id = {id} no banco de dados!')
            eel.mensagem(f'Erro ao tentar remover o livro" {nome}" do banco de dados, verifique se o há algum exemplar pendente para devolução!')
        else:
            print(f'Livro com id = {id} removido no banco de dados com sucesso!')
            eel.mensagem(f'Livro removido do banco de dados com sucesso!')
            return True

        return False


@eel.expose
def busca(tipo):

    lista = []

    if tipo=='remover':

        i = 0
        dados = busca_livros_all()
        for d in dados:
            lista.append(d['id'])
            lista.append(i)
            lista.append(f"{d['nome_livro']} | {d['autor']} | {d['exemplares']}")
            i+=1

    if tipo=='remover1':

        i = 0
        dados = busca_livros_all()
        for d in dados:
            lista.append(d['id'])
            lista.append(i)
            lista.append(f"{d['exemplares']}")
            lista.append(f"{d['disponiveis']}")
            i+=1

    if tipo=='editar':

        dados = busca_livros_all()
        for d in dados:
            lista.append(d['id'])
            lista.append(f"{d['nome_livro']} | {d['autor']} | {d['exemplares']}")

    if tipo=='listar':

        dados = busca_livros_all()
        for d in dados:
            lista.append(d['id'])
            lista.append(f"{d['nome_livro']} | {d['autor']} | {d['exemplares']} | {d['disponiveis']}")

    if tipo=='retirada':

        i = 0
        dados = busca_livros_all()
        for d in dados:
            lista.append(d['id'])
            lista.append(i)
            lista.append(f"{d['nome_livro']} | {d['autor']}")
            i+=1

    if tipo=='retirada1':

        i = 0
        dados = busca_livros_all()
        for d in dados:
            lista.append(d['id'])
            lista.append(i)
            lista.append(f"{d['disponiveis']}")
            i+=1

    if tipo=='devolucao':

        dados = busca_retiradas()

        for d in dados:
            lista.append(d['id_ret'])
            lista.append(f"{d['nome_aluno']} | {d['turma_aluno']} | {d['nome_livro']} | {d['autor_livro']} | {d['data_retirada'][8:10]}/{d['data_retirada'][5:7]}/{d['data_retirada'][0:4]} | {d['data_entrega'][8:10]}/{d['data_entrega'][5:7]}/{d['data_entrega'][0:4]}")

    if tipo=='emAberto':

        dados = busca_retiradas()

        for d in dados:
            lista.append(d['id_ret'])
            lista.append(f"{d['nome_aluno']} | {d['turma_aluno']} | {d['nome_livro']} | {d['autor_livro']} | {d['data_retirada'][8:10]}/{d['data_retirada'][5:7]}/{d['data_retirada'][0:4]} | {d['data_entrega'][8:10]}/{d['data_entrega'][5:7]}/{d['data_entrega'][0:4]}")

    if tipo=='historico':

        dados = busca_historico()
        #print(dados)

        for d in dados:
            lista.append(d['id'])
            lista.append(f"{d['nome_aluno']} | {d['turma']} | {d['livro']} | {d['autor']} | {d['data_retirada'][8:10]}/{d['data_retirada'][5:7]}/{d['data_retirada'][0:4]} | {d['prazo_entrega'][8:10]}/{d['prazo_entrega'][5:7]}/{d['prazo_entrega'][0:4]} | {d['data_devolucao'][8:10]}/{d['data_devolucao'][5:7]}/{d['data_devolucao'][0:4]} | R$ {d['multa']:.2f}")

    if(tipo!='retirada1' and tipo!='remover1'):
        lista.append(tipo)

    return lista


@eel.expose
def busca_select(select):

    lista = []
    dados = busca_historico(select)
    print(dados)

    for d in dados:
        lista.append(d['id'])
        lista.append(f"{d['nome_aluno']} | {d['turma']} | {d['livro']} | {d['autor']} | {d['data_retirada'][8:10]}/{d['data_retirada'][5:7]}/{d['data_retirada'][0:4]} | {d['prazo_entrega'][8:10]}/{d['prazo_entrega'][5:7]}/{d['prazo_entrega'][0:4]} | {d['data_devolucao'][8:10]}/{d['data_devolucao'][5:7]}/{d['data_devolucao'][0:4]} | R$ {d['multa']:.2f}")

    lista.append('historico')

    return lista

@eel.expose
def busca_select_aberto(select):

    lista = []
    dados = busca_retiradas(select)

    for d in dados:
        lista.append(d['id_ret'])
        lista.append(f"{d['nome_aluno']} | {d['turma_aluno']} | {d['nome_livro']} | {d['autor_livro']} | {d['data_retirada'][8:10]}/{d['data_retirada'][5:7]}/{d['data_retirada'][0:4]} | {d['data_entrega'][8:10]}/{d['data_entrega'][5:7]}/{d['data_entrega'][0:4]}")

    lista.append('emAberto')

    return lista


def busca_historico(param='no'):

    if param == 'no':
        sql = f'SELECT * FROM historico'
        lista = []

        try:
            cursor.execute(sql)
            historico = cursor.fetchall()
            #print(f'historico: {historico}')
        except:
            print(f'Erro ao buscar histórico no banco de dados!')
        else:
            print(f'Histórico buscado com sucesso!')

        for i in historico:
            dictDados = {'id': i[0], 'nome_aluno': i[1], 'turma': i[2], 'livro': i[3], 'autor': i[4], 'data_retirada': i[5], 'prazo_entrega': i[6], 'data_devolucao': i[7], 'multa': i[8]}
            lista.append(dictDados)

        lista = sorted(lista, key=lambda k: k['data_devolucao'], reverse=True)

        return lista

    else:
        sql = f'SELECT * FROM historico'
        lista = []

        try:
            cursor.execute(sql)
            historico = cursor.fetchall()
            #print(f'historico: {historico}')
        except:
            print(f'Erro ao buscar histórico no banco de dados!')
        else:
            print(f'Histórico buscado com sucesso!')

        for i in historico:
            dictDados = {'id': i[0], 'nome_aluno': i[1], 'turma': i[2], 'livro': i[3], 'autor': i[4], 'data_retirada': i[5], 'prazo_entrega': i[6], 'data_devolucao': i[7], 'multa': i[8]}
            lista.append(dictDados)

        if param == 'data_retirada':
            lista = sorted(lista, key=lambda k: k['data_retirada'], reverse=True)
        elif param == 'prazo_devolucao':
            lista = sorted(lista, key=lambda k: k['prazo_entrega'], reverse=True)
        elif param == 'data_devolucao' or 'a':
            lista = sorted(lista, key=lambda k: k['data_devolucao'], reverse=True)

        return lista


@eel.expose
def busca_num(tipo):
    sql = f'SELECT COUNT(id) FROM livro'
    dados = None
    lista = []

    try:
        cursor.execute(sql)
        dados = cursor.fetchall()
        #print(dados)
    except:
        print('Erro ao buscar n° de livros no banco de dados!')
        return None

    lista.append(dados)
    lista.append(tipo)

    #print(lista)
    return lista


@eel.expose
def registraHistorico(array, dataDevolucao, multa):

    id_aluguel = array[0]
    dados_aluguel = None
    dados_aluno = None
    dados_livro = None
    sucesso = 0

    sql = f'SELECT * FROM aluguel WHERE id="{id_aluguel}"'

    try:
        cursor.execute(sql)
        dados_aluguel = cursor.fetchall()
        #print(dados_aluguel)
    except:
        print(f'Erro ao buscar o aluguel no banco de dados!')
    else:
        print(f'Aluguel encontrado no banco de dados!')

    id_livro = dados_aluguel[0][1]
    id_aluno = dados_aluguel[0][2]
    data_retirada = dados_aluguel[0][3]
    prazo_entrega = dados_aluguel[0][4]

    sql = f'SELECT * FROM aluno WHERE id="{id_aluno}"'

    try:
        cursor.execute(sql)
        dados_aluno = cursor.fetchall()
        #print(dados_aluno)
    except:
        print(f'Erro ao buscar dados do aluno no banco de dados!')
    else:
        print(f'Dados do aluno encontrados no banco de dados!')

    nome_aluno = dados_aluno[0][1]
    turma = dados_aluno[0][2]

    sql = f'SELECT * FROM livro WHERE id="{id_livro}"'

    try:
        cursor.execute(sql)
        dados_livro = cursor.fetchall()
        #print(dados_livro)
    except:
        print(f'Erro ao buscar dados do aluno no banco de dados!')
    else:
        print(f'Dados do aluno encontrados no banco de dados!')

    livro = dados_livro[0][1]
    autor = dados_livro[0][2]

    #print(multa)

    sql = f'INSERT INTO historico (nome_aluno, turma, livro, autor, data_retirada, prazo_entrega, data_devolucao, multa) VALUES ("{nome_aluno}", {turma}, "{livro}", "{autor}", "{data_retirada}", "{prazo_entrega}", "{dataDevolucao}", {multa})'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print('Erro ao tentar inserir registro no histórico do banco de dados!')
    else:
        print('Registro inserido no histórico do banco de dados com sucesso!')
        sucesso = 1
        eel.sucCadastroHistorico()

    if sucesso == 0:
        eel.mensagem('Erro ao registrar devolução, tente novamente!')


@eel.expose
def renovaAluguel(array, datePrazo):
    id_aluguel = array[0]

    sql = f'UPDATE aluguel SET data_entrega="{datePrazo}" WHERE id="{id_aluguel}"'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print(f'Erro ao tentar atualizar o prazo de entrega!')
        eel.mensagem('Erro ao tentar renovar registro, tente novamente!')
    else:
        print(f'Prazo de entrega atualizado com sucesso!')
        eel.sucRenovacao()


@eel.expose
def removerAluguelBD(array):

    id_aluguel = array[0]

    sql = f'DELETE FROM aluguel WHERE id="{id_aluguel}"'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print(f'Erro ao tentar remover aluguel do banco de dados!')
    else:
        print(f'Aluguel removido no banco de dados com sucesso!')


@eel.expose
def buscaDataDevolução(array):

    id_aluguel = array[0]

    sql = f'SELECT data_entrega FROM aluguel WHERE id="{id_aluguel}"'
    d = None
    lista = []

    try:
        cursor.execute(sql)
        d = cursor.fetchall()
        #print(f'data: {d}')
    except:
        print(f'Erro ao buscar data de entrega no banco de dados!')
    else:
        print(f'Data de entrega encontrada com sucesso!')

    lista.append(f"{d[0][0][0:4]}-{d[0][0][5:7]}-{d[0][0][8:10]}")
    lista.append(const.periodo)
    lista.append(const.valor)
    #print(f'lista: {lista}')

    return lista


def busca_retiradas(param='no'):

    if param == 'no':

        sql = f'SELECT * FROM aluguel'
        retiradas = None
        lista = []

        try:
            cursor.execute(sql)
            retiradas = cursor.fetchall()
            #print(f'retiradas: {retiradas}')
        except:
            print(f'Erro ao buscar retiradas no banco de dados!')
        else:
            print(f'Retiradas buscadas com sucesso!')

        for i in retiradas:
            dictDados = {'id_ret': i[0], 'id_livro': i[1], 'id_aluno': i[2], 'data_retirada': i[3], 'data_entrega': i[4]}

            sql = f'SELECT nome, autor FROM livro WHERE id={dictDados["id_livro"]}'
            dadosLivro = None

            try:
                cursor.execute(sql)
                dadosLivro = cursor.fetchall()
                #print(f'dadosLivro: {dadosLivro}')
            except:
                print(f'Erro ao buscar dados do livro no banco de dados!')
            else:
                print(f'Dados do livro buscados com sucesso!')

            dictDados['nome_livro'] = dadosLivro[0][0]
            dictDados['autor_livro'] = dadosLivro[0][1]

            sql = f'SELECT nome, turma FROM aluno WHERE id={dictDados["id_aluno"]}'
            dadosAluno = None

            try:
                cursor.execute(sql)
                dadosAluno = cursor.fetchall()
                #print(f'dadosAluno: {dadosAluno}')
            except:
                print(f'Erro ao buscar dados do aluno no banco de dados!')
            else:
                print(f'Dados do aluno buscados com sucesso!')

            dictDados['nome_aluno'] = dadosAluno[0][0]
            dictDados['turma_aluno'] = dadosAluno[0][1]

            lista.append(dictDados)

        #print(lista)
        return lista

    else:

        sql = f'SELECT * FROM aluguel'
        retiradas = None
        lista = []

        try:
            cursor.execute(sql)
            retiradas = cursor.fetchall()
            #print(f'retiradas: {retiradas}')
        except:
            print(f'Erro ao buscar retiradas no banco de dados!')
        else:
            print(f'Retiradas buscadas com sucesso!')

        for i in retiradas:
            dictDados = {'id_ret': i[0], 'id_livro': i[1], 'id_aluno': i[2], 'data_retirada': i[3], 'data_entrega': i[4]}

            sql = f'SELECT nome, autor FROM livro WHERE id={dictDados["id_livro"]}'
            dadosLivro = None

            try:
                cursor.execute(sql)
                dadosLivro = cursor.fetchall()
                #print(f'dadosLivro: {dadosLivro}')
            except:
                print(f'Erro ao buscar dados do livro no banco de dados!')
            else:
                print(f'Dados do livro buscados com sucesso!')

            dictDados['nome_livro'] = dadosLivro[0][0]
            dictDados['autor_livro'] = dadosLivro[0][1]

            sql = f'SELECT nome, turma FROM aluno WHERE id={dictDados["id_aluno"]}'
            dadosAluno = None

            try:
                cursor.execute(sql)
                dadosAluno = cursor.fetchall()
                #print(f'dadosAluno: {dadosAluno}')
            except:
                print(f'Erro ao buscar dados do aluno no banco de dados!')
            else:
                print(f'Dados do aluno buscados com sucesso!')

            dictDados['nome_aluno'] = dadosAluno[0][0]
            dictDados['turma_aluno'] = dadosAluno[0][1]

            lista.append(dictDados)

        if param == 'data_retirada':
            lista = sorted(lista, key=lambda k: k['data_retirada'], reverse=True)
        elif param == 'prazo_devolucao':
            lista = sorted(lista, key=lambda k: k['data_entrega'], reverse=True)

        #print(lista)
        return lista


@eel.expose
def busca_livros_all():

    sql = f'SELECT * FROM livro'
    dados = None
    lista = []

    try:
        cursor.execute(sql)
        dados = cursor.fetchall()
        #print(dados)
    except:
        print('Erro ao buscar livros no banco de dados!')
        return None
    else:
        print('Livros encontrados no banco de dados!')

    for i in dados:
        dictDados = {'id': i[0], 'nome_livro': i[1], 'autor': i[2], 'exemplares': i[3], 'disponiveis': i[4]}
        lista.append(dictDados)

    #print(lista)

    organizar_alfabeticamente(lista)

    #print(lista)
    return lista


def organizar_alfabeticamente(lista):
    #print(lista)
    for x in range (len(lista)):
        for y in range (len(lista)):
            if lista[x]['nome_livro'] < lista[y]['nome_livro']:
                lista[x], lista[y] = lista[y], lista[x]


@eel.expose
def testaLivro(nome, autor):
    sql = f'SELECT nome, autor FROM livro'
    dados = None

    try:
        cursor.execute(sql)
        dados = cursor.fetchall()
        #print(dados)
    except:
        print('Erro ao buscar nomes dos livros cadastrados no banco de dados!')
        return False
    else:
        print('Nomes dos livros cadastrados encontrados com sucesso!')

    for d in dados:
        if nome == d[0] and autor == d[1]:
            eel.mensagem('Já existe um livro com esse nome e com o mesmo autor cadastrado no banco de dados, consulte a aba listar!')
            return False

    return True


@eel.expose
def insereLivroBD(nome, autor, exemplares):
    sql = f'INSERT INTO livro (nome, autor, exemplares, disponiveis) VALUES ("{nome}", "{autor}", {exemplares}, {exemplares})'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print('Erro ao tentar inserir livro no banco de dados!')
        eel.mensagem('Erro ao tentar cadastrar livro!')
    else:
        print('Livro inserido no banco de dados com sucesso!')
        eel.mensagem('Livro cadastrado com sucesso!')

    sql = f'INSERT INTO historico_livros (nome, autor) VALUES ("{nome}", "{autor}")'

    try:
        cursor.execute(sql)
        banco.commit()
    except:
        print('Erro ao tentar inserir livro no historico do banco de dados!')
    else:
        print('Livro inserido no historico do banco de dados com sucesso!')


@eel.expose
def alteraSenha(senhaAtual, novaSenha):

    senhaAtualBD = get_senha()

    if senhaAtualBD[0] == hashlib.md5(senhaAtual.encode()).hexdigest():

        senha_crip = hashlib.md5(novaSenha.encode()).hexdigest()

        sql = f'UPDATE login SET senha="{senha_crip}"'

        try:
            cursor.execute(sql)
            banco.commit()
        except:
            print('Erro ao atualizar senha no banco de dados!')
        else:
            print('Senha atualizada no banco de dados com sucesso!')
            eel.mensagem('Senha alterada com sucesso!')

    else:
        eel.mensagem('Senha atual inválida!')



def get_senha():

    sql = f'SELECT senha FROM login'

    try:
        cursor.execute(sql)
        banco.commit()
        dados = cursor.fetchone()
    except:
        print('Erro')
        return False
    else:
        #print(dados)
        return dados


@eel.expose
def login(senha):

    senha_bd = get_senha()

    if senha_bd[0] == hashlib.md5(senha.encode()).hexdigest():
        eel.redireciona_index()
    else:
        eel.mensagem('Senha inválida!')


# -------------------- MAIN -------------------- #
#import eel.browsers

if __name__ == '__main__':

    eel.init('web')

    banco = sqlite3.connect('bibliotecact.db')
    cursor = banco.cursor()

    initParam()

    eel.start('login.html')