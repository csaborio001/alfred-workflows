"""Extra everyday search words, grouped by the emoji names they describe."""
from emoji_data import RELATED_WORDS

GROUPS = [
    ('smile smiley grinning grin blush relaxed', 'happy cheerful pleased delighted glad positive happiness smiling friendly'),
    ('joy laughing satisfied', 'laugh funny hilarious lol lmao haha giggle laughing comedy amused'),
    ('heart sparkling_heart heart_eyes cupid two_hearts', 'love adore affection romance romantic sweetheart loving'),
    ('kissing kissing_heart kissing_closed_eyes kissing_smiling_eyes', 'kiss kisses smooch mwah affection romantic'),
    ('cry sob disappointed pensive', 'sad unhappy sadness upset crying sorrow miserable heartbroken'),
    ('angry rage', 'angry mad furious annoyed irritated anger frustrated grumpy'),
    ('worried fearful cold_sweat anxious', 'anxious anxiety worried nervous stressed stress scared concern'),
    ('scream astonished open_mouth', 'shocked surprise surprised omg disbelief amazed wow'),
    ('sleeping sleepy zzz', 'tired sleepy exhausted sleep bedtime nap snooze bored fatigue'),
    ('sunglasses smirk', 'cool confident swag smooth smug'),
    ('confused question interrobang', 'confused confusion unsure puzzled why what huh question'),
    ('thinking thinking_face', 'think thinking ponder wondering consider hmm'),
    ('flushed see_no_evil', 'embarrassed shy awkward blush bashful oops'),
    ('mask face_with_thermometer face_with_head_bandage', 'sick ill unwell sickness flu fever covid'),
    ('tada confetti_ball balloon party_popper', 'party celebration celebrate congratulations congrats hooray birthday festive'),
    ('birthday cake gift', 'birthday anniversary celebration present surprise bday'),
    ('+1 thumbsup ok_hand white_check_mark heavy_check_mark', 'yes agree agreed approve approval correct okay ok done success approved'),
    ('-1 thumbsdown x negative_squared_cross_mark', 'no disagree disapprove reject wrong incorrect denied nope'),
    ('clap raised_hands', 'bravo applause applaud well done congratulations congrats praise celebrate'),
    ('pray', 'thanks thank you grateful gratitude please hope hoping prayer namaste'),
    ('wave', 'hello hi hey goodbye bye welcome farewell greeting'),
    ('muscle', 'strong strength workout exercise gym fitness flex effort power'),
    ('100 fire', 'awesome amazing excellent perfect epic impressive lit'),
    ('rocket', 'launch ship deploy release fast speed startup liftoff'),
    ('computer briefcase office clipboard calendar', 'work working job business office productivity professional meeting'),
    ('computer keyboard', 'coding programming developer software tech technology code'),
    ('bug beetle', 'bug insect debugging issue error problem'),
    ('wrench hammer gear', 'fix repair tool maintenance settings configure'),
    ('bulb', 'idea ideas inspiration solution eureka insight'),
    ('books book notebook pencil pencil2 memo', 'study school learning education homework notes writing read reading'),
    ('coffee tea', 'drink hot beverage break morning caffeine cuppa'),
    ('beer beers wine_glass cocktail tropical_drink', 'drink alcohol booze cheers pub bar happy hour'),
    ('pizza hamburger fries spaghetti', 'food hungry lunch dinner meal takeaway takeout eating'),
    ('yum', 'yummy delicious tasty hungry food appetite nom'),
    ('moneybag dollar credit_card', 'money payment cash pay salary shopping purchase budget finance'),
    ('airplane luggage suitcase', 'travel trip holiday vacation flight airport flying'),
    ('house house_with_garden', 'home house family residence staying home'),
    ('sunny sunrise', 'sun sunshine sunny bright summer morning warmth'),
    ('umbrella cloud', 'rain rainy weather cloudy wet drizzle'),
    ('snowflake snowman', 'winter snow cold chilly freezing frost'),
    ('dog dog2 cat cat2 paw_prints', 'pet pets animal furry cute companion'),
    ('rose bouquet blossom cherry_blossom', 'flower flowers floral garden spring bloom'),
    ('musical_note notes headphones', 'music song songs listen listening audio tune melody'),
    ('warning rotating_light', 'warning alert attention caution urgent emergency'),
    ('hourglass hourglass_flowing_sand watch clock1', 'time wait waiting pending soon deadline delay'),
    ('eyes', 'look looking watching see attention curious checking'),
    ('checkered_flag trophy medal', 'finished finish win winner winning achievement goal complete victory'),
    ('broken_heart', 'breakup heartbreak heartbroken grief hurt sad loss'),
]


def expanded_words(symbols):
    words = {name: list(RELATED_WORDS.get(name, [])) for name in symbols}
    for names, synonyms in GROUPS:
        for name in names.split():
            if name in words:
                words[name] = list(dict.fromkeys(words[name] + synonyms.split()))
    return words
