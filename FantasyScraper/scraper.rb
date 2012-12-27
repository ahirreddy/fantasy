require 'wombat'
require 'pp'
require 'pg'
require 'uri'

p = URI.parse(ENV['DATABASE_URL'] || 'postgres://localhost/fantasy')

db = PGconn.open(:host => p.host, :port => p.port, :user => p.user, :password => p.password)

# Create Database Fantasy if it does not exist
res = db.exec "SELECT 1 FROM pg_database WHERE datname='fantasy'"
if res.ntuples == 0
  db.exec "CREATE DATABASE fantasy"
end

db.close

db = PGconn.open(:host => p.host, :port => p.port, :user => p.user, :password => p.password, :dbname => 'fantasy')

db.exec "CREATE TABLE IF NOT EXISTS fantasy (player_name TEXT, fteam INT, fgm INT, fga INT, ftm INT, fta INT, reb INT, ast INT, stl INT, blk INT, tover INT, pts INT, fpts INT, opp TEXT, slot TEXT, period_id INT)"

opening_night = Time.parse("30/10/2012")
one_day = 60*60*24
current_period = ((Time.now - opening_night) / one_day).to_i

last_update = ((db.exec "SELECT MAX(period_id) FROM fantasy;")[0][0] or 0) + 1

(last_update..current_period).each do |period_id|
  (1..8).each do |team_id|
    data = Wombat.crawl do  
      base_url "http://games.espn.go.com"
      path "/fba/clubhouse?leagueId=202659&teamId=#{team_id}&seasonId=2013&scoringPeriodId=#{period_id}"

      players "css=.pncPlayerRow", :iterator do
        name  "css=td.playertablePlayerName a"
        opp   "css=td div a"
        slot  "css=td.playerSlot"
        stats "css=td.playertableStat", :list
      end
    end
    data["players"].each do |p|
      stats = p["stats"]
      if stats[0] == '--'
        next
      end
      p["name"].gsub!(/[`'"]|(\ \ )/," ")
      query = "INSERT INTO fantasy VALUES ('#{p["name"]}', #{team_id}, #{stats[0]}, #{stats[1]}, #{stats[2]}, #{stats[3]}, #{stats[4]}, #{stats[5]}, #{stats[6]}, #{stats[7]}, #{stats[8]}, #{stats[9]}, #{stats[10]}, '#{p["opp"]}', '#{p["slot"]}', #{period_id});"
      pp query
      db.exec query
    end
  end      
end

###########################
# Insert free agent records
###########################
(last_update..current_period).each do |period_id|
  (0..250).step(50).each do |start_idx|
    data = Wombat.crawl do  
      base_url "http://games.espn.go.com"
      path "/fba/leaders?leagueId=202659&scoringPeriodId=#{period_id}&seasonId=2013&startIndex=#{start_idx}"

      players "css=.pncPlayerRow", :iterator do
        name  "css=td.playertablePlayerName a"
        opp   "css=td div a"
        stats "css=td.playertableStat", :list
      end
    end
    data["players"].each do |p|
      stats = p["stats"]
      if stats[0] == '--'
        break
      end
      p["name"].gsub!(/[`'"]|(\ \ )/," ")
      if db.exec("SELECT count(*) FROM fantasy WHERE player_name = '#{p["name"]}' AND period_id = #{period_id};")[0][0] == 0
        query = "INSERT INTO fantasy VALUES ('#{p["name"]}', '', #{stats[1]}, #{stats[2]}, #{stats[3]}, #{stats[4]}, #{stats[5]}, #{stats[6]}, #{stats[7]}, #{stats[8]}, #{stats[9]}, #{stats[10]}, #{stats[11]}, '#{p["opp"]}', 'FA', #{period_id});"
        pp query
        db.exec query
      end
    end
  end      
end

db.close

