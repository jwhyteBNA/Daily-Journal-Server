CREATE TABLE `Mood`
(
`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` NVARCHAR(50) NOT NULL
);

CREATE TABLE `Tag`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `subject` NVARCHAR(60) NOT NULL
);

CREATE TABLE `Entry`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` NVARCHAR(60) NOT NULL,
    `entry` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
    `date` DATETIME NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `EntryTag`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
    FOREIGN KEY(`entry_id`) REFERENCES `Entry`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`)
);

INSERT INTO `Mood` VALUES (null, "Happy");
INSERT INTO `Mood` VALUES (null, "Sad");
INSERT INTO `Mood` VALUES (null, "Angry");
INSERT INTO `Mood` VALUES (null, "Ok");

INSERT INTO `Tag` VALUES (null, "API");
INSERT INTO `Tag` VALUES (null, "Components");
INSERT INTO `Tag` VALUES (null, "Fetch");

INSERT INTO `Entry` VALUES (null, "JavaScript", "I learned about loops today. They can be a lot of fun. I learned about loops today. They can be a lot of fun. I learned about loops today. They can be a lot of fun.", 1, "Wed Sep 15 2021 10:10:47");
INSERT INTO `Entry` VALUES (null, "Python", "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", 4, "Wed Sep 15 2021 10:11:33");
INSERT INTO `Entry` VALUES (null, "Python", "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks", 3, "Wed Sep 15 2021 10:10:47");
INSERT INTO `Entry` VALUES (null, "JavaScript", "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", 3, "Wed Sep 15 2021 10:10:47");

INSERT INTO `EntryTag` VALUES (null, 4, 2);
INSERT INTO `EntryTag` VALUES (null, 4, 3);
INSERT INTO `EntryTag` VALUES (null, 2, 1);
INSERT INTO `EntryTag` VALUES (null, 2, 2);

SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.mood         
        FROM Entry e
        Join Mood m
            ON m.id = e.mood_id