CREATE TABLE IF NOT EXISTS genres(
    id SERIAL PRIMARY KEY,
    title VARCHAR(70)
);
CREATE TABLE IF NOT EXISTS platforms(
    id SERIAL PRIMARY KEY,
    title VARCHAR(70)
);
CREATE TABLE IF NOT EXISTS publishers(
    id SERIAL PRIMARY KEY,
    title VARCHAR(70)
);
CREATE TABLE IF NOT EXISTS languages(
    id SERIAL PRIMARY KEY,
    title VARCHAR(70)
);
CREATE TABLE IF NOT EXISTS games(
    id SERIAL PRIMARY KEY,
    title VARCHAR(50),
    description TEXT,
    cost NUMERIC,
    image_path VARCHAR(50),
    release_date DATE,
    publisher_id INTEGER REFERENCES publishers(id),
    language_id INTEGER REFERENCES languages(id)
);
CREATE TABLE IF NOT EXISTS game_genre(
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    genre_id INTEGER REFERENCES genres(id)
);
CREATE TABLE IF NOT EXISTS game_platform(
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    platform_id INTEGER REFERENCES platforms(id)
);
INSERT INTO genres(title)
VALUES ('Экшен'),
       ('Стратегии'),
       ('Ролевые'),
       ('Атмосфера'),
       ('Хорор'),
       ('Шутеры'),
       ('Симуляторы'),
       ('Приключения'),
       ('Фентези');
INSERT INTO platforms(title)
VALUES ('Windows'),
       ('Linux'),
       ('MacOS'),
       ('Android');
INSERT INTO publishers(title)
VALUES ('Io-Interactive A/S'),
       ('Plug in Digital'),
       ('FromSoftware Inc.'),
       ('Paradox Interactive'),
       ('PlayStation PC LLC'),
       ('Warner Bros. Games'),
       ('Electronic Arts'),
       ('505 Games');
INSERT INTO languages(title)
VALUES ('Английский'),
       ('Русский'),
       ('Русский(Субтитры)');
INSERT INTO games(title, description, cost, image_path, release_date, publisher_id, language_id)
VALUES
        ('Hitman: Absolution',  'Легендарный бесшумный убийца Агент 47 возвращается в Hitman Absolution', 496.4, 'hitman-absolution.jpg', '2019-11-19', 1, 2),
        ('Marvel’s Spider-Man Remastered',  'Без паники, это всего лишь ваш дружелюбный сосед-паук!', 23323.5, 'marvels-spider-man-remastered.jpg', '2022-08-12', 2, 2),
        ('ELDEN RING Deluxe Edition',  'Приоткройте завесу нового мира!', 37222.7, 'elden-ring-deluxe-edition.jpg', '2022-02-24', 3, 2),
        ('Victoria 3 Grand Edition',  'XIX век трансформировал практически всё человечество!', 27659.7, 'victoria-3-grand-edition.jpg', '2019-11-19', 4, 2),
        ('UNCHARTED: Legacy of Thieves Collection',  'Играйте за Натана Дрейка и Хлою Фрейзер в их собственных приключениях', 22768.7, 'uncharted-legacy-of-thieves-collection.jpg', '2022-10-19', 5, 2),
        ('Gotham Knights',  'Бэтмен мёртв. Растущий с невероятной скоростью преступный мир захлестнул улицы Готэм-Сити.', 21162.7, 'gotham-knights.jpg', '2022-10-21', 6, 2),
        ('God of War',  'Месть Богам Олимпа давно позади.', 18242.7, 'god-of-war.jpg', '2022-01-14', 5, 2),
        ('DARK SOULS III',  'Судьба усыпанная страданиями – теперь ваша судьба!', 14592.7, 'dark-souls-3.jpg', '2016-04-11', 3, 2),
        ('Mass Effect Legendary Edition',  'Основной одиночный контент всех трех игр (Mass Effect, Mass Effect 2 и Mass Effect 3)', 14592.7, 'mass-effect-legendary-edition.jpg', '2021-05-21', 7, 2),
        ('DEATH STRANDING DIRECTORS CUT',  'Таинственное событие, известное как Death Stranding', 13862.7, 'death-stranding-directors-cut.jpg', '2022-03-30', 8, 2);
INSERT INTO game_genre(game_id, genre_id)
VALUES (1, 1),
       (2, 1),
       (2, 8),
       (3, 1),
       (3, 3),
       (4, 7),
       (4, 2),
       (5, 8),
       (6, 1),
       (6, 3),
       (6, 8),
       (7, 1),
       (7, 3),
       (7, 8),
       (8, 1),
       (9, 1),
       (9, 3),
       (10, 1),
       (10, 3);
INSERT INTO game_platform(game_id, platform_id)
VALUES (1, 1),
       (1, 3),
       (3, 1),
       (4, 1),
       (4, 3),
       (4, 4),
       (5, 1),
       (6, 1),
       (7, 1),
       (8, 1),
       (9, 1),
       (10, 1);
