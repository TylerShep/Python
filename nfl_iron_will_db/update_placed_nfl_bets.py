#ADD 'bet_results' and 'iw_commissions' COLUMNS AND DATA FOR "placed_bet" TABLE:
conn = pyodbc.connect('DRIVER={' + SECRETS_USU_DRIVER + '};'
                      'Server=' + SECRETS_USU_SERVER + ';'
                      'Database=' + SECRETS_USU_DB + ';'
                      'UID=' + SECRETS_USU_UID + ';'
                      'PWD=' + SECRETS_USU_PWD + ';'
                      'Trusted_Connection=no;')

cursor = dmconn.cursor()

cursor.execute('''ALTER TABLE placed_bet
    ADD COLUMN IF NOT EXISTS bet_results VARCHAR(15),
    ADD COLUMN IF NOT EXISTS iw_commission INT;''')
cursor.commit()

dfc = pd.read_sql('''select iw.bet_id,
       iw.customer_id,
       iw.bet_on,
       iw.bet_amount,
       iw.bet_results,
       iw.iw_commission
from(select pb.bet_id,
       pb.customer_id,
       pb.bet_on,
       case
           when pb.bet_on = data.game_winner and pb.bet_on = data.game_team_favorite and
                data.actual_score_diff > data.game_fav_spread then 'win'
           when pb.bet_on = data.game_winner and pb.bet_on != data.game_team_favorite then 'win'
           when pb.bet_on != data.game_winner and pb.bet_on != data.game_team_favorite and
                data.actual_score_diff <= data.game_fav_spread then 'win'
           when (pb.bet_on = 'over' and data.over_under = 'over') or (pb.bet_on = 'under' and data.over_under = 'under')
               then 'win'
           when pb.bet_on in ('over', 'under') and data.over_under = 'push' then 'push'
           when pb.bet_on = data.game_winner and pb.bet_on = data.game_team_favorite and
                data.actual_score_diff = data.game_fav_spread then 'push'
           else 'loss' end as "bet_results",
    pb.bet_amount,
    case when pb.bet_amount <= 1000 then 0.10 * pb.bet_amount
        when pb.bet_amount <= 5000 then 100 + (0.08 * (pb.bet_amount -1000))
        when pb.bet_amount > 5000 then 100 + 80 + (0.06 * (pb.bet_amount -5000)) end as "iw_commission"

from placed_bet pb
         left join lateral (select ng.game_id,
                                   ng.game_team_favorite,
                                   abs(ng.game_favorite_spread)                 as "game_fav_spread",
                                   abs(ng.home_team_score - ng.away_team_score) as "actual_score_diff",
                                   case
                                       when ng.home_team_score > ng.away_team_score then ng.game_home_team
                                       else ng.game_away_team end               as "game_winner",
                                   case
                                       when (ng.away_team_score + ng.home_team_score) > ng.game_ou_line then 'over'
                                       when (ng.away_team_score + ng.home_team_score) < ng.game_ou_line then 'under'
                                       else 'push' end                          as "over_under"

                            from nfl_games ng
                            where ng.game_ou_line is not null
                              and ng.game_id = pb.game_id) as "data" on true
         join nfl_team nt on nt.team_name = data.game_winner) as "iw";''', dmconn)

for x in dfc.index:
    cursor.execute('''UPDATE placed_bet
                      SET bet_results= '%s', iw_commission= %d
                      WHERE bet_id = %d''' % (dfc['bet_results'].loc[x], dfc['iw_commission'].loc[x], dfc['bet_id'].loc[x]))
    dmconn.commit()
    bet_id_str = str(dfc['bet_id'].loc[x])
    print("Betting record id %s updated" % (bet_id_str))
