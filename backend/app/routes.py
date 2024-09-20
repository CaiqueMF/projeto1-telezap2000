from flask import Blueprint, jsonify, request
from .models import Cadeira, Sala, Professor, Turma, Alocacao, Login,Feedback, db
from datetime import time,datetime,timedelta
from . import jwt,blacklist
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

main = Blueprint('main', __name__)


@main.route('/api/cadeiras', methods=['POST'])
def add_cadeira():
    data = request.get_json()
    nova_cadeira = Cadeira(
        nome=data['nome'],
        necessidades_sala=data.get('necessidades_sala'),
        natureza=data.get('natureza'),
        semestre=data.get('semestre'),
        aulas_prolongadas=data.get('aulas_prolongadas'),
        curso=data.get('curso')
    )
    db.session.add(nova_cadeira)
    db.session.commit()
    return jsonify({'message': 'Cadeira adicionada com sucesso!'}), 201

@main.route('/api/cadeiras', methods=['GET'])
def get_cadeiras():
    cadeiras = Cadeira.query.all()
    return jsonify([{
        'id': cadeira.id,
        'nome': cadeira.nome,
        'necessidades_sala': cadeira.necessidades_sala,
        'natureza': cadeira.natureza,
        'semestre': cadeira.semestre,
        'aulas_prolongadas': cadeira.aulas_prolongadas,
        'curso': cadeira.curso
    } for cadeira in cadeiras])

@main.route('/api/cadeiras/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_cadeira(id):
    if request.method == 'GET':
        cadeira = Cadeira.query.get(id)
        if cadeira is None:
            return jsonify({'message': 'Cadeira não encontrada'}), 404
        return jsonify({
            'id': cadeira.id,
            'nome': cadeira.nome,
            'necessidades_sala': cadeira.necessidades_sala,
            'natureza': cadeira.natureza,
            'semestre': cadeira.semestre,
            'aulas_prolongadas': cadeira.aulas_prolongadas,
            'curso': cadeira.curso
        })
    elif request.method == 'PUT':
        data = request.get_json()
        cadeira = Cadeira.query.get(id)
        if cadeira is None:
            return jsonify({'message': 'Cadeira não encontrada'}), 404
        cadeira.nome = data.get('nome', cadeira.nome)
        cadeira.necessidades_sala = data.get('necessidades_sala', cadeira.necessidades_sala)
        cadeira.natureza = data.get('natureza', cadeira.natureza)
        cadeira.semestre = data.get('semestre', cadeira.semestre)
        cadeira.aulas_prolongadas = data.get('aulas_prolongadas', cadeira.aulas_prolongadas)
        cadeira.curso = data.get('curso', cadeira.curso)
        db.session.commit()
        return jsonify({'message': 'Cadeira atualizada com sucesso!'})
    elif request.method == 'DELETE':
        cadeira = Cadeira.query.get(id)
        if cadeira is None:
            return jsonify({'message': 'Cadeira não encontrada'}), 404
        db.session.delete(cadeira)
        db.session.commit()
        return jsonify({'message': 'Cadeira deletada com sucesso!'})


# Routes for Sala
@main.route('/api/salas', methods=['POST'])
def add_sala():
    data = request.get_json()
    nova_sala = Sala(
        nome=data['nome'],
        tipos=data.get('tipos')
    )
    db.session.add(nova_sala)
    db.session.commit()
    return jsonify({'message': 'Sala adicionada com sucesso!'}), 201

@main.route('/api/salas', methods=['GET'])
def get_salas():
    salas = Sala.query.all()
    return jsonify([{
        'id': sala.id,
        'nome': sala.nome,
        'tipos': sala.tipos
    } for sala in salas])

@main.route('/api/salas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_sala(id):
    if request.method == 'GET':
        sala = Sala.query.get(id)
        if sala is None:
            return jsonify({'message': 'Sala não encontrada'}), 404
        return jsonify({
            'id': sala.id,
            'nome': sala.nome,
            'tipos': sala.tipos
        })
    elif request.method == 'PUT':
        data = request.get_json()
        sala = Sala.query.get(id)
        if sala is None:
            return jsonify({'message': 'Sala não encontrada'}), 404
        sala.nome = data.get('nome', sala.nome)
        sala.tipos = data.get('tipos', sala.tipos)
        db.session.commit()
        return jsonify({'message': 'Sala atualizada com sucesso!'})
    elif request.method == 'DELETE':
        sala = Sala.query.get(id)
        if sala is None:
            return jsonify({'message': 'Sala não encontrada'}), 404
        db.session.delete(sala)
        db.session.commit()
        return jsonify({'message': 'Sala deletada com sucesso!'})

# Routes for Professor
@main.route('/api/professores', methods=['POST'])
def add_professor():
    data = request.get_json()
    novo_professor = Professor(
        nome=data['nome']
    )
    db.session.add(novo_professor)
    db.session.commit()

    nome_segmentado = data['nome'].split()
    primeiro_nome = nome_segmentado[0]
    iniciais = ''.join([part[0] for part in nome_segmentado[1:]]) if len(nome_segmentado) > 1 else ''
    login_base = f"{primeiro_nome}{iniciais}"
    login = login_base
    counter = 1
    while Login.query.filter_by(login=login).first() is not None:
        login = f"{login_base}{counter}"
        counter += 1

    novo_login = Login(
        nome = data['nome'],
        login = login,
        senha = '123',
        role = 'user',
        id_professor = novo_professor.id
    )
    db.session.add(novo_login)
    db.session.commit()

    return jsonify({'message': 'Professor adicionado com sucesso!','login': login}), 201

@main.route('/api/professores', methods=['GET'])
def get_professores():
    professores = Professor.query.all()
    return jsonify([{
        'id': professor.id,
        'nome': professor.nome
    } for professor in professores])

@main.route('/api/professores/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_professor(id):
    if request.method == 'GET':
        professor = Professor.query.get(id)
        if professor is None:
            return jsonify({'message': 'Professor não encontrado'}), 404
        login = Login.query.filter_by(id_professor=id).first()
        return jsonify({
            'id': professor.id,
            'nome': professor.nome,
            'login': login.login
        })
    elif request.method == 'PUT':
        data = request.get_json()
        professor = Professor.query.get(id)
        if professor is None:
            return jsonify({'message': 'Professor não encontrado'}), 404
        login = Login.query.filter_by(id_professor=id).first()
        professor.nome = data.get('nome', professor.nome)
        login.login = data.get('login',login.login)
        db.session.commit()
        return jsonify({'message': 'Professor atualizado com sucesso!'})
    elif request.method == 'DELETE':
        professor = Professor.query.get(id)
        if professor is None:
            return jsonify({'message': 'Professor não encontrado'}), 404
        login = Login.query.filter_by(id_professor=id).first()
        db.session.delete(professor)
        db.session.delete(login)
        db.session.commit()
        return jsonify({'message': 'Professor deletado com sucesso!'})

# Routes for Turma
@main.route('/api/turmas', methods=['POST'])
def add_turma():
    data = request.get_json()
    nova_turma = Turma(
        id_cadeira=data['id_cadeira'],
        id_professor=data['id_professor'],
        id_sala=data['id_sala'],
        n_turma=data['n_turma'],
        n_vagas=data['n_vagas'],
        curso=data['curso']
    )
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({'message': 'Turma adicionada com sucesso!'}), 201

@main.route('/api/turmas', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    return jsonify([{
        'id': turma.id,
        'id_cadeira': turma.id_cadeira,
        'id_professor': turma.id_professor,
        'id_sala': turma.id_sala,
        'n_turma': turma.n_turma,
        'n_vagas': turma.n_vagas,
        'curso': turma.curso
    } for turma in turmas])

@main.route('/api/turmas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_turma(id):
    if request.method == 'GET':
        turma = Turma.query.get(id)
        if turma is None:
            return jsonify({'message': 'Turma não encontrada'}), 404
        return jsonify({
            'id': turma.id,
            'id_cadeira': turma.id_cadeira,
            'id_professor': turma.id_professor,
            'id_sala': turma.id_sala,
            'n_turma': turma.n_turma,
            'n_vagas': turma.n_vagas,
            'curso': turma.curso
        })
    elif request.method == 'PUT':
        data = request.get_json()
        turma = Turma.query.get(id)
        if turma is None:
            return jsonify({'message': 'Turma não encontrada'}), 404
        turma.id_cadeira = data.get('id_cadeira', turma.id_cadeira)
        turma.id_professor = data.get('id_professor', turma.id_professor)
        turma.id_sala = data.get('id_sala', turma.id_sala)
        turma.n_turma = data.get('n_turma', turma.n_turma)
        turma.n_vagas = data.get('n_vagas', turma.n_vagas)
        turma.curso = data.get('curso', turma.curso)
        db.session.commit()
        return jsonify({'message': 'Turma atualizada com sucesso!'})
    elif request.method == 'DELETE':
        turma = Turma.query.get(id)
        if turma is None:
            return jsonify({'message': 'Turma não encontrada'}), 404
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'message': 'Turma deletada com sucesso!'})


# rota consulta geral
@main.route('/api/salasLivres', methods=['GET'])
def handle_salas_livres():
    agora = datetime.now()
    dia_semana = agora.weekday() + 1
    hora_atual = agora.time()
    salas = Sala.query.all()
    salas_livres = []

    for sala in salas:
        turma_com_horario = Alocacao.query.join(Turma).filter(
            Turma.id_sala == sala.id,
            Alocacao.dia == dia_semana,
            Alocacao.horario <= hora_atual
        ).first()

        if turma_com_horario:
            # Extraindo o horário e duração para fazer a comparação corretamente
            horario_inicio = turma_com_horario.horario
            duracao = turma_com_horario.duracao
            horario_fim = (datetime.combine(agora.date(), horario_inicio) + timedelta(hours=duracao)).time()

            if horario_fim > hora_atual:
                continue

        proximo_horario = Alocacao.query.join(Turma).filter(
            Turma.id_sala == sala.id,
            Alocacao.dia == dia_semana,
            Alocacao.horario > hora_atual
        ).order_by(Alocacao.horario.asc()).first()

        if proximo_horario:
            salas_livres.append({
                'sala': sala.nome,
                'disponivel': proximo_horario.horario.strftime('%H:%M:%S')
            })
        else:
            salas_livres.append({
                'sala': sala.nome,
                'disponivel': 'até o fim do dia'
            })

    return jsonify({'salas': salas_livres})


@main.route('/api/salasOcupadasAgora', methods=['GET'])
def handle_salas_ocupadas_agora():
    agora = datetime.now()
    dia_semana = agora.weekday() + 1
    hora_atual = agora.time()
    salas_ocupadas = []

    # Busca por aulas que estão acontecendo agora
    alocacoes_ocupadas = Alocacao.query.join(Turma).join(Sala).filter(
        Alocacao.dia == dia_semana,
        Alocacao.horario <= hora_atual
    ).all()

    # Monta a lista de salas ocupadas com as informações da aula
    for alocacao in alocacoes_ocupadas:
        sala = alocacao.turma.sala
        cadeira = alocacao.turma.cadeira

        # Extraindo valores específicos de `alocacao`
        horario_inicio = alocacao.horario
        duracao = alocacao.duracao  # Certifique-se de que `duracao` é um número, como inteiro ou float

        # Cálculo do horário de término da aula
        horario_termino = (datetime.combine(agora.date(), horario_inicio) + timedelta(hours=float(duracao))).time()

        # Verifica se a aula ainda está em andamento
        if horario_termino > hora_atual:
            salas_ocupadas.append({
                'sala': sala.nome,
                'cadeira': cadeira.nome,
                'horario_inicio': horario_inicio.strftime('%H:%M:%S'),
                'horario_termino': horario_termino.strftime('%H:%M:%S')
            })

    return jsonify({
        'salas_ocupadas': salas_ocupadas,
    })

# Routes for Alocacao
@main.route('/api/alocacoes', methods=['POST'])
def add_alocacao():
    data = request.get_json()
    duracao = 2
    if data['aulas_prolongadas']:
        duracao = 4
    nova_alocacao = Alocacao(
        id_turma=data['id_turma'],
        dia=int(data['dia']),
        horario=time(int(data['horario']),0),
        duracao = duracao
    )
    db.session.add(nova_alocacao)
    db.session.commit()
    return jsonify({'message': 'Alocação adicionada com sucesso!'}), 201

@main.route('/api/alocacoes', methods=['GET'])
def get_alocacoes():
    alocacoes = Alocacao.query.all()
    return jsonify([{
        'id': alocacao.id,
        'id_turma': alocacao.id_turma,
        'dia': alocacao.dia,
        'horario': alocacao.horario.hour,
        'duracao' : alocacao.duracao
    } for alocacao in alocacoes])

@main.route('/api/alocacoes/<int:id>', methods=['PUT','DELETE'])
def handle_alocacao(id):
    if request.method == 'PUT':
        data = request.get_json()
        print(data)
        alocacao = Alocacao.query.get_or_404(id)
        alocacao.id_turma = data.get('id_turma', alocacao.id_turma)
        alocacao.dia = data.get('dia', alocacao.dia)
        alocacao.horario = time(int(data.get('horario', alocacao.horario)),0)
        duracao = 2
        if data.get('aulas_prolongadas'):
            duracao = 4
        alocacao.duracao = duracao
        db.session.commit()
        return jsonify({'message': 'Alocação atualizada com sucesso!'}), 200
    elif request.method == 'DELETE':
        alocacao = Alocacao.query.get(id)
        if alocacao is None:
            return jsonify({'message': 'Alocação não encontrada'}), 404
        db.session.delete(alocacao)
        db.session.commit()
        return jsonify({'message': 'Alocação deletada com sucesso!'})

@main.route('/api/feedbacks', methods=['POST'])
def add_feedback():
    data = request.get_json()
    novo_feedback = Feedback(
    id_professor=data['id_professor'],
    feedback=data['feedback'],
)
    db.session.add(novo_feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback adicionada com sucesso!'}), 201

@main.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = Feedback.query.all()
    return jsonify([{
        'id': feedback.id,
        'id_professor': feedback.id_professor,
        'feedback': feedback.feedback
    } for feedback in feedbacks])



@main.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = Login.query.filter_by(login=username).first()
    print(db.session.query(Login).count())
    if not user or user.senha != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity={"username": username, "role": user.role})
    return jsonify(access_token=access_token, role = user.role)

@main.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@main.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # JWT ID (jti) é um identificador único para o token JWT
    blacklist.add(jti)
    return jsonify(msg="Successfully logged out"), 200

# Verificação do token na blacklist
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist