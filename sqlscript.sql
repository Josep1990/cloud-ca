create database users;

use users;

create table users (
 id int auto_increment primary key,
 username VARCHAR(128) NOT NULL,
 password VARCHAR(1024) NOT NULL
);

INSERT INTO `my_music`.`users` (`username`, `password`) VALUES ('test', 'bee63437ab1260e6a9cd66ce67afd8fc85fc826e');

CREATE TABLE playlists (
  id INT AUTO_INCREMENT PRIMARY KEY,
  playlist_name VARCHAR(255) NOT NULL UNIQUE,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE songs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  song_name VARCHAR(255) NOT NULL
);

CREATE TABLE playlist_songs (
  playlist_id INT,
  song_id INT,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (playlist_id) REFERENCES playlists(id),
  FOREIGN KEY (song_id) REFERENCES songs(id),
  PRIMARY KEY (user_id, playlist_id, song_id)
);

INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_a');
INSERT INTO `my_music`.`songs` (`song_name`)  VALUES ('song_b');
INSERT INTO `my_music`.`songs` (`song_name`)  VALUES ('song_c');
INSERT INTO `my_music`.`songs` (`song_name`)  VALUES ('song_d');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_e');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_f');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_g');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_h');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_j');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_k');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_l');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_m');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_n');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_o');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_p');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_q');
INSERT INTO `my_music`.`songs` (`song_name`) VALUES ('song_r');
INSERT INTO `my_music`.`songs` (`song_name`)  VALUES ('song_s');
INSERT INTO `my_music`.`songs` (`song_name`)  VALUES ('song_t');
INSERT INTO `my_music`.`songs` (`song_name`)  VALUES ('song_u');
