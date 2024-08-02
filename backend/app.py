from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    nome_sala = db.Column(db.String(100), nullable=False)
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

# Routes for Cadeira
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

# Routes for Sala
@app.route('/api/salas', methods=['POST'])
def add_sala():
    data = request.get_json()
    nova_sala = Sala(
        nome_sala=data['nome_sala'],
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
        'nome_sala': sala.nome_sala,
        'tipos': sala.tipos
    } for sala in salas])

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
    return jsonify({'message': 'Alocacao adicionada com sucesso!'}), 201

@app.route('/api/alocacoes', methods=['GET'])
def get_alocacoes():
    alocacoes = Alocacao.query.all()
    return jsonify([{
        'id': alocacao.id,
        'id_turma': alocacao.id_turma,
        'dia': alocacao.dia,
        'horario': alocacao.horario
    } for alocacao in alocacoes])

if __name__ == '__main__':
    app.run(debug=True)