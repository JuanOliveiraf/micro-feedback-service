from models import FeedbackSaida,FeedbackResponse
from typing import List
from db import get_connection


def gerar_feedbacks(mentored_id: int) -> List[FeedbackSaida]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(""" UPDATE mentorings
                       SET concluded = true
                       WHERE TIMESTAMPDIFF(MINUTE,scheduled_date,DATE_SUB(NOW(), INTERVAL 3 HOUR)) > 0
                       AND mentored_id = %s""",(mentored_id,))
    conn.commit()

    cursor.execute("""SELECT T2.id 
                    ,T3.name AS mentor_name
                    ,T2.name AS mentoring_name
                    ,T2.scheduled_date
                    ,T2.rating
                    FROM users T1
                    LEFT JOIN mentorings T2
                    	ON T1.id = T2.mentored_id
                    LEFT JOIN users T3
                    	ON T2.mentor_id = T3.id
                    WHERE TRUE
                    AND mentored_id = %s
                    AND concluded is true""", (mentored_id,))
    feedbacks = cursor.fetchall()
    print(feedbacks)
    cursor.close()
    conn.close()

    return [FeedbackSaida(
        id=feedback['id'],
        mentor_name=feedback['mentor_name'],
        mentoring_name=feedback['mentoring_name'],
        scheduled_date=feedback['scheduled_date'],
        mentoring_rating=feedback['rating']
    ) for feedback in feedbacks]


def gerar_avaliacao(dados: FeedbackResponse):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""UPDATE mentorings
                      SET RATING = %s
                      WHERE ID = %s""",(dados.rating,dados.mentoring_id,))
    
    conn.commit()

    cursor.close()
    conn.close()

    return