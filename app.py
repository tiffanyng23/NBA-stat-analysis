from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np 
import plotly.express as px
import dash_bootstrap_components as dbc

#datasets
#team data
team_data = pd.read_csv("cleaned_game_stats.csv")
team_data = team_data.drop(["Rk", "Top10"], axis=1)

#player data
player_data = pd.read_csv("player_stats_2022_2023.csv")
player_data = player_data.drop("RANK", axis=1)

#initializing app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

#controls
controls_1 = dbc.Card(
    [
        html.Div(
            [    
                dbc.Label(children="Choose a Season:"),
                dcc.Dropdown(
                    options=["2018-2019","2019-2020", "2020-2021", "2021-2022", "2022-2023"], 
                    value="2022-2023", 
                    id="season-chosen"
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label(children="Choose Two Teams to Compare:"),
                dcc.Dropdown(
                        options=['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'], 
                        value="Milwaukee Bucks", id="team-1"
                        ),
                dcc.Dropdown(
                    options=['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'], 
                    value="Boston Celtics", id="team-2"
                    ),
            ]
        ),
        html.Div(
            [
                dbc.Label(children="Choose a Statistical Category:"),
                dcc.Dropdown(
                    options=["FGA","FG%","3P","3P%","2P","2P%","FT","FT%","ORB","TRB","AST","STL","BLK","TOV","PF","PTS"],
                    value="PTS", id="team-var"
                    ), 
            ]
        ), 
     ],
    body=True, color= "lightgrey", 
)       

controls_2=dbc.Card([      
        html.Div(
            [
                dbc.Label(children="Choose a Season:"),
                dcc.Dropdown(
                    options=["2018-2019","2019-2020", "2020-2021", "2021-2022", "2022-2023"], 
                    value="2022-2023", id="scatter-season"
                    ),
            ]
        ),
        html.Div(
            [
                dbc.Label(children="Choose Two Different Statistical Categories:"),
                dcc.Dropdown(
                    options=["FGA","FG%","3P","3P%","2P","2P%","FT","FT%","ORB","TRB","AST","STL","BLK","TOV","PF","PTS"],
                    value="PTS", id="scatter-var-1"
                    ),
                dcc.Dropdown(options=["FGA","FG%","3P","3P%","2P","2P%","FT","FT%","ORB","TRB","AST","STL","BLK","TOV","PF","PTS"],
                value="AST", id="scatter-var-2"),

            ]
        ),
    ],
    body=True, color= "lightgrey", 
) 

controls_3=dbc.Card([      
        html.Div(
            [
                dbc.Label(children="Choose Two Players:"),
                dcc.Dropdown(
                    options=['A.J. Green', 'A.J. Lawson', 'AJ Griffin', 'Aaron Gordon', 'Aaron Holiday', 'Aaron Nesmith', 'Aaron Wiggins', 'Admiral Schofield', 'Al Horford', 'Alec Burks', 'Aleksej Pokusevski', 'Alex Caruso', 'Alex Len', 'Alize Johnson', 'Alondes Williams', 'Alperen Sengun', 'Amir Coffey', 'Andre Drummond', 'Andre Iguodala', 'Andrew Nembhard', 'Andrew Wiggins', 'Anfernee Simons', 'Anthony Davis', 'Anthony Edwards', 'Anthony Gill', 'Anthony Lamb', 'Austin Reaves', 'Austin Rivers', 'Ayo Dosunmu', 'Bam Adebayo', 'Ben Simmons', 'Bennedict Mathurin', 'Bismack Biyombo', 'Blake Griffin', 'Blake Wesley', 'Boban Marjanovic', 'Bobby Portis', 'Bogdan Bogdanovic', 'Bojan Bogdanovic', 'Bol Bol', 'Bones Hyland', 'Bradley Beal', 'Brandon Boston Jr.', 'Brandon Clarke', 'Brandon Ingram', 'Braxton Key', 'Brook Lopez', 'Bruce Brown', 'Bruno Fernando', 'Bryce McGowens', 'Bryn Forbes', 'Buddy Boeheim', 'Buddy Hield', 'CJ McCollum', 'Cade Cunningham', 'Caleb Houstan', 'Caleb Martin', 'Cam Reddish', 'Cam Thomas', 'Cameron Johnson', 'Cameron Payne', 'Caris LeVert', 'Carlik Jones', 'Cedi Osman', 'Chance Comanche', 'Charles Bassey', 'Chima Moneke', 'Chimezie Metu', 'Chris Boucher', 'Chris Duarte', 'Chris Paul', 'Chris Silva', 'Christian Braun', 'Christian Koloko', 'Christian Wood', 'Chuma Okeke', 'Clint Capela', 'Coby White', 'Cody Martin', 'Cody Zeller', 'Cole Anthony', 'Cole Swider', 'Collin Sexton', 'Corey Kispert', 'Cory Joseph', "D'Angelo Russell", 'Daishen Nix', 'Dalano Banton', 'Dalen Terry', 'Damian Jones', 'Damian Lillard', 'Damion Lee', 'Daniel Gafford', 'Daniel Theis', 'Danny Green', 'Danuel House Jr.', 'Dario Saric', 'Darius Bazley', 'Darius Days', 'Darius Garland', 'David Duke Jr.', 'David Roddy', 'Davion Mitchell', 'Davis Bertans', 'Davon Reed', "Day'Ron Sharpe", "De'Aaron Fox", "De'Andre Hunter", "De'Anthony Melton", 'DeAndre Jordan', 'DeMar DeRozan', 'Dean Wade', 'Deandre Ayton', 'Dejounte Murray', 'Delon Wright', 'Deni Avdija', 'Dennis Schroder', 'Dennis Smith Jr.', 'Deonte Burton', 'Dereon Seabron', 'Derrick Jones Jr.', 'Derrick Rose', 'Derrick White', 'Desmond Bane', 'Devin Booker', 'Devin Vassell', 'Devon Dotson', "Devonte' Graham", 'Dewayne Dedmon', 'Dillon Brooks', 'Domantas Sabonis', 'Dominick Barlow', 'Donovan Mitchell', 'Donovan Williams', 'Donte DiVincenzo', 'Dorian Finney-Smith', 'Doug McDermott', 'Draymond Green', 'Drew Eubanks', 'Dru Smith', 'Duane Washington Jr.', 'Duncan Robinson', 'Dwight Powell', 'Dylan Windler', 'Dyson Daniels', 'Edmond Sumner', 'Eric Gordon', 'Eugene Omoruyi', 'Evan Fournier', 'Evan Mobley', 'Facundo Campazzo', 'Frank Jackson', 'Frank Kaminsky', 'Frank Ntilikina', 'Franz Wagner', 'Fred VanVleet', 'Furkan Korkmaz', 'Gabe Vincent', 'Gabe York', 'Garrett Temple', 'Garrison Mathews', 'Gary Harris', 'Gary Payton II', 'Gary Trent Jr.', 'George Hill', 'Georges Niang', 'Giannis Antetokounmpo', 'Goga Bitadze', 'Goran Dragic', 'Gordon Hayward', 'Gorgui Dieng', 'Grant Williams', 'Grayson Allen', 'Greg Brown III', 'Hamidou Diallo', 'Harrison Barnes', 'Haywood Highsmith', 'Herbert Jones', 'Immanuel Quickley', 'Isaac Okoro', 'Isaiah Hartenstein', 'Isaiah Jackson', 'Isaiah Joe', 'Isaiah Livers', 'Isaiah Mobley', 'Isaiah Roby', 'Isaiah Stewart', 'Isaiah Todd', 'Ish Smith', 'Ish Wainright', 'Ivica Zubac', 'JD Davison', 'JT Thor', 'Ja Morant', 'JaMychal Green', 'JaVale McGee', 'Jabari Smith Jr.', 'Jabari Walker', 'Jack White', 'Jacob Gilyard', 'Jaden Hardy', 'Jaden Ivey', 'Jaden McDaniels', 'Jaden Springer', 'Jae Crowder', "Jae'Sean Tate", 'Jake LaRavia', 'Jakob Poeltl', 'Jalen Brunson', 'Jalen Duren', 'Jalen Green', 'Jalen Johnson', 'Jalen McDaniels', 'Jalen Smith', 'Jalen Suggs', 'Jalen Williams', 'Jamal Cain', 'Jamal Murray', 'Jamaree Bouyea', 'James Bouknight', 'James Harden', 'James Johnson', 'James Wiseman', 'Jared Butler', 'Jared Rhoden', 'Jaren Jackson Jr.', 'Jarred Vanderbilt', 'Jarrell Brantley', 'Jarrett Allen', 'Jarrett Culver', 'Jason Preston', 'Javonte Green', 'Jaxson Hayes', 'Jay Huff', 'Jay Scrubb', 'Jaylen Brown', 'Jaylen Nowell', 'Jaylin Williams', 'Jayson Tatum', 'Jeenathan Williams', 'Jeff Dowtin Jr.', 'Jeff Green', 'Jerami Grant', 'Jeremiah Robinson-Earl', 'Jeremy Sochan', 'Jericho Sims', 'Jevon Carter', 'Jimmy Butler', 'Jock Landale', 'Joe Harris', 'Joe Ingles', 'Joe Wieskamp', 'Joel Embiid', 'John Butler Jr.', 'John Collins', 'John Konchar', 'John Wall', 'Johnny Davis', 'Johnny Juzang', 'Jonas Valanciunas', 'Jonathan Isaac', 'Jonathan Kuminga', 'Jordan Clarkson', 'Jordan Goodwin', 'Jordan Hall', 'Jordan McLaughlin', 'Jordan Nwora', 'Jordan Poole', 'Jordan Schakel', 'Jose Alvarado', 'Josh Christopher', 'Josh Giddey', 'Josh Green', 'Josh Hart', 'Josh Minott', 'Josh Okogie', 'Josh Richardson', 'Joshua Primo', 'Jrue Holiday', 'Juan Toscano-Anderson', 'Juancho Hernangomez', 'Julian Champagnie', 'Julius Randle', 'Justin Champagnie', 'Justin Holiday', 'Justin Jackson', 'Justin Minaya', 'Justise Winslow', 'Jusuf Nurkic', 'KZ Okpala', 'Kai Jones', 'Karl-Anthony Towns', 'Kawhi Leonard', 'Keegan Murray', 'Keita Bates-Diop', 'Keldon Johnson', 'Kelly Olynyk', 'Kelly Oubre Jr.', 'Kemba Walker', 'Kendall Brown', 'Kendrick Nunn', 'Kennedy Chandler', 'Kenneth Lofton Jr.', 'Kenrich Williams', 'Kentavious Caldwell-Pope', 'Kenyon Martin Jr.', 'Keon Ellis', 'Keon Johnson', 'Kessler Edwards', 'Kevin Durant', 'Kevin Huerter', 'Kevin Knox II', 'Kevin Love', 'Kevin Porter Jr.', 'Kevon Harris', 'Kevon Looney', 'Khem Birch', 'Khris Middleton', 'Killian Hayes', 'Kira Lewis Jr.', 'Klay Thompson', 'Kobi Simmons', 'Kris Dunn', 'Kristaps Porzingis', 'Kyle Anderson', 'Kyle Kuzma', 'Kyle Lowry', 'Kyrie Irving', 'LaMelo Ball', 'Lamar Stevens', 'Landry Shamet', 'Larry Nance Jr.', 'Lauri Markkanen', 'LeBron James', 'Leandro Bolmaro', 'Lester Quinones', 'Lindell Wigginton', 'Lindy Waters III', 'Lonnie Walker IV', 'Louis King', 'Luguentz Dort', 'Luka Doncic', 'Luka Garza', 'Luka Samanic', 'Luke Kennard', 'Luke Kornet', 'Mac McClung', 'Malachi Flynn', 'Malaki Branham', 'Malcolm Brogdon', 'Malcolm Hill', 'Malik Beasley', 'Malik Monk', 'Mamadi Diakite', 'MarJon Beauchamp', 'Marcus Morris Sr.', 'Marcus Smart', 'Mark Williams', 'Markelle Fultz', 'Markieff Morris', 'Marko Simonovic', 'Marvin Bagley III', 'Mason Plumlee', 'Matisse Thybulle', 'Matt Ryan', 'Matthew Dellavedova', 'Max Christie', 'Max Strus', 'Maxi Kleber', 'McKinley Wright IV', 'Meyers Leonard', 'Mfiondu Kabengele', 'Micah Potter', 'Michael Carter-Williams', 'Michael Foster Jr.', 'Michael Porter Jr.', 'Mikal Bridges', 'Mike Conley', 'Mike Muscala', 'Miles McBride', 'Mitchell Robinson', 'Mo Bamba', 'Monte Morris', 'Montrezl Harrell', 'Moritz Wagner', 'Moses Brown', 'Moses Moody', 'Moussa Diabate', 'Myles Turner', 'Naji Marshall', 'Nassir Little', 'Nathan Knight', 'Naz Reid', 'Neemias Queta', 'Nerlens Noel', 'Nic Claxton', 'Nick Richards', 'Nickeil Alexander-Walker', 'Nicolas Batum', 'Nikola Jokic', 'Nikola Jovic', 'Nikola Vucevic', 'Noah Vonleh', 'Norman Powell', 'O.G. Anunoby', 'Obi Toppin', 'Ochai Agbaji', 'Olivier Sarr', 'Omer Yurtseven', 'Onyeka Okongwu', 'Orlando Robinson', 'Oshae Brissett', 'Otto Porter Jr.', 'Ousmane Dieng', 'P.J. Tucker', 'P.J. Washington', 'PJ Dozier', 'Paolo Banchero', 'Pascal Siakam', 'Pat Connaughton', 'Patrick Baldwin Jr.', 'Patrick Beverley', 'Patrick Williams', 'Patty Mills', 'Paul George', 'Paul Reed', 'Payton Pritchard', 'Peyton Watson', 'Precious Achiuwa', 'Quentin Grimes', 'Quenton Jackson', 'R.J. Hampton', 'RJ Barrett', 'RaiQuan Gray', 'Raul Neto', 'Reggie Bullock', 'Reggie Jackson', 'Richaun Holmes', 'Ricky Rubio', 'Robert Covington', 'Robert Williams III', 'Robin Lopez', 'Rodney McGruder', 'Romeo Langford', 'Ron Harper Jr.', "Royce O'Neale", 'Rudy Gay', 'Rudy Gobert', 'Rui Hachimura', 'Russell Westbrook', 'Ryan Arcidiacono', 'Ryan Rollins', 'Saben Lee', 'Saddiq Bey', 'Sam Hauser', 'Sam Merrill', 'Sandro Mamukelashvili', 'Santi Aldama', 'Scottie Barnes', 'Scotty Pippen Jr.', 'Serge Ibaka', 'Seth Curry', 'Shaedon Sharpe', 'Shai Gilgeous-Alexander', 'Shake Milton', 'Shaquille Harrison', 'Simone Fontecchio', 'Skylar Mays', 'Spencer Dinwiddie', 'Stanley Johnson', 'Stanley Umude', 'Stephen Curry', 'Sterling Brown', 'Steven Adams', 'Svi Mykhailiuk', 'T.J. McConnell', 'T.J. Warren', 'Taj Gibson', 'Talen Horton-Tucker', 'Tari Eason', 'Taurean Prince', 'Terance Mann', 'Terence Davis', 'Terrence Ross', 'Terry Rozier', 'Terry Taylor', 'Thaddeus Young', 'Thanasis Antetokounmpo', 'Theo Maledon', 'Theo Pinson', 'Thomas Bryant', 'Tim Hardaway Jr.', 'Tobias Harris', 'Tony Bradley', 'Torrey Craig', 'Trae Young', 'Tre Jones', 'Tre Mann', 'Trendon Watford', 'Trent Forrest', 'Trevelin Queen', 'Trevor Hudgins', 'Trevor Keels', 'Trey Lyles', 'Trey Murphy III', 'Troy Brown Jr.', 'Ty Jerome', 'TyTy Washington Jr.', 'Tyler Dorsey', 'Tyler Herro', 'Tyrese Haliburton', 'Tyrese Martin', 'Tyrese Maxey', 'Tyus Jones', 'Udoka Azubuike', 'Udonis Haslem', 'Usman Garuba', 'Vernon Carey Jr.', 'Victor Oladipo', 'Vince Williams Jr.', 'Vit Krejci', 'Vlatko Cancar', 'Walker Kessler', 'Wendell Carter Jr.', 'Wendell Moore Jr.', 'Wenyen Gabriel', 'Wesley Matthews', 'Will Barton', 'Willy Hernangomez', 'Xavier Cooks', 'Xavier Moon', 'Xavier Sneed', 'Xavier Tillman', 'Yuta Watanabe', 'Zach Collins', 'Zach LaVine', 'Zeke Nnaji', 'Ziaire Williams', 'Zion Williamson'],
                    value ="Joel Embiid", id="player-1"
                    ),
                dcc.Dropdown(
                    options=['A.J. Green', 'A.J. Lawson', 'AJ Griffin', 'Aaron Gordon', 'Aaron Holiday', 'Aaron Nesmith', 'Aaron Wiggins', 'Admiral Schofield', 'Al Horford', 'Alec Burks', 'Aleksej Pokusevski', 'Alex Caruso', 'Alex Len', 'Alize Johnson', 'Alondes Williams', 'Alperen Sengun', 'Amir Coffey', 'Andre Drummond', 'Andre Iguodala', 'Andrew Nembhard', 'Andrew Wiggins', 'Anfernee Simons', 'Anthony Davis', 'Anthony Edwards', 'Anthony Gill', 'Anthony Lamb', 'Austin Reaves', 'Austin Rivers', 'Ayo Dosunmu', 'Bam Adebayo', 'Ben Simmons', 'Bennedict Mathurin', 'Bismack Biyombo', 'Blake Griffin', 'Blake Wesley', 'Boban Marjanovic', 'Bobby Portis', 'Bogdan Bogdanovic', 'Bojan Bogdanovic', 'Bol Bol', 'Bones Hyland', 'Bradley Beal', 'Brandon Boston Jr.', 'Brandon Clarke', 'Brandon Ingram', 'Braxton Key', 'Brook Lopez', 'Bruce Brown', 'Bruno Fernando', 'Bryce McGowens', 'Bryn Forbes', 'Buddy Boeheim', 'Buddy Hield', 'CJ McCollum', 'Cade Cunningham', 'Caleb Houstan', 'Caleb Martin', 'Cam Reddish', 'Cam Thomas', 'Cameron Johnson', 'Cameron Payne', 'Caris LeVert', 'Carlik Jones', 'Cedi Osman', 'Chance Comanche', 'Charles Bassey', 'Chima Moneke', 'Chimezie Metu', 'Chris Boucher', 'Chris Duarte', 'Chris Paul', 'Chris Silva', 'Christian Braun', 'Christian Koloko', 'Christian Wood', 'Chuma Okeke', 'Clint Capela', 'Coby White', 'Cody Martin', 'Cody Zeller', 'Cole Anthony', 'Cole Swider', 'Collin Sexton', 'Corey Kispert', 'Cory Joseph', "D'Angelo Russell", 'Daishen Nix', 'Dalano Banton', 'Dalen Terry', 'Damian Jones', 'Damian Lillard', 'Damion Lee', 'Daniel Gafford', 'Daniel Theis', 'Danny Green', 'Danuel House Jr.', 'Dario Saric', 'Darius Bazley', 'Darius Days', 'Darius Garland', 'David Duke Jr.', 'David Roddy', 'Davion Mitchell', 'Davis Bertans', 'Davon Reed', "Day'Ron Sharpe", "De'Aaron Fox", "De'Andre Hunter", "De'Anthony Melton", 'DeAndre Jordan', 'DeMar DeRozan', 'Dean Wade', 'Deandre Ayton', 'Dejounte Murray', 'Delon Wright', 'Deni Avdija', 'Dennis Schroder', 'Dennis Smith Jr.', 'Deonte Burton', 'Dereon Seabron', 'Derrick Jones Jr.', 'Derrick Rose', 'Derrick White', 'Desmond Bane', 'Devin Booker', 'Devin Vassell', 'Devon Dotson', "Devonte' Graham", 'Dewayne Dedmon', 'Dillon Brooks', 'Domantas Sabonis', 'Dominick Barlow', 'Donovan Mitchell', 'Donovan Williams', 'Donte DiVincenzo', 'Dorian Finney-Smith', 'Doug McDermott', 'Draymond Green', 'Drew Eubanks', 'Dru Smith', 'Duane Washington Jr.', 'Duncan Robinson', 'Dwight Powell', 'Dylan Windler', 'Dyson Daniels', 'Edmond Sumner', 'Eric Gordon', 'Eugene Omoruyi', 'Evan Fournier', 'Evan Mobley', 'Facundo Campazzo', 'Frank Jackson', 'Frank Kaminsky', 'Frank Ntilikina', 'Franz Wagner', 'Fred VanVleet', 'Furkan Korkmaz', 'Gabe Vincent', 'Gabe York', 'Garrett Temple', 'Garrison Mathews', 'Gary Harris', 'Gary Payton II', 'Gary Trent Jr.', 'George Hill', 'Georges Niang', 'Giannis Antetokounmpo', 'Goga Bitadze', 'Goran Dragic', 'Gordon Hayward', 'Gorgui Dieng', 'Grant Williams', 'Grayson Allen', 'Greg Brown III', 'Hamidou Diallo', 'Harrison Barnes', 'Haywood Highsmith', 'Herbert Jones', 'Immanuel Quickley', 'Isaac Okoro', 'Isaiah Hartenstein', 'Isaiah Jackson', 'Isaiah Joe', 'Isaiah Livers', 'Isaiah Mobley', 'Isaiah Roby', 'Isaiah Stewart', 'Isaiah Todd', 'Ish Smith', 'Ish Wainright', 'Ivica Zubac', 'JD Davison', 'JT Thor', 'Ja Morant', 'JaMychal Green', 'JaVale McGee', 'Jabari Smith Jr.', 'Jabari Walker', 'Jack White', 'Jacob Gilyard', 'Jaden Hardy', 'Jaden Ivey', 'Jaden McDaniels', 'Jaden Springer', 'Jae Crowder', "Jae'Sean Tate", 'Jake LaRavia', 'Jakob Poeltl', 'Jalen Brunson', 'Jalen Duren', 'Jalen Green', 'Jalen Johnson', 'Jalen McDaniels', 'Jalen Smith', 'Jalen Suggs', 'Jalen Williams', 'Jamal Cain', 'Jamal Murray', 'Jamaree Bouyea', 'James Bouknight', 'James Harden', 'James Johnson', 'James Wiseman', 'Jared Butler', 'Jared Rhoden', 'Jaren Jackson Jr.', 'Jarred Vanderbilt', 'Jarrell Brantley', 'Jarrett Allen', 'Jarrett Culver', 'Jason Preston', 'Javonte Green', 'Jaxson Hayes', 'Jay Huff', 'Jay Scrubb', 'Jaylen Brown', 'Jaylen Nowell', 'Jaylin Williams', 'Jayson Tatum', 'Jeenathan Williams', 'Jeff Dowtin Jr.', 'Jeff Green', 'Jerami Grant', 'Jeremiah Robinson-Earl', 'Jeremy Sochan', 'Jericho Sims', 'Jevon Carter', 'Jimmy Butler', 'Jock Landale', 'Joe Harris', 'Joe Ingles', 'Joe Wieskamp', 'Joel Embiid', 'John Butler Jr.', 'John Collins', 'John Konchar', 'John Wall', 'Johnny Davis', 'Johnny Juzang', 'Jonas Valanciunas', 'Jonathan Isaac', 'Jonathan Kuminga', 'Jordan Clarkson', 'Jordan Goodwin', 'Jordan Hall', 'Jordan McLaughlin', 'Jordan Nwora', 'Jordan Poole', 'Jordan Schakel', 'Jose Alvarado', 'Josh Christopher', 'Josh Giddey', 'Josh Green', 'Josh Hart', 'Josh Minott', 'Josh Okogie', 'Josh Richardson', 'Joshua Primo', 'Jrue Holiday', 'Juan Toscano-Anderson', 'Juancho Hernangomez', 'Julian Champagnie', 'Julius Randle', 'Justin Champagnie', 'Justin Holiday', 'Justin Jackson', 'Justin Minaya', 'Justise Winslow', 'Jusuf Nurkic', 'KZ Okpala', 'Kai Jones', 'Karl-Anthony Towns', 'Kawhi Leonard', 'Keegan Murray', 'Keita Bates-Diop', 'Keldon Johnson', 'Kelly Olynyk', 'Kelly Oubre Jr.', 'Kemba Walker', 'Kendall Brown', 'Kendrick Nunn', 'Kennedy Chandler', 'Kenneth Lofton Jr.', 'Kenrich Williams', 'Kentavious Caldwell-Pope', 'Kenyon Martin Jr.', 'Keon Ellis', 'Keon Johnson', 'Kessler Edwards', 'Kevin Durant', 'Kevin Huerter', 'Kevin Knox II', 'Kevin Love', 'Kevin Porter Jr.', 'Kevon Harris', 'Kevon Looney', 'Khem Birch', 'Khris Middleton', 'Killian Hayes', 'Kira Lewis Jr.', 'Klay Thompson', 'Kobi Simmons', 'Kris Dunn', 'Kristaps Porzingis', 'Kyle Anderson', 'Kyle Kuzma', 'Kyle Lowry', 'Kyrie Irving', 'LaMelo Ball', 'Lamar Stevens', 'Landry Shamet', 'Larry Nance Jr.', 'Lauri Markkanen', 'LeBron James', 'Leandro Bolmaro', 'Lester Quinones', 'Lindell Wigginton', 'Lindy Waters III', 'Lonnie Walker IV', 'Louis King', 'Luguentz Dort', 'Luka Doncic', 'Luka Garza', 'Luka Samanic', 'Luke Kennard', 'Luke Kornet', 'Mac McClung', 'Malachi Flynn', 'Malaki Branham', 'Malcolm Brogdon', 'Malcolm Hill', 'Malik Beasley', 'Malik Monk', 'Mamadi Diakite', 'MarJon Beauchamp', 'Marcus Morris Sr.', 'Marcus Smart', 'Mark Williams', 'Markelle Fultz', 'Markieff Morris', 'Marko Simonovic', 'Marvin Bagley III', 'Mason Plumlee', 'Matisse Thybulle', 'Matt Ryan', 'Matthew Dellavedova', 'Max Christie', 'Max Strus', 'Maxi Kleber', 'McKinley Wright IV', 'Meyers Leonard', 'Mfiondu Kabengele', 'Micah Potter', 'Michael Carter-Williams', 'Michael Foster Jr.', 'Michael Porter Jr.', 'Mikal Bridges', 'Mike Conley', 'Mike Muscala', 'Miles McBride', 'Mitchell Robinson', 'Mo Bamba', 'Monte Morris', 'Montrezl Harrell', 'Moritz Wagner', 'Moses Brown', 'Moses Moody', 'Moussa Diabate', 'Myles Turner', 'Naji Marshall', 'Nassir Little', 'Nathan Knight', 'Naz Reid', 'Neemias Queta', 'Nerlens Noel', 'Nic Claxton', 'Nick Richards', 'Nickeil Alexander-Walker', 'Nicolas Batum', 'Nikola Jokic', 'Nikola Jovic', 'Nikola Vucevic', 'Noah Vonleh', 'Norman Powell', 'O.G. Anunoby', 'Obi Toppin', 'Ochai Agbaji', 'Olivier Sarr', 'Omer Yurtseven', 'Onyeka Okongwu', 'Orlando Robinson', 'Oshae Brissett', 'Otto Porter Jr.', 'Ousmane Dieng', 'P.J. Tucker', 'P.J. Washington', 'PJ Dozier', 'Paolo Banchero', 'Pascal Siakam', 'Pat Connaughton', 'Patrick Baldwin Jr.', 'Patrick Beverley', 'Patrick Williams', 'Patty Mills', 'Paul George', 'Paul Reed', 'Payton Pritchard', 'Peyton Watson', 'Precious Achiuwa', 'Quentin Grimes', 'Quenton Jackson', 'R.J. Hampton', 'RJ Barrett', 'RaiQuan Gray', 'Raul Neto', 'Reggie Bullock', 'Reggie Jackson', 'Richaun Holmes', 'Ricky Rubio', 'Robert Covington', 'Robert Williams III', 'Robin Lopez', 'Rodney McGruder', 'Romeo Langford', 'Ron Harper Jr.', "Royce O'Neale", 'Rudy Gay', 'Rudy Gobert', 'Rui Hachimura', 'Russell Westbrook', 'Ryan Arcidiacono', 'Ryan Rollins', 'Saben Lee', 'Saddiq Bey', 'Sam Hauser', 'Sam Merrill', 'Sandro Mamukelashvili', 'Santi Aldama', 'Scottie Barnes', 'Scotty Pippen Jr.', 'Serge Ibaka', 'Seth Curry', 'Shaedon Sharpe', 'Shai Gilgeous-Alexander', 'Shake Milton', 'Shaquille Harrison', 'Simone Fontecchio', 'Skylar Mays', 'Spencer Dinwiddie', 'Stanley Johnson', 'Stanley Umude', 'Stephen Curry', 'Sterling Brown', 'Steven Adams', 'Svi Mykhailiuk', 'T.J. McConnell', 'T.J. Warren', 'Taj Gibson', 'Talen Horton-Tucker', 'Tari Eason', 'Taurean Prince', 'Terance Mann', 'Terence Davis', 'Terrence Ross', 'Terry Rozier', 'Terry Taylor', 'Thaddeus Young', 'Thanasis Antetokounmpo', 'Theo Maledon', 'Theo Pinson', 'Thomas Bryant', 'Tim Hardaway Jr.', 'Tobias Harris', 'Tony Bradley', 'Torrey Craig', 'Trae Young', 'Tre Jones', 'Tre Mann', 'Trendon Watford', 'Trent Forrest', 'Trevelin Queen', 'Trevor Hudgins', 'Trevor Keels', 'Trey Lyles', 'Trey Murphy III', 'Troy Brown Jr.', 'Ty Jerome', 'TyTy Washington Jr.', 'Tyler Dorsey', 'Tyler Herro', 'Tyrese Haliburton', 'Tyrese Martin', 'Tyrese Maxey', 'Tyus Jones', 'Udoka Azubuike', 'Udonis Haslem', 'Usman Garuba', 'Vernon Carey Jr.', 'Victor Oladipo', 'Vince Williams Jr.', 'Vit Krejci', 'Vlatko Cancar', 'Walker Kessler', 'Wendell Carter Jr.', 'Wendell Moore Jr.', 'Wenyen Gabriel', 'Wesley Matthews', 'Will Barton', 'Willy Hernangomez', 'Xavier Cooks', 'Xavier Moon', 'Xavier Sneed', 'Xavier Tillman', 'Yuta Watanabe', 'Zach Collins', 'Zach LaVine', 'Zeke Nnaji', 'Ziaire Williams', 'Zion Williamson'],
                    value ="Luka Doncic", id="player-2"
                    ),
            ]
        ),
        html.Div(
            [
                dbc.Label(children="Choose a Statistical Category:"),
                dcc.Dropdown(
                    options = ["AGE","GP","MPG","USG%","TO%","FTA","FT%","2PA","2P%","3PA","3P%","eFG%","TS%","PPG","RPG","APG","SPG","BPG","TPG","P+R","P+A","P+R+A","VI","ORtg","DRtg"],
                value="PPG", id="player-var"
                ),
            ]
        ),
    ],
    body=True, color= "lightgrey", 
) 

controls_4=dbc.Card([      
        html.Div(
            [
                dbc.Label(children="Choose Two Statistical Categories:"),
                dcc.Dropdown(options = 
                    ["AGE","GP","MPG","USG%","TO%","FTA","FT%","2PA","2P%","3PA","3P%","eFG%","TS%","PPG","RPG","APG","SPG","BPG","TPG","P+R","P+A","P+R+A","VI","ORtg","DRtg"],
                    value="PPG", id="player-scatter-var-1"
                    ),
                dcc.Dropdown(options = ["AGE","GP","MPG","USG%","TO%","FTA","FT%","2PA","2P%","3PA","3P%","eFG%","TS%","PPG","RPG","APG","SPG","BPG","TPG","P+R","P+A","P+R+A","VI","ORtg","DRtg"],
                value="RPG", id="player-scatter-var-2"),
            ]
        ),
    ],
    body=True, color= "lightgrey", 
) 

title_card= dbc.Card(
    dbc.CardBody(
        [
        html.H1(children='NBA Team and Player Statistics Comparison'),
        ], 
    ),
)



#app layout
app.layout = dbc.Container([
    dbc.Row([
        title_card
    ],className="card-title"
    ),
    #team stats
    dcc.Tabs([
        dcc.Tab(label="Team Statistics", children=[
            dbc.Row([
                html.H3(children="Team Comparison"),
            ]),
            dbc.Row([
                html.Div(children= "This barplot allows for direct statistical comparison of two NBA teams."),             
            ]),
            dbc.Row([
                dbc.Col(controls_1, width=3),
                dbc.Col(dcc.Graph(figure={}, id="bar-graph"), width=9),
            ],
            align= "center",
            ),
            dbc.Row([
                html.H3(children="Assess Relationships Between Statistical Categories for Each Team"),
                
            ]),
            dbc.Row([
                html.Div(children="The scatterplot allows for statistical comparison of all NBA teams by default; and optional customization to compare as many NBA teams as desired. To remove any teams, single-click on the team in the legend. To isolate a specific team, double-click on the team and then single click on additional teams you would like to include. Double-click to reset to default."),
            ]),
            dbc.Row([
                dbc.Col(controls_2, width=3),
                dbc.Col(dcc.Graph(figure={}, id="scatter-graph"), width=9),
            ],
            align="center",
            ),
        ]),

        #player stats
        dcc.Tab(label="Player Statistics", children=[
            dbc.Row([
                html.H3(children="Player Comparison"),
            ]),
            dbc.Row([
                html.Div(children= "This barplot allows for direct statistical comparison of two NBA players."),             
            ]),
            dbc.Row([
                dbc.Col(controls_3, width=3),
                dbc.Col(dcc.Graph(figure={}, id="player-bar-graph"),width=9),
            ],
            align="center",
            ),
            dbc.Row([
                html.H3(children="Assess Relationships Between Two Statistical Categories Among All Players"),
                
            ]),
            dbc.Row([
                html.Div(children="The scatterplot allows for statistical comparison of all NBA players by default; and optional customization to compare as many NBA players as desired. To remove any players, single-click on the player in the legend. To isolate a specific player, double-click on the player and then single click on additional players you would like to include. Double-click to reset to default."),
            ]),
            dbc.Row([
                dbc.Col(controls_4, width=3),
                dbc.Col(dcc.Graph(figure={}, id="player-scatter-graph"), width=9),
            ],
            align="center",
            ),
        ])
    ]),
],fluid=True)




#callbacks
@callback(
    Output("bar-graph", "figure"),
    Input("team-1", "value"),
    Input("team-2", "value"),
    Input("team-var", "value"),
    Input("season-chosen", "value"),
)

def update_team_bar(team_1, team_2, team_var, year):
    #make dataset dynamic depending on teams chosen
    team_bar_data = team_data.loc[team_data["Team"].isin([team_1,team_2])]
    #filter for year depending on year chosen 
    team_bar_data = team_bar_data[team_bar_data["Year"]== year]

    #barplot
    fig = px.bar(team_bar_data, 
                x=team_var,
                y="Team",
                color="Team", 
                title=f"Barplot Comparing {team_var} Between {team_1} and {team_2} in {year}", 
                template="ggplot2",)
    fig.update_layout(xaxis_title=f"{team_var}")
    return fig


@callback(
    Output("scatter-graph", "figure"),
    Input("scatter-season", "value"),
    Input("scatter-var-1", "value"),
    Input("scatter-var-2", "value")
)

def update_scatter(year, var_1, var_2):
    #create dataframe with year filtered
    scatter_data = team_data.loc[team_data["Year"]== year]

    fig = px.scatter(scatter_data,
                    x=var_1,
                    y=var_2,
                    size=var_2,
                    color="Team",
                    template="seaborn",
                    trendline="ols",
                    trendline_scope="overall",
                    trendline_color_override="black",
                    title= f"Scatterplot Comparing {var_1} with {var_2} in {year}",
                    height=600)
    fig.update_layout(xaxis_title=f"{var_1}", yaxis_title=f"{var_2}")
    return fig

#graphs for player data
#barplot
@callback(
    Output("player-bar-graph", "figure"),
    Input("player-1", "value"),
    Input("player-2", "value"),
    Input("player-var", "value")
)

def update_player_bar(player_1, player_2, var):
    new_player_data = player_data.loc[player_data["NAME"].isin([player_1, player_2])]

    fig = px.bar(new_player_data,
                x=var,
                y= "NAME",
                color="NAME",
                title=f"Barplot Comparing {var} Between {player_1} and {player_2} in 2022-2023", 
                template="ggplot2",)
    fig.update_layout(xaxis_title=f"{var}")
    return fig

@callback(
    Output("player-scatter-graph", "figure"),
    Input("player-scatter-var-1", "value"),
    Input("player-scatter-var-2", "value")
)

def update_scatter(scatter_var_1, scatter_var_2):

    fig = px.scatter(player_data,
                    x=scatter_var_1,
                    y=scatter_var_2,
                    size=scatter_var_2,
                    color="NAME",
                    template="seaborn",                    
                    trendline="ols",
                    trendline_scope="overall",
                    trendline_color_override="black",
                    title= f"Scatterplot Comparing {scatter_var_1} with {scatter_var_2}",
                    height=600)
    fig.update_layout(xaxis_title=f"{scatter_var_1}", yaxis_title=f"{scatter_var_2}")
    return fig


#run app
if __name__ == '__main__':
    app.run(debug=True)
