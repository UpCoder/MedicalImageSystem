from django.conf.urls import url
from back_end import views

urlpatterns = [
    url(r'login/$', views.login),
    url(r'logout/$', views.logout),
    url(r'upload_file/$', views.upload_file),
    url(r'get_check_data/$', views.get_check_data),
    url(r'get_file_construction_json/$', views.get_file_construction_json),
    url(r'save_image_address_cookie/$', views.save_image_address_cookie),
    url(r'save_mask/$', views.save_mask),
    url(r'segement_cyst/$', views.segement_cyst),
    url(r'get_save_mask_path/$', views.get_save_mask_path),
    url(r'create_new_folder/$', views.create_new_folder),
    url(r'delete_path/$', views.delete_path),
    url(r'delete_check_by_pk/$', views.delete_check_by_pk),
    url(r'load_mask_image/$', views.load_mask_image),
    url(r'load_main_image/$', views.load_main_image),
    url(r'get_main_images/$', views.get_main_images),
    url(r'get_images_multiphase/$', views.get_images_multiphase),
    url(r'get_masks_multiphases/$', views.get_masks_multiphases),
]