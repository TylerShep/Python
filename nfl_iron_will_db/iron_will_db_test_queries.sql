#No.1 Output first 5 rows of data in each table:
select * from nfl_games order by game_id ASC limit 5;
select * from nfl_stadium order by stadium_name limit 5;
select * from nfl_team order by team_name limit 5;
select * from bet_customer order by customer_id limit 5;
select * from placed_bet order by bet_id limit 5;


#No.2a $2000 commissions paid percentage:
select iw.tot_2000_club_bettors,
       iw.tot_customers,
       (iw.tot_2000_club_bettors / iw.tot_customers) * 100 as "percent_basket_recievers"
from (select count(*)          as "tot_customers",
             count(data.customer_id) as "tot_2000_club_bettors"
      from bet_customer bc
          left join lateral (select pb.customer_id,
                                         sum(pb.iw_commission) as "tot_comission_paid"
                                  from placed_bet pb
                                  where bc.customer_id = pb.customer_id
                                  group by pb.customer_id
                                  having sum(pb.iw_commission) > 2000) as "data" on true) as "iw";
 
 
#No.2b Top 20 paying customers:
select pb.customer_id,
       bc.customer_fname,
       bc.customer_lname,
       sum(pb.iw_commission)::money as "tot_comission_paid"
from placed_bet pb
    join bet_customer bc on pb.customer_id = bc.customer_id
group by bc.customer_fname, pb.customer_id, bc.customer_lname
having sum(pb.iw_commission) > 2000
order by 4 desc limit 20;


#No.3 10 luckiest bettors:
select data.customer_id,
    data.customer_fname,
       data.customer_lname,
       data.tot_bets,
       data.tot_wins,
       to_char(data.win_percentage,'999D99%') as "win_percentage",
       data.tot_winnings
from(select bc.customer_id,
       bc.customer_fname,
       bc.customer_lname,
       count(pb.bet_id)                                        as "tot_bets",
       sum(case when pb.bet_results = 'win' then 1 else 0 end) as "tot_wins",
       ((sum(case when pb.bet_results = 'win' then 1 else 0 end)::float4) / (count(pb.bet_id)::float)) * 100 as "win_percentage",
       sum(case when pb.bet_results = 'win' then (pb.bet_amount * 2)
            when pb.bet_results = 'loss' then ((pb.bet_amount + pb.iw_commission) * -1)
            when pb.bet_results = 'push' then 0 end)::money as "tot_winnings"
from placed_bet pb
   join bet_customer bc on pb.customer_id = bc.customer_id
group by bc.customer_id, bc.customer_fname, bc.customer_lname
having count(pb.bet_id) >=  6) as "data"
order by data.win_percentage DESC, data.tot_winnings DESC limit 10;


#No.4 Teams bet for/against stats:
with home_team as (select nt.team_name,
                          sum(case when ng.home_team_score > ng.away_team_score then 1 else 0 end) as "tot_wins_as_home",
                          sum(case when ng.home_team_score < ng.away_team_score then 1 else 0 end) as "tot_losses_as_home",
                          sum(case
                                  when ng.game_home_team = ng.game_team_favorite and
                                       ng.home_team_score > ng.away_team_score and
                                       abs(ng.game_favorite_spread) < abs(ng.home_team_score - ng.away_team_score)
                                      then 1
                                  when ng.game_home_team != ng.game_team_favorite and
                                       ng.home_team_score > ng.away_team_score then 1
                                  when ng.game_home_team != ng.game_team_favorite and
                                       ng.home_team_score < ng.away_team_score and
                                       abs(ng.game_favorite_spread) > abs(ng.home_team_score - ng.away_team_score)
                                      then 1
                                  else 0 end)                                                      as "tot_times_beat_spread_home"
                   from nfl_team nt
                       join nfl_games ng on nt.team_name = ng.game_home_team
                   where ng.game_season = '2022'
                   group by nt.team_name),

     away_team as (select nt.team_name,
                          sum(case when ng.away_team_score > ng.home_team_score then 1 else 0 end) as "tot_wins_as_away",
                          sum(case when ng.away_team_score < ng.home_team_score then 1 else 0 end) as "tot_losses_as_away",
                          sum(case
                                  when ng.game_away_team = ng.game_team_favorite and
                                       ng.away_team_score > ng.home_team_score and
                                       abs(ng.game_favorite_spread) < abs(ng.away_team_score - ng.home_team_score)
                                      then 1
                                  when ng.game_away_team != ng.game_team_favorite and
                                       ng.away_team_score > ng.home_team_score then 1
                                  when ng.game_away_team != ng.game_team_favorite and
                                       ng.away_team_score < ng.home_team_score and
                                       abs(ng.game_favorite_spread) > abs(ng.away_team_score - ng.home_team_score)
                                      then 1
                                  else 0 end)                                                      as "tot_times_beat_spread_away"
                   from nfl_team nt
                      join nfl_games ng on nt.team_name = ng.game_away_team
                   where ng.game_season = '2022'
                   group by nt.team_name),
    bet_on_team as (select pb.bet_id,
                        pb.bet_on
                    from placed_bet pb)

select nt.team_name,
       sum(ht.tot_wins_as_home + at.tot_wins_as_away)                     as "tot_wins",
       sum(ht.tot_losses_as_home + at.tot_losses_as_away)                 as "tot_losses",
       sum(ht.tot_times_beat_spread_home + at.tot_times_beat_spread_away) as "tot_times_beat_spread"
from nfl_team nt
  join home_team ht on nt.team_name = ht.team_name
  join away_team at on nt.team_name = at.team_nam
group by nt.team_name
order by nt.team_name ASC;


#No.5 Top 20 costliest customer for IW:
select bc.customer_fname,
       bc.customer_lname,
       count(pb.bet_id) as "tot_bets",
       sum(case when pb.bet_results = 'win' then 1 else 0 end) as "tot_bets_won",
       sum(case when pb.bet_results = 'win' then ((pb.bet_amount * 2) * -1)
            when pb.bet_results = 'loss' then (pb.bet_amount + pb.iw_commission)
            when pb.bet_results = 'push' then 0 end)::money as "iw_betting_net"
from placed_bet pb
  join  bet_customer bc on pb.customer_id = bc.customer_id
group by bc.customer_fname, bc.customer_lname
order by iw_betting_net ASC limit 20;


#No.6 Weeks percentage of bet winners/losers:
select ng.game_season,
       substring(ng.game_id,5,2) as "week",
       count(pb.bet_id) as "num-bets",
       to_char((sum(case when pb.bet_results = 'win' then 1 else 0 end)::float4 / count(pb.bet_id)::float4) * 100,'999D99%') as "percent_win",
        to_char((sum(case when pb.bet_results = 'loss' then 1 else 0 end)::float4 / count(pb.bet_id)::float4) * 100,'999D99%') as "percent_win"
from placed_bet pb
  join bet_customer bc on pb.customer_id = bc.customer_id
  join nfl_games ng on pb.game_id = ng.game_id
where game_season = '2022'
group by ng.game_season, substring(ng.game_id,5,2)
order by 2 asc;
