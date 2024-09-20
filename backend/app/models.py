from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



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
    natureza = db.Column(db.String(16))
    semestre = db.Column(db.Integer)
    aulas_prolongadas = db.Column(db.Boolean, default=False)
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
    dia = db.Column(db.Integer, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    turma = db.relationship('Turma', backref='alocacoes')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    feedback = db.Column(db.String(1000), nullable=False)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id'))
    professor = db.relationship('Professor', backref='Login')

def inicializar_logins():
    logins_existentes = db.session.query(Login).count()
    if logins_existentes == 0:
        coordenadores = [
            Login(
            nome = 'nome coordenador 1',
            login = 'coordenador1',
            senha = '123',
            role = 'admin'
            ),
            Login(
            nome = 'nome coordenador 2',
            login = 'coordenador2',
            senha = '123',
            role = 'admin'
            ),
            Login(
            nome = 'nome coordenador 2',
            login = 'coordenador2',
            senha = '123',
            role = 'admin'
            ),

        ]
        db.session.add_all(coordenadores)
        db.session.commit()

def iniciar_db():
    db.create_all()
    inicializar_logins()