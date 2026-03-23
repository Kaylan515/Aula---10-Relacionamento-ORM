# DESAFIO - Cardápio por faixa de preço
# 
# Exercício: UM Departamento tem vários Funcionários.
#            Cada funcionario pertence a apenas UM departamento.
#            colunas do Departamento: id, nome, funcionarios
#            colunas do Funcionario: id, nome, salario, departamento_id
# Regra de ouro: a chave estrangeira (ForeignKey) sempre fica
# na tabela do lado "muitos" - neste caso, na tabela Funcionario.

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Departamento(Base):
    __tablename__ = "departamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    funcionarios = relationship("Funcionario", back_populates="departamento")

    # Função para exibir os dados
    def __repr__(self):
        return f"<Departamento(id={self.id}, nome='{self.nome}')>"

class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    salario = Column(Float, nullable=False)
    cargo = Column(String(100), nullable=False)

    # Chave estrangeira
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))

    # Relacionamento
    departamento = relationship("Departamento", back_populates="funcionarios")


    def __repr__(self):
        return f"<Funcionario(id={self.id}, nome='{self.nome}', salario={self.salario}, cargo='{self.cargo}', departamento_id={self.departamento_id})>"

engine = create_engine("sqlite:///empresa.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def cadastrar_departamento():
    with Session() as session:
        try:
            departamento1 = input("Digite o nome do departamento: ")
            departamento2 = input("Digite o nome do departamento: ")
            
            #Criar objetos
            dep01 = Departamento(nome=departamento1)
            dep02 = Departamento(nome=departamento2)

            #Adicionar os departamentos
            session.add_all([dep01, dep02])
            session.commit()
            print(f"Departamentos {departamento1} e {departamento2} cadastrados com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Erro ao cadastrar departamento: {erro}")
# cadastrar_departamento()

def cadastrar_funcionario():
    with Session() as session:
        try:
            nome = input("Digite o nome do funcionário: ").capitalize()
            cargo = input(f"Digite o cargo do funcionário {nome}: ").capitalize()
            salario = float(input(f"Digite o salário do funcionário {nome}: "))
            #Buscar o departamento do funcionário
            #Como bsucar uma informação no banco com sqlalchemy
            ti = session.query(Departamento).filter_by(id=4).first()

            #criar os funcionários
            funcionario = Funcionario(nome=nome, cargo=cargo, salario=salario, departamento=ti)
            #Adicionar o funcionário
            session.add(funcionario)
            session.commit()
            print(f"Funcionário '{nome}' cadastrado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Erro ao cadastrar funcionário: {erro}")
# cadastrar_funcionario()

def listar_departamentos():
    with Session() as session:
        try:
            departamentos = session.query(Departamento).all()
            for departamento in departamentos:
                print(f"\n{departamento.nome}")
                for funcionario in departamento.funcionarios:
                    print(funcionario)
        except Exception as erro:
            print(f"Erro ao listar departamentos: {erro}")
# listar_departamentos()

# Listar todos funcionarios que recebem acima de 3000,00
def listar_funcionarios():
    with Session() as session:
        try:
            funcionarios = session.query(Funcionario).filter(Funcionario.salario > 5000, Funcionario.departamento_id == 3).all()
            for funcionario in funcionarios:
                print(f"Nome: {funcionario.nome}, Salário: {funcionario.salario}")
        except Exception as erro:
            print(f"Erro ao listar funcionários: {erro}")
# listar_funcionarios()

def excluir_funcionario():
    with Session() as session:
        try:
            nome = input("Digite o nome do funcionário a ser excluído: ").capitalize().strip()
            funcionario = session.query(Funcionario).filter_by(nome=nome).first()
            if funcionario == None:
                session.delete(funcionario)
                session.commit()
                print(f"Funcionário excluído com sucesso!")
            else:
                print("Funcionário não encontrado.")
        except Exception as erro:
            session.rollback()
            print(f"Erro ao excluir funcionário: {erro}")
# excluir_funcionario()

def atualizar_departamento():
    with Session() as session:
        try:
            nome = input("Digite o nome do departamento a ser atualizado: ").capitalize().strip()
            departamento = session.query(Departamento).filter_by(nome=nome).first()
            if departamento:
                novo_nome = input("Digite o novo nome do departamento: ")
                departamento.nome = novo_nome
                session.commit()
                print(f"Departamento atualizado com sucesso!")
            else:
                print("Departamento não encontrado.")
        except Exception as erro:
            session.rollback()
            print(f"Erro ao atualizar departamento: {erro}")
# atualizar_departamento()

def atualizar_funcionario():
    with Session() as session:
        try:
            nome = input("Digite o nome do funcionário a ser atualizado: ").capitalize().strip()
            funcionario = session.query(Funcionario).filter_by(nome=nome).first()
            if funcionario:
                novo_nome = input("Digite o novo nome do funcionário: ")
                novo_cargo = input("Digite o novo cargo do funcionário: ")
                novo_salario = float(input("Digite o novo salário do funcionário: "))
                novo_departamento_id = int(input("Digite o novo ID do departamento: "))
                funcionario.nome = novo_nome
                funcionario.cargo = novo_cargo
                funcionario.salario = novo_salario
                funcionario.departamento_id = novo_departamento_id
                session.commit()
                print(f"Funcionário atualizado com sucesso!")
            else:
                print("Funcionário não encontrado.")
        except Exception as erro:
            session.rollback()
            print(f"Erro ao atualizar funcionário: {erro}")
# atualizar_funcionario()

def excluir_departamento():
    departamento_id = int(input("Digite o ID do departamento a ser excluído: "))
    with Session() as session:
        departamento = session.query(Departamento).get(departamento_id)
        if departamento:
            session.delete(departamento)
            session.commit()
            print(f"Departamento '{departamento.nome}' excluído com sucesso!")
        else:
            print("Departamento não encontrado.")
# excluir_departamento()