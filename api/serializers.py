from rest_framework import serializers
from projects.models import Keyword
from ranking.models import KeywordSerp, Ranking


class KeywordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'keyword', 'updated_at')


class KeywordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('updated_at',)


class KeywordSerpSerializer(serializers.ModelSerializer):
    keyword = serializers.PrimaryKeyRelatedField(queryset=Keyword.objects.filter())

    class Meta:
        model = KeywordSerp
        fields = (
            'keyword',
            'url_1', 
            'url_2', 
            'url_3', 
            'url_4', 
            'url_5', 
            'url_6', 
            'url_7', 
            'url_8', 
            'url_9', 
            'url_10',
            'url_11',
            'url_12',
            'url_13',
            'url_14',
            'url_15',
            'url_16',
            'url_17',
            'url_18',
            'url_19',
            'url_20',
            'url_21',
            'url_22',
            'url_23',
            'url_24',
            'url_25',
            'url_26',
            'url_27',
            'url_28',
            'url_29',
            'url_30',
            'url_31',
            'url_32',
            'url_33',
            'url_34',
            'url_35',
            'url_36',
            'url_37',
            'url_38',
            'url_39',
            'url_40',
            'url_41',
            'url_42',
            'url_43',
            'url_44',
            'url_45',
            'url_46',
            'url_47',
            'url_48',
            'url_49',
            'url_50',
            'url_51',
            'url_52',
            'url_53',
            'url_54',
            'url_55',
            'url_56',
            'url_57',
            'url_58',
            'url_59',
            'url_60',
            'url_61',
            'url_62',
            'url_63',
            'url_64',
            'url_65',
            'url_66',
            'url_67',
            'url_68',
            'url_69',
            'url_70',
            'url_71',
            'url_72',
            'url_73',
            'url_74',
            'url_75',
            'url_76',
            'url_77',
            'url_78',
            'url_79',
            'url_80',
            'url_81',
            'url_82',
            'url_83',
            'url_84',
            'url_85',
            'url_86',
            'url_87',
            'url_88',
            'url_89',
            'url_90',
            'url_91',
            'url_92',
            'url_93',
            'url_94',
            'url_95',
            'url_96',
            'url_97',
            'url_98',
            'url_99',
            'url_100',
            'title_1', 
            'title_2', 
            'title_3', 
            'title_4', 
            'title_5', 
            'title_6', 
            'title_7', 
            'title_8', 
            'title_9', 
            'title_10',
            'title_11',
            'title_12',
            'title_13',
            'title_14',
            'title_15',
            'title_16',
            'title_17',
            'title_18',
            'title_19',
            'title_20',
            'title_21',
            'title_22',
            'title_23',
            'title_24',
            'title_25',
            'title_26',
            'title_27',
            'title_28',
            'title_29',
            'title_30',
            'title_31',
            'title_32',
            'title_33',
            'title_34',
            'title_35',
            'title_36',
            'title_37',
            'title_38',
            'title_39',
            'title_40',
            'title_41',
            'title_42',
            'title_43',
            'title_44',
            'title_45',
            'title_46',
            'title_47',
            'title_48',
            'title_49',
            'title_50',
            'title_51',
            'title_52',
            'title_53',
            'title_54',
            'title_55',
            'title_56',
            'title_57',
            'title_58',
            'title_59',
            'title_60',
            'title_61',
            'title_62',
            'title_63',
            'title_64',
            'title_65',
            'title_66',
            'title_67',
            'title_68',
            'title_69',
            'title_70',
            'title_71',
            'title_72',
            'title_73',
            'title_74',
            'title_75',
            'title_76',
            'title_77',
            'title_78',
            'title_79',
            'title_80',
            'title_81',
            'title_82',
            'title_83',
            'title_84',
            'title_85',
            'title_86',
            'title_87',
            'title_88',
            'title_89',
            'title_90',
            'title_91',
            'title_92',
            'title_93',
            'title_94',
            'title_95',
            'title_96',
            'title_97',
            'title_98',
            'title_99',
            'title_100',
        )
    
#    def create(self, validated_data):
#        keyword = validated_data.pop('keyword')
#        keyword_serp = KeywordSerp(keyword=Keyword.objects.get(id=keyword), **validated_data)
#        keyword_serp.save()
#        return keyword_serp
#
#
#class KeywordSerpSerializer(serializers.ListSerializer):
#    child = KeywordSerpSerializer()
#
#    def create(self, validated_data):
#        keyword_serps = []
#        for serp_data in validated_data:
#            keyword = validated_data.pop('keyword')
#            keyword_serps.append(KeywordSerp(keyword=Keyword.objects.get(id=keyword), **validated_data))
#        return KeywordSerp.objects.bulk_create(keyword_serps)