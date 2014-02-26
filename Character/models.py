from django.db import models
from django.contrib.auth import User

BA_TYPE_CHOICE = {
    ('FULL', 'Full'),
    ('HALF', 'Half'),
    ('3/4', 'Three-Quarters'),
}
SAVE_TYPE_CHOICE = {
    ('GOOD', 'Good'),
    ('BAD', 'Bad'),
}
MODIFIER_CHOICE = {
    ('STR', 'Strength'),
    ('DEX', 'Dexterity'),
    ('CON', 'Constitution'),
    ('WIS', 'Wisdom'),
    ('INT', 'Intelligence'),
    ('CHA', 'Charisma'),
    ('NULL', 'None'),
}
ABILITY_TYPE = {
    ('Feat', 'Feat'),
    ('Attack_Modifier', 'Attack Modifier'),
    ('Ability_Modifier', 'Ability Modifier'),
    ('Skill_Modifier', 'Skill Modifier'),
    ('AC_Modifier', 'AC Modifier'),
    ('Special_Attack', 'Special Attack'),
}
AC_TYPE = {
    ('Armor', 'Armor Bonus'),
    ('Shield', 'Shield Bonus'),
    ('DEX', 'Dexterity Bonus'),
    ('Size', 'Size Bonus'),
    ('Natural', 'Natural Armor Bonus'),
    ('Deflection', 'Deflection Bonus'),
    ('Dodge', 'Dodge Bonus'),
    ('Misc', 'Misc Bonus'),
}
ATTACK_TYPE = {
    ('Melee', 'Melee'),
    ('Ranged', 'Ranged'),
    ('Touch', 'Touch'),
    ('Ranged_Touch', 'Ranged Touch'),
}

class Character(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    character_class = models.ForeignKey(CharacterClass)
    level = models.IntegerField(default=1)
    
    fort_base = models.IntegerField(default=0)
    ref_save = models.IntegerField(default=0)
    will_save = models.IntegerField(default=0)

    base_attack = models.IntegerField(default=0)

    feats = models.ManyToManyField(Ability)

    max_HP = models.IntegerField()
    current_HP = models.IntegerField()

    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    wisdom = models.IntegerField()
    intelligence = models.IntegerField()
    charisma = models.IntegerField()


class CharacterClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_attack = models.CharField(choice=BA_TYPE, max_length=15)
    fort_base = models.CharField(choice=SAVE_TYPE_CHOICE, max_length=15)
    ref_base = models.CharField(choice=SAVE_TYPE_CHOICE, max_length=15)
    will_base = models.CharField(choice=SAVE_TYPE_CHOICE, max_length=15)
    class_skills = models.ManyToManyField(Skill)
    hit_dice = models.IntegerField(default=4)


class SkillRanks(models.Model):
    ranks = models.IntegerField(default=0)
    character = models.ForeignKey(Character)
    skill = models.ForeignKey(Skill)
    modifier = models.IngtegerField(default=0)
    is_class_skill = models.BooleanField(default=False)


class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    untrained = models.BooleanField(default=False)
    armor_check = models.BooleanField(default=False)
    modifier = CharField(max_length=10, choice=MODIFIER_CHOICE)


class Ability(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choice=ABILITY_TYPE)
    attack_modifier = models.OneToOneField(AttackModifier, null=True)
    ability_modifier = models.OneToOneField(AbilityModifier, null=True)
    skill_modifier = models.OneToOneField(SkillModifier, null=True)
    ac_modifier = models.OneToOneField(ACModifier, null=True)
    special_attack = models.OneToOneField(SpecialAttack, null=True)
    condition = models.ManyToManyField(AbilityCondition, null=True)


class AttackModifier(models.Model):
    attack_bonus = models.IntegerField(default=0)
    damage_bonus = models.IntegerField(default=0)

    def __unicode__(self):
        return self.ability.name

    def apply(self):
        return


class AbilityModifier(models.Model):
    ability = models.CharField(max_length=3, choice=MODIFIER_CHOICE)
    bonus = models.IntegerField(default=0)

    def __unicode__(self):
        return self.ability.name

    def apply(self):
        return


class SkillModifier(models.Model):
    skill = models.ForeignKey(Skill)
    bonus = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.ability.name
    
    def apply(self):
        return


class ACModifier(models.Model):
    type = models.CharField(max_length=20, choice=AC_TYPE)
    bonus = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.ability.name
    
    def apply(self):
        return


class SpecialAttack(models.Model):
    attack_type = models.CharField(max_length=20, choice=ATTACK_TYPE)
    base_dc = models.IntegerField(default=10)
    dc_bonus = models.ManyToManyField(DCBonus, null=True)
    damage_roll = models.IntegerField(default=4)
    damage_bonus = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.ability.name
    
    def apply(self):
        return


class Condition(models.Model):
    #item = models.ManyToMany(Item, null=True)
    name = models.CharField(max_length=50)
 

    def __unicode__(self):
        return self.name