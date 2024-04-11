"""
URL configuration for farm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from poultry_b import views as new_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('poultry.urls')),
    path('chicken_b/', new_views.chicken_b, name='chicken_b'),
    path('chickens_out_b/', new_views.chickens_out_b, name='chickens_out_b'),
    path('chickens_slaughtered_b/', new_views.chickens_slaughtered_b, name='chickens_slaughtered_b'),
    path('delete_chickens_slaughtered_b/<int:id>/', new_views.delete_chickens_slaughtered_b, name='delete_chickens_slaughtered_b'),
    path('chickens_mortality_b/', new_views.chickens_mortality_b, name='chickens_mortality_b'),
    path('delete_chickens_mortality_b/<int:id>/', new_views.delete_chickens_mortality_b, name='delete_chickens_mortality_b'),
    path('feed_b/', new_views.feed_b, name='feed_b'),
    path('feed_overview_b/', new_views.feed_overview_b, name='feed_overview_b'),
    path('drugs_b/', new_views.drugs_b, name='drugs_b'),
    path('notepad_detail_b/<int:id>/', new_views.notepad_detail_b, name='notepad_detail_b'),
    path('notepad_delete_b/<int:id>/', new_views.notepad_delete_b, name='notepad_delete_b'),
    path('delete_production_b/<int:id>/', new_views.delete_production_b, name='delete_production_b'),
    path('delete_drugs_b/<int:id>/', new_views.delete_drugs_b, name='delete_drugs_b'),
    path('drugs_overview_b/', new_views.drugs_overview_b, name='drugs_overview_b'),
    path('necessities_b/', new_views.necessities_b, name='necessities_b'),
    path('necessities_overview_b/', new_views.necessities_overview_b, name='necessities_overview_b'),
    path('delete_necessities_b/<int:id>/', new_views.delete_necessities_b, name='delete_necessities_b'),
    path('coldroom_in_b/', new_views.coldroom_in_b, name='coldroom_in_b'),
    path('total_coldroom_b/', new_views.total_coldroom_b, name='total_coldroom_b'),
    path('production_b/', new_views.production_b, name='production_b'),
    path('imprest_b/', new_views.imprest_b, name='imprest_b'),
    path('total_imprest_b/', new_views.total_imprest_b, name='total_imprest_b'),
    path('notepad_b/', new_views.notepad_b, name='notepad_b'),
    path('notepad_overview_b/', new_views.notepad_overview_b, name='notepad_overview_b'),
    path('offals_b/', new_views.offals_b, name='offals_b'),
    path('offals_overview_b/', new_views.offals_overview_b, name='offals_overview_b'),
    path('offals_overview_delete_b/<int:id>/', new_views.offals_overview_delete_b, name='offals_overview_delete_b'),
    path('update_chicken_b/<int:id>/', new_views.update_chicken_b, name='update_chicken_b'),
    path('delete_chicken_b/<int:id>/', new_views.delete_chicken_b, name='delete_chicken_b'),
    path('update_chicken_out_b/<int:id>/', new_views.update_chicken_out_b, name='update_chicken_out_b'),
    path('update_drugs_b/<int:id>/', new_views.update_drugs_b, name='update_drugs_b'),
    path('update_feed_b/<int:id>/', new_views.update_feed_b, name='update_feed_b'),
    path('update_production_b/<int:id>/', new_views.update_production_b, name='update_production_b'),
    path('update_necessities_b/<int:id>/', new_views.update_necessities_b, name='update_necessities_b'),
    path('delete_models_b/', new_views.delete_models_b, name='delete_models_b'),
    path('index_b/', new_views.index_b, name='index_b'),
    path('add_b/', new_views.add_b, name='add_b'),




]
