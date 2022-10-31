import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = \
            mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `dougfit`;")

cursor.execute("CREATE DATABASE `dougfit`;")

cursor.execute("USE `dougfit`;")

# criando tabelas (ARRUMAR FK)
TABLES = {}
TABLES['Musculo'] = ('''
      CREATE TABLE `musculo` (
      `ID` int NOT NULL AUTO_INCREMENT,
      `NOME` varchar(255) NOT NULL,
      `CATEGORIA` varchar(255) NOT NULL,
      PRIMARY KEY (`ID`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')

TABLES['RelacaoMusculo'] = ('''
      CREATE TABLE `relacao_musculo` (
      `ID` int NOT NULL AUTO_INCREMENT,
      `REF_1` int NOT NULL,
      `REF_2` int DEFAULT NULL,
      `REF_3` int DEFAULT NULL,
      PRIMARY KEY (`ID`),      
      CONSTRAINT `relacao_musculo_ibfk_1` FOREIGN KEY (`REF_1`) REFERENCES `musculo` (`ID`),
      CONSTRAINT `relacao_musculo_ibfk_2` FOREIGN KEY (`REF_2`) REFERENCES `musculo` (`ID`),
      CONSTRAINT `relacao_musculo_ibfk_3` FOREIGN KEY (`REF_3`) REFERENCES `musculo` (`ID`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')

TABLES['Exercicio'] = ('''
      CREATE TABLE `exercicio` (
      `ID` int NOT NULL AUTO_INCREMENT,
      `NOME` varchar(255) NOT NULL,
      `RELACAO_MUSCULO` int NOT NULL,
      `DESCRICAO` varchar(255) DEFAULT NULL,
      PRIMARY KEY (`ID`),
      KEY `RELACAO_MUSCULO` (`RELACAO_MUSCULO`),
      CONSTRAINT `exercicio_ibfk_1` FOREIGN KEY (`RELACAO_MUSCULO`) REFERENCES `relacao_musculo` (`ID`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')

TABLES['RelacaoExercicio'] = ('''
      CREATE TABLE `relacao_exercicio` (
      `ID` int NOT NULL AUTO_INCREMENT,
      `REF_1` int NOT NULL,
      `REF_2` int DEFAULT NULL,
      `REF_3` int DEFAULT NULL,
      `REF_4` int DEFAULT NULL,
      `REF_5` int DEFAULT NULL,
      `REF_6` int DEFAULT NULL,
      `REF_7` int DEFAULT NULL,
      `REF_8` int DEFAULT NULL,
      `REF_9` int DEFAULT NULL,
      PRIMARY KEY (`ID`),      
      CONSTRAINT `relacao_exercicio_ibfk_1` FOREIGN KEY (`REF_1`) REFERENCES `exercicio` (`ID`),
      CONSTRAINT `relacao_exercicio_ibfk_2` FOREIGN KEY (`REF_2`) REFERENCES `exercicio` (`ID`),
      CONSTRAINT `relacao_exercicio_ibfk_3` FOREIGN KEY (`REF_3`) REFERENCES `exercicio` (`ID`),
      CONSTRAINT `relacao_exercicio_ibfk_4` FOREIGN KEY (`REF_4`) REFERENCES `exercicio` (`ID`),
      CONSTRAINT `relacao_exercicio_ibfk_5` FOREIGN KEY (`REF_5`) REFERENCES `exercicio` (`ID`),
      CONSTRAINT `relacao_exercicio_ibfk_6` FOREIGN KEY (`REF_6`) REFERENCES `exercicio` (`ID`),
      CONSTRAINT `relacao_exercicio_ibfk_7` FOREIGN KEY (`REF_7`) REFERENCES `exercicio` (`ID`),
      CONSTRAINT `relacao_exercicio_ibfk_8` FOREIGN KEY (`REF_8`) REFERENCES `exercicio` (`ID`),
      CONSTRAINT `relacao_exercicio_ibfk_9` FOREIGN KEY (`REF_9`) REFERENCES `exercicio` (`ID`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')

TABLES['Treino'] = ('''
      CREATE TABLE `treino` (
      `ID` int NOT NULL AUTO_INCREMENT,
      `NOME` varchar(255) NOT NULL,
      `RELACAO_MUSCULO` int NOT NULL,
      `RELACAO_EXERCICIO` int NOT NULL,
      PRIMARY KEY (`ID`),
      CONSTRAINT `treino_ibfk_1` FOREIGN KEY (`RELACAO_MUSCULO`) REFERENCES `relacao_musculo` (`ID`),
      CONSTRAINT `treino_ibfk_2` FOREIGN KEY (`RELACAO_EXERCICIO`) REFERENCES `relacao_exercicio` (`ID`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')

TABLES['TreinoCompleto'] = ('''
      CREATE TABLE `treino_completo` (
      `ID` int NOT NULL AUTO_INCREMENT,
      `NOME` varchar(255) NOT NULL,
      `NIVEL` varchar(255) NOT NULL,
      `OBJETIVO` varchar(255) NOT NULL,
      `FOCO` varchar(255) NOT NULL,
      `TREINO_A` int NOT NULL,
      `TREINO_B` int DEFAULT NULL,
      `TREINO_C` int DEFAULT NULL,
      `TREINO_D` int DEFAULT NULL,
      `TREINO_E` int DEFAULT NULL,
      `TREINO_F` int DEFAULT NULL,
      PRIMARY KEY (`ID`),
      CONSTRAINT `treino_completo_ibfk_1` FOREIGN KEY (`TREINO_A`) REFERENCES `treino` (`ID`),
      CONSTRAINT `treino_completo_ibfk_2` FOREIGN KEY (`TREINO_B`) REFERENCES `treino` (`ID`),
      CONSTRAINT `treino_completo_ibfk_3` FOREIGN KEY (`TREINO_C`) REFERENCES `treino` (`ID`),
      CONSTRAINT `treino_completo_ibfk_4` FOREIGN KEY (`TREINO_D`) REFERENCES `treino` (`ID`),
      CONSTRAINT `treino_completo_ibfk_5` FOREIGN KEY (`TREINO_E`) REFERENCES `treino` (`ID`),
      CONSTRAINT `treino_completo_ibfk_6` FOREIGN KEY (`TREINO_F`) REFERENCES `treino` (`ID`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nick` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nick`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nick, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Douglas Aguiar", "ell", generate_password_hash("1111").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from dougfit.usuarios')
print('-------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo musculos
musculos_sql = 'INSERT INTO musculo (NOME, CATEGORIA) VALUES (%s, %s)'
musculos = [
      ('Peito', 'Grande'),
      ('Costas', 'Grande'),
      ('Perna', 'Grande'),
      ('Biceps', 'Pequeno'),
      ('Triceps', 'Pequeno'),
      ('Ombro', 'Pequeno'),
      ('Panturrilha', 'Resistente'),
      ('Abdomen', 'Resistente'),
      ('Antebraço', 'Pequeno'),
      ('Trapezio', 'Pequeno')
]
cursor.executemany(musculos_sql, musculos)

cursor.execute('select * from dougfit.musculo')
print(' -------------  Musculos:  -------------')
for musculo in cursor.fetchall():
    print(musculo[1])

# inserindo relacao musculo
relacao_musculos_sql = 'INSERT INTO relacao_musculo (REF_1) VALUES (%s)'
relacao_musculos = [
      (1,),
      (2,),
      (3,),
      (4,),
      (5,),
      (6,),
      (7,),
      (8,),
      (9,),
      (10,)
]
cursor.executemany(relacao_musculos_sql, relacao_musculos)

cursor.execute('select * from dougfit.relacao_musculo')
print(' -------------  Relacao Musculos:  -------------')
for relacao_musculo in cursor.fetchall():
    print(relacao_musculo[1])

# inserindo relacao musculo2
relacao_musculos2_sql = 'INSERT INTO relacao_musculo (REF_1, REF_2, REF_3) VALUES (%s, %s, %s)'
relacao_musculos2 = [
      (1, 5, 7),
      (2, 4, 9),
      (3, 6, 8)
]
cursor.executemany(relacao_musculos2_sql, relacao_musculos2)

cursor.execute('select * from dougfit.relacao_musculo')
print(' -------------  Relacao Musculos:  -------------')
for relacao_musculo2 in cursor.fetchall():
    print(relacao_musculo2[1])

# inserindo exercicio
exercicios_sql = 'INSERT INTO exercicio (NOME, RELACAO_MUSCULO, DESCRICAO) VALUES (%s, %s, %s)'
exercicios = [
      ('Supino Reto', 1, 'Exercício construtor de peito com barra e anilhas'),
      ('Dumbell Press', 1, 'Exercício construtor de peito com halteres'),
      ('Voador', 1, 'Exercício localizado de peito na máquina'),
      ('Barra Fixa', 2, 'Exercício construtor de costas com peso livre'),
      ('Remada Curvada Supinada', 2, 'Exercício construtor de costas com barra e anilhas'),
      ('Puxador Frente Triângulo', 2, 'Exercício localizado de costas na máquina'),
      ('Agachamento', 3, 'Exercício construtor de perna com barra e anilhas'),
      ('Cadeira Extensora', 3, 'Exercício localizado de perna na máquina com foco em quadríceps'),
      ('Leg Press 45º', 3, 'Exercício construtor de perna na máquina'),
      ('Rosca Direta Barra', 4, 'Exercício construtor de bíceps com barra e anilhas'),
      ('Rosca Concentrada', 4, 'Exercício localizado de bíceps com halteres'),
      ('Rosca Alternada', 4, 'Exercício unilateral de bíceps com halteres'),
      ('Paralelas', 5, 'Exercício construtor de tríceps com peso livre'),
      ('Triceps Testa', 5, 'Exercício construtor de tríceps com barra e anilhas'),
      ('Triceps Corda', 5, 'Exercício localizado de tríceps na máquina'),
      ('Elevação Lateral', 6, 'Exercício localizado de ombro com halteres'),
      ('Desenvolvimento', 6, 'Exercício construtor de ombro com halteres'),
      ('Elevação Frontal Anilha', 6, 'Exercício localizado de ombro com anilhas'),
      ('Gêmeos Em Pé Na Máquina', 7, 'Exercício localizado de panturrilha na máquina'),
      ('Gêmeos Banco', 7, 'Exercício localizado de panturrilha na máquina'),
      ('Gêmeos Leg 45º', 7, 'Exercício localizado de panturrilha na máquina'),
      ('Supra', 8, 'Exercício localizado de abdômen com peso livre foco parte superior'),
      ('Infra', 8, 'Exercício localizado de abdômen com peso livre foco parte inferior'),
      ('Prancha', 8, 'Exercício localizado de abdômen com peso livre foco no core'),
      ('Rosca Invertida', 9, 'Exercício construtor de antebraço com barra e anilhas'),
      ('Extensão Punho', 9, 'Exercício localizado de antebraço com halteres'),
      ('Segurar Haltere', 9, 'Exercício isométrico com halteres'),
      ('Encolhimento', 10, 'Exercício isolado de trapézio com halteres'),
      ('Remada Alta', 10, 'Exercício construtor de trapézio com barra w e anilhas')
]
cursor.executemany(exercicios_sql, exercicios)

cursor.execute('select * from dougfit.exercicio')
print(' -------------  Exercicios:  -------------')
for exercicio in cursor.fetchall():
    print(exercicio[1])

# inserindo relacao exercicio
relacao_exercicios_sql = 'INSERT INTO relacao_exercicio (REF_1, REF_2, REF_3, REF_4, REF_5, REF_6, REF_7, REF_8, REF_9) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
relacao_exercicios = [
      (1, 2, 3, 13, 14, 15, 19, 20, 21),
      (4, 5, 6, 10, 11, 12, 25, 26, 27),
      (7, 8, 9, 16, 17, 18, 22, 23, 24)
]
cursor.executemany(relacao_exercicios_sql, relacao_exercicios)

cursor.execute('select * from dougfit.relacao_exercicio')
print(' -------------  Relacao Exercicios:  -------------')
for relacao_exercicio in cursor.fetchall():
    print(relacao_exercicio[1])

# inserindo treino
treinos_sql = 'INSERT INTO treino (NOME, RELACAO_MUSCULO, RELACAO_EXERCICIO) VALUES (%s, %s, %s)'
treinos = [
      ('Push', 11, 1),
      ('Pull', 12, 2),
      ('Legs', 13, 3)
]
cursor.executemany(treinos_sql, treinos)

cursor.execute('select * from dougfit.treino')
print(' -------------  Treinos:  -------------')
for treino in cursor.fetchall():
    print(treino[1])

# inserindo treino completo

treinos_completos_sql = 'INSERT INTO treino_completo (NOME, NIVEL, OBJETIVO, FOCO, TREINO_A, TREINO_B, TREINO_C, TREINO_D, TREINO_E,  TREINO_F) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
treinos_completos = [
      ('1 - ABC - Push, Pull, Legs', 'Intermediário', 'Hipertrofia', 'Total', 1, 2, 3, 1, 2, 3),
      ('2 - ABC - Push, Pull, Legs', 'Intermediário', 'Hipertrofia', 'Total', 1, 2, 3, 1, 2, 3),
      ('3 - ABC - Push, Pull, Legs', 'Intermediário', 'Hipertrofia', 'Total', 1, 2, 3, 1, 2, 3)
]

cursor.executemany(treinos_completos_sql, treinos_completos)

cursor.execute('select * from dougfit.treino_completo')
print(' -------------  Treinos Completos:  -------------')
for treino_completo in cursor.fetchall():
    print(treino_completo[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()