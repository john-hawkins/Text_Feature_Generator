# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd 
import numpy as np
import math
import os
import re

from .process import load_word_list
from .process import load_word_pattern

"""
    texturizer.topics: Common Topic Features

    Simple pattern matching to generate features for very common topics for text data.
    We have focused on topics that are common in both traditional and social media, 
    as well as commentary and discussion by the general public.
  
    The goal with these features is to provide a count of words which are 
    unambigously related to a specific topic.

    NOTE: That the words in these sets have been deliberately selected to be a set 
          that are less likely to match false positives. In other words they are 
          generally only used when talking about that specific topic, or when talking
          using metaphor or analogy.
"""

########################################################################################

religion_pat = load_word_pattern('religion.dat', "\\bchristi|\\bislam|")
religion_re = re.compile(religion_pat)

politics_pat = load_word_pattern('politics.dat', "\\bpoliti|")
politics_re = re.compile(politics_pat)

sex_pat = load_word_pattern('sex.dat', "\\bsex[^t]|")
sex_re = re.compile(sex_pat)

ethno_pat = load_word_pattern('ethnicity.dat', "\\bethn|")
ethno_re = re.compile(ethno_pat)

health_pat = load_word_pattern('health.dat', "\\bhealth|")
health_re = re.compile(health_pat)
 
econo_pat = load_word_pattern('economics.dat', "\\becono|\\bfinan|")
econo_re = re.compile(econo_pat) 
 
sport_pat = load_word_pattern('sports.dat', "\\bathlet|")
sport_re = re.compile(sport_pat)
 
arts_pat = load_word_pattern('arts.dat', "\\bartist|")
arts_re = re.compile(arts_pat)

family_pat = load_word_pattern('family.dat', "\\bfamil|")
family_re = re.compile(family_pat)
 
love_pat = load_word_pattern('love.dat', "\\bromanc|")
love_re = re.compile(love_pat)
 
crime_pat = load_word_pattern('crime.dat', "\\bcrimina|")
crime_re = re.compile(crime_pat)
 
travel_pat = load_word_pattern('travel.dat', "\\btravel|")
travel_re = re.compile(travel_pat)
 
food_pat = load_word_pattern('food.dat')
food_re = re.compile(food_pat)
 
technology_pat = load_word_pattern('technology.dat', "\\btechnol[^t]|")

fashion_pat = load_word_pattern('fashion.dat', "\\bfashion[^i]|")

culture_pat = load_word_pattern('culture.dat', "\\bcultur|")

education_pat = load_word_pattern('education.dat', "\\beducat|")

########################################################################################
def add_text_topics_features(df, columns, type="flag"):
    """
        Given a pandas dataframe and a set of column names.
        calculate the simple text summary features and add them.
    """
    rez = df.copy()
    for col in columns:
        if type=="count":
            rez = add_topic_counts(rez, col)
            #rez = add_topic_features(rez, col)
        else:
            rez = add_topic_indicators(rez, col)
    return rez

########################################################################################
def add_topic_features(df, col):
    """
        Given a pandas dataframe and a column name.
        Count the text matches for topic keywords.
    """

    def prof_features(x, col):
        religion_wds = 0
        sex_wds = 0
        politics_wds = 0
        ethno_wds = 0
        econo_wds = 0
        health_wds = 0 
        sport_wds = 0 
        arts_wds = 0 
        family_wds = 0 
        love_wds = 0 
        crime_wds = 0 
        travel_wds = 0 
        food_wds = 0 
        if x[col]!=x[col]:
            sex_wds = 0
        else:
            text = (x[col].lower())
            religion_wds = len(religion_re.findall(text))
            politics_wds = len(politics_re.findall(text))
            sex_wds = len(sex_re.findall(text))
            ethno_wds = len(ethno_re.findall(text))
            econo_wds = len(econo_re.findall(text))
            health_wds = len(health_re.findall(text))
            sport_wds = len(sport_re.findall(text))
            arts_wds = len(arts_re.findall(text))
            family_wds = len(family_re.findall(text))
            love_wds = len(love_re.findall(text))
            crime_wds = len(crime_re.findall(text))
            travel_wds = len(travel_re.findall(text))
            food_wds = len(food_re.findall(text))
        return religion_wds, politics_wds, sex_wds, ethno_wds, econo_wds, health_wds, sport_wds, arts_wds, family_wds, love_wds, crime_wds, travel_wds, food_wds

    df[[ col+'_religion', col+'_politics', col+'_sex', col+'_ethnicity', col+'_economics', col+'_health', col+'_sport', col+'_arts', col+'_family', col+'_love', col+'_crime', col+'_travel', col+'_food']] = df.apply(prof_features, col=col, axis=1, result_type="expand")
    return df

########################################################################################
def add_topic_indicators(df, col):
    """
        Given a pandas dataframe and a column name.
        add simple text match for top indicators.
    """ 
    df[ col+'_religion' ] = 0
    df.loc[(df[col].notnull()) & (df[col].str.contains(religion_pat)), col+'_religion' ] = 1
    df[ col+'_politics' ] = 0
    df.loc[(df[col].notnull()) & (df[col].str.contains(politics_pat)), col+'_politics' ] = 1
    df[ col+'_sex' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(sex_pat)), col+'_sex' ]=1
    df[ col+'_ethnicity' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(ethno_pat)), col+'_ethnicity' ]=1
    df[ col+'_economics' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(econo_pat)), col+'_economics' ]=1
    df[ col+'_health' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(health_pat)), col+'_health' ]=1
    df[ col+'_sport' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(sport_pat)), col+'_sport' ]=1
    df[ col+'_arts' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(arts_pat)), col+'_arts' ]=1
    df[ col+'_family' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(family_pat)), col+'_family' ]=1
    df[ col+'_love' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(love_pat)), col+'_love' ]=1
    df[ col+'_crime' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(crime_pat)), col+'_crime' ]=1
    df[ col+'_travel' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(travel_pat)), col+'_travel' ]=1
    df[ col+'_food' ]=0
    df.loc[(df[col].notnull()) & (df[col].str.contains(food_pat)), col+'_food' ]=1

    return df

########################################################################################
def add_topic_counts(df, col):
    """
        Given a pandas dataframe and a column name.
        Count the number of keywor matches for each topic
    """
    df[col+'_religion']=df[col].str.count(religion_pat, flags=re.IGNORECASE)
    df[col+'_politics']=df[col].str.count(politics_pat, flags=re.IGNORECASE)
    df[col+'_sex']=df[col].str.count(sex_pat, flags=re.IGNORECASE)
    df[col+'_ethnicity']=df[col].str.count(ethno_pat, flags=re.IGNORECASE)
    df[col+'_economics']=df[col].str.count(econo_pat, flags=re.IGNORECASE)
    df[col+'_health']=df[col].str.count(health_pat, flags=re.IGNORECASE)
    df[col+'_sport']=df[col].str.count(sport_pat, flags=re.IGNORECASE)
    df[col+'_arts']=df[col].str.count(arts_pat, flags=re.IGNORECASE)
    df[col+'_family']=df[col].str.count(family_pat, flags=re.IGNORECASE)
    df[col+'_love']=df[col].str.count(love_pat, flags=re.IGNORECASE)
    df[col+'_crime']=df[col].str.count(crime_pat, flags=re.IGNORECASE)
    df[col+'_travel']=df[col].str.count(travel_pat, flags=re.IGNORECASE)
    df[col+'_food']=df[col].str.count(food_pat, flags=re.IGNORECASE)
    df[col+'_technology']=df[col].str.count(technology_pat, flags=re.IGNORECASE)
    df[col+'_fashion']=df[col].str.count(fashion_pat, flags=re.IGNORECASE)
    df[col+'_culture']=df[col].str.count(culture_pat, flags=re.IGNORECASE)
    df[col+'_education']=df[col].str.count(education_pat, flags=re.IGNORECASE)
    return df

