import os
from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from app.settings import FILES_PATH


class FileList(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, date=None):
        # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
        files_list = os.listdir(FILES_PATH)
        files_list_res = []
        filtering_date = datetime.strptime(date, '%Y-%m-%d').date() if date else ''
        for file in files_list:
            path_to_file = os.path.join(FILES_PATH, file)
            file_res_stat = dict()
            file_res_stat['name'] = file
            file_res_stat['ctime'] = datetime.utcfromtimestamp(os.stat(path_to_file).st_ctime)
            file_res_stat['mtime'] = datetime.utcfromtimestamp(os.stat(path_to_file).st_mtime)
            if date:
                if file_res_stat['ctime'].date() == filtering_date:
                    files_list_res.append(file_res_stat)
            else:
                files_list_res.append(file_res_stat)
        return {'files': files_list_res,
                'date': filtering_date,
                }


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    if os.path.exists(os.path.join(FILES_PATH, name)):
        with open(os.path.join(FILES_PATH, name)) as file:
            file_content = file.read
            return render(
                request,
                'file_content.html',
                context={'file_name': name, 'file_content': file_content}
            )
    return HttpResponse('Данный файл отсутствует', status=400)

