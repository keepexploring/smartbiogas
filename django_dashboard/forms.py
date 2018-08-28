from dal import autocomplete

from django import forms
from searchableselect.widgets import SearchableSelect
#from django.contrib.auth.models import User
from django_dashboard.models import UserDetail
from django_dashboard.models import AddressData, BiogasPlant
#class RegionForm(forms.ModelForm):
 #   region = forms.ModelChoiceField(
 #       queryset=AddressData.objects.only('region'),
 #       widget=autocomplete.ModelSelect2(url='/dashboard/region-autocomplete')
 #   )

 #   class Meta:
 #       model = AddressData
 #       fields = ('region')


class UserForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        exclude = ('email', 'password', 'is_superuser')
        widgets = {
            'user' : SearchableSelect(model='django_dashboard.User', search_field='username', many=False, limit=1000)
        }

class BiogasForm(forms.ModelForm):

    class Meta:
        model = BiogasPlant
        fields = ('__all__')
        widgets = {
            'region': autocomplete.ListSelect2(url='region-autocomplete'),
            'district': autocomplete.ListSelect2(url='district-autocomplete'),
            'country': autocomplete.ListSelect2(url='country-autocomplete'),
            'continent': autocomplete.ListSelect2(url='continent-autocomplete'),
            'ward': autocomplete.ListSelect2(url='ward-autocomplete'),
            'village': autocomplete.ListSelect2(url='village-autocomplete'),
            #'supplier': autocomplete.ListSelect2(url='supplier-autocomplete'),
            #'volume_biogas': autocomplete.ListSelect2(url='volume-autocomplete'),

        }

class CompanyForm(forms.ModelForm):

    class Meta:
        model = BiogasPlant
        fields = ('__all__')
        widgets = {
            'region': autocomplete.ListSelect2(url='region-autocomplete'),
            'district': autocomplete.ListSelect2(url='district-autocomplete'),
            'country': autocomplete.ListSelect2(url='country-autocomplete'),
            'continent': autocomplete.ListSelect2(url='continent-autocomplete'),
            'ward': autocomplete.ListSelect2(url='ward-autocomplete'),
            'village': autocomplete.ListSelect2(url='village-autocomplete'),

        }

class UserDetailForm(forms.ModelForm):

    class Meta:
        model = BiogasPlant
        fields = ('__all__')
        widgets = {
            'region': autocomplete.ListSelect2(url='region-autocomplete'),
            'district': autocomplete.ListSelect2(url='district-autocomplete'),
            'country': autocomplete.ListSelect2(url='country-autocomplete'),
            'continent': autocomplete.ListSelect2(url='continent-autocomplete'),
            'ward': autocomplete.ListSelect2(url='ward-autocomplete'),
            'village': autocomplete.ListSelect2(url='village-autocomplete'),

        }


