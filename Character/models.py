from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

BA_TYPE_CHOICE = (
    ('FULL', 'Full'),
    ('HALF', 'Half'),
    ('3/4', 'Three-Quarters'),
)
SAVE_TYPE_CHOICE = (
    ('GOOD', 'Good'),
    ('BAD', 'Bad'),
)
MODIFIER_CHOICE = (
    ('STR', 'Strength'),
    ('DEX', 'Dexterity'),
    ('CON', 'Constitution'),
    ('WIS', 'Wisdom'),
    ('INT', 'Intelligence'),
    ('CHA', 'Charisma'),
    ('NULL', 'None'),
)
ABILITY_TYPE_CHOICE = (
    ('Feat', 'Feat'),
    ('Attack_Modifier', 'Attack Modifier'),
    ('Ability_Modifier', 'Ability Modifier'),
    ('Skill_Modifier', 'Skill Modifier'),
    ('AC_Modifier', 'AC Modifier'),
    ('Special_Attack', 'Special Attack')
)
AC_TYPE_CHOICE = (
    ('Armor', 'Armor Bonus'),
    ('Shield', 'Shield Bonus'),
    ('DEX', 'Dexterity Bonus'),
    ('Size', 'Size Bonus'),
    ('Natural', 'Natural Armor Bonus'),
    ('Deflection', 'Deflection Bonus'),
    ('Dodge', 'Dodge Bonus'),
    ('Misc', 'Misc Bonus')
)
ATTACK_TYPE_CHOICE = (
    ('Melee', 'Melee'),
    ('Ranged', 'Ranged'),
    ('Touch', 'Touch'),
    ('Ranged_Touch', 'Ranged Touch')
)
CONDITION_TYPE_CHOICE = (
    ("__lte", "Less than or Equal to Value"),
    ("__gte", "Greater than or Equal to Value"),
    ("__iexact", "Equals Value"),
    ("__in", "Is one of Thes: (seperatted by commas)")
)
ALIGNMENT_CHOICES = (
    ("LG", "Lawful Good"),
    ("TG", "True Good"),
    ("CG", "Chaotic Good"),
    ("LN", "Lawful Neutral"),
    ("TN", "True Neutral"),
    ("CN", "Chaotic Neutral"),
    ("LE", "Lawful Evil"),
    ("TE", "True Evil"),
    ("CE", "Chaotic Evil")
)

class Condition(models.Model):
    #item = models.ManyToMany(Item, null=True)
    name = models.CharField(max_length=50)
    model = models.ForeignKey(ContentType, help_text="Model", blank=True)

    def __unicode__(self):
        return self.name


class Filter(models.Model):
    condition = models.ForeignKey(Condition)
    field = models.CharField(max_length=40, help_text='Filter Fields')
    condition = models.CharField(max_length=10, choices=CONDITION_TYPE_CHOICE)
    value = models.CharField(max_length=255, help_text="Condition Value")

class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    untrained = models.BooleanField(default=False)
    armor_check = models.BooleanField(default=False)
    modifier = models.CharField(max_length=10, choices=MODIFIER_CHOICE)
    
    def __unicode__(self):
        return self.name


class AttackModifier(models.Model):
    attack_bonus = models.IntegerField(default=0)
    damage_bonus = models.IntegerField(default=0)

    def __unicode__(self):
        return self.ability.name

    def apply(self):
        return


class AbilityModifier(models.Model):
    ability_name = models.CharField(max_length=3, choices=MODIFIER_CHOICE)
    bonus = models.IntegerField(default=0)

    def __unicode__(self):
        return self.ability.name

    def apply(self):
        return


class SkillModifier(models.Model):
    skill = models.ForeignKey(Skill)
    bonus = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.skill.name
    
    def apply(self):
        return


class ACModifier(models.Model):
    type = models.CharField(max_length=20, choices=AC_TYPE_CHOICE)
    bonus = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.ability.name
    
    def apply(self):
        return


class DCBonus(models.Model):
    modifier = models.CharField(max_length=3, choices=ABILITY_TYPE_CHOICE)
    level = models.BooleanField(default=False)
    hit_dice = models.BooleanField(default=False)


class SpecialAttack(models.Model):
    attack_type = models.CharField(max_length=20, choices=ATTACK_TYPE_CHOICE)
    base_dc = models.IntegerField(default=10)
#    dc_bonus = models.Foreign(DCBonus, null=True)
    damage_roll = models.IntegerField(default=4)
    damage_bonus = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.ability.name
    
    def apply(self):
        return


class Ability(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=ABILITY_TYPE_CHOICE)
    attack_modifier = models.OneToOneField(AttackModifier, null=True)
    ability_modifier = models.OneToOneField(AbilityModifier, null=True)
    skill_modifier = models.OneToOneField(SkillModifier, null=True)
    ac_modifier = models.OneToOneField(ACModifier, null=True)
    special_attack = models.OneToOneField(SpecialAttack, null=True)


class CharacterClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    base_attack = models.CharField(choices=BA_TYPE_CHOICE, max_length=15)
    fort_base = models.CharField(choices=SAVE_TYPE_CHOICE, max_length=15)
    ref_base = models.CharField(choices=SAVE_TYPE_CHOICE, max_length=15)
    will_base = models.CharField(choices=SAVE_TYPE_CHOICE, max_length=15)
    class_skills = models.ManyToManyField(Skill)
    hit_dice = models.IntegerField(default=4)
    base_skill_points = models.IntegerField(default=2)

    def __unicode__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=100)
    abilities = models.ForeignKey(Ability)

class Character(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    character_class = models.ForeignKey(CharacterClass)
    level = models.IntegerField(default=1)
    avatar = models.ImageField(blank=True, upload_to="character/avatars/", null=True)

    feats = models.ManyToManyField(Ability)

    max_HP = models.IntegerField(default=0)
    current_HP = models.IntegerField(default=0)
    current_experience = models.IntegerField(default=0)

    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    wisdom = models.IntegerField()
    intelligence = models.IntegerField()
    charisma = models.IntegerField()
    
    personality = models.TextField(blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    alignment = models.CharField(blank=True,null=True,choices=ALIGNMENT_CHOICES, max_length=50)
    height = models.CharField(blank=True, null=True, max_length=20)
    weight = models.CharField(blank=True, null=True, max_length=20)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, default="U", choices=(("M","Male"),("F","Female"),("U","Unspecified")))
    deity = models.CharField(max_length=50, blank=True, null=True)
    
    def __unicode__(self):
        return self.name


class SkillRanks(models.Model):
    ranks = models.IntegerField(default=0)
    character = models.ForeignKey(Character)
    skill = models.ForeignKey(Skill)
    modifier = models.IntegerField(default=0)
    is_class_skill = models.BooleanField(default=False)
