from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

#Criar base da classe
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))

    #Relacionamento com pedidos
    pedidos = relationship("Pedido", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}')>"
    
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto = Column(String(150))

    #Chave Estrangeira
    # Onde tem o foreign key, tem o relacionamento muitos para um (Muitos pedidos para um usuário)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    #Relacionamento
    usuario = relationship("Usuario", back_populates="pedidos")

    def __repr__(self):
        return f"<Pedido(id={self.id}, produto='{self.produto}')>"

#Criar engine e sessão
engine = create_engine("sqlite:///loja.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#Criar usuários
usuario1 = Usuario(nome="Enzo")

#Criar pedidos
pedido1 = Pedido(produto="BYD")
pedido2 = Pedido(produto="Crack")

#Associar pedidos ao usuário
# usuario1.pedidos.append(pedido1)
# usuario1.pedidos.append(pedido2)

# #Salvar no banco de dados
# session.add(usuario1)
# session.commit()

# print(f"Usuário cadastrado: {usuario1}")
# for pedido in usuario1.pedidos:
#     print(f"Pedido cadastrado: {pedido}")

todos_usuarios = session.query(Usuario).all()
for usuario in todos_usuarios:
    print(f"\nNome: {usuario.nome}")
    for pedido in usuario.pedidos:
        print(f"Produto: {pedido.produto}")