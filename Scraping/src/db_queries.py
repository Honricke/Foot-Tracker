from src.conn import conn
from src.classes import Rating, Matches
from datetime import datetime

cursor = conn.cursor()

def get_last_date():
    # Executando a consulta
    cursor.execute("""
        SELECT match_date
        FROM Matches
        ORDER BY match_date DESC
        LIMIT 1;
    """)

    return cursor.fetchone()[0]

def get_player_add_if_not(player_name: str, team_id: int):
    global cursor
    # Verificar se o jogador já existe na tabela Player com base no nome e no time
    cursor.execute("""
        SELECT id FROM Player 
        WHERE player_name = %s AND team_id = %s
    """, (player_name, team_id))
    
    existing_player = cursor.fetchone()
    
    # Se o jogador não existe, realiza o INSERT
    if not existing_player:
        cursor.execute("""
            INSERT INTO Player (player_name, team_id)
            VALUES (%s, %s)
            RETURNING id;
        """, (player_name, team_id))
        player_id = cursor.fetchone()[0]
        print("Jogador adicionado com ID:", player_id)
        return player_id
    else:
        print("Jogador já existe com ID:", existing_player[0])
        return existing_player[0]

def get_stadium_add_if_not(stadium_name: str):
    global cursor
    # Verificar se o estádio já existe na tabela Stadium com base no nome
    cursor.execute("""
        SELECT id FROM Stadium 
        WHERE stadium_name = %s
    """, (stadium_name,))
    
    # Se o estádio já existe, o SELECT retornará um valor
    existing_stadium = cursor.fetchone()
    
    # Se o estádio não existe, realiza o INSERT
    if not existing_stadium:
        cursor.execute("""
            INSERT INTO Stadium (stadium_name)
            VALUES (%s)
            RETURNING id;
        """, (stadium_name,))
        stadium_id = cursor.fetchone()[0]
        print("Estádio adicionado com ID:", stadium_id)
        return stadium_id
    else:
        print("Estádio já existe com ID:", existing_stadium[0])
        return existing_stadium[0]

def get_referee_add_if_not(referee_name: str):
    global cursor
    # Verificar se o árbitro já existe na tabela Referee com base no nome
    cursor.execute("""
        SELECT id FROM Referee 
        WHERE referee_name = %s
    """, (referee_name,))
    
    # Se o árbitro já existe, o SELECT retornará um valor
    existing_referee = cursor.fetchone()
    
    # Se o árbitro não existe, realiza o INSERT
    if not existing_referee:
        cursor.execute("""
            INSERT INTO Referee (referee_name)
            VALUES (%s)
            RETURNING id;
        """, (referee_name,))
        referee_id = cursor.fetchone()[0]
        print("Árbitro adicionado com ID:", referee_id)
        return referee_id
    else:
        print("Árbitro já existe com ID:", existing_referee[0])
        return existing_referee[0]

def get_team_add_if_not(team_name: str):
    global cursor
    # Verificar se o time já existe na tabela Team com base no nome
    cursor.execute("""
        SELECT id FROM Team 
        WHERE team_name = %s
    """, (team_name,))
    
    existing_team = cursor.fetchone()
    
    # Se o time não existe, realiza o INSERT
    if not existing_team:
        cursor.execute("""
            INSERT INTO Team (team_name)
            VALUES (%s)
            RETURNING id;
        """, (team_name,))
        team_id = cursor.fetchone()[0]
        print("Time adicionado com ID:", team_id)
        return team_id
    else:        
        print("Time já existe com ID:", existing_team[0])
        return existing_team[0]

def add_injurie(match_id: int, player_id: int):
    insert_injury_query = """
        INSERT INTO Injuries (match_id, player_id)
        VALUES (%s, %s)
        RETURNING id;
    """

    # Executando o comando
    cursor.execute(insert_injury_query, (match_id, player_id))

def add__player_rating(home_score: list[Rating],away_score: list[Rating], match_id: int, home_id: int, away_id: int):
    global cursor

    for player in home_score:
        player_id = get_player_add_if_not(player['name'],home_id)
        
        if player["injurie"]: add_injurie(match_id,player_id)
        
        cursor.execute("""
            INSERT INTO Rating (player_id, match_id, rating)
            VALUES (%s, %s, %s)
        """, (player_id, match_id, player["score"]))

    for player in away_score:
        player_id = get_player_add_if_not(player['name'],away_id)
        
        if player["injurie"]: add_injurie(match_id,player_id)
        
        cursor.execute("""
            INSERT INTO Rating (player_id, match_id, rating)
            VALUES (%s, %s, %s)
        """, (player_id, match_id, player["score"]))

def save_match_data(data: Matches):
    global cursor
    home_team_id = get_team_add_if_not(data.home_team)
    away_team_id = get_team_add_if_not(data.away_team)
    
    referee_id = get_referee_add_if_not(data.referee)
    stadium_id = get_stadium_add_if_not(data.stadium)
        
    date = datetime.strptime(data.date, "%d/%m/%Y")
    
    cursor.execute("""
                INSERT INTO Matches (
                    home_team_id, away_team_id, referee_id, stadium_id, scoreboard, match_date, 
                    possession, expected_goals, shots, goalkeeper_saves,
                    corners, fouls, passes, tackles, direct_kicks, yellow_cards, red_cards,
                    home_ranking, away_ranking
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s
                )
                RETURNING id
            """, ( home_team_id, away_team_id, referee_id, stadium_id, data.scoreboard, date,
                ' - '.join(data.game_statistic['Posse de bola']),
                ' - '.join(data.game_statistic['Expected goals']),
                # ' - '.join(data.game_statistic['Grandes chances de gol']),
                ' - '.join(data.game_statistic['Finalizações']),
                ' - '.join(data.game_statistic['Defesas do goleiro']),
                ' - '.join(data.game_statistic['Escanteios']),
                ' - '.join(data.game_statistic['Faltas']),
                ' - '.join(data.game_statistic['Passes']),
                ' - '.join(data.game_statistic['Desarmes']),
                ' - '.join(data.game_statistic['Faltas (Tiros Diretos)']),
                data.game_statistic['Cartões amarelos'],
                data.game_statistic['Cartões vermelhos'],
                data.home_classification,
                data.away_classification,
            ))
    
    match_id = cursor.fetchone()[0]

    add__player_rating(data.home_player_score,data.away_player_score,match_id,home_team_id,away_team_id)
    
    conn.commit()