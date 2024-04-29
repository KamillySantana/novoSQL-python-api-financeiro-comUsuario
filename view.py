from flask import Flask, jsonify, request, session, flash
from main import app, db
from models import Receitas, Despesas, Guardar, Usuario

from flask_bcrypt import generate_password_hash, check_password_hash #lidar com a criptografia de senhas

#=============================USUARIO LOGIN==========================================
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    # Consulta o usuário no banco de dados pelo email fornecido
    usuarios = Usuario.query.filter_by(email=email).first()

    # Verifica se o e-mail está cadastrado e se a senha está correta, alem da descriptografia da senha
    if usuarios and check_password_hash(usuarios.senha, senha):
        # Salva o email do usuário na sessão
        session['id_usuario'] = usuarios.id_usuario
        return jsonify({'mensagem': 'Login com sucesso'}), 200
    else:
        # Se as credenciais estiverem incorretas, retorna uma mensagem de erro
        return jsonify({'mensagem': 'Email ou senha inválido'})


#=======================AUTENTICAÇÃO====================================================
# Rota protegida que requer autenticação
@app.route('/protected', methods=['GET'])
def protected():
    # Verifica se o usuário está autenticado verificando se o email está na sessão
    if 'id_usuario' in session:
        return jsonify({'mensagem': 'Rota Protegida'})
    else:
        # Se o usuário não estiver autenticado, retorna uma mensagem de erro
        return jsonify({'mensagem': 'Requer Autorização'})


#=============================DESLOGAR USUARIO=========================================
# Rota para fazer logout
@app.route('/logout', methods=['POST'])
def logout():
    # Remove o email da sessão, efetivamente fazendo logout
    session.pop('id_usuario', None)
    return jsonify({'mensagem': 'Logout bem Sucedido'})


#=============================CRIAR USUARIO==========================================
@app.route('/criarUser', methods=['POST'])
def criar_user():
    dataG = request.json
    nome = dataG.get('nome')
    email = dataG.get('email')
    senha = dataG.get('senha')

    #verifica se tem um email ja existente
    user = Usuario.query.filter_by(email=email).first()
    if user:
        return jsonify(
            mensagem='Usuario ja existente',
        )
    else:
        #senha fornecida é criptografada
        senha_hash = generate_password_hash(senha).decode('utf-8')
        #passando os dados para a classe
        novo_usuario = Usuario(email=email, senha=senha_hash, nome=nome)
        #adiciona o novo usuario ao banco
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify(
            mensagem='Usuario Cadastrado com Sucesso',
            livro={
              'id_usuario': novo_usuario.id_usuario,
              'nome': novo_usuario.nome,
              'email': novo_usuario.email,
              'senha': novo_usuario.senha
            }
        )





#=============================EXIBIR RECEITA==========================
@app.route('/receita', methods = ['GET'])
def get_receita():
    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        return jsonify({'mensagem': 'Faça login para acessar as receitas'})

    receitas = Receitas.query.filter_by(id_usuario=id_usuario).all()
    receitas_dic = []

    for rece in receitas:
        rece_dic = {
            'id_receitas': rece.id_receitas,
            'nome': rece.nome,
            'valor': rece.valor,
            'data': rece.data
        }
        receitas_dic.append(rece_dic)

    if receitas_dic:
        return jsonify(
            mensagem='Lista das Receitas',
            receitas=receitas_dic
        )
    else:
        return jsonify({'mensagem': 'Não há nenhuma receita cadastrada nesta conta'})

#=============================CADASTRAR RECEITA==========================
@app.route('/receita', methods=['POST'])
def post_receita():
    receita = request.json
    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        return jsonify({'mensagem': 'Faça login para cadastrar uma receita'})

    nova_receita = Receitas(
        id_usuario=id_usuario,
        nome=receita.get('nome'),
        valor=receita.get('valor'),
        data=receita.get('data')
    )

    db.session.add(nova_receita)
    db.session.commit()

    return jsonify(
        mensagem='Receita Cadastrada com Sucesso',
        receitas={
            'id_receitas': nova_receita.id_receitas,
            'nome': nova_receita.nome,
            'valor': nova_receita.valor,
            'data': nova_receita.data
        }
    )







#=============================EXIBIR DESPESA==========================
@app.route('/despesa', methods = ['GET'])
def get_despesa():
    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        return jsonify({'mensagem': 'Faça login para acessar as Despesas'})

    despesas = Despesas.query.filter_by(id_usuario=id_usuario).all()
    despesas_dic = []

    for despe in despesas:
        despe_dic = {
            'id_despesas': despe.id_despesas,
            'nome': despe.nome,
            'valor': despe.valor,
            'data': despe.data
        }
        despesas_dic.append(despe_dic)

    if despesas_dic:
        return jsonify(
            mensagem='Lista das Despesas',
            despesas=despesas_dic
        )
    else:
        return jsonify({'mensagem': 'Não há nenhuma despesa cadastrada nesta conta'})

#=============================CADASTRAR DESPESA=======================
@app.route('/despesa', methods=['POST'])
def post_despesa():
    despesa = request.json
    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        return jsonify({'mensagem': 'Faça login para cadastrar uma Despesa'})

    nova_despesa = Despesas(
        id_despesas=despesa.get('id_despesas'),
        nome=despesa.get('nome'),
        valor=despesa.get('valor'),
        data=despesa.get('data')
    )

    db.session.add(nova_despesa)
    db.session.commit()

    return jsonify(
        mensagem='Despesa Cadastrada com Sucesso',
        despesas={
            'id_despesas': nova_despesa.id_despesas,
            'nome': nova_despesa.nome,
            'valor': nova_despesa.valor,
            'data': nova_despesa.data
        }
    )








#=============================EXIBIR GUARDAR==========================
@app.route('/guardar', methods = ['GET'])
def get_guardar():
    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        return jsonify({'mensagem': 'Faça login para acessar as Despesas'})

    guardar = Guardar.query.filter_by(id_usuario=id_usuario).all()
    guardar_dic = []

    for guar in guardar:
        guar_dic = {
            'id_guardar': guar.id_guardar,
            'nome': guar.nome,
            'valor': guar.valor,
            'data': guar.data
        }
        guardar_dic.append(guar_dic)

    if guardar_dic:
        return jsonify(
            mensagem='Lista do Dinheiro Guardado',
            guardar=guardar_dic
        )
    else:
        return jsonify({'mensagem': 'Não há nenhum dinheiro guardado nesta conta'})

#=============================CADASTRAR GUARDAR=======================
@app.route('/guardar', methods=['POST'])
def post_guardar():
    guardar = request.json
    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        return jsonify({'mensagem': 'Faça login para cadastrar uma receita'})

    novo_guardar = Guardar(
        id_guardar=guardar.get('id_guardar'),
        nome=guardar.get('nome'),
        valor=guardar.get('valor'),
        data=guardar.get('data')
    )

    db.session.add(novo_guardar)
    db.session.commit()

    return jsonify(
        mensagem='Dinheiro guardado com Sucesso',
        guardar={
            'id_guardar': novo_guardar.id_guardar,
            'nome': novo_guardar.nome,
            'valor': novo_guardar.valor,
            'data': novo_guardar.data
        }
    )



#========================DELETAR RECEITAS============================
@app.route('/receita/<int:id_receitas>', methods=['DELETE'])
def delete_receita(id_receitas):

    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        return jsonify({'mensagem': 'Faça login para excluir uma receita'})

    receita = Receitas.query.filter_by(id_receitas=id_receitas, id_usuario=id_usuario).first()

    if receita:
        # Remove a receita do banco de dados
        db.session.delete(receita)
        db.session.commit()

        return jsonify({'mensagem': 'Receita excluída com sucesso'})
    else:
        return jsonify({'mensagem': 'Receita não encontrada ou não pertence a esta conta'}), 404




#========================DELETAR DESPESA============================
@app.route('/despesa/<int:id_despesas>', methods=['DELETE'])
def delete_despesa(id_despesas):
    if 'id_usuario' in session:
        despesa = Despesas.query.get(id_despesas)

        if despesa:
            db.session.delete(despesa)
            db.session.commit()

            return jsonify({'mensagem': 'Despesa excluída com sucesso'})
        else:
            return jsonify({'mensagem': 'Despesa não encontrada'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})





#========================DELETAR GUARDAR============================
@app.route('/guardar/<int:id_guardar>', methods=['DELETE'])
def delete_guardar(id_guardar):
    if 'id_usuario' in session:
        guardar = Guardar.query.get(id_guardar)

        if guardar:
            db.session.delete(guardar)
            db.session.commit()

            return jsonify({'mensagem': 'Dinheiro Guardado excluída com sucesso'})
        else:
            return jsonify({'mensagem': 'Dinheiro Guardado não encontrada'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})