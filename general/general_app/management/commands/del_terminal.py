import sqlite3
from sqlite3 import Error

from django.core.management.base import BaseCommand
from general_app.models import SimCards, TerminalSimCard, SimCard, Terminals


class Command(BaseCommand):
    help = 'rename Comment model'

    def handle(self, *args, **options):
        sim_list = SimCards.objects.all()
        for sim in sim_list:
            s1 = SimCard(
                    operator=sim.operator,
                    number=sim.number,
                    icc=sim.icc
                )
            s1.save()
            if sim.terminal:
                t1 = TerminalSimCard(
                    terminal=sim.terminal,
                    sim_card=s1
                )
                t1.save()
            sim.delete()




#        def sql_connection():
#            try:
#                return sqlite3.connect('db.sqlite3')
#            except Error:
#                print(Error)
#
#        def sql_table(con):
#            cursor = con.cursor()
#            cursor.execute(
#                'ALTER TABLE "reviews_comments" RENAME TO "reviews_comment"'
#            )
#            con.commit()
#
#        con = sql_connection()
#        sql_table(con)