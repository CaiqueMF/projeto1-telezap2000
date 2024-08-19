from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importe o Flask-CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
CORS(app)  # Habilite CORS para todas as rotas
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'senha_mudar_depois'
jwt = JWTManager(app)

db = SQLAlchemy(app)

# Models definition
professor_cadeira = db.Table('professor_cadeira',
    db.Column('professor_id', db.Integer, db.ForeignKey('professor.id')),
    db.Column('cadeira_id', db.Integer, db.ForeignKey('cadeira.id'))
)

cadeira_prerequisito = db.Table('cadeira_prerequisito',
    db.Column('cadeira_id', db.Integer, db.ForeignKey('cadeira.id')),
    db.Column('prerequisito_id', db.Integer, db.ForeignKey('cadeira.id'))
)

class Cadeira(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    professores = db.relationship('Professor', secondary=professor_cadeira, backref='cadeiras')
    prerrequisitos = db.relationship('Cadeira', secondary=cadeira_prerequisito,
                                     primaryjoin=(id == cadeira_prerequisito.c.cadeira_id),
                                     secondaryjoin=(id == cadeira_prerequisito.c.prerequisito_id),
                                     backref='prerequisitada_por')
    necessidades_sala = db.Column(db.String(100))
    obrigatoria = db.Column(db.Boolean, default=False)
    eletiva = db.Column(db.Boolean, default=False)
    optativa = db.Column(db.Boolean, default=False)
    semestre = db.Column(db.Integer)
    curso = db.Column(db.String(100))

class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipos = db.Column(db.String(100))

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cadeira = db.Column(db.Integer, db.ForeignKey('cadeira.id'), nullable=False)
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    n_turma = db.Column(db.Integer, nullable=False)
    n_vagas = db.Column(db.Integer, nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    cadeira = db.relationship('Cadeira', backref='turmas')
    professor = db.relationship('Professor', backref='turmas')
    sala = db.relationship('Sala', backref='turmas')

class Alocacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_turma = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    dia = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    turma = db.relationship('Turma', backref='alocacoes')

@app.before_request
def create_tables():
    db.create_all()

@app.route('/api/cadeiras', methods=['POST'])
def add_cadeira():
    data = request.get_json()
    nova_cadeira = Cadeira(
        nome=data['nome'],
        necessidades_sala=data.get('necessidades_sala'),
        obrigatoria=data.get('obrigatoria', False),
        eletiva=data.get('eletiva', False),
        optativa=data.get('optativa', False),
        semestre=data.get('semestre'),
        curso=data.get('curso')
    )
    db.session.add(nova_cadeira)
    db.session.commit()
    return jsonify({'message': 'Cadeira adicionada com sucesso!'}), 201

@app.route('/api/cadeiras', methods=['GET'])
def get_cadeiras():
    cadeiras = Cadeira.query.all()
    return jsonify([{
        'id': cadeira.id,
        'nome': cadeira.nome,
        'necessidades_sala': cadeira.necessidades_sala,
        'obrigatoria': cadeira.obrigatoria,
        'eletiva': cadeira.eletiva,
        'optativa': cadeira.optativa,
        'semestre': cadeira.semestre,
        'curso': cadeira.curso
    } for cadeira in cadeiras])

@app.route('/api/cadeiras/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_cadeira(id):
    if request.method == 'GET':
        cadeira = Cadeira.query.get(id)
        if cadeira is None:
            return jsonify({'message': 'Cadeira não encontrada'}), 404
        return jsonify({
            'id': cadeira.id,
            'nome': cadeira.nome,
            'necessidades_sala': cadeira.necessidades_sala,
            'obrigatoria': cadeira.obrigatoria,
            'eletiva': cadeira.eletiva,
            'optativa': cadeira.optativa,
            'semestre': cadeira.semestre,
            'curso': cadeira.curso
        })
    elif request.method == 'PUT':
        data = request.get_json()
        cadeira = Cadeira.query.get(id)
        if cadeira is None:
            return jsonify({'message': 'Cadeira não encontrada'}), 404
        cadeira.nome = data.get('nome', cadeira.nome)
        cadeira.necessidades_sala = data.get('necessidades_sala', cadeira.necessidades_sala)
        cadeira.obrigatoria = data.get('obrigatoria', cadeira.obrigatoria)
        cadeira.eletiva = data.get('eletiva', cadeira.eletiva)
        cadeira.optativa = data.get('optativa', cadeira.optativa)
        cadeira.semestre = data.get('semestre', cadeira.semestre)
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
@app.route('/api/salas', methods=['POST'])
def add_sala():
    data = request.get_json()
    nova_sala = Sala(
        nome=data['nome'],
        tipos=data.get('tipos')
    )
    db.session.add(nova_sala)
    db.session.commit()
    return jsonify({'message': 'Sala adicionada com sucesso!'}), 201

@app.route('/api/salas', methods=['GET'])
def get_salas():
    salas = Sala.query.all()
    return jsonify([{
        'id': sala.id,
        'nome': sala.nome,
        'tipos': sala.tipos
    } for sala in salas])

@app.route('/api/salas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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
@app.route('/api/professores', methods=['POST'])
def add_professor():
    data = request.get_json()
    novo_professor = Professor(
        nome=data['nome']
    )
    db.session.add(novo_professor)
    db.session.commit()
    return jsonify({'message': 'Professor adicionado com sucesso!'}), 201

@app.route('/api/professores', methods=['GET'])
def get_professores():
    professores = Professor.query.all()
    return jsonify([{
        'id': professor.id,
        'nome': professor.nome
    } for professor in professores])

@app.route('/api/professores/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_professor(id):
    if request.method == 'GET':
        professor = Professor.query.get(id)
        if professor is None:
            return jsonify({'message': 'Professor não encontrado'}), 404
        return jsonify({
            'id': professor.id,
            'nome': professor.nome
        })
    elif request.method == 'PUT':
        data = request.get_json()
        professor = Professor.query.get(id)
        if professor is None:
            return jsonify({'message': 'Professor não encontrado'}), 404
        professor.nome = data.get('nome', professor.nome)
        db.session.commit()
        return jsonify({'message': 'Professor atualizado com sucesso!'})
    elif request.method == 'DELETE':
        professor = Professor.query.get(id)
        if professor is None:
            return jsonify({'message': 'Professor não encontrado'}), 404
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'message': 'Professor deletado com sucesso!'})

# Routes for Turma
@app.route('/api/turmas', methods=['POST'])
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

@app.route('/api/turmas', methods=['GET'])
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

@app.route('/api/turmas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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

# Routes for Alocacao
@app.route('/api/alocacoes', methods=['POST'])
def add_alocacao():
    data = request.get_json()
    nova_alocacao = Alocacao(
        id_turma=data['id_turma'],
        dia=data['dia'],
        horario=data['horario']
    )
    db.session.add(nova_alocacao)
    db.session.commit()
    return jsonify({'message': 'Alocação adicionada com sucesso!'}), 201

@app.route('/api/alocacoes', methods=['GET'])
def get_alocacoes():
    alocacoes = Alocacao.query.all()
    return jsonify([{
        'id': alocacao.id,
        'id_turma': alocacao.id_turma,
        'dia': alocacao.dia,
        'horario': alocacao.horario
    } for alocacao in alocacoes])

@app.route('/api/alocacoes/<int:id>', methods=['PUT'])
def update_alocacao(id):
    data = request.get_json()
    alocacao = Alocacao.query.get_or_404(id)
    alocacao.id_turma = data.get('id_turma', alocacao.id_turma)
    alocacao.dia = data.get('dia', alocacao.dia)
    alocacao.horario = data.get('horario', alocacao.horario)
    db.session.commit()
    return jsonify({'message': 'Alocação atualizada com sucesso!'}), 200

#teste de login
users = {
    "coordenador": {"password": "123", "role": "admin"},
    "professor": {"password": "123", "role": "user"}
}


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = users.get(username)
    if not user or user['password'] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity={"username": username, "role": user['role']})
    return jsonify(access_token=access_token, role = user['role'])

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)