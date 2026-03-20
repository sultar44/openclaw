# Rolling Jokers — Listings API PATCH Payloads

All 3 ASINs, all changes. Review before I submit.

---

## ASIN 1: B0B6Q77S57 (RJ3P - Main Game, SKU: NER-RJ3P-202312)

### Patch payload:
```json
{
  "productType": "BOARD_GAME",
  "patches": [
    {
      "op": "replace",
      "path": "/attributes/manufacturer_minimum_age",
      "value": [{"value": 168, "marketplace_id": "ATVPDKIKX0DER"}]
    },
    {
      "op": "replace",
      "path": "/attributes/item_name",
      "value": [{"language_tag": "en_US", "value": "Rolling Jokers - The Ultimate Wooden Jokers and Marbles Game - Premium Gift for Game Night, Grandparents & Friends - Classic Card Strategy Meets Modern Fun - Ages 14+", "marketplace_id": "ATVPDKIKX0DER"}]
    },
    {
      "op": "replace",
      "path": "/attributes/bullet_point",
      "value": [
        {"language_tag": "en_US", "value": "A HIT AT EVERY GATHERING - BRING EVERYONE TO THE TABLE: Rolling Jokers is loved by game night regulars, retirees, couples, and friend groups alike, making every evening a cherished memory. Perfect for holidays, get-togethers, or casual gatherings.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "SCREEN-FREE FUN THAT BRINGS PEOPLE TOGETHER: Turn off the devices and share laughs face-to-face. This engaging game is the perfect way to reconnect for genuine, memorable moments.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "EASY TO LEARN, DELIGHTFUL TO MASTER: Start playing in minutes; Rolling Jokers' rules are simple for beginners, but its strategy keeps experienced players coming back for more. Great for adults and game enthusiasts ages 14 and up.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "EXCLUSIVE ARTWORK, PREMIUM COMPONENTS: Features stunning original cards, vibrant marbles, and beautifully crafted wooden boards built to last for years of play. More choices, more strategy, more fun!", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "THE PERFECT GIFT FOR GAME LOVERS: Gift-ready and designed to impress, Rolling Jokers is ideal for birthdays, holidays, retirements, or any celebration. Give the gift of laughter, strategy, and togetherness.", "marketplace_id": "ATVPDKIKX0DER"}
      ]
    },
    {
      "op": "replace",
      "path": "/attributes/product_description",
      "value": [{"language_tag": "en_US", "value": "Rediscover the joy of real connection with Rolling Jokers, the ultimate Jokers and Marbles board game for friends, couples, and adults who love a great game night. Whether you're hosting a gathering, celebrating the holidays, or searching for a memorable gift for someone who appreciates quality time, Rolling Jokers brings everyone to the table with laughter, strategy, and timeless fun.\n\nWhy Choose Rolling Jokers?\n\nPerfect for Every Gathering: Rolling Jokers is designed to be enjoyed by adults of all ages—whether it's couples, friend groups, retirees, or the whole extended family on game night. Our customers rave about the way this game turns any evening into something special.\n\nEasy to Learn, Strategic to Win: Don't let complicated rules get in the way of fun. Rolling Jokers features straightforward instructions, so new players can jump right in. But with endless possibilities for clever moves, the game keeps experienced players engaged and challenged.\n\nPremium Wooden Craftsmanship: Our deluxe set features beautifully stained wooden boards, vibrant marbles, and exclusive playing cards—engineered for years of joyful play. It's a centerpiece-worthy addition to any game collection and makes a lasting gift for board game enthusiasts.\n\nUnplug and Reconnect: In a world full of screens, Rolling Jokers offers a much-needed opportunity for real, in-person connection. Enjoy screen-free game nights filled with laughter, friendly rivalry, and lasting memories.\n\nSupports 2–8 Players: Unlike many games, Rolling Jokers is flexible—play one-on-one, with a partner, or with a big group of up to eight people. It's ideal for game nights, parties, or community gatherings.\n\nThe Ideal Gift for Board Game Lovers: Looking for a birthday, holiday, retirement, or anniversary present? Rolling Jokers is a thoughtful, premium gift—perfect for grandparents, empty nesters, couples, and anyone who cherishes quality time with loved ones.\n\nHow to Play:\nRolling Jokers combines the classic fun of a marbles and jokers board game with strategic card play. Race to move your marbles from START to HOME by drawing and playing cards, while outmaneuvering opponents and collaborating with partners in team play. Each game is a new adventure—full of surprises, laughter, and friendly competition.\n\nGame Features:\nSturdy, beautifully finished wooden boards\nVibrant glass marbles\nExclusive deck of cards with classic and custom jokers\nEasy-to-follow instructions and quick-start video link\nSupports up to 8 players (modular board system)\nDesigned for ages 14+\n\nLoved by All, Built to Last:\nRolling Jokers stands out as a top-rated strategy game for adults seeking more meaningful game nights. Durable, eye-catching, and endlessly replayable—Rolling Jokers will become a tradition for years to come.\n\nRediscover the magic of game night—bring home Rolling Jokers today and make every gathering unforgettable.", "marketplace_id": "ATVPDKIKX0DER"}]
    }
  ]
}
```

**Changes from current:**
- `manufacturer_minimum_age`: 96 → **168**
- Title: "Families" → "Game Night", "Ages 8+" → "Ages 14+"
- Bullet 1: "ACROSS GENERATIONS" → "AT EVERY GATHERING", removed "parents, and kids alike"
- Bullet 2: "CONNECTS FAMILIES" → "BRINGS PEOPLE TOGETHER"
- Bullet 3: "ages 8 and up" → "adults and game enthusiasts ages 14 and up"
- Bullet 5: "OF ANY AGE" removed
- Description: Full rewrite removing all "kids/teens/grandkids/8+" language

---

## ASIN 2: B0CKY6BLS2 (RJ - Card Set, SKU: NER-RJ-202305)

### Patch payload:
```json
{
  "productType": "BOARD_GAME",
  "patches": [
    {
      "op": "replace",
      "path": "/attributes/manufacturer_minimum_age",
      "value": [{"value": 168, "marketplace_id": "ATVPDKIKX0DER"}]
    },
    {
      "op": "replace",
      "path": "/attributes/bullet_point",
      "value": [
        {"language_tag": "en_US", "value": "EASY TO LEARN, FUN FOR ALL: Rolling Jokers is a breeze to pick up, making it an excellent strategy game for adults and enthusiasts ages 14 and up. Whether you're a novice or a seasoned pro, this game guarantees fun for everyone.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "UNIQUE, EYE-CATCHING ARTWORK: This marbles and jokers board game wooden set features beautifully crafted boards and cards, blending timeless appeal with modern design for a game that's as visually stunning as it is entertaining.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "PERFECT FOR GAME NIGHT WITH FRIENDS: Enjoy endless laughter and competition with one of the best group board games. Rolling Jokers is ideal for game nights or gatherings, fostering connection and friendly rivalry.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "DURABLE WOODEN GAME CONSTRUCTION: Built with sturdy materials, this wooden game is designed to last through countless game nights. Its robust design ensures a premium experience with every play.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "A MEMORABLE GIFT FOR GAME LOVERS: Whether for fans of pegs and jokers board game or those discovering it for the first time, Rolling Jokers makes a fantastic gift. Perfect for birthdays, holidays, or any occasion, this game delivers hours of strategic fun.", "marketplace_id": "ATVPDKIKX0DER"}
      ]
    },
    {
      "op": "replace",
      "path": "/attributes/product_description",
      "value": [{"language_tag": "en_US", "value": "Nerkin Games Rolling Jokers Board Game - A Fresh Twist on The Classic Jokers and Marbles Game - Board Games for Adults, Seniors, and Game Night Enthusiasts for 2 to 8 Players\n\nDive into the fun and strategy with Rolling Jokers, a captivating board game that brings friends and fellow game lovers together. Whether you're planning a cozy game night or a competitive evening with friends, Rolling Jokers is the perfect addition to any game collection. Easy to learn for players ages 14 and up, it offers a unique blend of luck and tactical play that keeps every round exciting and unpredictable.\n\nBeautifully crafted, Rolling Jokers is not only durable but also a visually stunning piece. Each set features original, eye-catching artwork on the cards and a finely polished board that underscores its premium feel. Ideal for gift-giving or simply adding to your home's game night rotation, Rolling Jokers promises endless hours of laughter and enjoyment for board game lovers.\n\nPerfect for game nights, gatherings, or as a thoughtful gift, Rolling Jokers combines simplicity, beauty, and lasting enjoyment in one package. Embrace the fun, foster togetherness, and create cherished memories with this exceptional game set.", "marketplace_id": "ATVPDKIKX0DER"}]
    }
  ]
}
```

**Changes from current:**
- `manufacturer_minimum_age`: 96 → **168**
- Title: NO CHANGE (no age reference in current title) ✅
- Bullet 1: "aged 8 and up" → "adults and enthusiasts ages 14 and up"
- Bullet 3: "FAMILY AND FRIENDS" → "GAME NIGHT WITH FRIENDS", "6 player board games" → "group board games"
- Description: "Family Games for Kids and Adults" → "Board Games for Adults, Seniors, and Game Night Enthusiasts", "aged 8 and up" → "ages 14 and up", removed "families" as primary audience

---

## ASIN 3: B0DTQ94JX8 (Parent, SKU: LC-VD0G-FBVQ)

### Patch payload:
```json
{
  "productType": "BOARD_GAME",
  "patches": [
    {
      "op": "replace",
      "path": "/attributes/manufacturer_minimum_age",
      "value": [{"value": 168, "marketplace_id": "ATVPDKIKX0DER"}]
    },
    {
      "op": "replace",
      "path": "/attributes/bullet_point",
      "value": [
        {"language_tag": "en_US", "value": "EASY TO LEARN, FUN FOR ALL: Rolling Jokers is a breeze to pick up, making it an excellent strategy game for adults and enthusiasts ages 14 and up. Whether you're a novice or a seasoned pro, this game guarantees fun for everyone.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "UNIQUE, EYE-CATCHING ARTWORK: This marbles and jokers board game wooden set features beautifully crafted boards and cards, blending timeless appeal with modern design for a game that's as visually stunning as it is entertaining.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "PERFECT FOR GAME NIGHT WITH FRIENDS: Enjoy endless laughter and competition with one of the best group board games. Rolling Jokers is ideal for game nights or gatherings, fostering connection and friendly rivalry.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "DURABLE WOODEN GAME CONSTRUCTION: Built with sturdy materials, this wooden game is designed to last through countless game nights. Its robust design ensures a premium experience with every play.", "marketplace_id": "ATVPDKIKX0DER"},
        {"language_tag": "en_US", "value": "A MEMORABLE GIFT FOR GAME LOVERS: Whether for fans of pegs and jokers board game or those discovering it for the first time, Rolling Jokers makes a fantastic gift. Perfect for birthdays, holidays, or any occasion, this game delivers hours of strategic fun.", "marketplace_id": "ATVPDKIKX0DER"}
      ]
    },
    {
      "op": "replace",
      "path": "/attributes/product_description",
      "value": [{"language_tag": "en_US", "value": "Nerkin Games Rolling Jokers Board Game - A Fresh Twist on The Classic Jokers and Marbles Game - Board Games for Adults, Seniors, and Game Night Enthusiasts for 2 to 8 Players\n\nDive into the fun and strategy with Rolling Jokers, a captivating board game that brings friends and fellow game lovers together. Whether you're planning a cozy game night or a competitive evening with friends, Rolling Jokers is the perfect addition to any game collection. Easy to learn for players ages 14 and up, it offers a unique blend of luck and tactical play that keeps every round exciting and unpredictable.\n\nBeautifully crafted, Rolling Jokers is not only durable but also a visually stunning piece. Each set features original, eye-catching artwork on the cards and a finely polished board that underscores its premium feel. Ideal for gift-giving or simply adding to your home's game night rotation, Rolling Jokers promises endless hours of laughter and enjoyment for board game lovers.\n\nPerfect for game nights, gatherings, or as a thoughtful gift, Rolling Jokers combines simplicity, beauty, and lasting enjoyment in one package. Embrace the fun, foster togetherness, and create cherished memories with this exceptional game set.", "marketplace_id": "ATVPDKIKX0DER"}]
    }
  ]
}
```

**Changes from current (same as RJ card set — parent and card set shared identical copy):**
- `manufacturer_minimum_age`: 96 → **168**
- Title: NO CHANGE (already clean) ✅
- Bullets and Description: same changes as RJ card set above

---

## Note: FBM SKU (NER-RJ3P-202312-FBM)
There's also an FBM SKU for the main game on the same ASIN B0B6Q77S57. Since it shares the ASIN, the listing content is shared. The PATCH on the FBA SKU should update the listing for both. But I can also PATCH the FBM SKU's `manufacturer_minimum_age` separately to be safe.

---

## Summary of ALL changes across 3 ASINs:
| Field | Old | New |
|-------|-----|-----|
| manufacturer_minimum_age | 96 (8 yrs) | 168 (14 yrs) |
| RJ3P title | "Families" / "Ages 8+" | "Game Night" / "Ages 14+" |
| All bullets | "ages 8 and up" / "kids" | "ages 14 and up" / adult language |
| All descriptions | "kids and adults" / "8+" | "adults, seniors" / "14+" |
